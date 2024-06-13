import random
import time
import hmac
import hashlib
import os
import sys
import json
import requests

API_KEY = ""
API_SECRET = ""
SN = ""
API_KEY = os.environ.get('ECOFLOW_ACCESS_KEY')
API_SECRET = os.environ.get('ECOFLOW_SECRET_KEY')
SN = os.environ.get('SN')

HOST = "api-e.ecoflow.com"
PATH = "/iot-open/sign/device/quota"
ID = 94

# Check if the correct number of arguments are provided
if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <number>")
    sys.exit(1)

# Get the argument
arg = sys.argv[1]

try:
    # Convert the argument to an integer
    number = int(arg)
    print(f"The provided number is {number}")
except ValueError:
    print(f"Error: The provided argument '{arg}' is not a valid integer.")
    sys.exit(1)


nonce = random.randint(100000, 999999)
timestamp = int(time.time() * 1000)
params = f'params.bpPowerSoc={number}&params.cmdSet=32&params.id={
    ID}&params.isConfig=1&params.maxChgSoc=90&params.minDsgSoc=10&sn={
    SN}&accessKey={API_KEY}&nonce={nonce}&timestamp={timestamp}'
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
        "id": ID,
        "bpPowerSoc": number,
        "isConfig": 1,
        "minDsgSoc": 10,
        "maxChgSoc": 90,
    },
    "sn": SN
}

response = requests.put(
    f"https://{HOST}{PATH}", headers=headers, data=json.dumps(body), timeout=3)

print(response.json())
