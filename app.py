import flask
from flask import Flask, render_template, redirect
from flask_cors.extension import CORS 

app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect('https://accounts.spotify.com/authorize?')


# @app.route('/redirect')
# def redirect():
#     #
# @app.route()

if __name__ == '__main__':
    app.run()