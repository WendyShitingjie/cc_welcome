import requests
import json


def send_rabbitmq_11s():
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 构建请求参数
    payload = {
        "isAdmin": True,
        "sendType": "Queue",
        "msgList": [
            {
                "payload": json.dumps(

                    {
                        "orderNo": "RCPLXZRW-202600000029",
                        "status": "STATUS_REJECTED",
                        "processInstId": "67b85e3e-4b18-4a3d-8cda-629a580fa4ee",
                        "dataMap": "{\"fileName\":\"批量新增任务_测试模板1条.xlsx\",\"sceneType\":\"jdbcInputBatchAddTask\",\"createdBy\":\"施婷杰\",\"batchTaskId\":385,\"scOwnerUid\":\"6260e238-93c5-4324-8d0f-e3ba17659a14\",\"taskId\":385,\"recordCnt\":1,\"scene\":\"jdbcInputBatchAddTask\"}",
                        "operatorUid": "6260e238-93c5-4324-8d0f-e3ba17659a14",
                        "operator": "陈沈伟",
                        "startName": "施婷杰"



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
