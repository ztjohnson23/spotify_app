import flask
from flask import Flask, render_template, redirect, request, jsonify, Response, session
from flask_cors.extension import CORS
# from flask_session import Session
import requests
import pandas as pd
import json
from io import StringIO
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

app = Flask(__name__)
cors = CORS(app)
app.secret_key = "it's/a/secret"

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

    return render_template('home.html',token=access_token,body=body)


@app.route('/run', methods = ['POST'])
def run():
    track_data = json.loads(request.form['data'])
    df = pd.read_json(track_data)
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['explicit'] = df['explicit'].replace({True:1,False:0})
    X = df.drop(['title','id','artist_name','album_name','album_image'],axis=1)
    X['release_date'] = (X['release_date'] - min(X['release_date'])) / (max(X['release_date']) - min(X['release_date']))
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    n_clusters = len(X_scaled) / 50
    groups = Kmeans(n_clusters=n_clusters).fit_predict(X_scaled)
    # df['cluster'] = kmeans
    

    return str(groups.tolist())


if __name__ == '__main__':
    app.run()