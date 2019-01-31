from gevent import monkey
monkey.patch_all()

# monkey.patch_all()的导入要放在所有的前面
import requests


create_urllib3_context()
from flask import Flask, render_template
from flask_socketio import SocketIO
import random

async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

#http://localhost:5000/
@app.route('/')#网页url的当前路径

@app.route('/test')
def index():
    return render_template('test.html')


@socketio.on('connect', namespace='/test_conn')
def try_connect():

    ##while导致链接不上，发不出去消息
    # while True:
    #     socketio.sleep(5)

        # t = random_int_list(1, 100, 10)
        t='欢迎来到flask_socketio'
        socketio.emit('server_response',
                      {'data': t},
                      namespace='/test_conn')


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


if __name__ == '__main__':
    socketio.run(app, debug=True)
