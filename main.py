import os
import json
import lxml
import time
import getpass
import unicodedata
import configparser
import requests as rq
from downcount import dw
from bs4 import BeautifulSoup as BS
from selenium import webdriver


def main():
    os.system("")
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        urn = config["user"]["username"]
        pwd = config["user"]["password"]
    except:
        print("Failed to load config.ini,please input data.")
        urn = input("Username:")
        pwd = input("Password:\033[47m")
        print("\033[0m", end="")

    driver = webdriver.Chrome()  # Firefox()

    driver.get("https://myfcu.fcu.edu.tw/main/infomyfculogin.aspx")

    driver.find_element_by_name("txtUserName").send_keys(urn)
    driver.find_element_by_name("txtPassword").send_keys(pwd)
    driver.find_element_by_name("OKButton").click()

    dw(1)
    driver.get("https://myfcu.fcu.edu.tw/main/S3202/S3202_timetable_new.aspx")

    dw(3)
    lessons = BS(driver.page_source, "lxml").find_all(
        "tr", {"class": "ng-scope", "ng-repeat": "cur in linecourselists"})

    driver.close()

    res = make_course(lessons)
    print_course(res)
    save_course(res)

    input("press enter to close:")


def make_course(lessons):
    def clean(s): return s.replace("\n", "").replace(" ", "")
    # print(lessons)
    fl = format_lesson("", "")
    res = [[fl for i in range(5)] for j in range(14)]

    week_ch = "一二三四五"
    for l in lessons:
        l_data = l.find_all("td")
        week = week_ch.find(clean(l_data[0].text)[1])
        if week == -1:
            continue
        session = int(clean(l_data[0].text)[3:5])-1
        res[session][week] = format_lesson(
            clean(l_data[1].text), clean(l_data[3].text).split('(')[0])

    for i in range(14):
        res[i].insert(0, ["|  ", "|  ", f"|{i+1:02d}", "|  ", "|  "])
    return res


def print_course(lessons):
    def create_line(l): return f"|--|"+("-"*12+"|")*l

    os.system("cls")
    print(create_line(5))
    print("|  ", end="|")
    for c in "一二三四五":
        print(f"{c: ^11}", end="|")
    print()
    print(create_line(5,))
    for session in lessons:
        for i in range(5):
            for s in session:
                print(s[i], end="|")
            print()
        print(create_line(5))
    print("\033[1A", end="")
    print(create_line(5))


def save_course(lessons):
    def create_line(l): return f"|--|"+("-"*12+"|")*l

    with open("course.txt", "w") as f:
        f.write(create_line(5)+"\n")
        f.write("|  |")
        for c in "一二三四五":
            f.write(f"{c: ^11}|")
        f.write("\n")
        f.write(create_line(5)+"\n")
        for session in lessons:
            for i in range(5):
                for s in session:
                    f.write(s[i]+"|")
                f.write("\n")
            f.write(create_line(5)+"\n")


def format_lesson(name, room):
    res = ["", "", "", "", room]
    index_ = 0
    len_ = 0
    for c in name:
        size_ = 1
        if unicodedata.east_asian_width(c) == 'W':
            size_ += 1
        print(c, size_)
        if len_ + size_ > 12:
            len_ = 0
            index_ += 1

        res[index_] += c
        len_ += size_

    if len(res[2]) == 0:
        res.pop(2)
        res.insert(0, "")

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


if __name__ == "__main__":
    main()
