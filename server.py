from flask import Flask
import datetime as dt
# import sys, os
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from infrastructure import chat_client

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hi'

@app.route('/start', methods=['POST'])
def start():
    message = "자동 매매를 시작합니다."
    chat_client.send_message(message)
    return message

@app.route('/stop', methods=['POST'])
def stop():
    message = "자동 매매를 종료합니다."
    chat_client.send_message(message)
    return message

app.run(debug=True)