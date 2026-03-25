import os
import pytest

import re,time
import subprocess
import psutil#pip3 install psutil  不行的话使用360安装C++ 2015
from utils.threading_func import thread_it
import sys
"""
运行前先执行flask创建本地测试接口
1，IR目录下的类名需要Test开头Moudle结尾
2，用例函数test_开头，可以重名 
"""


def start_serve():
    """
    自动allure web服务 一定时间后自动结束
    :return:
    """
    def kill_serve(process_pid):
        time.sleep(3)
        print("结束web服务")
        parent = psutil.Process(process_pid)
        children = parent.children(recursive=True)
        all_processes= children + [parent]

        #结束所有进程
        for process in all_processes:
            process.kill()

    process = subprocess.Popen('allure serve ./temp', shell =True, stdout=subprocess.PIPE)
    process_pid=process.pid
    thread_it(kill_serve, process_pid=process_pid)
    for i in iter(process.stdout.readline,'b'):
        print(i)
        try:
            url = re.search("<(.*?)>\.",str(i)).group(1)
            print(url)
        except:
            if str(i) == "b''":
                print("结束进程")
                sys.exit(0)

# RenameTest().rename_func2()
if __name__ == '__main__':
    # try:
    #     shutil.rmtree('./temp')
    #     shutil.rmtree('./report')
    # except:
    #     pass
    #pytest.main(['-s', '--alluredir', r'C:\fq\fq_api_automation\temp'])#
    pytest.main()
    #把json文件生成测试报告
    os.system('allure generate ./temp -o ./report  --clean')
    #进入report文件路径 allure open ./打开报告
    # start_serve()