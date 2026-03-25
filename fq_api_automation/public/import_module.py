import os,re
from importlib import import_module
from cachetools import cached,TTLCache
import inspect
class ImportModule():
    IR_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),'IR')
    @staticmethod
    @cached(TTLCache(maxsize=1000,ttl=1800))
    def import_module(class_name):
        for dirpath,dirnames,filenames in os.walk(ImportModule.IR_path):
            for filename in filenames:
                if filename.endswith('.py'):
                    file = re.sub(r'[\\/]','.',dirpath.split('fq_api_automation')[1])
                    module = import_module(file.strip(".")+"." + filename.split(".") [0])
                    #获取模块所有成员
                    members = inspect.getmembers(module)
                    for name,obj in  members:
                        if inspect.isclass(obj) and obj.__name__ == class_name:
                            return getattr(module,class_name)
        raise ImportError(f"Module{class_name} not found")

if __name__ == '__main__':
    print(ImportModule.import_module('ClassName1Module').__dict__)