import os.path

import pandas as pd
import demjson3
from cachetools import cached,TTLCache
from config.setting import data_file_root_path



@cached(TTLCache(maxsize=100,ttl=100))
def get_csv(module_name,file_name):
    csv_path=os.path.join(data_file_root_path,module_name,file_name)
    csv=pd.read_csv(csv_path,encoding='gbk')
    print("测试11",csv)
    print(f"行列数：{csv.shape},请确认没有空行，有空行请删除", )
    #csv[['接口参数', '请求头', '预期结果']] = csv[['接口参数', '请求头', '预期结果']].astype(str)
    csv['接口参数'] = csv['接口参数'].str.replace('True', 'true')
    # 请求头和请求参数为空的替换成空字典
    csv['接口参数'] = csv['接口参数'].apply(lambda x: '{}' if pd.isna(x) or x == '' or x.isspace() else x)
    csv['请求头'] = csv['请求头'].apply(lambda x: '{}' if pd.isna(x) or x == '' or x.isspace() else x)
    csv['预期结果']=csv['预期结果'].str.replace('TRUE','True')

    try:
        for index, i in enumerate(csv['接口参数']):
            demjson3.decode(i)
    except Exception as e:
        print("接口参数可能有问题,详细如下，或有空白行")
        print("问题行数：", index + 2)
        print(i)
    return csv
    print("测试",sv)
if __name__ == '__main__':
    #print(get_table().to_dict(orient='records'))
    print(get_csv("物联网","方顷接口.csv").to_dict())