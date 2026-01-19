import pymysql
import requests
import json


# !/user/bin/env pytho
# -*- coding:utf-8 -*-
# connect2mysql
    conn = pymysql.connect(host='bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
                           port=3306,
                           user='bdsit_user_0e0bc33',
                           password='bdsit_user_0e0bc33_26587a',
                           db='dataops',
                           charset='utf8')
    cursor = conn.cursor()
    sql_list =[ "select concat_ws('_', cluster_name, topic) from dataops_extract_input_datasource_config_info
    where  id = 873])
    cursor2.execute(sql2)
    res2= cursor2.fetchall()
    print(res2)

def del_tb():




    cursor1.execute("delete\n"
                   "a,b,c,d\n"
                   "from\n"
                   "dataops_extract_input_datasource_config_info as a\n"
                   "INNER JOIN\n"
                   "dataops_extract_node_config_info as b\n"
                   "INNER JOIN\n"
                   "dataops_process_instance_info as c\n"
                   "INNER JOIN\n"
                   "dataops_lake_job_info as d\n"
                   "on  \n"
                   "a.id = b.extract_input_datasource_config_id\n"
                   "and b.id=c.process_business_id\n"
                   "and c.id=d.task_id\n"
                   "where a.id=813 ")
    results = cursor1.fetchall()
    conn.commit()
    cursor1.close()
    conn.close()
    return results



def dropTable():

    url_params = {'table': 'dp_ext_hudi_test_sls_newbro_user_behavior'}
    r1 = requests.get(url='http://lakeservice.apps01.ali-bj-sit03.shuheo.net/lakeservice/table/drop',
                      params=url_params)  # 带参数的get请求
    print(r1.content)
    return r1


def del_task():
    url_params = {'jobName': 'dp_ext_hudi_test_sls_newbro_user_behavior'}
    r2 = requests.get(url='http://lakeservice.apps01.ali-bj-sit03.shuheo.net/lakeservice/lake_job/clean',
                      params=url_params)  # 带参数的get请求
    print(r2.content)
    return r2


if __name__ == '__main__':
    del_tb()
    dropTable()
    del_task()
