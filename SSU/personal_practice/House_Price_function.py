from selenium import webdriver
import requests
from bs4 import BeautifulSoup
from scrapy.http import TextResponse
import time
import matplotlib.pylab as plt
from IPython.display import display,Markdown

def search_real_estate(loc='Seoul'):
    '''
    return option : location_name , house_name , house_price , location_div
    loc_option : Seoul , GyeongGi , Incheon , ChungcheongNam , ChungcheongBuk 
    , JeollaNam , JeollaBuk , KyungsangNam , KyungsangBuk , Jeju , GangWon , DaeGu , Ulsan , Busan  , SeJong , Daejeon , GwangJu
    '''
    if loc == 'Seoul': url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=1100000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'GyeongGi':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4100000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'Incheon':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=2800000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'ChungcheongNam':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4400000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'ChungcheongBuk':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4300000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'JeollaNam':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4600000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'JeollaBuk':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4500000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'KyungsangNam':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4800000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'KyungsangBuk':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4700000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'Jeju':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=5000000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'GangWon':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=4200000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'DaeGu':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=2700000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'Ulsan':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=3100000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'Busan':url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=2600000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='
    elif loc == 'SeJong':url = 'https://land.naver.com/article/divisionArticleList.nhn?rletTypeCd=A01&tradeTypeCd=&cortarNo=3611000000'
    elif loc == 'Daejeon':url = 'https://land.naver.com/article/cityInfo.nhn?rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&cortarNo=3000000000'
    else : url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=2900000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=&cpId=&location=&siteOrderCode='        
        
    location_name = []
    house_name = []
    house_price = []
    location_div = []
    
    
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(2)

    for i in range(1,51):
        try : 
            if len(location_name) > 1 : location_name.pop()
            location_name.append(driver.find_element_by_css_selector('#regionListArea > div.area.scroll > ul > li:nth-child({}) > a'.format(i)).text)
            driver.find_element_by_css_selector('#regionListArea > div.area.scroll > ul > li:nth-child({}) > a'.format(i)).click()
        except : break

        for k in range(50):
            for j in range(1,50+1):
                driver.execute_script('window.scrollTo(100,{});'.format((j+4)*100))
                try : 
                    if k == 25 : 
                        time.sleep(1)
                    house_name.append(driver.find_element_by_css_selector('#depth4Tab0Content > div > table > tbody > tr:nth-child({}) > td.align_l.name > div > a'.format(2*j-1)).text)
                    location_div.append(driver.find_element_by_css_selector('#depth4Tab0Content > div > table > tbody > tr:nth-child({}) > td:nth-child(6) > div'.format(2*j-1)).text)
                    house_price.append(driver.find_element_by_css_selector('#depth4Tab0Content > div > table > tbody > tr:nth-child({}) > td.num.align_r > div > strong'.format(2*j-1)).text)
                    location_name.append(location_name[-1])
                except : pass

            try : 
                time.sleep(1)
                driver.find_element_by_css_selector("#depth4Tab0Content > div > div > div > a:last-child").click()
                driver.execute_script('window.scrollTo(100,{});'.format(0))
            except : 
                break

        driver.get(url)
    driver.close()
    
    return location_name , house_name , house_price , location_div


def tuning_df(df):
    new_house_price = []
    for i in (df['house_price']):
        if '/' in i : 
            new_house_price.append(i[:i.find('/')])
        else : 
            new_house_price.append(i)
    display(len(new_house_price))
    
    df['house_price'] = new_house_price
    df['house_price'] = df['house_price'].apply(lambda x : x.replace(',',''))
    df['house_price'] = [int(i) for i in df['house_price']]
    
    return df


###################################################################################

def appending_url():
    url = 'https://land.naver.com/article/cityInfo.nhn?cortarNo=1100000000&rletNo=&rletTypeCd=A01&tradeTypeCd=&hscpTypeCd=A01%3AA03%3AA04&cpId=&location=&siteOrderCode='        
    location_name = []
    url_ls = []
    driver = webdriver.Chrome()
    driver.get(url)

    for i in range(1,51):
        try : 
            if len(location_name) > 1 : location_name.pop()
            location_name.append(driver.find_element_by_css_selector('#regionListArea > div.area.scroll > ul > li:nth-child({}) > a'.format(i)).text)
            driver.find_element_by_css_selector('#regionListArea > div.area.scroll > ul > li:nth-child({}) > a'.format(i)).click()
        except : break

        for _ in range(50):
            url_ls.append(driver.current_url)
            driver.execute_script('window.scrollTo(100,{});'.format((10)*100))
            time.sleep(1)
            driver.execute_script('window.scrollTo(100,{});'.format((55)*100))
            try : 
                time.sleep(1)
                driver.find_element_by_xpath('//*[@id="depth4Tab0Content"]/div/div/div/a[{}]'.format(11)).click()
                driver.execute_script('window.scrollTo(100,{});'.format(0))
            except : 
                driver.find_element_by_xpath('//*[@id="depth4Tab0Content"]/div/div/div/a[{}]'.format(10)).click()
                time.sleep(1)
                driver.execute_script('window.scrollTo(100,{});'.format(0))
        display(Markdown('### {} is over'.format(location_name[-1])))

        driver.get(url)
    driver.close()
    
    return location_name , url_ls
