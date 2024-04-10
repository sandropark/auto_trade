from threading import Thread
from flask import Flask
from crypto import crypto_app
from infrastructure import chat_client

app = Flask(__name__)
crypto = crypto_app.Crypto()
# Thread(target=crypto.start).start()
# message = "자동 매매를 시작합니다."
# chat_client.send_message(message)

@app.route('/')
def index():
    return 'Hi'

@app.route('/start', methods=['POST'])
def start():
    Thread(target=crypto.start).start()
    message = "자동 매매를 시작합니다."
    chat_client.send_message(message)
    return message

@app.route('/stop', methods=['POST'])
def stop():
    crypto.stop()
    message = "자동 매매를 종료합니다."
    chat_client.send_message(message)
    return message

@app.route('/restart', methods=['POST'])
def restart():
    crypto.stop()
    Thread(target=crypto.start).start()
    message = "자동 매매를 재시작합니다."
    chat_client.send_message(message)
    return message

if __name__ == '__main__':
    app.run(debug=True)
    start()