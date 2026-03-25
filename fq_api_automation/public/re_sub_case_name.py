
import os
import re
from utils.get_project_name_util import JarProjectUtil
from utils.get_random_str import random_str



def replace_test_functions(case_file_txt):
    # 初始化一个字典来存储已生成的随机字符串
    replacements = {}
    # 使用正则表达式找到所有匹配的 `test_` 后缀
    matches = re.findall(r"test_(\w+)", case_file_txt)
    # 遍历匹配项，为每个不同的 `test_` 后缀生成或获取一个随机字符串
    for match in set(matches):  # 使用集合去重
        if match not in replacements:
            # 如果这个后缀还没有对应的随机字符串，则生成一个
            replacements[match] = f"test_{random_str(15)}"
    for match in matches:
        case_file_txt = case_file_txt.replace(f"test_{match}", f"{replacements[match]}")
    return case_file_txt

class RenameTest():
    """
    重命名case
    """
    project_path = JarProjectUtil.project_root_path()
    IR_path = os.path.join(project_path,'case')

    @staticmethod
    def rename_func():
        """
        从命名test_开头的测试用例名称
        从命名规则是，若多个用例名称一样（或者有依赖关系的用例时）替换时也命名成一样
        :return:
        """
        for dirpath,dirnames,filenames in os.walk(RenameTest.IR_path):
            for filename in filenames:
                if filename.endswith('.py') and filename.startswith('test_'):
                    fpath = os.path.join(dirpath,filename)
                    with open(fpath,'r',encoding='utf-8') as f:
                        content = replace_test_functions(f.read())
                        with open(fpath, 'w', encoding='utf-8') as f:
                            f.write(content)


    @staticmethod
    def rename_func2():
        """
        从命名test_开头的测试用例名称
        从命名规则是，test_开头的用例名称全部批量随机替换
        :return:
        """
        for dirpath,dirnames,filenames in os.walk(RenameTest.IR_path):
            for filename in filenames:
                if filename.endswith('.py'):
                    fpath = os.path.join(dirpath,filename)
                    content = ''
                    with open(fpath,'r',encoding='utf-8') as f:
                        for line in f.readlines():
                            line = re.sub(r"def test_\w+",f"def test_{random_str(15)}",line)
                            content +=line
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(content)

if __name__ == '__main__':
    RenameTest().rename_func()