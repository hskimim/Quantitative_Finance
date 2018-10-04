from selenium import webdriver
import time


def show_me_the_corp_code(days = 5):
    driver = webdriver.Chrome()
    url = 'https://dart.fss.or.kr/dsac001/mainY.do#'
    driver.get(url)
    ls = []
    
    for j in range(2,days+1): 
        driver.find_element_by_css_selector('#date > p > a:nth-child({})'.format(j)).click()            
        time.sleep(1)
        for _ in range(2):
            for i in range(1,101):
                try : 
                    driver.execute_script('window.scrollTo(10,{});'.format(i*100))
                    driver.find_element_by_css_selector('#listContents > div.table_list > table > tbody > tr:nth-child({}) > td:nth-child(2) > span > a'.format(i)).click()
                    time.sleep(1)
                    ls.append(driver.find_element_by_css_selector('#pop_body > div > table > tbody > tr:nth-child(4) > td').text)
                    time.sleep(1)
                    driver.find_element_by_css_selector('#ext-gen48').click()
                except : pass
            try :
                driver.find_element_by_css_selector('#listContents > div.page_list > input[type="button"]:nth-child(4)').click()
            except : pass

    driver.find_element_by_css_selector('#date > p > a:nth-child(1)').click()
    for i in range(101):
        try : 
            driver.execute_script('window.scrollTo(10,{});'.format(i*100))
            driver.find_element_by_css_selector('#listContents > div.table_list > table > tbody > tr:nth-child({}) > td:nth-child(2) > span > a'.format(i)).click()
            time.sleep(1)
            ls.append(driver.find_element_by_css_selector('#pop_body > div > table > tbody > tr:nth-child(4) > td').text)
            time.sleep(1)
            driver.find_element_by_css_selector('#ext-gen48').click()
        except : pass

    driver.close()
    return ls


def download_xls_file():
    driver = webdriver.Chrome()
    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=loadInitPage'
    driver.get(url)

    driver.find_element_by_css_selector('#rWertpapier').click()
    driver.find_element_by_xpath('//*[@id="searchForm"]/section/div/div[3]/a[1]').click()
    driver.find_element_by_xpath('//*[@id="searchForm"]/section/div/div[3]/a[2]').click()
    driver.close()
    print('excel file is downloaded in home/hskimim/Downloads :PATH')