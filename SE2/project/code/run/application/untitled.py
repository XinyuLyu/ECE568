导入数据库模块
import pymysql
#导入Flask框架，这个框架可以快捷地实现了一个WSGI应用 
from flask import Flask
#默认情况下，flask在程序文件夹中的templates子文件夹中寻找模块
from flask import render_template
#导入前台请求的request模块
from flask import request   
from . import loginmanager  
@loginmanager.user_loader  
def load_user(id):  
    return User.query.get(int(id))  