# -*- coding: utf-8 -*-
# from flask_other.app import app
from flask import Flask
import os,sys 
# sys.path.append('/home/kai/data/wei/Chatbot1.0/')
sys.path.append('../')
# sys.path.append('/home/kai/data/Chatbot1.0/API/v1/frontend/')
app=Flask("demo")
from flask import  render_template,request
from app.mong_database import MongoManager
import time
import re
mongo_db=MongoManager(server_ip='chatbotdb')

import urllib.request
from urllib.parse import quote
import pandas as pd
import numpy as np
import time
import re
import requests
import uuid

##################################
url = 'http://localhost:8889/chatbotv1'


def get_data(sentence, uid):
    sessionId = cache.uid_dict[uid]
    response = requests.get(url, timeout=10, params={'data':sentence, 
                                                     'action':'chat', 
                                                     'sessionId':sessionId})
    
    if response.status_code == 200:
        req = response.json()
        if req.get('status').lower() == 'successful':
            msg = req.get('message')
        else:
            msg = req

        return msg
    else:
        return 'Internet Connection Issue, error code {}'.format(response.status_code)



@app.route('/')
@app.route('/index')
def index0():
    return render_template(
                           # "index0.html",
                           "index.html",
                           )

@app.route("/createCookie", methods = ['POST'])
def createCookie():
    if request.method == 'POST':
        
        cookieid = request.form.get('cookie');
        if cookieid:
            print('already exists')
            print(cookieid)
            return('')
        else:
            print('new user')
            uid = str(uuid.uuid1())
            print('create cookie {}'.format(uid))
            return(str(uuid.uuid1()))



@app.route("/predict", methods= ["POST"])
def background_process():
    if request.method == 'POST':
        try:
            query = request.form.get('query')#前端查询的内容
            uid = request.form.get('uid')
            print(uid)
            if query:

                    
                    # time.sleep(5)
                    result = get_data(query, uid)
                    mongo_db.save_query(query, str(result))
                    print('saving to mongo db successfully!')
                    return str(result)
                    

            else:

                    return str('请输入查询内容')


        except Exception as e:
            print(e)

            if 'duplicate' in str(e):
                e_str = e.details['errmsg']
                dup_id=re.search('\{ : "(.*)" \}',e_str).group(1)
                print('query duplicated! Use same id to save')
                mongo_db.update_dup_query( dup_id, str(result))
                return str(result)

            else:
                print(e)
                return str('MM出故障啦')


    else:
        return 'ok'
    
    
@app.route("/newConversation", methods= ["POST"])
def new_conversation():
    
    print('new conversation called!!!!!!!!!!!!!!!!!!!!!!!')
    if request.method == 'POST':
        cookie = request.form.get('uid');
        if cookie:
            print(cookie)
            cache.new_conversation(cookie)
            return cookie
        else:
            print('cookie lost')
            return('error')

class Cache:
    def __init__(self):
#         self.new_conversation()
        self.uid_dict = {}
            
    def new_conversation(self):
        req = requests.get(url, timeout=10, params={'action':'create'})
        if req.status_code == 200:
            msg = req.json()
            if msg['status'] == 'successful':
                
                self.sessionId = msg['message']['sessionId']
                print(self.sessionId)
            else:
                
                raise ValueError('cannot get new sessionId, cannot start chat')
        else:
            print(req.status_code)
            
    def new_conversation(self, uid):
        req = requests.get(url, timeout=10, params={'action':'create'})
        if req.status_code == 200:
            msg = req.json()
            if msg['status'] == 'successful':
                sessionId = msg['message']['sessionId']
                self.uid_dict[uid] = sessionId
                print(self.uid_dict[uid])
            else:
            
                raise ValueError('cannot get new sessionId, cannot start chat')
        else:
            print(req.status_code)
        


if __name__ == "__main__":
    cache = Cache()   
    app.debug = False
    port = 6006
    print('running at http://10.0.24.31:{}'.format(port))
    app.run(host='0.0.0.0',port=port)   

