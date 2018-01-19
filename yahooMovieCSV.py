import requests
import re
from bs4 import BeautifulSoup
import csv

file = open('../Desktop/yahoo-spyder/movie.csv','w',encoding="utf-8")
writer = csv.writer(file)
movie_index = ['name','english_name','category',
               'release','time','company','director',
               'actor','expectation','expectation_people',
               'satisfaction','satisfaction_people']
writer.writerow(movie_index)

for i in range(8000):
    #print(i)
    url = 'https://movies.yahoo.com.tw/movieinfo_main.html/id=' + str(i)
    html = requests.get(url)
    sp = BeautifulSoup(html.text, 'html.parser')
    
    script = sp.find_all("script")
    #print(script[-2].text)
    
    if "找不到您訪問的頁面" in script[-2].text:
        print("break")
    else:
        movie_block = sp.select(".l_box_inner")#尋找電影資訊相關區塊 -- select 網頁中class名為l_box_inner的tag 
        #print(movie_block)

        movie_intro_foto = movie_block[0].select(".movie_intro_foto")
        movie_photo_url = movie_intro_foto[0].img['src']
        print(movie_photo_url)
        #print(html.text)

        movie_infor = sp.select(".movie_intro_info_r")#尋找電影資訊相關區塊 -- select 網頁中class名為movie_intro_info_r的tag 
        #print(movie_infor)

        #----------電影中文名稱----------
        movie_name = movie_infor[0].find_all('h1')#找電影中文名稱
        print("電影名稱：" + str(movie_name[0].text))
        name = str(movie_name[0].text)
        
        #----------找電影中文名稱----------
        movie_englishName = movie_infor[0].find_all('h3')#找電影英文名稱
        print("電影英文名稱：" + str(movie_englishName[0].text))
        english_name = str(movie_englishName[0].text)
        
        #----------電影分類----------
        category=""
        movie_category_block = movie_infor[0].select('.level_name_box')
        movie_category = movie_category_block[0].find_all('a',{'class':'gabtn'})
        print("電影分類：", end="")
        for i in range(len(movie_category)):
            print(movie_category[i].text.replace('\n','').replace(' ',''), end=" ")
            category += movie_category[i].text.replace('\n','').replace(' ','')
        #     print(movie_category[i]['data-ga'])
        #     print((movie_category[i]['data-ga'][23:-2]), end=" ")
        print()
        
        movie_span = movie_infor[0].find_all('span')
        #print(movie_span)

        #----------上映日期----------
        movie_release = movie_span[0]
        movie_release_len = len(movie_release.text)
        #print("len"+str(movie_release_len))
        print("上映日期："+movie_release.text[5:movie_release_len])
        release = movie_release.text[5:movie_release_len]

        #----------片長---------
        movie_time = movie_span[1]
        movie_time_len = len(movie_time.text)
        print("片長："+movie_time.text[5:movie_time_len])
        time = movie_time.text[5:movie_time_len]
        
        #----------發行公司---------
        movie_company = movie_span[2]
        movie_company_len = len(movie_company.text)
        print("發行公司："+movie_company.text[5:movie_company_len])
        company  = movie_company.text[5:movie_company_len]
        
        #----------導演---------
        movie_intro_list = sp.select(".movie_intro_list") 
        print("導演："+movie_intro_list[0].text.replace('\n','').replace(' ',''))
        director = movie_intro_list[0].text.replace('\n','').replace(' ','')
        
        #----------演員---------
        #print(movie_intro_list[1])
        print("演員："+movie_intro_list[1].text.replace('\n','').replace(' ','').replace('、',','))
        # movie_actor = movie_intro_list[1].find_all('a')
        # movie_actor_len = len(movie_actor)
        # if not movie_actor_len == 0:
        #     for i in range(movie_actor_len):
        #         print(movie_actor[i].text)
        actor = movie_intro_list[1].text.replace('\n','').replace(' ','').replace('、',',')

        evaluatebox = sp.select(".evaluatebox")#尋找電影資訊相關區塊 -- select 網頁中class名為l_box_inner的tag 
        #print(evaluatebox)

        expectation = evaluatebox[0].find_all('dt')
        #print(expectation)
        expectation_people_vote = expectation[0].find_all('span')
        #print(expectation_people_vote)
        expectation_value = 0
        if len(expectation_people_vote) == 2:
            expectation_value = int(expectation_people_vote[1].text)

        print("期待度："+str(expectation_value)+"%")
        print(expectation_people_vote[0].text[2:-4])
        expectation_people = expectation_people_vote[0].text[2:-4]
        
        satisfaction = evaluatebox[0].find_all('dd')
        #print(satisfaction)
        satisfaction_people_vote = satisfaction[0].find_all('span')
        #print(satisfaction_people_vote)
        satisfaction_value = 0
        satisfaction_value = satisfaction[0].find_all('div',{'class':'score_num'})[0].text

        print("滿意度："+str(satisfaction_value)+"%")
        print(satisfaction_people_vote[0].text[2:-4])
        satisfaction_people = satisfaction_people_vote[0].text[2:-4]
        
        row = [name,english_name,category,
               release,time,company,director,
               actor,expectation_value,expectation_people,
               satisfaction_value,satisfaction_people]
        writer.writerow(row)

file.close()