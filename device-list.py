import hashlib
import hmac
import json
import os
import pprint
import random
import requests
import time

API_KEY=os.environ.get('ECOFLOW_ACCESS_KEY')
API_SECRET=os.environ.get('ECOFLOW_SECRET_KEY')
HOST='api-e.ecoflow.com'

# Device list URL:
URL=f'https://{HOST}/iot-open/sign/device/list'

nonce = random.randint(100000, 999999)
timestamp = int(time.time() * 1000)

params=f'accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
hmac_sha256 = hmac.new(API_SECRET.encode('utf-8'), params.encode('utf-8'), hashlib.sha256)
signature = hmac_sha256.hexdigest()


headers = dict(
    accessKey = API_KEY,
    # ContentType
    nonce = str(nonce),
    timestamp = str(timestamp),
    sign = signature,
)

result = requests.get(url=URL,headers=headers)
result_json = json.loads(result.text)

# pprint.pprint(result_json)

for device in result_json['data']:
    print(device['deviceName'], f": Online - {device['online']}")
