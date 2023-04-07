import flask
from flask import Flask, render_template, redirect, request, jsonify, session
from flask_cors.extension import CORS
# from flask_session import Session
import requests


app = Flask(__name__)
cors = CORS(app)

app.secret_key = 'g43tjbofq0'
# SESSION_TYPE = 'redis'
# app.config['SECRET_KEY']='sxZZZ1234'
# app.config.from_object(__name__)
# Session(app)

client_id = 'e9e658d5ab0647c5b2979a9b0dccea05'
redirect_uri = 'https://librarian-for-spotify.onrender.com/home'
client_secret = '1772fc32f7f0486b883e3f3f3911f358'
scope = 'user-library-read'
        # playlist-modify-public


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}')


@app.route('/home')
def callback():
    code = request.values.get('code')
    state = request.values.get('state')
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
        'grant_type': 'authorization_code',
        # 'scope': scope
    }
    body = requests.post('https://accounts.spotify.com/api/token',data=data).json()
    access_token = body['access_token']

   
    session['access_token'] = access_token
    #############################################
    header = {'Authorization':f'Bearer {access_token}'}
    body = requests.get('https://api.spotify.com/v1/me',headers=header).json()

    username = body['display_name']

    body = requests.get('https://api.spotify.com/v1/me/tracks',headers=header).json()
            # ,data={'limit':50}
    user_songs = body['items']
    i=0
    while body['next'] != None and i<20:
        body = requests.get(body['next'],headers=header).json()
        user_songs.extend(body['items'])
        i+=1
    print(len(user_songs))
    return render_template('home.html',username=username,n_songs = len(user_songs))



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