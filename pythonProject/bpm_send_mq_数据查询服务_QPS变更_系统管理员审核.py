import requests
import json


def send_rabbitmq_appbiz_qps_bpm_status(orderNo, apiId, bpmId, status):
    """
    函数功能描述...
    :param param_a: 参数描述...
    :param param_b: 参数描述...
    :param param_c: 参数描述...
    :return: 返回描述...
    """
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
                    "issue": f"【{orderNo}】施婷杰 2025-11-12 16:04 发起的【数据查询服务API-{apiId} 】接入流程",
                    "dataMap": json.dumps(
                        {
                            "apiName": "STJ自动化测试-DP-应用限流",
                            "needManager": "true",
                            "appInfos": {

                            },
                            "systemUserId": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                            "opType": "appManager",
                            "apiDesc": "勿动",
                            "diffPropertiesInfos": [
                                {
                                    "newValue": 20,
                                    "code": "qps",
                                    "noticeTypes": [
                                        1
                                    ],
                                    "name": "QPS阈值",
                                    "value": 10
                                }
                            ],
                            "opUserId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                            "version": 1,
                            "apiOwnerId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                            "apiOwner": "施婷杰",
                            "opUser": "施婷杰",
                            "sourceInfo": {
                                "sourceUrl": "http://dp.caijj.net/ops/instanceOps/cycleInstance?env=PROD&projectId=6706096317312448&tab=script&tenantId=300005953",
                                "sourceCode": "datasparrow",
                                "instanceName": "dataphin",
                                "sourceType": "dataphin",
                                "sourceName": "dataphin测试数据源"
                            },
                            "appOwnerIds": "",
                            "publishType": 2,
                            "safeLevel": "L4",
                            "appId": 140,
                            "appApiApplyInfo": {
                                "updatedBy": "施婷杰",
                                "sceneTags": "8",
                                "userAuth": 0,
                                "appId": 140,
                                "bizQps": 20,
                                "id": 125,
                                "apiId": apiId,
                                "applyDesc": "1"
                            },
                            "publishDec": "API 属性变更：QPS阈值",
                            "notifyUserIds": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                            "apiId": apiId,
                            "diffProperties": {
                                "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab": [
                                    {
                                        "newValue": 20,
                                        "code": "qps",
                                        "noticeTypes": [
                                            1
                                        ],
                                        "name": "QPS阈值",
                                        "value": 10
                                    }
                                ]
                            }
                        }
                    ),
                    "processInstId": bpmId,
                    "operatorUid": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                    "operator": "周泽锋",
                    "startName": "施婷杰",
                    "status": status
                })
            }
        ],
        "queue": "oneservice.queue.bpmMsg",
        "reason": "API 属性变更：应用QPS变动，系统管理员审批通过",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)
    print(f"响应状态: {response.status_code}, 返回内容: {response.text}")  # 添加日志输出


if __name__ == "__main__":
    orderNo = "APIFB-202500000138"
    apiId = "570"
    bpmId = "89c8a521-0b6b-4307-b56b-c2294bbe1f5c"
    status = "STATUS_APPROVED"
    send_rabbitmq_setProperty_bpm_status(orderNo, apiId, bpmId, status)
