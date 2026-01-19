import json
import random

import pymysql
import requests


class MyClass:

    def __init__(self):
        self.my_class = None
        self.random_number = self.generate_random_number()

    def generate_random_number(self):
        return random.randint(10, 99)

    def add_table(self):
        pass
        url = 'http://onecategory.apps01.ali-bj-sit03.shuheo.net/onecategory/glossary/node/add'
        table_name = 'test_cup8_attribute_fenqu'
        table_dec = '测试杯子分区表' + str(random.randint(1, 1000))
        # 定义你的JSON请求体数据
        data = {
                "tabs": "info",
                "treeType": 3,
                "nodeType": "TERM",
                "properties": {
                    "manageAttributes": {
                        "dataSecurityLevel": "L1",
                        "securityLevel": "外部公开"
                    },
                    "businessAttributes": {
                        "termEnIndex": table_name
                    }
                },
                "parentId": "5898",
                "inherit": [

                ],
                "nodeDesc": table_dec,
                "nodeName1": table_name,
                "nodeName": table_name,
                "p_u": "71e8b23d-45e2-497a-b247-f5b807fb4f65"
            }

        # 将数据转换为json格式
        payload_json = json.dumps(data)
        # 设置headers，一般情况下，当请求体是JSON时，需要设置Content-Type为application/json
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=payload_json, headers=headers)
        # 获取并打印响应内容
        if response.status_code == 200:
            print('请求成功')
            response_data = response.json()
            print(response_data)
        else:
            print(f'请求失败，状态码：{response.status_code}')


my_class = MyClass()

my_class.add_table()
