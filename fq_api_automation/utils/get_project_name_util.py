# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     LogHandler.py
   Description :  获取工程根目录
-------------------------------------------------
   Change Activity:
                   2024/09/06:
-------------------------------------------------
"""

import os

from openpyxl.styles.builtins import percent


class JarProjectUtil:
    @staticmethod
    def project_root_path(project_name="fq_api_automation"):
        """
        获取当前项目根路径
        :param project_name:
        :return: 根路径
        """
        p_name = 'project_demo' if project_name is None else project_name
        project_path = os.path.abspath(os.path.dirname(__file__))
        root_path = project_path[:project_path.find("{}\\".format(p_name)) + len("{}\\".format(p_name))]
        #print('当前项目名称：{}\r\n当前项目根路径：{}'.format(p_name, root_path))
        #print('测试'+project_path)
        #return root_path
        return root_path


if __name__ == '__main__':
    print(JarProjectUtil.project_root_path())