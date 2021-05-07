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
    
    dw(5)
    soup = BS(driver.page_source,lxml)

    soup.find()

    """js = ""\"var xmlhttp=new XMLHttpRequest();
        xmlhttp.open("GET","http://127.0.0.1/get.php",false);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.setRequestHeader("User-Agent","Mozilla/5.0");
        xmlhttp.setRequestHeader("Cookie","");
        xmlhttp.send("test=1");
        return xmlhttp.responseText;
	    ""\" 
    resp = brower.execute_script(js)"""

    input()
    
    driver.close()

    #dat = get_course(cookies)
    #print(dat)

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
