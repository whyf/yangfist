# import os.path
#
# import pandas as pd
# import demjson3
# from cachetools import cached,TTLCache
# from config.setting import excel_path
# from config.setting import data_file_root_path
#
#
# @cached(TTLCache(maxsize=100,ttl=100))
# def get_table():
#     table = pd.read_excel(excel_path,sheet_name='Sheet1')
#     print(f"行列数：{table.shape},请确认没有空行，有空行请删除",)
#     table['接口参数'] = table['接口参数'].str.replace('True','true')
#     # 请求头和请求参数为空的替换成空字典
#     table['接口参数'] = table['接口参数'].apply(lambda x: '{}' if pd.isna(x) or x == '' or x.isspace() else x)
#     table['请求头'] = table['请求头'].apply(lambda x: '{}' if pd.isna(x) or x == ''or x.isspace() else x)
#     try:
#         for index,i in enumerate(table['接口参数']):
#             demjson3.decode(i)
#     except Exception as e:
#         print("接口参数可能有问题,详细如下，或有空白行")
#         print("问题行数：",index+2)
#         print(i)
#     return table
#
#
# if __name__ == '__main__':
#     print(get_table().to_dict(orient='records'))
