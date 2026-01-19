import json
import random

import pymysql
import requests

"""
        for row in results:
            # print(row)
            # 打印出来字符串 客群ID: 635, 客群key: clc_usr_grp_635, 客群中文名:sl回归测试0803
            # print(f"客群ID: {row[0]}, 客群key: {row[1]}, 客群中文名:{row[2]}")
            # 打印出每个列，空格间隔：635 clc_usr_grp_635 sl回归测试0803
            print(row)
"""


class MyClass:

    def __init__(self):
        self.my_class = None

    def output_valid_kequn(self):
        conn = pymysql.connect(host='cjjarch.db.ali-bj-sit01.shuheo.net',
                               port=3306,
                               user='featurehub',
                               password='lohSh6Ya',
                               db='featurehub',
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute("""select id,name,chinese_name,status,user_group_type,available_day,check_pass_time
        from user_group ugr
        where (status="APPROVED" and check_pass_time+INTERVAL available_day DAY >= NOW())
        or (check_pass_time is null and available_day is null and status="APPROVED")  limit 5""")
        conn.commit()
        cursor.close()
        conn.close()
        results = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        # 将查询结果转化为列表的字典形式
        results_list = []
        for row in results:
            result_dict = {column_name: value for column_name, value in zip(column_names, row)}
            results_list.append(result_dict)
        # 将列表的字典形式转化为JSON字符串
        json_string = json.dumps(results_list)
        print(json_string)
        print("筛选出所有有效客群")
        return json_string


my_class = MyClass()
my_class.output_valid_kequn()
