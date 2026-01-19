import requests
import json
import random
import pymysql
from datetime import datetime


class MyClass:
    def __init__(self):
        self.my_class = None
        self.random_number = self.generate_random_number()

    def generate_random_number(self):
        return random.randint(10, 99)

    def __publish_kequn(self):
        url = 'http://ecube.apps01.ali-bj-sit03.shuheo.net/ecube/customer/journey/publish'
        with open('../data.json', 'r') as f:
            data = json.load(f)
        data['chineseName'] = "不校验特征_常规客群_API生成" + str(random.randint(1, 1000))
        data['name'] = "clc_usr_grp_bxy_tzc_gkq_ccd_qc" + str(random.randint(1, 1000))
        print("本次创建的客群名称: ", data['chineseName'])
        print("本次创建的客群key: ", data['name'])
        with open('../data.json', 'w') as f:
            json.dump(data, f)
        with open('../data.json', 'r') as f:
            data = json.load(f)
        data_json = json.dumps(data)
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=data_json)
        # print(response.text)
        # 解析response的json
        res_data = response.json()
        if res_data['code'] == 5001:
            print(res_data['data']['error'])
        elif res_data['code'] == 0:
            print("客群创建成功，客群ID：", res_data['data']['id'])
            # return res_data['data']['id']
        else:
            print("创建客群异常！")
        return res_data

    def __heYan(self):
        url = 'http://ecube.apps01.ali-bj-sit03.shuheo.net/ecube/check/complete'
        kequn_id = self.__publish_kequn()['data']['id']
        params = {
            "id": kequn_id,
            "p_u": "71e8b23d-45e2-497a-b247-f5b807fb4f65"
        }
        response = requests.get(url, params=params)
        res_data = response.json()
        # print(response.text)
        bpmNo = res_data['data']['orderNo']
        print("客群核验通过，生成BPM工单号: ", bpmNo)
        return bpmNo, kequn_id

    def bpm_approved(self):
        # 这两个值被封装成一个元组，然后被解包到变量`bpmNo`和`kequn_id`中。
        print("hello,tingjie")
        bpmNo, kequn_id = self.__heYan()
        conn = pymysql.connect(host='cjjarch.db.ali-bj-sit01.shuheo.net',
                               port=3306,
                               user='featurehub',
                               password='lohSh6Ya',
                               db='featurehub',
                               charset='utf8')
        cursor = conn.cursor()
        try:
            update_user_group = " update featurehub.user_group  SET status='APPROVED' where id='%s'" % kequn_id
            cursor.execute(update_user_group)
            update_bpm_status = ('''
                             update featurehub.user_group_flowplus_record 
                             SET status='STATUS_APPROVED'
                             where order_no='%s'
                             '''
                                 ) % bpmNo
            cursor.execute(update_bpm_status)
            conn.commit()
        except Exception as e:
            # 如果发生错误则回滚
            conn.rollback()
            print("Error: ", e)
        finally:
            # 关闭游标和连接
            cursor.close()
            conn.close()
            print("客群已生效！")

    def shiXiao(self):
        conn = pymysql.connect(host='cjjarch.db.ali-bj-sit01.shuheo.net',
                               port=3306,
                               user='featurehub',
                               password='lohSh6Ya',
                               db='featurehub',
                               charset='utf8')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO featurehub.ecube_identifier_update
        (identifier, insert_ck_time, created_at, updated_at, cluster)
        VALUES
        ('off_usr_iso_sex', now(), now(), now(), 'clickhouse-ha'),
        ('off_usr_iso_age', now(), now(), now(), 'clickhouse-ha'),
        ('clc_usr_reg_mob_new', now(), now(), now(), 'clickhouse-ha'),
        ('off_usr_reg_mob_new', now(), now(), now(), 'clickhouse-ha')""")
        conn.commit()
        cursor.close()
        conn.close()
        print("时效性校验已完成！")






my_class = MyClass()
# my_class.heYan()
# my_class.bpm_approved()
# msg = my_class.publish_kequn()
my_class.bpm_approved()
my_class.shiXiao()


# print(msg)
