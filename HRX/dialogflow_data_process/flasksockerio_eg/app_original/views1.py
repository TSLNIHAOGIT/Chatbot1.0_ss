from app import app
from flask import  render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': '大太阳'} # fake user

    posts = [  # fake array of posts
        {
            'author': {'nickname': '我好'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': '你好'},
            'body': 'The Avengers movie was so cool!'
        },
        {
            'author': {'nickname': '大家好'},
            'body': 'I love all body!'
        }
    ]
    return render_template(
                           "index0.html",
                           # "intelgence_law.html",
                           title='Home',
                           user=user,
                           posts=posts)

# def index():
#     user = {'nickname': '大爷'}  # fake user
#     return render_template('index0.html',
#                            title='Home',
#                            user=user)
    # return "Hello, World!"