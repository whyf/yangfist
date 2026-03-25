import json
import re
from operator import index
from re import split

import jsonpath

from public.get_api_msg import get_api_detail_msg


class AssertUtil:
    def contains(self,check_value,expected_value):
        """包含"""
        assert expected_value in check_value,f'{expected_value}in {check_value}'

    def equals(self,check_value,expected_value):
        """相等"""
        assert check_value == expected_value
            #f'{check_value} == {expected_value}'



    def less_than(self,check_value,expected_value):
        """小于"""
        assert check_value <expected_value,f'{check_value}<{expected_value}'
    def less_than_or_equals(self,check_value,expected_value):
        """小于等于"""
        assert check_value <= expected_value, f'{check_value} <= {expected_value})'

    def greater_than(self, check_value, expected_value):
        """大于"""
        assert check_value > expected_value, f'{check_value} > {expected_value})'

    def greater_than_or_equals(self, check_value, expected_value):
        """大于等于"""
        assert check_value >= expected_value, f'{check_value} >= {expected_value})'

    def not_equals(self,check_value,expected_value):
        """不等于"""
        assert check_value != expected_value, f'{check_value} != {expected_value})'

    def startswith(self,check_value,expected_value):
        "以什么开头"
        assert str(check_value).startswith(str(check_value)),f'{str(check_value)} startswith {str(expected_value)})'


    def endswith(self,check_value,expected_value):
        """以什么结尾"""
        assert str(check_value).endswith(str(expected_value)), f'{str(check_value)} endswith {str(expected_value)})'

    def length(self,check_value,expected_value):
        """校验数量"""
        assert len(check_value)==int(expected_value), f'{str(len(check_value))} == {str(expected_value)})'

    def is_instance(self, check_value,expected_value):
        """
        判断响应某个字段是否是某种类型结果数据
        :param check_value: 检查字段
        :param expected_value: 预期的数据类型
        :return:
        """
        assert  isinstance(check_value,eval(expected_value))

    def validate_response(self,actually_value,expected_value,chick_type):
        if chick_type in ['==','相等','等于','eq','equal']:
            if expected_value == 'true':
                expected_value = eval('true')
            if expected_value== 'false':
                expected_value = eval('false')
            if expected_value == 'True' or expected_value=='TRUE':
                expected_value= bool(True)
            if expected_value == 'False' or expected_value=='FALSE':
                expected_value = bool(False)
            self.equals(actually_value,expected_value)
        if chick_type in ['!=','不等于','不相等']:
            self.not_equals(actually_value,expected_value)
        if chick_type in ['<','小于']:
            self.less_than(actually_value,expected_value)
        if chick_type in ['<=','小于或等于']:
            self.greater_than_or_equals(actually_value,expected_value)
        if chick_type in ['>','大于']:
            self.greater_than(actually_value,expected_value)
        if chick_type in ['>=','大于或等于']:
            self.greater_than_or_equals(actually_value ,expected_value)
        if chick_type in ['in','包含']:
            self.contains(actually_value,expected_value)
        if chick_type in ['startswith']:
            self.startswith(actually_value,expected_value)
        if chick_type in ['endswith']:
            self.endswith(actually_value,expected_value)
        if chick_type in ['isinstance']:
            self.is_instance(actually_value,expected_value)







    def extract_by_jsonpath(self,extract_value:dict,extract_expression:str):
        """
        根据jsonpath表达式从响应中获取值
        :param extract_value: response.josn
        :param extract_expression:  json提取表达式 类似 $.token
        :return: None或 如果是一个列表中只有1个值则提取第一个值，或全部
        """
        extract_value=jsonpath.jsonpath(extract_value,extract_expression)
        if not extract_value:
            return
        elif len(extract_value)==1:
            return extract_value[0]
        else:
            return extract_value


    def assert_util(self,res,module_name,tips,data_module_path,file_name):
        self.request_target = get_api_detail_msg(module_name=module_name, tips=tips,
                                                 data_module_path=data_module_path, file_name=file_name)
        validate_value = self.request_target['validate_value']
        chick_type =self.request_target['chick_type']
        expected_value=self.request_target['expected_value']
        actually_value=self.extract_by_jsonpath(res.json(),extract_expression=f'$..{validate_value}')
        self.validate_response(actually_value,expected_value,chick_type)






if __name__=="__main__":
    assert_util=AssertUtil()
    data = get_api_detail_msg("物联网","方顷接口.csv","物联网","协议管理-成功获取协议列表")
    assert_util.assert_util('123',data['expected_value'])
