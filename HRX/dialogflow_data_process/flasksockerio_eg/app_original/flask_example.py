from flask import Flask

app = Flask(__name__)

#http://localhost:5000
@app.route('/')
def index():
    return '<h1>Hello 8888World!</h1>'



#http://localhost:5000/user/Dave，输入网址不同时，返回的也不同
@app.route('/user/<name>')
def user(name):
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=False)

