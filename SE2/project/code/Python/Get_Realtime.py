# written by: ZE LIU, Tong Wu
# assisted by: All members
# debugged by: All members


import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
import MySQLdb;

length=1000

def get_html(url):
    try:
        r = requests.get(url,timeout=30)
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
    for i in range(0,4):
        driver.execute_script("arguments[0].scrollIntoView();",target)
        time.sleep(2)

    data = driver.page_source
    return data

def get_content(stockUrl):
    comments = []
    html = get_html(stockUrl)
    soup = BeautifulSoup(html,'lxml')
    div = soup.find('div',attrs={'class': 'My(6px) smartphone_Mt(15px)'})
    tr = soup.find_all('tr',attrs={'class':'Bxz(bb) Bdbw(1px) Bdbs(s) Bdc($c-fuji-grey-c) H(36px) '})[6]
    comment = {}
    try:
        comment['Price'] = div.find('div').find('span').text.strip()
        comment['Time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        comment['Volume'] = tr.find('td',attrs={'class':'Ta(end) Fw(b) Lh(14px)'}).find('span').text.strip()
        comments.append(comment)
    except:
        print('Something Wrong')
    return comments
def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec;

def write_in_file(dict,name):
    with open('Realtime_'+name+'.txt','a+')as f:
        for comment in dict:
            f.write(' Time: {} \t Pirce: {} \t Volume: {} \t'.format(
              comment['Time'], comment['Price'],comment['Volume']))

        print('-----------------------')
        print('TXT Wirte Success!')


def write_in_csvfiletitle(name):
    with open(name+"_Realtime_Price.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        # columns_name
        writer.writerow(["Time", "Price", "Volume"])


def write_in_csvfile(dict,name):
    with open(name+"_Realtime_Price.csv", "a+") as csvfile:
        writer = csv.writer(csvfile)
        for comment in dict:
            everyLine = [comment['Time'], comment['Price'], comment['Volume']]
            writer.writerow(everyLine)
            del everyLine
            
        print('CSV Wirte Success!')


def InitializeDB(TableName):
    db=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306)
    dbcur = db.cursor()
    dbcur.execute("DROP TABLE IF EXISTS "+TableName+";")
    dbcur.close()
    db.close()
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306) 
    cur=conn.cursor()  

    sql = """
               CREATE TABLE """+TableName+"""(
               Time VARCHAR(128) primary key, 
               R_Price VARCHAR(20) NOT NULL,
               R_Volume VARCHAR(20) NOT NULL)"""

    cur.execute(sql)     
    
    conn.commit()  
    cur.close()  
    conn.close()  



def InsertDatabase(TableName,dict):  
   try:  
    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306)  
    cur=conn.cursor()  

    # sql = """CREATE TABLE TESTDB.AMZN_Realtime_Price(
    #           Time VARCHAR(20) NOT NULL,
    #           R_Price VARCHAR(20) NOT NULL,
    #           R_Volume VARCHAR(20) NOT NULL,
    #           PRIMARY KEY (Time))
    #           ENGINE = InnoDB;"""


    sql = "insert into "+TableName+"(Time, R_Price, R_Volume) values (%s, %s, %s)"  
    # param = [("tom", "24", "120"), ("alice", "25","dsa"), ("bob", "26","fda")]
    for eachDic in dict:
        try: 
            line = (eachDic["Time"], eachDic["Price"],eachDic["Volume"]) 
            cur.execute(sql, line) 
            conn.commit()  
            # print "success insert many records!"  
        except Exception as e:  
            conn.rollback()  
            print (e)  
        print('Database Wirte Success!')
        print('-----------------------')

    cur.close()  
    conn.close()  
  
   except MySQLdb.Error as e:  
     print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))




def main(base_url,name):
    second = sleeptime(0,0,10)
    priceName = name+'_Realtime_Price'
    write_in_csvfiletitle(name)
    InitializeDB(priceName)
    while 1==1:
        content = get_content(base_url)
        write_in_file(content,name)
        write_in_csvfile(content,name)
        InsertDatabase(priceName,content)
        time.sleep(second)
    print('Success all')

