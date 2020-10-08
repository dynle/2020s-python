from bs4 import BeautifulSoup as bs
from quart import Quart, jsonify
from functools import partial
from multiprocessing import Queue
import requests
import time as t
import asyncio
import logging
import sys
import re
import webbrowser

logging.basicConfig(format='%(asctime)s %(message)s',datefmt='%I:%M:%S', level=logging.INFO)

def show_country_list():
    page = requests.get("https://www.worldometers.info/coronavirus/")
    soup_country_list = bs(page.text,"html.parser")

    country_data = soup_country_list.find_all("a","mt_a")

    #country name
    country_name = [country_data[i].get_text() for i in range(len(country_data))]

    #get the text of how to write country names on terminal
    country_name_terminal = [country_data[i].get("href").replace("country/","") for i in range(len(country_data))]
    country_text = re.compile("\w+[-*\w+]*")
    country_result = country_text.findall(str(country_name_terminal))
    
    #list the top 100 countries by the number of total cases
    country_list = {}
    for j in range(len(country_name)):
        country_list.update({f"{country_name[j]}":f"{country_result[j]}"})
    
    i = 0
    for key,value in country_list.items():
        print(f"{key}: {value}")
        i += 1
        if i == 99:
            break

async def get_text_from_url(num_input,url_input):
    logging.info(f'Send request to ... {url_input}\n')

    request = partial(requests.get, url_input)
    
    res = await loop.run_in_executor(None, request)
    logging.info(f'Get response from ... {url_input}\n')
    soup = bs(res.text, 'html.parser')

    try:
        #beautiful soup - country name, coronavirus cases, deaths, and recovered, respectively
        country = soup.find(style="text-align:center;width:100%").get_text(strip=True)
        cases = soup.find_all("div","maincounter-number")[0].get_text(strip=True)
        deaths = soup.find_all("div","maincounter-number")[1].get_text(strip=True)
        recovered = soup.find_all("div","maincounter-number")[2].get_text(strip=True)

        # beautiful soup - New cases
        year = 0
        month = 0
        day = 0
        for i in range(int(t.strftime('%d'))):
            try:
                newcases = soup.find("div",id=f"newsdate{t.strftime('%Y')}-{t.strftime('%m')}-{int(t.strftime('%d'))-i}").get_text().strip()
                for r in (("\n","-"),("\u00a0",""),("[source]","")):
                    newcases = newcases.replace(*r)
                year = t.strftime('%Y') 
                month =t.strftime('%m')
                day = int(t.strftime('%d')) - i
                break
            except:
                continue
        if day == 0:
            year = "X"
            month = "X" 
            day = "X"
            newcases = f"No current new cases in {t.strftime('%m')}"

        #save coronavirus cases, deaths, recovered, and new cases in variable 'country_data'
        country_data = [{"Coronavirus Cases":cases,"Deaths":deaths,"Recovered":recovered,
        f"Total New Cases in {t.strftime('%m')} {year}-{month}-{day}":newcases}] 

        #save country_data in dictionary 'info' which collects individual country data
        info.update({f"{num_input} {country}":country_data})
    except:
        #terminate the program when a user inputs wrong country name text on terminal
        logging.info("Incorrect country name")
        sys.exit()

async def main():
    urls = ['https://www.worldometers.info/coronavirus/country/'+country for country in countries]

    logging.info("Program started\n")
    futures = [asyncio.create_task(get_text_from_url(num,url)) for num,url in enumerate(urls, start=1)]
    await asyncio.gather(*futures)                
    logging.info("Program ended\n")

"""Quart web server"""

app = Quart(__name__)

@app.route("/get_result")
async def get_result():
    return jsonify({"Coronavirus situation":info})

if __name__ == "__main__":
    #show possible country list on terminal
    show_country_list()
    
    #get inputs from terminal in list
    countries = sys.stdin.readline().split()
    logging.info(countries)

    info={}

    start = t.time()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    end = t.time()
    logging.info(f'time taken: {end-start}')
    webbrowser.open("http://127.0.0.1:5000/get_result")
    app.run(debug=True)
    