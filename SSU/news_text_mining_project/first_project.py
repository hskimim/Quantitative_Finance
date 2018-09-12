from selenium import webdriver
import time
import re
from sklearn.feature_extraction.text import CountVectorizer , TfidfVectorizer
import pandas as pd
from bs4 import BeautifulSoup
import string
import requests
import numpy as np
from IPython.display import display , Markdown 
from konlpy.tag import *

def light_crawling2(PageNum,day_ago=False):
    '''
    PageNum : 1 or 2
    day_ago : Among 1,2,3,4
    '''
    ls = []
    driver = webdriver.Chrome()
    url = 'https://finance.naver.com/news/mainnews.nhn?&page={}'.format(PageNum)
    response = requests.get(url)
    dom = BeautifulSoup(response.content , 'html.parser')
    length = len(dom.select('#contentarea_left > div.mainNewsList > ul > li'))
    driver.get(url)
    for i in range(1,length+1,1):
        try:
            driver.execute_script('window.scrollTo(100,{});'.format(i*100))
            driver.find_element_by_css_selector("#contentarea_left > div.mainNewsList > ul > li:nth-child({}) > dl > dt > a".format(i)).click()
            ls.append(driver.find_element_by_css_selector('#content').text)
            time.sleep(1)
            driver.get(url)
        except : 
            driver.execute_script('window.scrollTo(100,{});'.format(i*100))
            driver.find_element_by_css_selector("#contentarea_left > div.mainNewsList > ul > li:nth-child({}) > dl > dd > a".format(i)).click()
            ls.append(driver.find_element_by_css_selector('#content').text)
            time.sleep(1)
            driver.get(url)
    if day_ago : 
        for day in range(1,day_ago+1):
            driver.execute_script('window.scrollTo(100,{});'.format(10000))
            driver.find_element_by_css_selector("#contentarea_left > div.pagenavi_day > a:nth-child(3)".format(day_ago*2 + 1)).click()    
            for i in range(1,length+1,1):
                try:
                    driver.execute_script('window.scrollTo(100,{});'.format(i*100))
                    driver.find_element_by_css_selector("#contentarea_left > div.mainNewsList > ul > li:nth-child({}) > dl > dt > a".format(i)).click()
                    ls.append(driver.find_element_by_css_selector('#content').text)
                    time.sleep(1)
                    driver.get(url)
                except : 
                    driver.execute_script('window.scrollTo(100,{});'.format(i*100))
                    driver.find_element_by_css_selector("#contentarea_left > div.mainNewsList > ul > li:nth-child({}) > dl > dd > a".format(i)).click()
                    ls.append(driver.find_element_by_css_selector('#content').text)
                    time.sleep(1)
                    driver.get(url)
    driver.close()
    return ls


def light_crawling3(PageNum=1):
    '''
    PageNum : how many pages do you want to scrapy
    one page has 20 reports
    Roughly, It is used to take 40 secs for 1 page
    '''
    ls = []
    driver = webdriver.Chrome()
    url = 'https://news.naver.com/main/hotissue/sectionList.nhn?mid=hot&sid1=101&cid=996387&page={}'.format(PageNum)
    response = requests.get(url)
    dom = BeautifulSoup(response.content , 'html.parser')
    length = len(dom.select('div.hissue_cnt > ul > li'))
    driver.get(url)
    
    for i in range(1,length+1,1):
        try:
            driver.execute_script('window.scrollTo(100,{});'.format(i*100))
            driver.find_element_by_css_selector("div.hissue_cnt > ul > li:nth-child({}) > dl > dt > a".format(i)).click()
            ls.append(driver.find_element_by_css_selector('#articleBodyContents').text)
            time.sleep(1)
            driver.get(url)
            
        except : 
            driver.execute_script('window.scrollTo(100,{});'.format(i*100))
            driver.find_element_by_css_selector("div.hissue_cnt > ul > li:nth-child({}) > dl > dd > a".format(i)).click()
            ls.append(driver.find_element_by_css_selector('#articleBodyContents').text)
            time.sleep(1)
            driver.get(url)
            
        try : ls[i-1] = ls[i-1][:np.min([idx for idx,j in enumerate(ls[i-1]) if j == '▶'])]
        except : pass
        
        if i == (length) :
            driver.find_element_by_css_selector("div.hissue_cnt > ul > li:nth-child({}) > dl > dd > a".format(i)).click()
            try : 
                day = driver.find_element_by_css_selector('#main_content > div.article_header > div.article_info > div > span').text
                display(Markdown('### This report is from year : {}' .format(str(day))))            
            except : 
                display(Markdown("### Sorry, This report don't have data when it had been updated")) 
            
    driver.close()
    return ls


def operate_light_crawling(vers,day_ago=1,PageNum=1,make_df=True):
    '''
    vers : there are only two vers : 2 or 3
    if verse1 then parameter will be fixed, but verse2's parameter can be changed by params named "PageNum"
    make_df : if true, we return the dataframe or, return crawled list
    '''
    display(Markdown('#### vers :{} , make_df : {}'.format(vers,make_df)))
    t = time.localtime()
    if vers == 2 : 
        ls1 = light_crawling2(PageNum=1,day_ago=day_ago)
        ls2 = light_crawling2(PageNum=2,day_ago=day_ago)
        ls = ls1 + ls2
        if make_df : 
            df = pd.DataFrame(data=ls,columns=['report_bundles'])
            df.to_csv('light_crawling2_{}.csv'.format(str(t.tm_hour) + str(t.tm_min),header=False)
            return df
        else : return ls
    else : 
        ls = []
        for i in range(1,PageNum+1,1):
            try:
                ls.append(light_crawling3(PageNum=i))
            except : 
                print("{}th page data is not crawled. but we're gonna ignore it.".format(i))
            
        if make_df : 
            df = pd.DataFrame(data=ls,columns=np.arange(20))   
            df.to_csv('light_crawling3_{}.csv'.format(str(t.tm_hour) + str(t.tm_min)),header=False)
            return df
        else : return ls

def konlpy_tuning(csv_name):
    '''
    csv_name : data format from method operation named "operate_light_crawaling
    '''
    kkma = Kkma()
    train_df = pd.read_csv(str(csv_name))
    train = (train_df.values)
    train_report = [train[i][1] for i in range(len(train))]

    try:
        training_ls = [str(kkma.nouns(train_report[i])) for i in range(len(train_report))]
    except : 
        excepted_ls.append(i)
        print('{}th data is excepted, maybe it has NaN value'.format(i))

    display(Markdown('#### length of data : {}'.format(len(training_ls))))
    df = pd.DataFrame(data = training_ls,columns=np.arange(1))
    df.to_csv('first_konlpy_tuning.csv')
    return df

def tuning_word(word):
    '''
    this function only fit with method named light_crawling2
    '''
    new_word = str(word)
    new_word = new_word[1:-2]
    new_word = new_word.replace("'","")
    new_word = new_word.replace(',','')
    new_word = new_word.replace('  ','')
    new_word = new_word.replace('|-- ::','')
    new_word = new_word.replace('\\','')
    new_word = new_word.replace('\\t','')
    new_word = new_word.replace('\\n','')
    new_word = new_word.replace('\\xa','')
    new_word = re.sub('[0-9a-zA-Z]','',new_word)
    return new_word

def fine_tuning(word_list):
    '''
    this function only fit with method named light_crawling2
    '''
    word_list = word_list.split(' ')
    word_list = [re.sub('\W','',word) for word in word_list ]
    word_list = [word for word in word_list if word !='']

    pt = string.printable
    pt[62:]

    for word in word_list : 
        for i in word:
            if i in pt[62:]:
                word.pop(i)
    return word_list            