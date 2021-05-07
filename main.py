import json
import lxml
import time
import configparser
import requests as rq
from downcount import dw
from bs4 import BeautifulSoup as BS
from selenium import webdriver


def main():
    config = configparser.ConfigParser()
    config.read("config.ini")

    driver = webdriver.Chrome() #Firefox()

    driver.get("https://myfcu.fcu.edu.tw/main/infomyfculogin.aspx")

    driver.find_element_by_name("txtUserName").send_keys(config["user"]["username"])
    driver.find_element_by_name("txtPassword").send_keys(config["user"]["password"])
    driver.find_element_by_name("OKButton").click()
    
    """cookies = ""

    for coo in driver.get_cookies():
        cookies += "{name}={value};".format(**coo)
    """

    dw(1)
    driver.get("https://myfcu.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx")
    #time.sleep(5)
    #driver.find_element_by_xpath('//input[@type="checkbox"]').click()
    
    dw(3)
    lessons = BS(driver.page_source,"lxml").find_all("tr",{"class":"ng-scope","ng-repeat":"cur in linecourselists"})

    
    print(make_course(lessons))
    

    """js = ""\"var xmlhttp=new XMLHttpRequest();
        xmlhttp.open("GET","http://127.0.0.1/get.php",false);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.setRequestHeader("User-Agent","Mozilla/5.0");
        xmlhttp.setRequestHeader("Cookie","");
        xmlhttp.send("test=1");
        return xmlhttp.responseText;
	    ""\" 
    resp = brower.execute_script(js)"""

    input("click to close:")
    
    driver.close()

    #dat = get_course(cookies)
    #print(dat)

def make_course(lessons):
    print(lessons)
    res = [[None for i in range(5)] for j in range(14)]
    week_ch = "一二三四五"
    for l in lessons:
        l_data = l.find_all("td")
        week = week_ch.find(clean(l_data[0].text)[1])
        if week == -1:
            continue
        session = int(clean(l_data[0].text)[3:5])-1
        res[session][week] =[clean(l_data[1].text),clean(l_data[3].text).split('(')[0]]
        print(session,week)
    
    return res

def clean(s):
    return s.replace("\n","").replace(" ","")

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
