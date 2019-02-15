# // written by: Tong Wu, ZE LIU, Xinyu Lyu
# // assisted by: Xinwei Zhao
# // debugged by: All members

#导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import *
from flask import Flask, redirect
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
import traceback  
import json

#传递根目录

# import config


length=1000
# app = Flask(__name__)
app = Flask(__name__, static_url_path="")
app._static_folder = "static"
# app._static_folder = '/Users/louisliu/Desktop/application/static'

# 默认路径访问登录页面 
@app.route("/",methods=['POST','GET'])
def login():
	return render_template('Login.html')
 

@app.route('/login', methods=['GET', 'POST'])
def getLoginRequest():
	# if request.method == 'POST' and request.values.get('user') == 'a@b.com' and request.values.get('password') == '1234':	
	# if request.method == 'POST':
	accout = request.values.get('user')
	password = request.values.get('password')
	db = pymysql.connect("localhost","root","123456","TESTDB" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	sql = "select * from TESTDB.user where user=" + "'" + accout + "'" + " and password=" + "'" +password +"'"
	cursor.execute(sql)
	results = cursor.fetchall()
	# 提交到数据库执行
	
	print(len(results))
	if len(results)==1:
		return render_template('main.html') 
	else:
		# return 'username or password not right'
		return render_template('Login.html')
	db.commit()
	# 关闭数据库连接
	db.close()



@app.route("/preRegist",methods=['POST','GET'])
def preRegist():
	return render_template('Register.html')


#默认路径访问注册页面
@app.route('/Register', methods=['POST','GET'])
def regist():
	accout = request.values.get('user')
	password = request.values.get('password')
	print(accout)
	print(password)

	# Insert into database: user
	db = pymysql.connect("localhost","root","123456","TESTDB" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	sql2 = "insert into TESTDB.user(user, password) values (" + "'" + accout + "'" + "," + "'" + password + "')"
	# print(type(sql2))

	# sql2 = "insert into TESTDB.user(user, password) values ('fafa','1111111')"
	cursor.execute(sql2)
	db.commit()
	db.close()


	db = pymysql.connect("localhost","root","123456","TESTDB" )
	# 使用cursor()方法获取操作游标 
	cursor = db.cursor()
	sql = "create TABLE TESTDB." + accout + "(CompanyId VARCHAR(20) NOT NULL, PRIMARY KEY (CompanyId))"

	cursor.execute(sql)
	db.commit()
	db.close()
	return render_template('Login.html')
	



@app.route('/addFav')   
def insertfavourstock():
	# db = pymysql.connect("localhost","root","yfj520520","xinyu" )
	db = pymysql.connect("localhost","root","123456","TESTDB" )
	# 使用cursor()方法获取操作游标 
	cursor1 = db.cursor()
	sql1 = "SELECT EXISTS(SELECT * FROM "+ request.args.get('user') +"WHERE CompanyId = "+request.values.get('company')+")"
	n = cursor1.execute(sql1)
	if n== 0:
		cursor2 = db.cursor()
		sql2 ="Insert into" + request.args.get('user')+"(CompanyId) values ("+request.values.get('company')+")"
		cursor2.execute(sql2)
		db.commit()
	db.close()
	


@app.route('/test', methods=['POST','GET'])
def test():
	n = request.values.get()
	o = json.loads(n)
	print(o)




@app.route('/favorate')
def getFavorate():
	
	# db = pymysql.connect("localhost","root","yfj520520","xinyu" )
	db = pymysql.connect("localhost","root","123456","TESTDB" )
	cursor = db.cursor()
	sql = "SELECT * FROM "+request.args.get('user')
	result = cursor.execute(sql)
	db.close()
	return json.dumps(t)


	
	

	
#@app.route('/lstm2')
#def COSTpredict():
	#return render_template('test.html')
# =============================================================================
# @app.route('/choice')
# def choice():
#     if(request.args.get('company')=='SONY'):
#         companyname='SNE' 
#     elif(request.args.get('company')=='APPLE'):
#         companyname='AAPL'
#     elif(request.args.get('company')=='GOOGLE'):
#         companyname='GOOG'
#     elif(request.args.get('company')=='MICROSOFT'):
#         companyname='MSFT'
#     elif(request.args.get('company')=='COSTCO'):
#         companyname='COST'
#     elif(request.args.get('company')=='YAHOO'):
#         companyname='YAHO'
#     elif(request.args.get('company')=='NIKE'):
#         companyname='NKE'
#     elif(request.args.get('company')=='NITENDO'):
#         companyname='NTDO'
#     elif(request.args.get('company')=='AMAZON'):
#         companyname='AMAZ'
#     elif(request.args.get('company')=='MCD'):
#         companyname='MCD'
#     config.set_copname(companyname)
#     import lstm1
#     import svm
#     return render_template('choice.html')
# =============================================================================


# =============================================================================
# @app.route('/lstm')
# def test():
#     #companyname=request.args.get('company')
#     
#     import lstm1
#     
#     lstm1.main()
#     finalprice=config.get_price1()
#     
#     
#     import svm
#     svm.main()
#     svm_result1=config.get_svm()
#     svm_result2=config.get_svm2()
#     
#     return ('<div style="left: 400px; position: absolute; top: 200px;"><body background="https://ftafwm.files.wordpress.com/2017/01/finance-background.jpg?w=1180&h=610&crop=1">'
#             '<h2>ANN Result:  %s </h2>'
#             '<h2>SVM Result:  %s %s</h2></body>') % (finalprice,svm_result1,svm_result2)
#     
#     
# 
# =============================================================================


@app.route('/indicator')
def indicator():
# =============================================================================
#     company = request.args.get('company')
#     indicatorChoice = request.args.get('indicatorChoice')
# =============================================================================
	import Indicator
	company = request.args.get('company')
	indicatorChoice = request.args.get('indicatorChoice')

	# if indicatorChoice == 'ROC':
	#     Indicator.ROCIndicator(company)

	# if indicatorChoice == 'OBV':
	#     Indicator.OBVIndicator(company)

	# if indicatorChoice == 'MACD':
	#     Indicator.MACDIndicator(company)
	Indicator.main(company, indicatorChoice)
	# Indicator.main("GOOG","ROC")


#使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
#启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
   app.run(debug=True, port=8088)

	