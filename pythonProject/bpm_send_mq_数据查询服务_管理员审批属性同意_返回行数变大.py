import requests
import json


def send_rabbitmq_setProperty_bpm_status(orderNo, apiId, bpmId, status):
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
                            "apiName": "STJ自动化测试-SR- 属性变更（有下游应用）",
                            "needManager": "true",
                            "appInfos": {

                            },
                            "systemUserId": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                            "apiProperties": {
                                "limitSize": 900,
                                "id": 232,
                                "apiId": apiId
                            },
                            "opType": "setProperty",
                            "apiDesc": "勿动-自动化测试专用-edit",
                            "diffPropertiesInfos": [
                                {
                                    "newValue": 900,
                                    "code": "limitSize",
                                    "noticeTypes": [
                                        1
                                    ],
                                    "name": "返回行数限制",
                                    "value": 500
                                }
                            ],
                            "opUserId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                            "version": 1,
                            "apiOwnerId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                            "apiOwner": "施婷杰",
                            "opUser": "施婷杰",
                            "sourceInfo": {
                                "sourceUrl": "https://emr-next.console.aliyun.com/?spm=5176.21192661.0.0.36501812ZgB4XU#/region/cn-beijing/resource/all/serverless/starrocks/overview",
                                "sourceCode": "hydra_test_sr_bak",
                                "instanceName": "bd-starrocks-sit-backup",
                                "sourceType": "starrocks",
                                "sourceName": "hydra测试数据源（备选）"
                            },
                            "appOwnerIds": " ",
                            "publishType": 2,
                            "safeLevel": "L2",
                            "publishDec": "API 属性变更：返回行数限制",
                            "notifyUserIds": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                            "apiId": apiId,
                            "diffProperties": {
                                "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab": [
                                    {
                                        "newValue": 900,
                                        "code": "limitSize",
                                        "noticeTypes": [1],
                                        "name": "返回行数限制",
                                        "value": 500
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
        "reason": "API 属性变更：返回行数限制，系统管理员审批通过",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)
    print(f"响应状态: {response.status_code}, 返回内容: {response.text}")  # 添加日志输出


if __name__ == "__main__":
    orderNo = "APIFB-202500000120"
    apiId = "575"
    bpmId = "3b1f47d0-9d81-47f6-9aa5-4a2896a34127"
    status = "STATUS_APPROVED"
    send_rabbitmq_setProperty_bpm_status(orderNo, apiId, bpmId, status)
