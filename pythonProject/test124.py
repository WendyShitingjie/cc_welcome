import requests
import json
import uuid


def send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId, propertyId):
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建消息体
    message_body = {
        "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
        "orderNo": orderNo,
        "issue": f"【{orderNo}】施婷杰 2025-11-11 14:21 发起的【数据查询服务API-{apiId}】变更流程",
        "dataMap": json.dumps({
            "apiName": "STJ自动化测试-DP-有下游应用",
            "needManager": False,
            "appInfos": {
                "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab": [
                    {
                        "applyTags": ["自动化测试场景"],
                        "entityCode": " ",
                        "appName": "对外提供数仓数据服务的api的配置模块",
                        "appQPS": 10,
                        "appOwner": "周泽锋",
                        "appCode": "oneservicemanager",
                        "appOwnerId": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                        "applyDesc": "123"
                    }
                ]
            },
            "apiProperties": {
                "serviceStatus": 0,
                "id": propertyId
            },
            "opType": "setProperty",
            "apiDesc": "勿动",
            "diffPropertiesInfos": [
                {
                    "newValue": "关闭",
                    "code": "serviceStatus",
                    "noticeTypes": [0],
                    "name": "服务状态",
                    "value": "开启"
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
            "appOwnerIds": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
            "publishType": 2,
            "safeLevel": "L4",
            "publishDec": "API 属性变更：服务状态",
            "notifyUserIds": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
            "apiId": apiId,
            "diffProperties": {
                "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab": [
                    {
                        "newValue": "关闭",
                        "code": "serviceStatus",
                        "noticeTypes": [0],
                        "name": "服务状态",
                        "value": "开启"
                    }
                ]
            }
        }), # daytaMap是一个string，需要序列化
        "processInstId": bpmId,
        "operatorUid": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
        "operator": "周泽锋",
        "startName": "施婷杰",
        "status": "STATUS_APPROVED"
    }

    # 构建完整请求（外层和内层都需要序列化）
    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        "msgList": [
            {
                "payload": json.dumps(message_body),  # 仅此一处序列化
                "messageId": str(uuid.uuid4())  # 添加唯一ID
            }
        ],
        "queue": "oneservice.queue.bpmMsg",
        "reason": "测试设置服务状态OFF，下游应用审批通过",
        "message": "消息发送成功"
    }

    # 发送请求并打印详细日志
    print("=" * 50)
    print("发送消息到MQ服务...")
    print(f"目标URL: {url}")
    print(f"消息ID: {payload['msgList'][0]['messageId']}")

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

        print("\n响应状态:", response.status_code)
        print("响应内容:", response.text[:500])  # 显示前500字符

        if response.status_code == 200:
            print("消息发送成功")
        else:
            print(f"发送失败，状态码: {response.status_code}")

    except Exception as e:
        print(f"请求异常: {str(e)}")

    print("=" * 50)


if __name__ == "__main__":
    # 配置参数
    orderNo = "APIFB-202500000113"
    apiId = "555"
    bpmId = "c22bbd4b-a12e-4815-aa97-90055ef6d0be"
    propertyId = "212"  # 根据api_property_info查询出的id

    print("开始执行MQ消息发送...")
    send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId, propertyId)
    print("执行完成")