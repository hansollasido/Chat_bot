from audioop import reverse
from telnetlib import STATUS
from tkinter.messagebox import QUESTION
from typing import List
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from .models import *
import json
import csv
import pandas as pd
import random
import time
import tensorflow as tf
import pandas as pd
from tensorflow.keras.models import Model, load_model
from tensorflow.keras import preprocessing
from tensorflow.keras.layers import Input, Embedding, Dense, Dropout, Conv1D, GlobalMaxPool1D, concatenate
from hanspell import spell_checker
from konlpy.tag import Komoran
import numpy as np
from numpy import dot
from numpy.linalg import norm
from konlpy.tag import Komoran
import time
import re
import sys
import random
import datetime
from bs4 import BeautifulSoup
import requests
from datetime import date
from datetime import timedelta
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless= True
options.add_argument("window-size=1920x1080")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
browser = webdriver.Chrome(options=options) # 현재 폴더에 있는 chromedriver

browser.implicitly_wait(10)

data = pd.read_excel('C:\\Users\\beomh\\Desktop\\아주대\\2022\\프로젝트\\알고리즘\\data_for_chat.xlsx')
data.fillna('',inplace=True)

model = load_model('C:\\Users\\beomh\\Desktop\\아주대\\2022\\프로젝트\\알고리즘\\cnn_new_model.h5')
model2 = load_model('C:\\Users\\beomh\\Desktop\\아주대\\2022\\프로젝트\\알고리즘\\cnn_new_label2_model.h5')

m = re.compile("^N")
n = re.compile("^V")
o = re.compile("^X")

now = datetime.now()

headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

#오늘 최신 공지
def notice_latest():
    title_link_sum = ['notice_test']
    url = r'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset=0'
    res = requests.get(url,headers=headers)
    res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
    soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
    notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
    notices2 = soup.find_all("tr",attrs={"class":""})
    notices3 = notices2[1].find("td",attrs={"class":"b-num-box"})
    first_number = int(notices3.get_text())
    # print(first_number)

    notices1_2 = notices1[0].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
    notices1_3 = notices1[0].find("a")

    #년도-월-일
    date1 = now.strftime('%Y-%m-%d')
    # date1 = '2022-03-25'
    date2 = notices1_2.get_text()

    link1 = "https://ajou.ac.kr/kr/ajou/notice.do"+notices1_3['href']
    title1 = notices1_3['title']

    # print(date1)
    if date1 == date2 :
        # 오늘 중요 공지가 올라왔을 때 링크와 제목을 print
        print(link1)
        print(title1)


    # 두 페이지에 걸쳐서 오늘자로 나온 공지사항을 가져옴
    for i in range(2):

        # 최신 공지사항들
        url = 'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset={}'.format(i*10)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
        notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
        notices2 = soup.find_all("tr",attrs={"class":""})


        # notices3 = notices2[1].find("td",attrs={"class":"b-num-box"})
        # new_number = int(notices3.get_text())

        for k in range(len(notices2)-1):
            notices4 = notices2[k+1].find("td",attrs={"class":"b-td-left"})
            notices4_1 = notices2[k+1].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
            notices5 = notices4.find("a")
            date3 = notices4_1.get_text()
            title = notices5['title']
            link = "https://ajou.ac.kr/kr/ajou/notice.do"+notices5['href']

            if date3 == date1 :
                # print(title)
                # print(link)
                title_link_sum.append(title)
                title_link_sum.append(link)

        return title_link_sum

#어제 공지 함수
def notice_yesterday():
    title_link_sum = ['notice_test']
    date1 = (datetime.today()-timedelta(1)).strftime('%Y-%m-%d')

    url = r'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset=0'
    res = requests.get(url,headers=headers)
    res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
    soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
    notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
    notices2 = soup.find_all("tr",attrs={"class":""})
    notices3 = notices2[1].find("td",attrs={"class":"b-num-box"})
    first_number = int(notices3.get_text())

    notices1_2 = notices1[0].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
    notices1_3 = notices1[0].find("a")
    date2 = notices1_2.get_text()

    link1 = "https://ajou.ac.kr/kr/ajou/notice.do"+notices1_3['href']
    title1 = notices1_3['title']
    for i in range(4):

        # 최신 공지사항들
        url = 'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset={}'.format(i*10)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
        notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
        notices2 = soup.find_all("tr",attrs={"class":""})

        for k in range(len(notices2)-1):
            notices4 = notices2[k+1].find("td",attrs={"class":"b-td-left"})
            notices4_1 = notices2[k+1].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
            notices5 = notices4.find("a")
            date3 = notices4_1.get_text()
            title = notices5['title']
            link = "https://ajou.ac.kr/kr/ajou/notice.do"+notices5['href']

            if date3 == date1 :
                title_link_sum.append(title)
                title_link_sum.append(link)
    return title_link_sum

#이틀전 공지 함수
def notice_2days():

    title_link_sum = ['notice_test']
    date1 = (datetime.today()-timedelta(2)).strftime('%Y-%m-%d')

    url = r'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset=0'
    res = requests.get(url,headers=headers)
    res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
    soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
    notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
    notices2 = soup.find_all("tr",attrs={"class":""})
    notices3 = notices2[1].find("td",attrs={"class":"b-num-box"})
    first_number = int(notices3.get_text())

    notices1_2 = notices1[0].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
    notices1_3 = notices1[0].find("a")
    date2 = notices1_2.get_text()

    link1 = "https://ajou.ac.kr/kr/ajou/notice.do"+notices1_3['href']
    title1 = notices1_3['title']

    # 두 페이지에 걸쳐서 오늘자로 나온 공지사항을 가져옴
    for i in range(5):

        # 최신 공지사항들
        url = 'https://ajou.ac.kr/kr/ajou/notice.do?mode=list&&articleLimit=10&article.offset={}'.format(i*10)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
        notices1 = soup.find_all("tr",attrs={"class":"b-top-box"})
        notices2 = soup.find_all("tr",attrs={"class":""})

        for k in range(len(notices2)-1):
            notices4 = notices2[k+1].find("td",attrs={"class":"b-td-left"})
            notices4_1 = notices2[k+1].find("td",attrs={"class":"b-no-right"}).find_next_sibling("td").find_next_sibling("td")
            notices5 = notices4.find("a")
            date3 = notices4_1.get_text()
            title = notices5['title']
            link = "https://ajou.ac.kr/kr/ajou/notice.do"+notices5['href']

            if date3 == date1 :
                
                title_link_sum.append(title)
                title_link_sum.append(link)
                
        
    return title_link_sum
#알바 함수
def alba():
    alba_sum = ["notice_test"]
    headers = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}
    url = 'http://www.alba.co.kr/search/Search.asp?WsSrchWord=%BE%C6%C1%D6%B4%EB&wsSrchWordarea=&Section=0&Page=&hidschContainText=&hidWsearchInOut=Y&hidGroupKeyJobArea=&hidGroupKeyJobHotplace=&hidGroupKeyJobJobKind=&hidGroupKeyResumeArea=&hidGroupKeyResumeJobKind=&hidGroupKeyPay=&hidGroupKeyWorkWeek=&hidGroupKeyWorkPeriod=&hidGroupKeyOpt=&hidGroupKeyGender=&hidGroupKeyAge=&hidGroupKeyCareer=&hidGroupKeyLicense=&hidGroupKeyEduData=&hidGroupKeyWorkTime=&hidGroupKeyWorkState=&hidGroupKeyJobCareer=&hidSort=&hidSortOrder=1&hidSortDate=&hidSortCnt=&hidSortFilter=&hidArea=&area=&hidJobKind=&jobkind=&workperiod=&workweek='

    res = requests.get(url,headers=headers)
    res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
    soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

    first = soup.find("li",attrs={'class':'first'})
    first_text1 = first.find('a').get_text()
    first_link1 = 'http://www.alba.co.kr' + first.find('a')['href'] 
    first_info = first.find('p',attrs={'class':'info'}).get_text()
    first_pay = first.find('p',attrs={'class':'payInfo'}).get_text()

    next = first

    for i in range(19):
        next = next.find_next_sibling('li')
        next_text1 = next.find('a').get_text()
        next_link1 = 'http://www.alba.co.kr' + next.find('a')['href'] 
        next_info = next.find('p',attrs={'class':'info'}).get_text()
        next_pay = next.find('p',attrs={'class':'payInfo'}).get_text()
        alba_sum.append(next_text1)
        alba_sum.append(next_link1)
        # print(next_text1)
        # print(next_link1)
    return alba_sum
#장학 함수
def scholarship():
    scholarship_sum = ["notice_test"]
    for i in range(3):
    
            url = 'https://www.dreamspon.com/scholarship/list.html?page={}'.format(i+1)

            res = requests.get(url,headers=headers)
            res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
            soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦
            a = soup.find('tbody').find_all("tr")
            for k in range(len(a)):
                # 아래는 제목
                # print(a[0].get_text())
                # # 아래는 링크
                # print('https://www.dreamspon.com'+a[0].find('a')['href'])
                scholarship_sum.append((a[0].get_text()).replace("\n",""))
                scholarship_sum.append('https://www.dreamspon.com'+a[0].find('a')['href'])
    return scholarship_sum
#공모전 웹 함수
def wevity_web():
    wevity_web_sum = ['notice_test']
    for i in range(2):
        url = 'https://www.wevity.com/?c=find&s=1&gub=1&cidx=20&gp={}'.format(i+1)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

        a = soup.find_all("div",attrs={"class":"main-section"})
        b = a[2].find_all("li")

        for k in range(len(b)):
            if k == 0:
                continue
            # 아래 값들을 return으로 반환좀 
            # 제목
            remove = b[k].get_text().replace("\n","")
            remove = remove.replace("\t","")
            remove = remove.replace("\r","")
            # print(remove)
            # # 링크
            # print('https://www.wevity.com/'+b[k].find('a')['href'])
            wevity_web_sum.append(remove)
            wevity_web_sum.append('https://www.wevity.com/'+b[k].find('a')['href'])
    return wevity_web_sum
            
#공모전 UCC 함수
def wevity_UCC():
    wevity_UCC_sum = ['notice_test']
    for i in range(2):
        url = 'https://www.wevity.com/?c=find&s=1&gub=1&cidx=10&gp={}'.format(i+1)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

        a = soup.find_all("div",attrs={"class":"main-section"})
        b = a[2].find_all("li")
        
        for k in range(len(b)):
            if k == 0:
                continue
            # 아래 값들을 return으로 반환좀 
            # 제목
            remove = b[k].get_text().replace("\n","")
            remove = remove.replace("\t","")
            remove = remove.replace("\r","")
            # print(remove)
            # # 링크
            # print('https://www.wevity.com/'+b[k].find('a')['href'])
            wevity_UCC_sum.append(remove)
            wevity_UCC_sum.append('https://www.wevity.com/'+b[k].find('a')['href'])
    return wevity_UCC_sum


# 공모전_과학 함수
def wevity_Science():
    wevity_Science_sum = ['notice_test']
    for i in range(2):
        url = 'https://www.wevity.com/?c=find&s=1&gub=1&cidx=22&gp={}'.format(i+1)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

        a = soup.find_all("div",attrs={"class":"main-section"})
        b = a[2].find_all("li")
        
        for k in range(len(b)):
            if k == 0:
                continue
            remove = b[k].get_text().replace("\n","")
            remove = remove.replace("\t","")
            remove = remove.replace("\r","")
            # print(remove)
            # # 링크
            # print('https://www.wevity.com/'+b[k].find('a')['href'])
            wevity_Science_sum.append(remove)
            wevity_Science_sum.append('https://www.wevity.com/'+b[k].find('a')['href'])
    return wevity_Science_sum

#공모전_문학 함수
def wevity_literature():
    wevity_literature_sum = ['notice_test']
    for i in range(2):
        url = 'https://www.wevity.com/?c=find&s=1&gub=1&cidx=23&gp={}'.format(i+1)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

        a = soup.find_all("div",attrs={"class":"main-section"})
        b = a[2].find_all("li")
        
        for k in range(len(b)):
            if k == 0:
                continue
            remove = b[k].get_text().replace("\n","")
            remove = remove.replace("\t","")
            remove = remove.replace("\r","")
            # print(remove)
            # # 링크
            # print('https://www.wevity.com/'+b[k].find('a')['href'])
            wevity_literature_sum.append(remove)
            wevity_literature_sum.append('https://www.wevity.com/'+b[k].find('a')['href'])
    return wevity_literature_sum
#공모전_대학생 함수
def wevity_university():
    wevity_university_sum = ['notice_test']
    for i in range(3):
        url = 'https://www.wevity.com/?c=find&s=1&gub=2&cidx=5&gp={}'.format(i+1)
        res = requests.get(url,headers=headers)
        res.raise_for_status() # raise_for_status는 문제가 생기면 바로 에러를 출력
        soup = BeautifulSoup(res.text,"lxml") # res.text를 lxml통해서 beautiful soup 객체로 만듦

        a = soup.find_all("div",attrs={"class":"main-section"})
        b = a[2].find_all("li")
        
        for k in range(len(b)):
            if k == 0:
                continue
            remove = b[k].get_text().replace("\n","")
            remove = remove.replace("\t","")
            remove = remove.replace("\r","")
            # print(remove)
            # # 링크
            # print('https://www.wevity.com/'+b[k].find('a')['href'])
            wevity_university_sum.append(remove)
            wevity_university_sum.append('https://www.wevity.com/'+b[k].find('a')['href'])
    return wevity_university_sum

# 음식점 함수
def map(chat):
    map_sum = ['notice_test']
    browser.get("https://www.naver.com/")
    options.headless= True
    browser.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/div/input').send_keys("아주대 {}".format(chat),Keys.ENTER)
    try:
        for k in range(3):
            # time.sleep()
            a = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[3]/section[1]/div/div[2]/ul').find_elements_by_tag_name('li')
        
            for i in range(len(a)):
                store = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[3]/section[1]/div/div[2]/ul/li[{}]/div[1]/a/div[1]/div/span'.format(i+1)).text

                explain = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[3]/section[1]/div/div[2]/ul/li[{}]/div[1]/a/div[2]'.format(i+1)).text

                place = browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[3]/section[1]/div/div[2]/ul/li[{}]/div[1]'.format(i+1)).find_element_by_tag_name('a').get_attribute("href")  

                map_sum.append(store.replace("\n","<br/>"))
                map_sum.append(explain.replace("\n"," "))
                map_sum.append(place)


            browser.find_element_by_xpath('/html/body/div[3]/div[2]/div/div[1]/div[2]/div[3]/section[1]/div/div[2]/div[3]/a[2]').click()
        return map_sum
    except:
        return "뭔 말인지 모르겠어."
        
# 동아리 함수  
def group(chat):
    # options.headless= False
    browser = webdriver.Chrome(options=options)
    browser.get("https://linkareer.com/list/club")
    
    browser.maximize_window()

    group_sum = ['notice_test']
    for row in range(5):
        for n in range(4):
            title = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[4]/div/div[2]/div[1]/div[{}]/div[{}]/div/div[2]/a/h5'.format(row+1,n+1)).text
            d_day = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[4]/div/div[2]/div[1]/div[{}]/div[{}]/div/div[2]/div/div/h4[1]'.format(row+1,n+1)).text
            where = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[4]/div/div[2]/div[1]/div[{}]/div[{}]/div/div[2]/div/p'.format(row+1,n+1)).text
            link = browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/div[4]/div/div[2]/div[1]/div[{}]/div[{}]/div/div[2]/a'.format(row+1,n+1)).get_attribute("href")

            group_sum.append(title)
            group_sum.append(d_day)
            group_sum.append(where) 
            group_sum.append(link)

    return group_sum

class Preprocess:
    def __init__(self, userdic = None):
        self.komoran = Komoran(userdic=userdic)
        self.exclusion_tags = [
            'JKS','JKC', 'JKG', 'JKB', 'JKV', 'JKQ', 'JX', 'JC', 'SF', 'SP', 'SS', 'SE', 'SO', 'EP', 'EF', 'EC', 'ETN', 'ETM', 'XSN', 'XSV', 'XSA'
            ]
        
    def pos(self, sentence):
        return self.komoran.pos(sentence)
    
    def get_keywords(self, pos, without_tag = False):
        f = lambda x : x in self.exclusion_tags
        word_list = []
        for p in pos:
            if f(p[1]) is False:
                word_list.append(p if without_tag is False else p[0])
        return word_list

def cos_sim(vec1, vec2):
    return dot(vec1, vec2) / (norm(vec1)*norm(vec2))

def make_term_doc_mat(sentence_bow, word_dics):
    freq_mat={}
    
    for word in word_dics:
        freq_mat[word] = 0
        
    for word in word_dics:
        if word in sentence_bow:
            freq_mat[word] += 1
            
    return freq_mat

def make_vector(tdm):
    vec = []
    for key in tdm:
        vec.append(tdm[key])
    return vec


p = Preprocess(userdic='C:\\Users\\beomh\\Desktop\\아주대\\2022\\프로젝트\\알고리즘\\user_dic.tsv')

def data_loading3(request):
    path = "C:\\Users\\beomh\\Desktop\\아주대\\2022\\프로젝트\\csv_data\\test1.csv"
    reader = pd.read_csv(path,encoding='utf-8')
    print('===========',reader)
    
    list = []
    for i in range(len(reader)):
        
        list.append(data_save(  d_q = reader.loc[i][0],
                                d_a = reader.loc[i][1]))
        
    data_save.objects.bulk_create(list)
    
    return HttpResponse("csv 데이터 업로드 완료")

def data_csv_view(request):
    articles = data_save.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'data_csv_view.html', context)

def home(request):
    context = {}

    return render(request, "chathome1.html",context)
    

def chatanswer(request):
    context = {}
    ques = request.GET.get('questext')#html에 있는 strurl지정한 이름에 찾은 다음에 안의 data를 가져온다.
    start_time = time.time()
    
    chat_input2 = ques
    print(ques)
    number = random.randrange(1,4)
    # 안녕
    Hi = ['안녕','안늉','안뇽','ㅎㅇ','방가','반가워','하이루']
    if any(format in chat_input2 for format in Hi ): 
        if number == 1:
            context = "ㅎㅇ"
        elif number == 2:
            context = "하이루"
        elif number == 3:
            context = "방가방가"
        elif number == 4:
            context = "안녕"
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    # 잘가
    Bye = ['ㅂㅇ','잘가','빠이','바이','안녕히','ㅃㅇ']
    number = random.randrange(1,4)
    if any(format in chat_input2 for format in Bye ):
        if number == 1:
            context = "ㅂㅇ"
        elif number == 2:
            context = "잘가"
        elif number == 3:
            context = "ㅇㅋㅇㅋ 빠이!"
        elif number == 4:
            context = "빠이"
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

# 고마워
    Thx = ['땡큐','ㄳ','ㄱㅅ','고마','고맙','ㄸㅋ','땡삼']  
    number = random.randrange(1,4)
    if any(format in chat_input2 for format in Thx ) :
        if number == 1:
            context = "ㅎㅎ 아니야"
        elif number == 2:
            context = "ㅇㅋㅇㅋ"
        elif number == 3:
            context = "오케"
        elif number == 4:
            context = "오키"
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #교식
    if ((("메뉴" in chat_input2) or ("식" in chat_input2)) and ("교"in chat_input2)):
        now = str(date.today())
        url = "https://www.ajou.ac.kr/kr/life/food.do?mode=view&articleNo=221&date="+now+"#menu"
        res = requests.get(url)
        res.raise_for_status() 
        soup = BeautifulSoup(res.text,"lxml")
        menu = soup.find_all("div", attrs={"class":"b-menu-box"})
        for k in menu:
            k=k.text
            k=k.replace("등록된 식단이 없습니다.", " ")
            k=k.replace("\n","")
            k=k.replace("\r","<br/>")
            k=k.replace("*식당 출입시 마스크 착용 부탁드립니다*","")
            k=k.replace("(2학기 중 상시운영합니다.)","")
            k=k.replace("※ 운영시간 : 11:00~14:00","※ 중식 : 11:00~14:00")
            k=k.replace("※ 운영시간 : 17:00~18:40","※ 석식 : 17:00~18:40")
            if(len(k)<10):
                k = "오늘은 교직원 식당 운영 안 해!"
            context = k

        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    #코로나 확진자수
    if((("확진자"in chat_input2) or("코로나" in chat_input2)) and (("몇" in chat_input2)or("수" in chat_input2))):
        url="https://search.naver.com/search.naver?sm=tab_hty.top&query=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90&oquery=%EC%BD%94%EB%A1%9C%EB%82%98+%ED%99%95%EC%A7%84%EC%9E%90"
        res = requests.get(url)
        res.raise_for_status() 
        soup = BeautifulSoup(res.text,"lxml")
        corona = soup.find("li", attrs={"class":"info_01"}).text
        context = "{0}명이야!".format(corona)
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

        
    #날씨   
    def is_cold(Temp):
        if(Temp<5):
            comment = "추워! 따뜻하게 입어"
        elif(14<=Temp<20):
            comment = "따뜻해!"
        elif(20<=Temp):
            comment = "더워.."
        else: comment = "적당해!"
        return comment
    #온도    
    weather = ["추워","추우려","더워","더우려","날씨"]
    if any(format in chat_input2 for format in weather ): 
        url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%82%A0%EC%94%A8&oquery=%EB%8B%A4%EC%9D%8C&tqi=hBWHOlp0YidssgeiVVsssssstMN-400420"
        res = requests.get(url)
        res.raise_for_status() 
        soup = BeautifulSoup(res.text,"lxml")
        
        T = soup.find("div",attrs={"class":"temperature_text"}).find("strong").text
        Real_Temp = T.replace("°","")
        Real_Temp = int(Real_Temp.replace("현재 온도",""))
        lowest = soup.find("span",attrs={"class":"lowest"}).text
        highest = soup.find("span",attrs={"class":"highest"}).text
        low = int(lowest[4:-1])
        high = int(highest[4:-1])
        
        #현재온도
        if("지금"in chat_input2):
            context  = "{0}로 {1}".format(T,is_cold(Real_Temp))
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
        #현재X
        else:
            if(high-low>6):
                comment1 = "일교차가 크니 주의하고"
            else:
                if(is_cold(high)=="더워.."):
                    comment1 = "덥고"
                elif(is_cold(low)=="추워! 따뜻하게 입어"):
                    comment1 = "춥고"
                else:
                    comment1 = "적당하고"
            T = T.replace("현재 온도","")    
            context = lowest+highest+"로 "+comment1+" 지금은 {0}로 {1}".format(T,is_cold(Real_Temp))
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    #오늘 최신 공지
    notice = ['오늘 공지','최근 공지사항','최근 공지','최신 공지','오늘 공지']
    if any(format in chat_input2 for format in notice):
        notice_data = notice_latest()
        context = notice_data
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    #이틀전 공지
    notice_2day = ['그저께 공지사항','그저께 공지','이틀 전 공지사항','이틀전 공지','2일전 공지사항']
    if any(format in chat_input2 for format in notice_2day):
        notice2_data = notice_2days()

        if len(notice2_data) ==1:
            context = "그저께 공지사항 없어"
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
        else:
            context = notice_2days()
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #어제_공지
    notice_yester = ['어제 공지','어제 공지사항']
    if any(format in chat_input2 for format in notice_yester):
        notice_yester_data = notice_yesterday()

        if len(notice_yester_data) ==1:
            context = "어제 공지사항 없어"
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
        else:
            context = notice_yesterday()
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #알바
    alba_data = ['최신 알바','아주대 알바','근처 알바']
    if any(format in chat_input2 for format in alba_data):
        albadata = alba()
        context = albadata
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    
    #웹_장학
    scholarship_data = ['장학','장학신청','장학 신청','장학금 신청','장학금']
    if any(format in chat_input2 for format in scholarship_data):
        scholarship_data_fun = scholarship()
        context = scholarship_data_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #웹_공모전
    wevity_web_data = ["웹 공모전","IT 공모전","웹/모바일/IT 공모전","모바일 공모전"]
    if any(format in chat_input2 for format in wevity_web_data):
        wevity_web_data_fun_fun = wevity_web()
        context = wevity_web_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #UCC_공모전
    wevity_UCC_data = ["영상 공모전","UCC 공모전","사진 공모전","영상/UCC/사진 공모전"]
    if any(format in chat_input2 for format in wevity_UCC_data):
        wevity_UCC_data_fun_fun = wevity_UCC()
        context = wevity_UCC_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #과학 공모전
    wevity_Science_data = ["과학 공모전","공학 공모전"]
    if any(format in chat_input2 for format in wevity_Science_data):
        wevity_Science_data_fun_fun = wevity_Science()
        context = wevity_Science_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #공모전_문학
    wevity_literature_data = ["문학 공모전","글 공모전","시나리오 공모전","문학/글/시나리오 공모전"] 
    if any(format in chat_input2 for format in wevity_literature_data):
        wevity_literature_data_fun_fun = wevity_literature()
        context = wevity_literature_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #공모전_대학생
    wevity_university_data =  ["대학생 공모전"]
    if any(format in chat_input2 for format in wevity_university_data):
        wevity_university_data_fun_fun = wevity_university()
        context = wevity_university_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    # 동아리 추천
    if "동아리 추천" in chat_input2:
        group_word = group(chat_input2)
        context = group_word
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    #메뉴 추천
    if "추천" in chat_input2:
        word = chat_input2.replace("추천 ","")
        wevity_university_data_fun_fun = map(word)
        context = wevity_university_data_fun_fun
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

    if("교수님"in chat_input2 and "정보" in chat_input2 and "알려줘" in chat_input2):
        # browser = webdriver.Chrome("C:/Users/Bang/Desktop/chat/chromedriver.exe")
        browser.get("https://mportal.ajou.ac.kr/system/phone/phone.do")
        browser.find_element_by_xpath('//*[@id="nbContext"]/div[2]/div/div[1]/section[1]/div[1]/div/div/input').send_keys(chat_input2[:3])
        browser.find_element_by_xpath('//*[@id="nbContext"]/div[2]/div/div[1]/section[1]/div[2]/div/div/a').click()
        info = browser.find_element_by_xpath('//*[@id="nbContext"]/div[2]/div/div[1]/sp-grid/div/div/div/div[2]/div/div')
        context = (info.text).replace("\n","<br/>")
        middle_time8 = time.time()
        print("최종 시간 : %f"%(middle_time8-start_time))
        return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)
    
    #딥러닝 답변
    else:

        features = data['question'].tolist()
        corpus = [preprocessing.text.text_to_word_sequence(text) for text in features]
        tokenizer = preprocessing.text.Tokenizer()
        tokenizer.fit_on_texts(corpus)

        sent = []
        sent.append(chat_input2)
        chat_input = sent
        sequences2 = tokenizer.texts_to_sequences(chat_input)
        MAX_SEQ_LEN = 15
        padded_seqs = preprocessing.sequence.pad_sequences(sequences2, maxlen=MAX_SEQ_LEN, padding='post')

        predict = model.predict(padded_seqs)
        predict_class = tf.math.argmax(predict, axis=1)

        if predict_class.numpy() != 2:
            number = random.randrange(1,4)
            if number == 1:
                context = '무슨 말인지 모르겠어 ㅠㅠ'
            elif number == 2:
                context = '이해 못하겠어 ㅠㅠ'
            elif number == 3:
                context = '이해 못해서 답을 못해주겠어 ㅠㅠ'
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

        else:

            start = 11455
            end = 12580

            data2 = data.iloc[start:end+1]
            features = data2['question'].tolist()
            corpus = [preprocessing.text.text_to_word_sequence(text) for text in features]
            tokenizer = preprocessing.text.Tokenizer()
            tokenizer.fit_on_texts(corpus)
            sequences2 = tokenizer.texts_to_sequences(chat_input)
            padded_seqs = preprocessing.sequence.pad_sequences(sequences2, maxlen=MAX_SEQ_LEN, padding='post')

            predict2 = model2.predict(padded_seqs)
            predict_class2 = tf.math.argmax(predict2, axis=1)

            pos = p.pos(chat_input2)
            bow1 = []

            for i in range(len(pos)):
                if (m.search(pos[i][1])) is not None: 
                    bow1.append(pos[i][0])
                elif o.search(pos[i][1]) is not None: 
                    bow1.append(pos[i][0])    
                elif n.search(pos[i][1]) is not None:
                    bow1.append(pos[i][0])      

            r1 = 0 
            index=0
            bow2=[]
            bow=[]

            pcm = int(predict_class2.numpy())
            data3 = data2.groupby('label2').get_group(pcm).reset_index(drop=True)
            for i in range(len(data3['question'])):
                bow2 = list(data3['N'][i].split()+data3['V'][i].split())
                bow = bow1 + bow2 
                word_dics = []
                for token in bow:
                        if token not in word_dics:
                            word_dics.append(token)
                freq_list1 = make_term_doc_mat(bow1, word_dics)
                freq_list2 = make_term_doc_mat(bow2, word_dics)
                doc1 = np.array(make_vector(freq_list1))
                doc2 = np.array(make_vector(freq_list2))
                r2 = cos_sim(doc1, doc2)
                
                if r2 > r1 :
                    r1 = r2
                    index = i
                    bow3 = bow2
            if r1 < 0.4 :
                context  = "다르게 말해 줄래? 잘 모르겠어 ㅠ"
                middle_time8 = time.time()
                print("최종 시간 : %f"%(middle_time8-start_time))
                return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)

            context =data3['answer'][index]
            middle_time8 = time.time()
            print("최종 시간 : %f"%(middle_time8-start_time))
            return JsonResponse(json.dumps(context,ensure_ascii=False), content_type = "application/json",safe = False)