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
    client_id = '45145719fea4498bb99238355a19bf3c'
    redirect_uri = 'http://localhost:8888/callback'
    state = 'Aa0H6frT44j9mMmM9a'
    return redirect(f'https://accounts.spotify.com/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}')


# @app.route('/redirect')
# def redirect():
#     #
# @app.route()

if __name__ == '__main__':
    app.run()