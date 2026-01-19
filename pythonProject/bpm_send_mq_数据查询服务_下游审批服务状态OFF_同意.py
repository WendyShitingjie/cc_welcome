import requests
import json

def send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId,propertyId):
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建请求参数
    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        "msgList": [
            {
                "payload": json.dumps({  # 使用json.dumps转换为字符串
                    "processInstId": bpmId,
                    "orderNo": orderNo,
                    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                    "startName": "施婷杰",
                    "status": "STATUS_APPROVED",
                    "dataMap": json.dumps({
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
                        ],
                        "apiProperties ": {
                            "serviceStatus ": 0,
                            "id ": propertyId
                        }
                    })
                })
            }
        ],
        "queue": "oneservice.queue.bpmMsg",
        "reason": "测试设置服务状态OFF，下游应用审批通过",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)
    print(f"响应状态: {response.status_code}, 返回内容: {response.text}")  # 添加日志输出


if __name__ == "__main__":
    orderNo = "APIFB-202500000113"
    apiId = "555"
    bpmId = "c22bbd4b-a12e-4815-aa97-90055ef6d0be"
    propertyId = "212"  #根据api_property_info 根据apiid查询出id
    send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId, propertyId)