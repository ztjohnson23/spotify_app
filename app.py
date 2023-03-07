import flask
from flask import Flask, render_template, redirect, request, jsonify, session
from flask_cors.extension import CORS
# from flask_session import Session
import requests


app = Flask(__name__)
cors = CORS(app)
# SESSION_TYPE = 'redis'
# app.config['SECRET_KEY']='sxZZZ1234'
# app.config.from_object(__name__)
# Session(app)

client_id = 'e9e658d5ab0647c5b2979a9b0dccea05'
redirect_uri = 'https://librarian-for-spotify.onrender.com/callback'
client_secret = '1772fc32f7f0486b883e3f3f3911f358'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}')


@app.route('/home')
def callback():
    code = request.values.get('code')
    state = request.values.get('state')
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code'
    }
    body = requests.post('https://accounts.spotify.com/api/token',data=data).json()
    access_token = body['access_token']
    # print(f'p1 - token is:"{access_token}"')

    # session['access_token'] = access_token
    # print('p2 - token saved, redirecting to /home')
    # return redirect('/home')  

    #############################################
    header = {'Authorization':f'Bearer {access_token}'}
    body = requests.get('https://api.spotify.com/v1/me',headers=header).json()

    username = body['display_name']

    return render_template('home.html',username=username)


# @app.route('/home')
# def home():
#     print('p3 - start of home route')
#     access_token = session.get('access_token')
#     print(f'p4 - token is:"{access_token}. Success"')
#     header = {'Authorization':f'Bearer {access_token}'}
#     response = requests.post('https://api.spotify.com/v1/recommendations/available-genre-seeds',headers=header).json()
#     # return render_template('index.html')
#     return response


if __name__ == '__main__':
    app.run()