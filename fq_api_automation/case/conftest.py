from pickle import FALSE
from random import random

import pytest, json
import allure
from public.login import Auth
from config.configHandler import ConfigHandler
from filelock import FileLock
from utils.get_tokens import get_token
import traceback
from utils.log_utils import logger

conf = ConfigHandler()


def check_token(file_data):
    try:
        login = Auth(file_data.get("login1"),file_data.get("login2"),file_data.get('login3'),file_data.get('login4'),file_data.get('login5'))

        res = login.OauthModule.api("鉴权登录", "密码模式登录智慧后勤管理系统").response(cached=False)
        if res.json().get("access_token"):
            return True
        else:
            return False
    except:
        return False


def get_token_write_fn(fn, worker_id):
    with allure.step('步骤：获取认证'):
        login_data1 = get_token(conf.grant_type,conf.client_id,conf.client_secret,conf.username, conf.password)
        login_data2=get_token(conf.grant_type,conf.client_id,conf.client_secret,conf.username2,conf.password2)
        login_data3=get_token(conf.grant_type,conf.client_id,conf.client_secret,conf.username3,conf.password3)
        login_data4=get_token(conf.grant_type,conf.client_id,conf.client_secret,conf.username4,conf.password4)
        login_data5=get_token(conf.grant_type,conf.client_id,conf.client_secret,conf.username5,conf.password5)
        file_data = {"login1": login_data1, "login2": login_data2, "login3": login_data3, "login4": login_data4,"login5": login_data5}
        file_data.update({"worker_id": worker_id})
        login = Auth(login_data1,login_data2,login_data3,login_data4,login_data5)
        if isinstance(file_data, dict):
            with open(fn, 'w', encoding='utf-8') as file:
                file.write(json.dumps(file_data))
            print('测试一下下',type(login))
            return login
        else:
            allure.attach(json.dumps(file_data),"鉴权登录接口错误" )
            raise Exception("鉴权登录接口错误！")

@pytest.fixture(scope="session", autouse=False)
def login(tmp_path_factory, worker_id ='master'):
    root_tmp_dir = tmp_path_factory.getbasetemp().parent
    fn = root_tmp_dir / 'data.json'
    # 单机运行，则运行这里代码
    if worker_id == 'master':
        return get_token_write_fn(fn, worker_id)

    # 分布式运行
    # FileLock来给缓存文件上锁，第一个进程调用写入数据后，其余进程也可以访问该缓存文件，但只读取，就可以保证所有进程得到同样的数据
    with FileLock(str(fn) + '.lock'):
        if fn.exists():
            try:
                with open(fn, 'r', encoding='utf-8') as file:
                    file_data = json.loads(file.read())
                    file_data.update({"worker_id": worker_id})
                if check_token(file_data) is False:
                    fn.unlink()  # 删除原文件
                    login = get_token_write_fn(fn, worker_id)
                    return login
                else:
                    login = Auth(file_data.get("login1"),file_data.get("login2"),file_data.get("login3"),file_data.get("login4"),file_data.get("login5"))
                    return login
            except Exception as e:
                logger.info('ERROR:message:{0},traceback:{1}'.format(str(e),traceback.format_exc()))
                fn.unlink()
                login = get_token_write_fn(fn, worker_id)
                return login
        else:
            # 第一次生成缓存文件
            login = get_token_write_fn(fn, worker_id)
            return  login


# 编写钩子函数
# 失败用例自动截图函数
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    每个测试用例执行后,制作测试报告
    :param item: 测试用例对象
    :param call: 测试用例的测试步骤
            先执行 when = 'setup' 返回setup的执行结果
            然后执行 when = 'call' 返回call的执行结果
            然后执行 when = 'teardown' 返回teardown的执行结果
    :return:
    """

    # 获取钩子方法的调用结果，返回一个result对象
    out = yield
    # 获取调用结果的测试报告，返回一个report对象， report对象的属性包括 when(setup,call,reardown三个值)、nedeid （测试用例的名字）、outcome(用例的执行结果，passed,failed)
    report = out.get_result()
    if report.when == 'call' and report.failed:
        pass



