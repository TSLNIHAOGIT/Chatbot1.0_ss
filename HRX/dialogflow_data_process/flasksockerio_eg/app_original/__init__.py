from flask import Flask

app = Flask(__name__) #创建Flask application对象
from app import views1  #引入视图，还没实现