import json

from pandas.core.methods.to_dict import to_dict

from public.read_csv_api import get_csv


def get_api_detail_msg(data_module_path,file_name,module_name,tips):
    """

    :param module_name: excel中的模块名
    :param tips: 接口描述
    :return:
    """
    df = get_csv(data_module_path,file_name)
    row = df.loc[(df['模块名'] ==module_name) & (df['接口描述'] == tips)]
    if len(row) >1:
        print(f"{module_name}  {tips} 出现重复数据，请手动处理，这里只取第一个数据")
    try:
        row_dict = row.iloc[0].to_dict()
        dic = {
            "Url": row_dict.get("接口地址"),
            "Scheme": row_dict.get("Scheme"),
            "Method": row_dict.get("请求方式"),
            "Data": row_dict.get("接口参数"),
            "Header": row_dict.get("请求头"),
            "Tips": row_dict.get("接口描述"),
            "ModuleName": row_dict.get("模块名"),
            "validate_value":row_dict.get("校验字段"),
            "chick_type":row_dict.get("校验方式"),
            "expected_value":row_dict.get("预期结果")
        }
        return dic
    except IndexError:
        print(f"excel中 没有找到 {module_name}, {tips}  的数据")
        raise IndexError
if __name__ == '__main__':
    import pprint
    data = get_api_detail_msg("中央运输","方顷接口.csv","中央运输","运送列表-新增运送单")
    print(type(json.loads(data['expected_value'])))