import requests
import json


def send_rabbitmq_11s():
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建请求参数
    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        #"sendType": "Exchange",  # ⬅️ 改为 Exchange
        #"exchange": "flowplus.exchange.workOrder2",  # ⬅️ 指定 Exchange
        #"routingKey": "bg_jdbc_rc_plxz_rw.approval.completed",  # ⬅️ 指定 Routing Key
        "msgList": [
            {
                "payload": json.dumps(
                    {
                        "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                        "orderNo": "RCPLXZRW-202600000025",
                        #"issue": "【RCPLXZRW-202600000025】施婷杰发起的数据研发平台【JDBC入仓批量新增任务】审核工单",
                        "dataMap": "{\"fileName\":\"批量新增任务_测试模板1条.xlsx\",\"sceneType\":\"jdbcInputBatchAddTask\",\"createdBy\":\"施婷杰\",\"batchTaskId\":381,\"scOwnerUid\":\"6260e238-93c5-4324-8d0f-e3ba17659a14\",\"taskId\":381,\"recordCnt\":1,\"scene\":\"批量新增任务\"}",
                        "processInstId": "9e83d95a-58dd-4e89-9a0e-abade9f41c5f",
                        #"processKey": "bg_jdbc_rc_plxz_rw",  # 添加 processKey
                        #"orderInfos": "[{\"label\":\"任务ID\",\"value\":\"379\",\"key\":\"taskId\"},{\"label\":\"创建人\",\"value\":\"施婷杰\",\"key\":\"createdBy\"}]",
                        "operatorUid": "6260e238-93c5-4324-8d0f-e3ba17659a14",
                        "operator": "陈沈伟",
                        "startName": "施婷杰",
                        "status": "STATUS_APPROVED"
                 }

                )
            }
        ],
        "queue": "dataops.queue.receiveBatchOperationFlow",
        "clusterName": "amqp-cn-4591j61c6009",
        "reason": "测试mq消息",
        "message": "消息发送成功"
    }

    # 发送POST请求
    response = requests.post(url, json=payload)
    print(f"响应状态: {response.status_code}, 返回内容: {response.text}")  # 添加日志输出


if __name__ == "__main__":

    send_rabbitmq_11s()
