import requests
import json


def send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId, status):
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
                    "dataMap": json.dumps({
                        "apiName": "STJ自动化测试-DP-应用授权和解绑",
                        "systemUserId": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                        "appInfo": {
                            "applyTags": ["自动化测试新增"],
                            "entityCode": "",
                            "appName": "对外提供数仓数据服务的api的配置模块",
                            "appQPS": 10,
                            "appOwner": "周泽锋",
                            "appCode": "oneservicemanager",
                            "id": 140,
                            "appOwnerId": "0b7cd05f-d01a-41f3-8fa1-a3bd773d96ab",
                            "applyDesc": "自动化测试申请应用授权"
                        },
                        "opType": "appApply",
                        "apiDesc": "勿动",
                        "opUserId": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                        "exeInfo": {
                            "exeSql": "selectn  code,n  cardno,n  mobilenfromn  dwa_risk_sit.dwd_risk_sensitivestj_df  nwheren  ds = #{ds}"
                            },
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
                        "safeLevel": "L4",
                        "apiId": apiId
                    }),
                    "processInstId": bpmId,
                    "operatorUid": "94c6a832-8cef-491f-9e5d-239a716b7275",
                    "operator": "张培凡",
                    "startName": "施婷杰",
                    "status": status
                })
            }
        ],
        "queue": "oneservice.queue.bpmMsg",
        "reason": "测试应用授权，下游应用审批通过",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)
    print(f"响应状态: {response.status_code}, 返回内容: {response.text}")  # 添加日志输出


if __name__ == "__main__":
    orderNo = "XYYYSQ-202500000091"
    apiId = "571"
    bpmId = "f3e6b984-99a6-4056-a775-5e4943def892"
    status = "STATUS_APPROVED"
    send_rabbitmq_after_off_service_status(orderNo, apiId, bpmId, status)
