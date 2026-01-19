import json
import random
from datetime import datetime
import pymysql
import requests


class MyClass:


    def __init__(self):
        self.my_class = None
        self.random_number = self.generate_random_number()

    def generate_random_number(self):
        return random.randint(10, 99)

    def add_table(self):

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

    def add_colum(self):
        pass
        url = 'http://onecategory.apps01.ali-bj-sit03.shuheo.net/onecategory/glossary/node/add'
        colum_name = 'wenli2'
        colum_dec = '纹理'
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
                    "termEnIndex": colum_name
                }
            },
            "parentId": "5909",
            "inherit": [

            ],
            "nodeDesc": colum_dec,
            "nodeName1": colum_name,
            "nodeName": colum_name,
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

    def add_sy_colums(self, column_names, column_descs):
        
        url = 'http://onecategory.apps01.ali-bj-sit03.shuheo.net/onecategory/glossary/node/add'
        # 获取当前系统时间
        current_time = datetime.now()
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
        p_u = "71e8b23d-45e2-497a-b247-f5b807fb4f65"
        shuyu_nodeid = "5909"
        biaozhun_nodeid = "5907"
        for name, desc in zip(column_names, column_descs):
            # 定义你的JSON请求体数据（在每次循环中动态更新）
            data1 = {
                "tabs": "info",
                "treeType": 3,
                "nodeType": "TERM",
                "properties": {
                    "manageAttributes": {
                        "dataSecurityLevel": "L1",
                        "securityLevel": "外部公开"
                    },
                    "businessAttributes": {
                        "termEnIndex": name
                    }
                },
                "parentId": shuyu_nodeid,
                "inherit": [],
                "nodeDesc": desc,
                "nodeName1": name,
                "nodeName": name,
                "p_u": p_u
            }
            data2 = {
                "tabs": "info",
                "treeType": 1,
                "nodeType": "TERM",
                "properties": {
                    "manageAttributes": {
                        "dataSecurityLevel": "L1",
                        "securityLevel": "外部公开",
                        "expiredAt": formatted_time,
                        "standardStatus": 1,
                        "standardVersion": "v1.0.0"
                    },
                    "businessAttributes": {
                        "dataType": "文本类"
                    }
                },
                "parentId": biaozhun_nodeid,
                "inherit": [],
                "nodeName1": desc,
                "nodeDesc": desc,
                "nodeName": name,
                "p_u": p_u
            }
            self.send_post_request(url, data1)
            self.send_post_request(url, data2)

    def send_post_request(self, url, data):
        # 将数据转换为json格式
        payload_json = json.dumps(data)
        # 设置headers，一般情况下，当请求体是JSON时，需要设置Content-Type为application/json
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=payload_json, headers=headers)


my_class = MyClass()

my_class.add_table()
# my_class.add_colum()
#column_names = ['energy', 'protein', 'fat']
#ijh8 = ['能量', '蛋白质', '脂肪']
#my_class.add_sy_colums(column_names, column_descs)

