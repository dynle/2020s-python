from bs4 import BeautifulSoup as bs
import requests
import time
import asyncio
from functools import partial
import logging
import sys
import re
from multiprocessing import Queue
from quart import Quart, jsonify, request

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%I:%M:%S', level=logging.INFO)

async def get_text_from_url(num_input, url_input):
    global news
    logging.info(f'Send request to ... {url_input}\n')
    loop = asyncio.get_event_loop()

    request = partial(requests.get, url_input, headers={'user-agent': 'Mozilla/5.0'})
    
    res = await loop.run_in_executor(None, request)
    logging.info(f'Get response from ... {url_input}\n')
    soup = bs(res.text, 'html.parser')

    #beautiful soup - find date
    get_date = soup.find_all("dt",limit=int(news_num))
    date_find = re.compile("\d.*")
    date_list = date_find.findall(str(get_date))

    #beautiful soup - find the titles and addresses of news
    get_news = soup.find_all("dd",limit=int(news_num))
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

    n = [{f"{y+1} Post Date":date_list[y],f"{y+1} News Title":news_list[y],f"{y+1} Url":f"{url_list[y]}"} for y in range(len(date_list))]

    news.update({f"Page {num_input}":n})

    # print(f"{soup.title}\n")

async def main():
    url = ['index.html', 'index_2.html', 'index_3.html', 'index_4.html']
    urls = []
    
    for j in range(int(page_num)):
        urls.append('https://www.sfc.keio.ac.jp/en/news/sfc/'+url[j])

    logging.info("program started\n")
    futures = [asyncio.create_task(get_text_from_url(num, url)) for num, url in enumerate(urls, start=1)]
                                                           # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
    logging.info("program ended\n")

    # print(result)




"""Quart web programming"""


app = Quart(__name__)

@app.route("/")
async def result():
    pass

@app.route("/get_result")
async def get_result():
    return jsonify({"KEIO Latest News":news})



if __name__ == "__main__":
    page_num, news_num = sys.stdin.readline().split()
    news={}

    start = time.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = time.time()
    logging.info(f'time taken: {end-start}')

    app.run(debug=True)
    