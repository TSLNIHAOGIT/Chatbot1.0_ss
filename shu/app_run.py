# from flask_other.app import app
from flask import Flask
app=Flask(__name__)
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

def get_data(sentence):
    #url中含有中文时要单独处理
    req = urllib.request.Request(
        'http://drea.cc/api/chat.php?msg={}&uid=drea_bbs_chat'.format(quote(sentence)))
    req.add_header('Content-type', 'text/xml; charset="gbk"')
    response = urllib.request.urlopen(req)
    buff = response.read()
    the_page = buff.decode('gbk')
    print(type(the_page),eval(the_page)['reply'])
    response.close()
    return eval(the_page)['reply']



@app.route('/')
@app.route('/index')
def index0():
    return render_template(
                           # "index0.html",
                           "index.html",
                           )
@app.route("/test",methods=["POST"])
def test():
    return console.write
@app.route("/predict", methods= ["POST"])
def background_process():
    if request.method == 'POST':
        try:
            query = request.form.get('query')#前端查询的内容
            if query:

                    print('query',query)
                    # time.sleep(5)
                    result = get_data(query)
                    print('result',result)
                    mongo_db.save_query(query, str(result))
                    return str(result)

            else:

                    return str('请输入查询内容')


        except Exception as e:

            if 'duplicate' in str(e):
                e_str = e.details['errmsg']
                dup_id=re.search('\{ : "(.*)" \}',e_str).group(1)
                print('重复查询同一句话,存储时使用相同的_id_',dup_id)
                mongo_db.update_dup_query( dup_id, str(result))
                return str(result)

            else:
                print(e)
                print('有问题，MM出故障啦')
                return str('MM出故障啦')

        # finally:
        #     # print(e)
        #     print('有问题，MM出故障啦。。')
        #     return str('MM出故障啦。。')

    else:
        return 'ok'

# @app.route('/dataFromAjax_post',methods=['POST','GET'])
# def dataFromAjax_post():
#     if request.method == 'POST':
#
#         try:
#             # query = request.form.get('mydata')  # 前端查询的内容
#             query = request.form['mydata']  # 前端查询的内容
#             if query:
#
#                 print('query', query)
#                 # time.sleep(5)
#                 result = '欢迎光临'
#                 print('result', result)
#                 # mongo_db.save_query(query, str(result))
#                 return str(result)
#             else:
#
#                 return str('请输入查询内容')
#         except Exception as e:
#             print('exception', e)
#             return str('有问题')
#     else:
#         return 'ok'



if __name__=='__main__':
    app.debug = False
    app.run(host='0.0.0.0',port=5000)    #这样用来监听所有的ip，团队调试用

    # get_data('中国')
