import time 

from flask import Flask, jsonify, request
from datetime import datetime
from os import urandom
from base64 import b64encode
from hashlib import sha256

app = Flask(__name__)

messages = [
    {'name': 'admin', 'time': time.time(), 'text': 'Hello world!'} 
]

users = {
    "admin": {
        "password": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918" # admin
    },
    "bot": {
        "password": "9d74932bdb6f21dc7ab21d6fc5260f474e0d538571fba7a82b74ffe47e6f9a10" # bot
    }
}
tokens = {} # token:username

def authorize_user(user: str) -> str:
    token = find_user_token(user)
    if token:
        del tokens[token]
    token = get_random_token()
    while token in tokens:
        token = get_random_token()
    tokens[token] = user
    return token
    

def find_user_token(user: str) -> str:
    for token, name in tokens.items():
        if name == user:
            return token
    return None

def get_random_token() -> str:
    return str(b64encode(urandom(32)), encoding='utf-8')

@app.route("/register", methods=['POST'])
def register_view():
    try:
        name = request.json['name']
        password = request.json['password']
    except KeyError:
        return {'message': "Bad keys passed"}, 400
    if not name in users:
        password = password.encode('utf-8')
        users[name] = {
            'password': str(sha256(password).hexdigest()),
            }
        token = authorize_user(name)
        return jsonify({
            'ok': True,
            'token': token
            })
    return jsonify({'message': 'user already exists'}), 403

@app.route("/login", methods=['POST'])
def login_view():
    try:
        name = request.json['name']
        password :str= request.json['password']
        if not 0 < len(name) <= 255 or not 0 < len(password) <= 255:
            raise KeyError("Keys are too short or long")
    except KeyError as e:
        return {
            'message': f"Bad keys passed\n{e.args}"
            }, 400
    password = password.encode('utf-8')
    password = str(sha256(password).hexdigest())
    if password == users[name]['password']:
        token = authorize_user(name)
        return jsonify({
            'ok': True,
            'token': token
            })
    return {"message": "Bad credentials"}, 403

@app.route("/send", methods=['POST'])
def send_view():
    token = request.headers.get('Token')
    if not token or not token in tokens:
         return {'message': 'Expired token'}, 401
    try:
        text = request.json['text']
        if not 0 < len(text) <= 255:
                raise KeyError("Text is too short or long")
    except KeyError:
        return {"message": "Bad key error"}, 400
    name = tokens[token]
    messages.append({'name': name, 'text': text, 'time': time.time()})
    return {"ok": True}
   

@app.route("/messages")
def messages_view():
    token = request.headers.get('Token')
    if not token or not token in tokens:
        return {'message': 'Expired token'}, 401
    try:
        after = float(request.args['after'])
    except (KeyError, ValueError):
        return {'message': "Bad key passed"}, 400
    return jsonify({'messages': list(filter(lambda x: x['time'] > after, messages))})

@app.route('/')
def index_view():
    return 'Hello World!'

@app.route('/status')
def status_view():
    return jsonify({
        "status": True,
        "name": "Example messenger",
        "time": datetime.now(),
        "users": len(users),
        "messages": len(messages)
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0")
