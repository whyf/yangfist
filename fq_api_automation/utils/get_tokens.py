import requests
import arrow
from utils.webRequest import WebRequest
from cachetools import cached,TTLCache
from config.setting import login_api,Host,grant_type,client_id,client_secret,username,password,headers



@cached(TTLCache(maxsize=100, ttl=3600))
def get_token(grant_type,client_id,client_secret,username, password):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': f"https://{Host}",
        'priority': 'u=1, i',
        'referer': f'https://{Host}/',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }

    data = {
        "grant_type":grant_type,
        "client_id":client_id,
        "client_secret":client_secret,
            'username':username,
            'password':password
    }
    print(login_api)
    response1 = WebRequest().post(login_api, headers=headers, data=data)
    # json_data2 = {
    #     'ma': {
    #         'mobile': account,
    #         'region': '86',
    #         'code': arrow.now().format("DDHHmm"),
    #         'password':password,
    #     },
    #     'app': 'MANAGE_OP',
    #     'zone': 'CN',
    #     'platform': 'WEB',
    #     'secret': response1.json().get('secret'),
    # }
    # response2 = requests.post(conf.login_api, headers=headers, json=json_data2)
    # pprint.pprint(response2.json())
    response1.json = {'access_token':'1c0741f9-4818-4c92-9c16-6a634c30b517'}
    return {'access_token':'1c0741f9-4818-4c92-9c16-6a634c30b517'}


#
if __name__ == '__main__':
    from config.setting import login_api,Host,grant_type,client_id,client_secret,username,password
    print(get_token(grant_type,client_id,client_secret,username, password))
