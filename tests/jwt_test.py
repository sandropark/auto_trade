import jwt
import yaml
import requests
import uuid

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
ACCESS = _cfg['upbit']['access']
SECRET = _cfg['upbit']['secret']
server_url = "https://api.upbit.com/"

payload = {
    'access_key': ACCESS,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, SECRET)
authorization = 'Bearer {}'.format(jwt_token)
headers = {
  'Authorization': authorization,
}

res = requests.get(server_url + '/v1/accounts', headers=headers)
print(res.json())