from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username' : 'Robert'}
    
    posts = [
        {
            'author': {'username': 'Cathrine'},
            'body': 'Beautiful day in Linköping'
        },
        {
            'author': {'username': 'Robert'},
            'body': 'Alot of snow comming down in Cham now!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)
