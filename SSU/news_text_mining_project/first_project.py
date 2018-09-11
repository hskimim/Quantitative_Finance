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



def tuning_word(word):
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