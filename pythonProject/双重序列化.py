import requests
import json
import uuid


def send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId):
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建带类型声明的 payload
    payload_data = {
        "__type": "application/json",
        "__value": {
            "processInstId": bpmId,
            "orderNo": orderNo,
            "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
            "startName": "施婷杰",
            "status": "STATUS_APPROVED",
            "dataMap": {
                "opType": "setProperty",
                "opUserId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                "opUser": "施婷杰",
                "publishType": 2,
                "apiId": apiId,
                "diffPropertiesInfos": [
                    {
                        "newValue": "关闭",
                        "code": "serviceStatus",
                        "noticeTypes": [0],
                        "name": "服务状态",
                        "value": "开启"
                    }
                ]
            }
        }
    }

    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        "msgList": [{
            "payload": json.dumps(payload_data),  # 双重序列化
            "messageId": str(uuid.uuid4())  # 添加唯一ID
        }],
        "queue": "oneservice.queue.bpmMsg",
        "reason": "测试设置服务状态OFF，下游应用审批通过",
        "message": "消息发送成功"
    }

    headers = {"Content-Type": "application/json"}
    response = requests.post(url, json=payload, headers=headers)

    print("=== 请求详情 ===")
    print(f"URL: {url}")
    print(f"状态码: {response.status_code}")
    print(f"响应内容: {response.text}")
    print("===============")

    return response


if __name__ == "__main__":
    send_rabbitmq_after_off_service_status(
        orderNo="APIFB-202500000113",
        apiId="555",
        bpmId="c22bbd4b-a12e-4815-aa97-90055ef6d0be"
    )