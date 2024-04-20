from threading import Thread
from flask import Flask
from crypto import account
from crypto.crypto_app import Crypto
from crypto.strategy import AMStrategy, VBStrategy

app = Flask(__name__)
crypto = Crypto([AMStrategy(), VBStrategy()])

@app.route('/')
def index():
    return 'Hi'

@app.route('/start', methods=['POST'])
def start():
    Thread(target=crypto.start).start()
    return "자동 매매를 시작합니다."

@app.route('/stop', methods=['POST'])
def stop():
    crypto.stop()
    return "자동 매매를 종료합니다."

@app.route('/restart', methods=['POST'])
def restart():
    crypto.stop()
    Thread(target=crypto.start).start()
    return "자동 매매를 재시작합니다."

@app.route('/raw-data', methods=['PUT'])
def update_raw_data():
    crypto.__refresh__()
    return "데이터 업데이트 완료!"

@app.route('/account', methods=['PUT'])
def update_account():
    account.refresh()
    return "계좌 정보 업데이트 완료!"

if __name__ == '__main__':
    app.run(debug=True)