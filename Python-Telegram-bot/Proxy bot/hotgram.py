import base64
import requests
import json
from random import randint
from datetime import datetime
from Crypto.Cipher import AES

class proxy:
    def __init__(self):
        pass

    IV = "YC'2bmK=b%#NQ?9j"
    KEY = "KCH@LQj#>6VCqqLg"
    SALT = datetime.now().strftime("%s")  + str(randint(0, 999)).zfill(3)
    HOST = "lh{}.hotgram.ir".format(randint(1,80))
    URL = "http://{}/v1/proxy?slt={}&appId=3".format(HOST,SALT)

    headers = {
        "X-SLS-GPRS": "false",
        "X-SLS-Carrier": "",
        "X-SLS-UID": "0",
        "X-SLS-AppId": "3",
        "X-SLS-VersionCode": "135",
        "Authorization": "Custom QWxhZGRpbjpPcGVuU2VzYW1l",
        "Content-Type": "application/json",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.0; dolphin Build/NRD91N)",
        "Host": HOST,
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
    }
    @classmethod
    def get_proxy(cls,IV, KEY, URL):
        response = requests.post(URL, headers=cls.headers).text
        b64_encrypted_proxy = json.loads(response).get("data")[0]
        enc = base64.b64decode(b64_encrypted_proxy)
        cipher = AES.new(KEY, AES.MODE_CBC, IV)
        s = cipher.decrypt(enc)
        return s[:-ord(s[len(s)-1:])]

    @classmethod
    def return_proxy(cls):
        decoded_proxy = cls.get_proxy(cls.IV, cls.KEY, cls.URL)
        parsed_output = json.loads(decoded_proxy.decode('utf-8'))

        return parsed_output