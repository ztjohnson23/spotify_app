import flask
from flask import Flask, render_template, redirect, request, jsonify
from flask_cors.extension import CORS
import requests


app = Flask(__name__)
cors = CORS(app)

client_id = 'e9e658d5ab0647c5b2979a9b0dccea05'
redirect_uri = 'https://librarian-for-spotify.onrender.com/callback'
client_secret = '1772fc32f7f0486b883e3f3f3911f358'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}')


@app.route('/callback')
def callback():
    code = request.values.get('code')
    state = request.values.get('state')
    data = {
        'code': code,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }
    headers = {
        'Authorization': f'Basic{client_id}:{client_secret}'
    }
    body = requests.post('https://accounts.spotify.com/api/token',data=data,headers=headers)
    return jsonify(body.text)
    



# @app.route()

if __name__ == '__main__':
    app.run()