import requests
import re 
import mysql.connector 
from bs4 import BeautifulSoup

def get_data(): 
    for i in range(10):

        #print(i)
        url = 'https://movies.yahoo.com.tw/movieinfo_main.html/id=' + str(i)
        html = requests.get(url)
        sp = BeautifulSoup(html.text, 'html.parser')

        script = sp.find_all("script")
        #print(script[-2].text)

        if "找不到您訪問的頁面" in script[-2].text:
            print("break")
        else:
            if(check_yahoo_id(i)==False):
                print("id:"+str(i))
                movie_block = sp.select(".l_box_inner")#尋找電影資訊相關區塊 -- select 網頁中class名為l_box_inner的tag 
                #print(movie_block)

                movie_intro_foto = movie_block[0].select(".movie_intro_foto")
                movie_photo_url = movie_intro_foto[0].img['src']
                print(movie_photo_url)
                #print(html.text)
                movie_poster_url = upload_to_S3(movie_photo_url,i)#儲存海報至S3
                movie_poster_url_resize = upload_to_S3_resize(movie_photo_url,i)#調整海報大小
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

                #----------電影介紹----------
                movie_intro_block = sp.select(".gray_infobox_inner")
                movie_intro = movie_intro_block[0].find_all('span')[0].text
                print("電影介紹：" + movie_intro)

                ##----------電影分類----------
                category=""
                category_array = []
                movie_category_block = movie_infor[0].select('.level_name_box')
                movie_category = movie_category_block[0].find_all('a',{'class':'gabtn'})
                print("電影分類：", end="")
                #print(movie_category)
                for i in range(len(movie_category)):
    #                 print(movie_category[i].text.replace('\n','').replace(' ',''), end=" ")
                    category += movie_category[i].text.replace('\n','').replace(' ','')
                    movie_category_per = movie_category[i].text.replace('\n','').replace(' ','').replace('"','')
                    print("movie_category_per"+movie_category_per)#print category name
                    category_array.append(movie_category_per)
                #     print(movie_category[i]['data-ga'])
                #     print((movie_category[i]['data-ga'][23:-2]), end=" ")
                print()
                print("category_array"+json.dumps(category_array, ensure_ascii=False))
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

                #----------官方網站--------
                movie_url_company = movie_infor[0].find_all('a', attrs={'class':'gabtn','target':'_blank'})
                movie_url_array = []
                #movie_url_company = movie_infor[0].find_all('a', attrs={'data-ga':'[\'電影介紹\',\'電影介紹_類型icon\',\'劇情\']'})
                for a in range(len(movie_url_company)):
                    print(movie_url_company[a].text)
                    movie_url_array.append(movie_url_company[a].text)
                movie_url_json = json.dumps(movie_url_array, ensure_ascii=False)
                print(movie_url_json)

                #----------期待度--------
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

                #----------滿意度--------
                satisfaction = evaluatebox[0].find_all('dd')
                #print(satisfaction)
                satisfaction_people_vote = satisfaction[0].find_all('span')
                #print(satisfaction_people_vote)
                satisfaction_value = 0
                satisfaction_value = satisfaction[0].find_all('div',{'class':'score_num'})[0].text

                print("滿意度："+str(satisfaction_value)+"%")
                print(satisfaction_people_vote[0].text[2:-4])
                satisfaction_people = satisfaction_people_vote[0].text[2:-4]


                connect_to_mysql(name,english_name,category,
                       release,time,company,director,
                       actor,expectation_value,expectation_people,
                       satisfaction_value,satisfaction_people,movie_poster_url)

def connect_to_mysql(name,english_name,category, release,time,company,director, actor,expectation_value,expectation_people, satisfaction_value,satisfaction_people,movie_photo_url): 
    cnx = mysql.connector.connect(user='username', password='password', host='127.0.0.1', database='movie')

    cursor = cnx.cursor()

    query = ("INSERT INTO `movies`"+
             "(`id`, `name`, `englishName`, `category`, `release`, `time`, `company`, `director`, `actor`, `expectation_value`, `expectation_people`, `satisfaction_value`, `satisfaction_people`, `movie_img`) "+
             "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
    #print(query)
    test = ('null',name,english_name,category,
                   release,time,company,director,
                   actor,expectation_value,expectation_people,
                   satisfaction_value,satisfaction_people,movie_photo_url)

    # Insert new employee
    cursor.execute(query, test)
    # cursor.execute(query)
    emp_no = cursor.lastrowid

    cnx.commit()
    cursor.close()

    cnx.close()
#--------------------------------------uplooad to S3--------------------------------------
import boto 
import boto.s3 
import sys 
from boto.s3.key import Key

from PIL import Image 
from urllib.request import urlopen 
import urllib

def upload_to_S3(movie_url,movie_number): 
    AWS_ACCESS_KEY_ID = '' #AWS_ACCESS_KEY_ID 
    AWS_SECRET_ACCESS_KEY = '' #AWS_SECRET_ACCESS_KEY

    bucket_name = 'bucket_name' #bucket_name
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)# connect S3
    bucket = conn.get_bucket(bucket_name)
    img_name = "movie_"+str(movie_number) #create image name
    urllib.request.urlretrieve(movie_url, "photo/"+str(img_name)+".png") #download and save

    testfile = "photo/"+img_name+".png" #file path

    k = Key(bucket)
    k.key = img_name+'.png' #upload file name
    k.set_contents_from_filename(testfile,cb=percent_cb, num_cb=10)
    k.make_public()# make image access public
    url = k.generate_url(expires_in=0, query_auth=False)# get generate url
    print(url)
    return url


def upload_to_S3_resize(movie_url,movie_number): 
    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''

    bucket_name = 'bucket_name' #bucket_name
    conn = boto.connect_s3(AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY)# connect S3
    bucket = conn.get_bucket(bucket_name)
    img_name = "movie_"+str(movie_number) #create image name
    urllib.request.urlretrieve(movie_url, "photo/"+str(img_name)+".png") #download and save

    testfile = "photo/"+img_name+".png" #file path
    im = Image.open(testfile)
    print(im.size)

    # Calculate the ratio
    width = 500
    ratio = float(width)/im.size[0]
    height = int(im.size[1]*ratio)
    nim = im.resize( (width, height), Image.BILINEAR )
    print(nim.size)
    #nim.show()
    resizefile = "photo/"+img_name+"_resize.png"
    nim.save(resizefile)
    
    k = Key(bucket)
    k.key = img_name+'_resize.png' #upload file name
    k.set_contents_from_filename(resizefile,cb=percent_cb, num_cb=10)
    k.make_public()# make image access public
    url = k.generate_url(expires_in=0, query_auth=False)# get generate url
    print(url)
    return url

def percent_cb(complete, total): 
    sys.stdout.write('.') 
    sys.stdout.flush()

#------------------------------ check yahoo movie id arleay exist------------------------------
def check_yahoo_id(yahoo_id):
    cnx = mysql.connector.connect(user='root', password='', host='127.0.0.1', database='movier')

    cursor = cnx.cursor()

    query = ("SELECT * FROM `yahoo` WHERE `movie_id`=%d"%(yahoo_id))
    print(query)
    yahoo_id_sql = yahoo_id

    # Insert new employee
#     cursor.execute(query, (yahoo_id_sql))
    cursor.execute(query)
    # cursor.execute(query)
    row = cursor.fetchone()
    if(row == None):
        return False
    else:
        return True

    cnx.commit()
    cursor.close()

    cnx.close()

get_data()