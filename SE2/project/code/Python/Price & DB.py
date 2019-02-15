#python3
# -*- coding: utf-8 -*-
"""
Use API to get the history prices and realtime prices from Yahoo Finance 
and save them into local csv file and database.
The date is on standard format (can be sorted) and price doesn't have comma

# written by: ZE LIU
# assisted by: All members
# debugged by: All members

"""

from alpha_vantage.timeseries import TimeSeries
import MySQLdb
import csv
import json

def GetHistory(StockName):
	ts = TimeSeries(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data= ts.get_daily(symbol=StockName,outputsize='full')
	# data= ts.get_daily(symbol=StockName,outputsize='full')
	realdata=data[0]
	print(type(realdata))
	json_path = './prediction.json'
	with open(json_path, "w") as f:
		json.dump(realdata, f)
		print("Complete...")

	realdata.to_csv(StockName+'_History_Price.csv',index=True,sep=',')  
	InsertDatabase(StockName+'_History_Price')
	print('Success')
	


def GetRealtime(StockName):
	ts = TimeSeries(key='QBGRPFYFV5WBTTCO', output_format='pandas')
	data= ts.get_intraday(symbol=StockName,interval='1min',outputsize='compact')
	realdata=data[0]
	realdata.to_csv(StockName+'_Realtime_Price.csv',index=True,sep=',') 
	InsertDatabase(StockName+'_Realtime_Price')
	print('Success')


def InsertDatabase(TableName):  
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='TESTDB',port=3306)  
		cur=conn.cursor()  
		cur.execute("DROP TABLE IF EXISTS "+TableName+";")
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
		csv_reader = csv.reader(open(TableName+'.csv', encoding='utf-8'))
		cur.execute(sql)
		flag = 0
		# for row in range(0, 365):
		# i = 1
		for row in csv_reader:
			if flag != 0:
				ROWstr=''
				ROWstr=(ROWstr+'"%s"'+',')%(row[0]) 
				ROWstr=(ROWstr+'"%s"'+',')%(row[1]) 
				ROWstr=(ROWstr+'"%s"'+',')%(row[2]) 
				ROWstr=(ROWstr+'"%s"'+',')%(row[3]) 
				ROWstr=(ROWstr+'"%s"'+',')%(row[4]) 
				ROWstr=(ROWstr+'"%s"'+',')%(row[5])
				cur.execute("INSERT INTO %s VALUES (%s)"%(TableName,ROWstr[:-1]))  
				# i = i + 1
			flag = flag + 1 
	
		conn.commit()
		cur.close()
		conn.close()  
	
	except MySQLdb.Error as e:  
		print ("Mysql Error %d: %s" % (e.args[0], e.args[1]))


def main():
	companyNameList = ["GOOG","AABA","AMZN","OPK","FB","TWTR","NFLX","TSLA","BABA","SPLK"]
	# print("Welcome! Please select the option:")
	# print("1. Get History Price")
	# print("2. Get Realtime Price" )
	# choice = input()
	# if choice == "1":
	# 	print("Please input the company name: ")
	# 	print(companyNameList)
	# 	name = input()
	# 	GetHistory(name)
	# if choice == "2":
	# 	print("Please input the company name: ")
	# 	print(companyNameList)
	# 	name = input()
	# 	GetRealtime(name)

	# Automatically run the program 20 times
	for com in companyNameList:
		GetRealtime(com)
		# GetHistory(com)


if __name__ == '__main__':
	main()
