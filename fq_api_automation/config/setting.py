import arrow
from utils.get_file import get_file_path
env = 'auto'
if env == "sit":     #开发环境
        Host = "172.16.172.130:23210"
        grant_type = "password"  # 13600136002
        client_id = "portal"
        client_secret = "portal123"  # 13600136008
        username = "liuyang"
        password = "123456"
        data_file_root_path = r"C:\fq\fq_api_automation\api_data_file"


elif env=="test":      #测试环境
        Host ="172.16.172.130:23740"
        grant_type ="password"  #13600136002
        client_id = "portal"
        client_secret="portal123" #13600136008
        username = "test01"
        password="123456"
        data_file_root_path=r"D:\interface_automated\fq_api_automation\api_data_file"



elif env=="auto":      #测试环境
        Host =r"devices.uat.zhhq.for-change.cn"
        grant_type ="password"
        client_id = "portal"
        client_secret="portal123"
        username = "admin1"
        password="123"
        username2="lx"
        password2='123456'
        username3="ly"
        password3="123456"
        username4="test01"
        password4="123456"
        username5="yangfan"
        password5="123456"
        data_file_root_path = r"D:\杨帆\fq_api_automation\api_data_file"


login_api = f'https://{Host}/oauth2/token'
headers  = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin':f'https://{Host}',
        'priority': 'u=1, i',
        'referer': f'https://{Host}',
        'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',

    }
