# -*- coding: utf-8 -*-
# @ KFootball_bot

import telegram

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup 

import time
from datetime import datetime

# global variable정
alert_date = 1              # 알림을 받고 싶은 날짜 지정 가능


kfootball = {"date": [], "time": [], "country": [], "place": []}


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_driver_path = "C:/Users/SKTelecom/Downloads/chromedriver.exe"
driver = webdriver.Chrome(options = chrome_options, executable_path = chrome_driver_path)

today = time.localtime()
today = str(time.asctime(today))
year = str(today[len(today)-4:len(today)])

url = str("https://sports.news.naver.com/kfootball/schedule/index.nhn?year=" + year + "&category=amatch")

driver.get(url)
html = BeautifulSoup(driver.page_source, features="lxml")     
play_list = html.find("tbody", {"id": "_monthlyScheduleList"}).findAll("tr", {"class": "division"})

for i in range(len(play_list)):
    schedule_date = (play_list[i].find("th").find("div", {"class": "inner"}).find("em")).string
    schedule_date = str(schedule_date.split(".")[0] + "월 " + schedule_date.split(".")[1] + "일 ")
    
    schedule_day = str(play_list[i].find("th").find("div", {"class": "inner"}))
    schedule_day = schedule_day[schedule_day.find("(")+1:schedule_day.find(")")]
    
    schedule_date = schedule_date + schedule_day + "요일"
    
    schedule_time = (play_list[i].find("td", {"class": "time_place"}).find("div", {"class": "inner"}).find("span", {"class": "time"})).string
    schedule_minute = schedule_time.split(":")[1]
    schedule_time = schedule_time.split(":")[0]
    
    if int(schedule_time) > 12:
        schedule_time = "오후 " + str((int(schedule_time) - 12)) + "시"
    else:
        schedule_time = "오전 " + schedule_time + "시"
    
    if schedule_minute != "00":
        schedule_time = schedule_time + " " + schedule_minute + "분"
        
        
    schedule_place = str((play_list[i].find("td", {"class": "time_place"}).find("div", {"class": "inner"}).find("span", {"class": "place"})).string)
    if schedule_place == "None":
        schedule_place = "<장소 미정>"

    schedule_country = play_list[i].find("td", {"class": None})
    #schedule_country = schedule_country.find("div", {"class": "inner "})
    schedule_country = schedule_country.find("span", {"class": "team_right"})
    schedule_country = schedule_country.find("span", {"class": "name"}).string
    
    kfootball["date"].append(schedule_date)
    kfootball["time"].append(schedule_time)
    kfootball["place"].append(schedule_place)
    kfootball["country"].append(schedule_country)
        

        
import os

def Compare(kfootball):
    
    bot = telegram.Bot(token = ##########)
    chat_id = bot.getUpdates()[-1].message.chat.id                    #메세지를 보내기 위한 chat id 구하기
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    temp = []
    cnt = 0
    
    with open(os.path.join(BASE_DIR, 'DO_NOT_DELETE.txt'), 'r') as f_read:     #compare.txt 열기
        before = f_read.readlines()             # 개행 구분하여 읽기
        before = [line.rstrip() for line in before] #(/n)strip in list
        f_read.close()
        
        for i in kfootball["date"]:
            if i not in before:
                temp.append(i)
                cnt = cnt + 1
                with open(os.path.join(BASE_DIR, 'DO_NOT_DELETE.txt'), 'a') as f_write:
                    f_write.write(i+'\n') 
                    f_write.close()
        if cnt > 0:
            maintext(kfootball, chat_id, bot)
            
        today_date = int(str(datetime.now()).split(" ")[0].split("-")[2])
        
        if today_date == alert_date:
            dateChecker(kfootball, chat_id, bot)
            
            
            

def maintext(kfootball, chat_id, bot):
    NEW = "[+] 대한민국 축구 대표팀 경기가 새로 업데이트되었습니다."
    bot.sendMessage(chat_id = chat_id, text = NEW)
    
    
    my_text = ""
    for i in range(len(kfootball["date"])):
        my_text = my_text + "[" + str(kfootball["date"][i]) + "] " + "대한민국 vs. " + str(kfootball["country"][i])
        my_text = my_text + "\n"
    bot.sendMessage(chat_id = chat_id, text = my_text)





def dateChecker(kfootball, chat_id, bot):
    today_month = int(str(datetime.now()).split(" ")[0].split("-")[1])
    my_text = ""
    
    for i in range(len(kfootball["date"])):
        if int(kfootball["date"][i].split("월")[0]) == today_month:
            my_text = my_text + "[" + str(kfootball["date"][i]) + "] " + "대한민국 vs. " + str(kfootball["country"][i])
            my_text = my_text + "\n"
            
    if my_text != "":
        ALERT = "★ %d월에 예정되어있는 대한민국 축구 대표팀 경기 일정 알려드릴게요." % today_month
        bot.sendMessage(chat_id = chat_id, text = ALERT)
        bot.sendMessage(chat_id = chat_id, text = my_text)
    else:
        ALERT = "%d월에는 대한민국 축구 대표팀 경기가 예정되어 있지 않습니다." % today_month
        bot.sendMessage(chat_id = chat_id, text = ALERT)
            
            
            
Compare(kfootball)

while True:
    time.sleep(1000)
