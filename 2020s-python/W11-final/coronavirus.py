from bs4 import BeautifulSoup as bs
import requests
import time as t
import asyncio
from functools import partial
import logging
import sys
import re
from multiprocessing import Queue, Process
# from collections import OrderedDict
from quart import Quart, jsonify, request
import webbrowser
import os

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%I:%M:%S', level=logging.INFO)

# @app.route("/")
def show_country_list():
    # countries = sys.stdin.readline().split()
    # q1 = request.args.get("q1")
    # q2 = request.args.get("q2")
    page = requests.get("https://www.worldometers.info/coronavirus/")
    soup_country_list = bs(page.text,"html.parser")

    country_data = soup_country_list.find_all("a","mt_a")

    #country name
    country_name = [country_data[i].get_text() for i in range(len(country_data))]

    #how to write the country name on terminal
    country_name_terminal = [country_data[i].get("href").replace("country/","") for i in range(len(country_data))]
    country_text = re.compile("\w+[-*\w+]*")
    x = country_text.findall(str(country_name_terminal))
    
    country_list = {}
    for j in range(len(country_name)):
        country_list.update({f"{country_name[j]}":f"{x[j]}"})
        # print({f"{country_name[j]}":f"{x[j]}"})
    
    i = 0
    #list the top 100 countries 
    for key,value in country_list.items():
        print(f"{key}: {value}")
        i += 1
        if i == 99:
            break

    # logging.info(country_list)
    
    # return jsonify({"Country List":country_list})

async def get_text_from_url(num_input,url_input):
    logging.info(f'Send request to ... {url_input}\n')
    loop = asyncio.get_event_loop()

    request = partial(requests.get, url_input, headers={'user-agent': 'Mozilla/5.0'})
    
    res = await loop.run_in_executor(None, request)
    logging.info(f'Get response from ... {url_input}\n')
    soup = bs(res.text, 'html.parser')

    try:
        #beautiful soup - coronavirus cases
        cases = soup.find_all("div","maincounter-number")[0].get_text(strip=True)

        #beautiful soup - deaths
        deaths = soup.find_all("div","maincounter-number")[1].get_text(strip=True)

        #beautiful soup - recovered
        recovered = soup.find_all("div","maincounter-number")[2].get_text(strip=True)

        # beaitufiul soup - New cases
        year = 0
        month = 0
        day = 0
        for i in range(int(t.strftime('%d'))):
            try:
                newcases = soup.find("div",id=f"newsdate{t.strftime('%Y')}-{t.strftime('%m')}-{int(t.strftime('%d'))-i}").get_text().strip()
                for r in (("\n","-"),("\u00a0[source]","")):
                    newcases = newcases.replace(*r)
                day = int(t.strftime('%d')) - i
                break
            except:
                continue
        year = t.strftime('%Y')
        month = t.strftime('%m')
        
        if day == 0:
            year = "X"
            month = "X"
            day = "X"
            newcases = "No current new cases"

        
        #beautifulsoup - country name
        country = soup.find(style="text-align:center;width:100%").get_text(strip=True)

        # n=[] #refresh
        n = [{"Coronavirus Cases":cases,
        "Deaths":deaths,
        "Recovered":recovered,
        f"New cases on {t.strftime('%m')} {year}-{month}-{day}":newcases}]

        info.update({f"{num_input+1} {country}":n})
    except:
        logging.info("Incorrect country name")
        sys.exit()


async def main():
    urls = ['https://www.worldometers.info/coronavirus/country/'+country for country in countries]

    logging.info("program started\n")
    futures = [asyncio.create_task(get_text_from_url(num,url)) for num,url in enumerate(urls)]
                                                           # 태스크(퓨처) 객체를 리스트로 만듦
    result = await asyncio.gather(*futures)                # 결과를 한꺼번에 가져옴
    logging.info("program ended\n")

    # print(result)



"""Quart web programming"""


app = Quart(__name__)


@app.route("/get_result")
async def get_result():
    return jsonify({"Coronavirus situation":info})



if __name__ == "__main__":
    
    show_country_list()
    
    countries = sys.stdin.readline().split() #get inputs from terminal in the form of list
    print(countries)

    info={}

    
    start = t.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = t.time()
    logging.info(f'time taken: {end-start}')
    webbrowser.open("http://127.0.0.1:5000/get_result")
    app.run(debug=True)
    # server = Process(target=app.run(debug=True))
    # server.start()
    # server.terminate()
    # server.join()


    #country 목록 확인
    #refresh
    