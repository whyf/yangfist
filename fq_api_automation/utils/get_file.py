# -*- coding: utf-8 -*-
import os
from utils.get_project_name_util import JarProjectUtil


def get_file_path(dirname,endswithstr,infilestr):
    """

    :param dirname: 需要寻找的文件夹名字
    :param endswithstr: 文件结尾
    :param infilestr: 文件名称包含的文字
    :return:
    """
    project_path = JarProjectUtil.project_root_path()
    path = os.path.join(project_path,dirname)
    for dirpath, dirnames,filenames in os.walk(path):
        for f in  filenames:
            fpath = os.path.join(dirpath,f)
            if os.path.isfile(fpath):
                if fpath.endswith(endswithstr) and infilestr in f and "$" not in f:
                    return os.path.join(dirpath,f)


if __name__ == '__main__':
    file =  get_file_path('api_data_file','.csv','方顷接口')
    print(file)