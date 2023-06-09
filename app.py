import flask
from flask import Flask, render_template, redirect, request, jsonify, Response
from flask_cors.extension import CORS
# from flask_session import Session
import requests
import pandas as pd
import json
from io import StringIO

app = Flask(__name__)
cors = CORS(app)

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
    tracks_df = pd.DataFrame(track_data)

    file_buffer = StringIO()
    tracks_df.to_csv(file_buffer)
    file_buffer.seek(0)
    response = Response(file_buffer,mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="usertracks.csv")
    return response

    # return jsonify(track_data)

@app.route('/test')
def getfile():
    test_data = {'c1':[0,1,2,3,4],'c2':[1,2,3,4,5],'c3':['a','b','c','d','e']}
    df = pd.DataFrame(test_data)
    file = StringIO()
    df.to_csv(file)
    file.seek(0)
    response=Response(file,mimetype='text/csv')
    response.headers.set("Content-Disposition", "attachment", filename="test.csv")
    return response

if __name__ == '__main__':
    app.run()