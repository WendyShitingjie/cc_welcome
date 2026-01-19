import requests
import json


def send_rabbitmq_after_publish_success(orderNo, taskId, instanceName, dbName, tableName):
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建请求参数
    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        "msgList": [
            {
                "payload": json.dumps({
                    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                    "orderNo": orderNo,
                    "issue": f"【{orderNo}】施婷杰2024-11-18发起的【离线抽数任务删除申请工单】流程",
                    "dataMap": json.dumps({
                        "instanceName": instanceName,
                        "etlxFields": "已经完善元数据",
                        "schedulerRate": "日",
                        "dbName": dbName,
                        "requirement": "自动化测试需求目的",
                        "applicant": "施婷杰",
                        "tableName": tableName,
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
                })
            }
        ],
        "queue": "dataops.queue.receiveDataLakeDataSourceFlow",
        "reason": "测测测",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)


if __name__ == "__main__":
    orderNo = ""  # 替换为实际的instanceId
    taskId = "1215"
    instanceName = "cjjcommon"
    dbName = "dataops_shitingjie"
    tableName = "stj_auto_api_test_only_complete"
    send_rabbitmq_after_publish_success(orderNo, taskId, instanceName, dbName, tableName)
