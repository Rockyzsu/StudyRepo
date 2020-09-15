#!urs/bin/env python
#coding:utf-8

from selenium import webdriver

def bar():
    driver = webdriver.PhantomJS()
    driver.get("http://hotel.qunar.com/")
    data = driver.title
    print(data)
    
    driver.quit()


def foo():
    driver = webdriver.PhantomJS()
    driver.get('http://hotel.qunar.com/city/beijing_city/dt-20438/?in_track=hotel_recom_beijing_city02')
    data = driver.find_element_by_id("jd_comments").text
    print(data)
    driver.quit()
    
    
def my_post():
    import sys  
    import time  
    from selenium import webdriver  
      
    driver =webdriver.PhantomJS(executable_path="phantomjs.exe")  
    driver.get("https://www.shanbay.com/accounts/login/")  
    elem_user = driver.find_element_by_xpath('//*[@id="id_username"]')   
    elem_user.send_keys('用户名')  
    elem_pwd = driver.find_element_by_xpath('//*[@id="id_password"]')  
    elem_pwd.send_keys('密码')  
    elem_sub = driver.find_element_by_xpath('//*[@id="loginform"]/div[3]/button')  
    elem_sub.click()  
      
    time.sleep(1)  
    driver.get("https://www.shanbay.com/team/team/")  
    elem_keyword = driver.find_element_by_xpath('//*[@id="group-form"]/div/input')  
    elem_keyword.send_keys(u'雅思')  
    elem_button = driver.find_element_by_xpath('//*[@id="group-form"]/div/button')  
    elem_button.click() 
    time.sleep(1)  
    teams=[]  
    for team in driver.find_elements_by_class_name('title'):  
        if team.get_attribute("href")!=None:  
            teams.append(team.get_attribute("href"))  
    members=[]  
    for team in teams[:5]:  
        driver.get(team)  
        for i in range(10):  
            member=driver.find_element_by_xpath('//*[@id="team_rank_table"]/tbody/tr['+str(i+1)+']/td[2]/a')  
            members.append(member.get_attribute('href'))  
    bookdic={}  
    for member in members:  
        driver.get(member)  
        bookurl=driver.find_element_by_xpath('//*[@id="my-wordbooks-heading"]/h3/small/a')  
        bookurl.click()  
        time.sleep(1)  
        books=driver.find_elements_by_class_name('wordbook-title')  
        for book in books:  
            title=book.get_attribute('title')  
            if title in bookdic:  
                bookdic[title]=bookdic[title]+1  
            else:  
                bookdic[title]=1  
    retbook=sorted(bookdic.iteritems(), key=lambda d:d[1], reverse = True )   
    for i in range(5):  
        print(retbook[i][0])  
    driver.close()  
    
def baidu_get():
    url = 'http://www.baidu.com/link?url=UPQnZtuEZ_LaiK7XArXlbyiveWOAGzgJdkRNVR1rxiTV12QN4PE93HcMbbFOy3A_dCS6WOqlB3SMwpa-AMesPPRZIKCUcHYR-cV91DnGd-7b3HHfbzjbEWAurBJQM3LyYqQflR-YJqX8-_pzDMLIYYWt8vev669Pt-OgwJUdLsNK9qyEHqFPeQKwOhe-2qyT7IfLOE6b3yI7QtQv9mktjKt_HfG4LfI77CB0jYpHCb_'
    driver = webdriver.PhantomJS()
    driver.get(url)
    print(driver.page_source)
    driver.close()
    
def baidu_get_normal():
    import requests
    s = requests.Session()
#     url = 'http://www.baidu.com/link?url=dN1r1Yhegnsql5Z1RZabW_0davm2zbkQyZdIZ5BlSoZlvsAJEuBpuUcBsMSMAjh282jcRFJ_8PHblhsAXO5G0uec_wsQJX3Xo7zLanGU5al3f0GHtajUoNkV_J0VH7zLq_JgYQdAMRLRkC3HX5fAT34M2sie8egLAIboMpY9XDWSp9Lzz8WRhJYi5dZj2Dag'
    url = 'http://www.baidu.com/link?url=kcpNxtBi-jyqRuTgPhhRnXD9zYEH6NbdlzbLYMVZ7olHV7831RIDGZHDtqBuflcR&wd=&eqid=b8e4202100000c7c00000005586cc466'
#     url = 'http://www.baidu.com/link?url=Jq030Gz4FmyTXD_0UbdpkEDyARGpE0xIWrezPcHk8WNQ2tuVfTHie2k_e_y90wnFYZTyNENNCzPdrktrxOpIa_'
#     url = 'http://www.baidu.com/link?url=tNznB3XGCEMl_C3HD3uXrGAp2Zx3a5NMSSpSXXG2tHy'
#     url = 'http://www.baidu.com/link?url=iTdrDdImEQTEpaVddyH5pqfDQo5X6iFrL4-Doq-d6su'
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
    "Connection": "keep-alive",
    "Cookie":    
    "BAIDUID=6C7E491097282445965D7BC0DE9E3331:FG=1; BIDUPSID=6C7E491097282445965D7BC0DE9E3331; PSTM=1480902480"\
    "; HMACCOUNT=3096B32A33665EB3; BDUSS=AwakluMEt5aUhZcGlOSkMtdWdrbzlpfmF0MTlqSUJ5YlVQS0Zza3VRVXkzV3hZSV"\
    "FBQUFBJCQAAAAAAAAAAAEAAAAPNXAdNzIzOTgzMDI0AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADJQRVgyUEVYcX"\
    "; MCITY=-%3A; H_PS_PSSID=; HMVT=9c7f4d9b7c00cb5aba2c637c64a41567|1483516655|; PSINO=3; BDRCVFR[57XbQL1Xi00"\
    "]=mk3SLVN4HKm; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm",
    "Host": "hm.baidu.com",
    "If-None-Match": "ebc5eb38ea960a84892a9de428f17df2",
    "Referer": "http://tu.duowan.com/m/meinv",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"          
    }
#     s.headers = headers
    import re
    response = requests.get(url, allow_redirects=False)  
    if response.status_code == 200:  
        urlMatch = re.search(r'URL=\'(.*?)\'', response.text, re.S)  
        print(urlMatch.group(1))
    elif response.status_code == 302:  
        result = response.headers.get('location')
        print(result)
        
def duowan():
    driver = webdriver.PhantomJS()
    driver.get("http://lol.duowan.com/camille/")
    tag = driver.find_element_by_xpath(".//*[@id='hero-guide']/div[2]/div/div[2]/div[1]/div[2]/div/div/img[1]")
    print(tag)

    
if __name__ == '__main__':
#     foo()
#     my_post()
#     baidu_get()
#     baidu_get_normal()
    duowan()