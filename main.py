import os
import json
import lxml
import time
import unicodedata
import configparser
import requests as rq
from downcount import dw
from bs4 import BeautifulSoup as BS
from selenium import webdriver


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    driver = webdriver.Chrome()  # Firefox()

    driver.get("https://myfcu.fcu.edu.tw/main/infomyfculogin.aspx")

    driver.find_element_by_name("txtUserName").send_keys(
        config["user"]["username"])
    driver.find_element_by_name("txtPassword").send_keys(
        config["user"]["password"])
    driver.find_element_by_name("OKButton").click()

    """cookies = ""

    for coo in driver.get_cookies():
        cookies += "{name}={value};".format(**coo)
    """

    dw(1)
    driver.get("https://myfcu.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx")
    # time.sleep(5)
    # driver.find_element_by_xpath('//input[@type="checkbox"]').click()

    dw(3)
    lessons = BS(driver.page_source, "lxml").find_all(
        "tr", {"class": "ng-scope", "ng-repeat": "cur in linecourselists"})

    driver.close()
    print_course(make_course(lessons))

    """js = ""\"var xmlhttp=new XMLHttpRequest();
        xmlhttp.open("GET","http://127.0.0.1/get.php",false);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.setRequestHeader("User-Agent","Mozilla/5.0");
        xmlhttp.setRequestHeader("Cookie","");
        xmlhttp.send("test=1");
        return xmlhttp.responseText;
	    ""\" 
    resp = brower.execute_script(js)"""

    input("press enter to close:")


    #dat = get_course(cookies)
    # print(dat)


def make_course(lessons):
    print(lessons)
    fl = format_lesson("","")
    res = [[fl for i in range(5)] for j in range(14)]
    
    week_ch = "一二三四五"
    for l in lessons:
        l_data = l.find_all("td")
        week = week_ch.find(clean(l_data[0].text)[1])
        if week == -1:
            continue
        session = int(clean(l_data[0].text)[3:5])-1
        res[session][week] = format_lesson(clean(l_data[1].text),clean(l_data[3].text).split('(')[0])

    for i in range(14):
        res[i].insert(0,["  ","  ",f"{i+1:02d}","  ","  "])
    return res

def print_course(lessons):
    os.system("cls")
    print("  ",end="|")
    for c in "一二三四五":
        print(f"{c: ^11}",end="|")
    print()
    print_line()
    for session in lessons:
        for i in range(5):
            for s in session:
                print(s[i],end="|")
            print()
        print_line()


def format_lesson(name,room):
    res = ["","","","",room]
    index_ = 0
    len_ = 0
    for c in name:
        size_ = 1
        if unicodedata.east_asian_width(c) == 'W':
            size_ += 1
        print(c,size_)
        if len_ + size_ > 12:
            len_ = 0
            index_ += 1

        res[index_] += c
        len_ += size_
    
    if len(res[2]) == 0:
        res.pop(2)
        res.insert(0,"")

    for i in range(5):

        for j in range(12-width(res[i])):
            if j % 2 == 0:
                res[i] = res[i] + ' '
            else:
                res[i] = ' ' + res[i]


    return res

def width(s):
    size_ = 0
    for c in s:
        size_ += 1
        if unicodedata.east_asian_width(c) == 'W':
            size_ += 1
    return size_

def clean(s):
    return s.replace("\n", "").replace(" ", "")

def print_line(l=5):
    print("--",end="|")
    for i in range(l):
        i = i + 0
        print("-"*12,end="|")
    print()
"""
def get_course(cookies="",year=109,smester=2):
    data = {
        "year":year,
        "smester":smester
    }
    headers = {
        "Cookie":cookies
    }
    r = rq.post("https://myfcu.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx/GetCurriculum",data=data,headers=headers)
    print(r)
    print(r.text)
    return json.loads(r.text)

#driver.close()"""

if __name__ == "__main__":
    main()
