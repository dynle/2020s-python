from bs4 import BeautifulSoup as bs
import requests
import time as t
import asyncio
from functools import partial
import logging
import sys
import re
from multiprocessing import Queue
# from collections import OrderedDict
from quart import Quart, jsonify, request

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%I:%M:%S', level=logging.INFO)

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

        #beaitufiul soup - New cases
        newcases = soup.find("div",id=f"newsdate{t.strftime('%Y')}-{t.strftime('%m')}-{int(t.strftime('%d'))-2}").get_text().strip().replace("\n","-")
        
        #beautifulsoup - country name
        country = soup.find(style="text-align:center;width:100%").get_text(strip=True)

        # n=[] #refresh
        n = [{"Coronavirus Cases":cases,
        "Deaths":deaths,
        "Recovered":recovered,
        "New cases":newcases}]

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

@app.route("/")
async def result():
    pass

@app.route("/get_result")
async def get_result():
    return jsonify({"Coronavirus situation":info})



if __name__ == "__main__":
    countries = sys.stdin.readline().split()
    print(countries)
    info={} #refresh

    start = t.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = t.time()
    logging.info(f'time taken: {end-start}')

    app.run(debug=True)
    