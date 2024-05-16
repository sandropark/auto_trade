import yaml
import pyupbit as pu

with open('config/auto-trade-config.yml', encoding='UTF-8') as ymlfile:
    _cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

upbit : pu.Upbit = pu.Upbit(_cfg['upbit']['access'], _cfg['upbit']['secret'])