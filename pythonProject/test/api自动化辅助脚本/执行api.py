import requests
import json


def exc_api(orderNo=None, taskId=None):
    # 消息内容
    message = {
        "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
        "orderNo": orderNo,
        "issue": f"{orderNo}+'施婷杰2024-11-18发起的【离线抽数任务删除申请工单】流程'",
        "dataMap": json.dumps({
            "instanceName": "cjjcommon",
            "etlxFields": "已经完善元数据",
            "schedulerRate": "日",
            "dbName": "dataops_shitingjie",
            "requirement": "自动化测试需求目的",
            "applicant": "施婷杰",
            "tableName": "stj_auto_api_test_only_complete",
            "scene": "delTaskAfterPublishSuccess",
            "userJourney": "T00000006",
            "schedulerTime": "03:34",
            "techOwner": "施婷杰",
            "dataLakeConfig": f"http://moka.dmz.sit.caijj.net/analytoolui/#/edit-task?id={taskId}",
            "metaDataPath": "http://moka.dmz.sit.caijj.net/midwareui/#/mysql-metadata",
            "businessOwner": "施婷杰",
            "dataSource": "input_mysql_cjjcommon_dataops_shitingjie",
            "dataSourceType": "mysql",
            "isMetaDataPerfect": True
        }),
        "activityName": "数仓负责人审核",
        "activityDefId": "obj_caee368ae7a00001451ae500a8c012a7",
        "operator": "何胜",
        "startName": "施婷杰",
        "status": "STATUS_APPROVED"
    }

    # 目标URL
    url = "http://example.com/api/receive_message"  # 请替换为实际的URL

    # 发送POST请求
    try:
        response = requests.post(url, json=message)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        print("消息发送成功")
        print("响应内容:", response.json())  # 打印响应内容
    except requests.exceptions.RequestException as e:
        print(f"消息发送失败: {e}")


# 示例调用
del_message_trigger(orderNo="CSRE-202400000423", taskId="12345")
```