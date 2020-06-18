import re 
import csv 
import requests 
from bs4 import BeautifulSoup as bs

page = requests.get("https://darksky.net/forecast/37.2004,127.0958/si12/en")
soup = bs(page.text,"html.parser")

with open("weather_data.csv","w",encoding="utf-8", newline='') as f:
    wr = csv.writer(f)

    #store summary
    summary = soup.find("div",{"class":"summary"})
    summary_find = re.compile("[A-Z][^\.!?]*[\.!?]")
    summary_search = summary_find.findall(str(summary))

    #store day
    day = soup.find_all(class_="name")
    day_find = re.compile("\s+[A-Z]+\w+")
    day_list = day_find.findall(str(day))
    for i in range(len(day_list)):
        day_list[i] = day_list[i].replace("\n","").strip()

    #store min temp
    min_ = soup.find_all(class_="minTemp")
    min_num_find = re.compile("\d+˚")
    min_list = min_num_find.findall(str(min_))
    for j in range(len(min_list)):
        min_list[j] = min_list[j].replace("˚","")

    #store max temp
    max_ = soup.find_all(class_="maxTemp")
    max_num_find = re.compile("\d+˚")
    max_list = max_num_find.findall(str(max_))
    for z in range(len(max_list)):
        max_list[z] = max_list[z].replace("˚","")

    #store min and max time for each day
    time = soup.find_all("div",{"highLowTemp swip"})
    time_find = re.compile("\d+\w{2}")
    time_list = time_find.findall(str(time))

    #store rain
    rain = soup.find_all("span",{"class":"num swip"})
    rain_find = re.compile("\d+\.*\d*")
    rain_list = rain_find.findall(str(rain))
    
    #save csv file
    wr.writerow(["Weather in the area where I live in"])
    wr.writerow(summary_search)
    wr.writerow(["Day","Min temp","Min time","Max temp","Max time","Rain"])
    for y in range(len(day_list)):
        wr.writerow([day_list[y],min_list[y],time_list[2*y],max_list[y],time_list[2*y+1 if y != 0 else 1],rain_list[y]+" mm"])


