#导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
import traceback  
import json

#传递根目录

import config


length=1000
app = Flask(__name__)
#默认路径访问登录页面

@app.route('/')
def login():
    return render_template('login.html')
    #return render_template('new.html')

#默认路径访问注册页面
@app.route('/regist')
def regist():
    return render_template('regist.html')
    #return render_template('reg.html')

#获取注册请求及处理
@app.route('/registuser')
def getRigistRequest():
#把用户名和密码注册到数据库中

    #连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost","root","yfj520520","xinyu" )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO user(user, password) VALUES ("+request.args.get('user')+", "+request.args.get('password')+")"
    sql = """
			  CREATE TABLE """+request.args.get('user')+"""(
			  CompanyId VARCHAR(20) NOT NULL,
			  PRIMARY KEY (CompanyId))
			  ENGINE = InnoDB;"""
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
         #注册成功之后跳转到登录页面
        return render_template('login.html') 
    except:
        #抛出错误信息
        traceback.print_exc()
        # 如果发生错误则回滚
        db.rollback()
        return '注册失败'
    # 关闭数据库连接
    db.close()

    #获取登录参数及处理
@app.route('/addFav')   
def insertfavourstock():
    db = pymysql.connect("localhost","root","yfj520520","xinyu" )
    # 使用cursor()方法获取操作游标 
    cursor1 = db.cursor()
    sql1 = "SELECT EXISTS(SELECT * FROM "+ request.args.get('user') +"WHERE CompanyId = "+request.args.get('company')+")"
    n = cursor1.execute(sql1)
    if n== 0:
        cursor2 = db.cursor()
        sql2 ="Insert into" + request.args.get('user')+"(CompanyId) values ("+request.args.get('company')+")"
        cursor2.execute(sql2)
        db.commit()
    db.close()
    
@app.route('/login')
def getLoginRequest():
#查询用户名及密码是否匹配及存在
    #连接数据库,此前在数据库中创建数据库TESTDB
    db = pymysql.connect("localhost","root","yfj520520","xinyu" )
    # 使用cursor()方法获取操作游标 
    cursor = db.cursor()
    # SQL 查询语句
    sql = "select * from user where user="+request.args.get('user')+" and password="+request.args.get('password')+""
    try:
        # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        print(len(results))
        if len(results)==1:
            return render_template('main.html') 
        
        else:
            return 'username or password not right'
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        traceback.print_exc()
        db.rollback()
    # 关闭数据库连接
    db.close()
   # return render_template('main.html')

@app.route('/favorate')
def getFavorate():
    
    db = pymysql.connect("localhost","root","yfj520520","xinyu" )
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
    import Indicator1
    Indicator1.main("GOOG","ROC")


#使用__name__ == '__main__'是 Python 的惯用法，确保直接执行此脚本时才
#启动服务器，若其他程序调用该脚本可能父级程序会启动不同的服务器
if __name__ == '__main__':
   app.run(debug=True, port=8086)

    