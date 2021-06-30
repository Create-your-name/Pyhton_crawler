import requests
from bs4 import BeautifulSoup
import pymysql
import tkinter as t
import tkinter.messagebox as tm

news_title = []
news_link = []


def s():
    url = "http://news.baidu.com/game"

    str1 = requests.get(url).content

    soup = BeautifulSoup(str1, "lxml")
    for x in range(1, 5):
        path = "#col-left > div:nth-child(3) > div.bd > div > div.one-pic-pics > div:nth-child(1) > div > div > ul > " \
               "li:nth-child({}) > a".format(x)
        data = soup.select(path)
        news_title.append(data[0].text)
        news_link.append(data[0].get('href'))


def mysql():
    db = pymysql.connect(host="localhost", port=3306, user="root", password="123456", database="bbs", charset="utf8")
    if db:
        print("连接")
    cursor = db.cursor()
    cursor.execute("drop table if exists kcsj")
    sql = """create table kcsj(
         id int unsigned primary key auto_increment,
         title varchar(5000),
         linkUrl varchar(5000))
     """
    cursor.execute(sql)

    sum = len(news_title)
    for d in range(0, sum):
        sql = "insert into kcsj (title,linkUrl) values('{}','{}')".format(news_title[d], news_link[d])
        cursor.execute(sql)
        db.commit()
        num = cursor.rowcount
    db.close()


def create_windows():
    w = t.Tk()
    w.geometry('1x1')
    ask_1 = tm.askyesno('提醒', '即将进行爬取操作，是否继续？')
    if ask_1:
        s()
        ask_2 = tm.askyesno('提醒', '是否将信息存入数据库')
        if ask_2:
            mysql()
            ask_3 = tm.askyesno('提醒', '信息已爬取进数据库')
    w.mainloop()


def main():
    create_windows()


if __name__ == '__main__':
    main()

