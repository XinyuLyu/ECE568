# -*- coding: utf-8 -*-
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
import csv;
import MySQLdb;

length = 1000


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Error"


def get_html2(url):
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.maximize_window()
    driver.get(url)
    time.sleep(2)
    target = driver.find_element_by_xpath("//td[@data-reactid = '1553']")
    for i in range(0, 4):
        driver.execute_script("arguments[0].scrollIntoView();", target)
        time.sleep(2)

    data = driver.page_source
    return data


def get_content(stockUrl):
    comments = []
    html = get_html2(stockUrl)
    soup = BeautifulSoup(html, 'lxml')

    trTags = soup.find_all('tr', attrs={'class': 'BdT Bdc($c-fuji-grey-c) Ta(end) Fz(s) Whs(nw)'})

    for tr in trTags:

        comment = {}

        try:

            td1 = tr.find('td', attrs={'class': 'Py(10px) Ta(start) Pend(10px)'})
            comment['Time'] = td1.find('span').text.strip()
            comment['Open'] = tr.find_all('td', attrs={'class': 'Py(10px) Pstart(10px)'})[0].find('span').text.strip()
            comment['High'] = tr.find_all('td', attrs={'class': 'Py(10px) Pstart(10px)'})[1].find('span').text.strip()
            comment['Low'] = tr.find_all('td', attrs={'class': 'Py(10px) Pstart(10px)'})[2].find('span').text.strip()

            comment['Close'] = tr.find_all('td', attrs={'class': 'Py(10px) Pstart(10px)'})[3].find('span').text.strip()

            comment['Volume'] = tr.find_all('td', attrs={'class': 'Py(10px) Pstart(10px)'})[5].find('span').text.strip()

            comments.append(comment)

        except:
            print('Something Wrong')
    return comments


def write_in_csvfile(dict,name):
    with open(name+"_History_Price.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        # columns_name
        writer.writerow(["Time", "Open", "High", "Low", "Close", "Volume"])
        for comment in dict:
            everyLine = [comment['Time'], comment['Open'], comment['High'],
                         comment['Low'], comment['Close'], comment['Volume']]
            writer.writerow(everyLine)
            del everyLine
            
        print('Wirte Success!')


def write_in_file(dict,name):
    with open(name+'_History_Price.txt', 'a+')as f:
        for comment in dict:
            f.write('Time: {} \t Open: {} \t High: {} \t Low: {} \t Close: {} \t Volume: {} \n'.format(
                comment['Time'], comment['Open'], comment['High'], comment['Low'], comment['Close'], comment['Volume']))

        print('Wirte Success!')



def InsertDatabase(TableName,array):  
     
   try:
    db=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306)
    dbcur = db.cursor()
    dbcur.execute("DROP TABLE IF EXISTS "+TableName+";")
    dbcur.close()
    db.close()
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306)  
    cur=conn.cursor()  

    sql = """
              CREATE TABLE """+TableName+"""(
              Date VARCHAR(20) NOT NULL,
              Open_Price VARCHAR(15) NOT NULL,
              High_Price VARCHAR(15) NOT NULL,
              Low_Price VARCHAR(15) NOT NULL,
              Close_Price VARCHAR(15) NOT NULL,
              H_Volume VARCHAR(20) NOT NULL,
              PRIMARY KEY (Date))
              ENGINE = InnoDB;"""


  
    try:  
      cur.execute("SELECT * FROM  %s"%(TableName))  
      for eachdic in array:
        ROWstr=''  
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Time"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Open"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["High"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Low"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Close"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Volume"])
        cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))  
    
    except MySQLdb.Error as e:   
      cur.execute(sql)   
      for eachdic in array:
        ROWstr='' 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Time"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Open"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["High"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Low"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Close"]) 
        ROWstr=(ROWstr+'"%s"'+',')%(eachdic["Volume"])
        cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))  
    
    conn.commit()  
    cur.close()  
    conn.close()  
  
   except MySQLdb.Error as e:  
      print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))



def main(base_url,name):
    content = get_content(base_url)
    write_in_csvfile(content,name)
    InsertDatabase(name+'_History_Price',content) 
    # write_in_file(content)
    print('Success all')

