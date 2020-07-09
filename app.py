from flask import Flask
from flask import jsonify
from datetime import datetime


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/status')
def status():
    return jsonify({
        "status": True,
        "name": "Example messenger",
        "time": datetime.now()
    })

if __name__ == '__main__':
    app.run()
