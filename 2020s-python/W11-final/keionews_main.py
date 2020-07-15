from bs4 import BeautifulSoup as bs
import requests
import re
import asyncio
import logging
import time
from multiprocessing import Queue, Process
from quart import Quart, jsonify, request

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%I:%M:%S', level=logging.INFO)

page = requests.get("https://www.sfc.keio.ac.jp/en/news/sfc/")
soup = bs(page.text,"html.parser")

def get_keio_news(num,num_result):
    """find the date, titles, and addresses of news"""

    logging.info("ready to get keio news")
    while True:
        get_num = num.get()
        logging.info(f"Find the latest {get_num} news")

        #find date
        get_date = soup.find_all("dt",limit=get_num)
        date_find = re.compile("\d.*")
        date_list = date_find.findall(str(get_date))

        #find the titles and addresses of news
        get_news = soup.find_all("dd",limit=get_num)
        news_list = []
        url_list = []
        for i in range(len(get_news)):
            news_list.append(get_news[i].get_text())
            string = ""
            if "http" not in get_news[i].a["href"]:
                string = "https://www.sfc.keio.ac.jp" + get_news[i].a["href"]
                url_list.append(string)
            else:
                 url_list.append(get_news[i].a["href"])

        num_result.put([{f"{y+1} Post Date":date_list[y],f"{y+1} News Title":news_list[y],f"{y+1} Url":f"{url_list[y]}"} for y in range(len(date_list))])

"""Quart web programming"""

app = Quart(__name__)


@app.route("/")
async def get_num(): 
    global q_num, q_result

    num = request.args.get("num")

    num_total_news = len(soup.find_all("dd"))
    if int(num) > num_total_news:
        return jsonify({"Maximum number of news":num_total_news})
    else:
        print(num)
        print(num_total_news)

        q_num.put((int(num)))

        return jsonify({"Number of the latest KEIO news you want to get": num})


@app.route("/get_result")
async def get_result():
    result = q_result.get(True)
    return jsonify({"KEIO Latest News":result})


if __name__ == "__main__":
    q_num = Queue()
    q_result = Queue()
    p = Process(target=get_keio_news, args=(q_num,q_result))
    p.start()
    app.run(debug=True)
    p.join()
    # add consuming time
    # more work asynchronously



