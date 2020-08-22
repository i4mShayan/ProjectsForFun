from googletrans import Translator
import proxy
import socks
import socket
import os
import urllib3

def translate(txt,lang):
    try :
        proxy_info = proxy.return_proxy()
        ip = proxy_info["ip"]
        port = proxy_info["prt"]
        user_name = proxy_info["usr"]
        password = proxy_info["pwd"]
        print('{}:{}@{}:{}'.format(user_name,password,ip,port))
        return Translator(proxies={'http': 'socks5://{}:{}@{}:{}'.format(user_name,password,ip,port)}).translate(text=txt,dest=lang).text
    except:
        return "مشکلی پیش آمده است:(\n" \
               "این مشکل میتواند از سمت گوگل ترنسلیت باشد"