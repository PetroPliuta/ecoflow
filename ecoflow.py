"""
device_list
"""

import hashlib
import hmac
import json
import os
import pprint
import random
import time
import requests

API_KEY = os.environ.get('ECOFLOW_ACCESS_KEY')
API_SECRET = os.environ.get('ECOFLOW_SECRET_KEY')
HOST = 'api-e.ecoflow.com'

# Device list URL:
URL = f'https://{HOST}/iot-open/sign/device/list'

nonce = random.randint(100000, 999999)
timestamp = int(time.time() * 1000)

params = f'accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
hmac_sha256 = hmac.new(API_SECRET.encode(
    'utf-8'), params.encode('utf-8'), hashlib.sha256)
signature = hmac_sha256.hexdigest()


headers = dict(
    accessKey=API_KEY,
    # ContentType
    nonce=str(nonce),
    timestamp=str(timestamp),
    sign=signature,
)

result = requests.get(url=URL, headers=headers, timeout=3)
result_json = json.loads(result.text)

pprint.pprint(result_json)
sn = result_json['data'][0]['sn']
# print(f"{sn=}")

for device in result_json['data']:
    print(device['deviceName'], f": Online - {device['online']}")

# Get Delta Pro all quota values
path = f"/iot-open/sign/device/quota/all?sn={sn}"
nonce = random.randint(100000, 999999)
timestamp = int(time.time() * 1000)
params = f'sn={sn}&accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
hmac_sha256 = hmac.new(API_SECRET.encode(
    'utf-8'), params.encode('utf-8'), hashlib.sha256)
signature = hmac_sha256.hexdigest()


headers = dict(
    accessKey=API_KEY,
    # ContentType
    nonce=str(nonce),
    timestamp=str(timestamp),
    sign=signature,
)

result = requests.get(url=f"https://{HOST}{path}", headers=headers, timeout=3)
# pprint.pprint(result.json())

# set pd.bppowerSoc bpPowerSoc
for i in range(94, 95):
    path = "/iot-open/sign/device/quota"
    # nonce = random.randint(100000, 999999)
    # timestamp = int(time.time() * 1000)
    params = f'params.bpPowerSoc=51&params.cmdSet=32&params.id={
        i}&params.isConfig=1&params.maxChgSoc=90&params.minDsgSoc=10&sn={
        sn}&accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
    hmac_sha256 = hmac.new(API_SECRET.encode(
        'utf-8'), params.encode('utf-8'), hashlib.sha256)
    signature = hmac_sha256.hexdigest()

    headers = {
        "accessKey": API_KEY,
        "Content-Type": 'application/json;charset=UTF-8',
        "nonce": str(nonce),
        "timestamp": str(timestamp),
        "sign": signature,
    }

    body = {
        "params": {
            "cmdSet": 32,
            "id": i,
            "bpPowerSoc": 51,
            "isConfig": 1,
            "minDsgSoc": 10,
            "maxChgSoc": 90,
            # "closeOilSoc": 61
        },
        "sn": sn
    }

    response = requests.put(
        f"https://{HOST}{path}", headers=headers, data=json.dumps(body), timeout=3)

    print(i, response.json(), sep=" ")


for i in range(94, 95):
    path = "/iot-open/sign/device/quota"
    nonce = random.randint(100000, 999999)
    timestamp = int(time.time() * 1000)
    params = f'params.cmdSet=32&params.id={i}&params.quotas[0]=pd.bppowerSoc&sn={
        sn}&accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
    hmac_sha256 = hmac.new(API_SECRET.encode(
        'utf-8'), params.encode('utf-8'), hashlib.sha256)
    signature = hmac_sha256.hexdigest()

    headers = {
        "accessKey": API_KEY,
        "Content-Type": 'application/json;charset=UTF-8',
        "nonce": str(nonce),
        "timestamp": str(timestamp),
        "sign": signature,
    }

    body = {
        "params": {
            "cmdSet": 32,
            "id": i,
            "quotas": ["pd.bppowerSoc"]
            # "bpPowerSoc": 61
            # "closeOilSoc": 61
        },
        "sn": sn
    }

    response = requests.post(
        f"https://{HOST}{path}", headers=headers, data=json.dumps(body), timeout=3)

    print(i, response.json(), sep=" ")
