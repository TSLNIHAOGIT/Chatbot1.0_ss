from flask_other.app import app

# from flask import Flask
# app = Flask(__name__) #创建Flask application对象
# from flask_other.app import views0 #引入视图，还没实现

app.debug = False
app.run(host='0.0.0.0',port=5000)    #这样用来监听所有的ip，团队调试用
# app.run()