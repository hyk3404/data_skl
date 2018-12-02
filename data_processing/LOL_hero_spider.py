import  requests
from bs4 import BeautifulSoup
import csv
import json

LOL_url = 'http://lol.duowan.com/hero/' #用變數儲存要爬的網址

def get_all_href(url): #功能 ： 把所有不同英雄的網址加進list裏面
     
    all_href_list = [] #存所有href的list
    re = requests.get(url) #get網頁資料
    soup = BeautifulSoup(re.text, "html.parser") #用BeautifulSoup解析網頁的變數
    results = soup.findAll("a",{"target":"_blank", "class":"lol_champion"}) #用soup變數找href

    for item in results: #用for把所有爬到的href append至all_href_list
        all_href_list.append(item.get('href'))
    return get_hero_data(all_href_list) #把list傳給下一個def

def get_hero_data(href):# 功能 ： 把list裏面的網址一個個get,並把英雄資訊爬下來存成dic

    all_hero_list = []  #預設1個存全英雄資料的list

    for hero_href in href:  #用for把每個網址從href提出來

        em_list = []    #預設1個list 用來存全部<em>
        span_list = []  #預設1個list 用來存全部<span>
        hero_dic = {}   #預設1個Dictionary 用來存單個英雄資料
        hero_name = hero_href.replace("http://lol.duowan.com/","")[:-1] #預設1個擁有英雄名稱的變數

        if(hero_href[0]=="h"): #href第1個字=="h",直接get               <---
            re = requests.get(hero_href)#                               |
            soup = BeautifulSoup(re.text, "html.parser")#               |
                                                        #               |---用來處理寫很亂的網頁
        else:#                                                          |                                             
            re = requests.get(hero_href[1:]) #反之從herf[1:]開始get      |
            soup = BeautifulSoup(re.text, "html.parser")#            <---
            
        div = soup.find("div", {"class":"hero-box ext-attr"}) #把網頁1層層拆解
        div2 = div.find("div", {"class":"hero-box__bd"})      #建議拆兩層以上,因為有些網頁寫很亂,這樣比較能爬到正確資料
        em = div2.findAll("em") #要爬的key
        span =div2.findAll("span") #要爬的value

        for dirty_em in em: #把每個em的字元append到em_list
            em_list.append(dirty_em.text[:-1])
            # print(dirty_em.text[:-1])
        for dirty_span in span: #把每個span的字元append到span_list
            span_list.append(dirty_span.text)
            # print(dirty_span.text)
        
        hero_dic = dict(zip(em_list, span_list)) #以em為key,span為value合併成1個各英雄的Dictionary
        hero_dic["name"] = hero_name #為這個Dictionary新增name的資料來存放hero_name
        
        all_hero_list.append(hero_dic) #把每隻英雄的Dictionary append至all_hero_list

        print(hero_dic)
        print("=======")
    
    return json_output(all_hero_list) #把dic傳給下一個def

def json_output(all_hero_list): #功能 ： 把儲存所有英雄資料的dic轉成json格式,並寫成json檔

    with open('data.json', 'w') as f: #創一個叫data.json的檔案,並write資料
        json.dump(all_hero_list, f) #把資料轉換成json
    

get_all_href(LOL_url)
