import requests
import json

def mq_sender_diagnostic_skill(payload_data, queue, exchange, routing_key):
    url = "http://mqplus.apps01.ali-bj-sit03.shuheo.net/mqplus/amqp/v2/sendMsg"

    # 尝试三种常见的 mqplus 参数组合
    configs = [
        # 组合 1: 尝试增加 virtualHost (通常是业务域名称)
        {
            "isAdmin": True,
            "sendType": "Queue",
            "queue": queue,
            "virtualHost": "dataops",  # 尝试根据 context 填入 vhost
            "msgList": [{"payload": json.dumps(payload_data, ensure_ascii=False)}],
            "reason": "Diagnostic: With VHost"
        },
        # 组合 2: 完全模仿你之前成功的 oneservice 结构，只换 queue 名
        {
            "isAdmin": True,
            "sendType": "Queue",
            "queue": queue,
            "msgList": [{"payload": json.dumps(payload_data, ensure_ascii=False)}],
            "reason": "Diagnostic: Pure Queue Mode"
        },
        # 组合 3: 尝试 Exchange + RoutingKey (最匹配日志的形式)
        {
            "isAdmin": True,
            "sendType": "Exchange",
            "exchange": exchange,
            "routingKey": routing_key,
            "virtualHost": "dataops",
            "msgList": [{"payload": json.dumps(payload_data, ensure_ascii=False)}],
            "reason": "Diagnostic: Exchange Mode"
        }
    ]

    for i, payload in enumerate(configs):
        print(f"\n--- 正在尝试配置方案 {i+1} ---")
        try:
            response = requests.post(url, json=payload, timeout=5)
            print(f"请求内容概要: sendType={payload['sendType']}, target={payload.get('queue') or payload.get('exchange')}")
            print(f"响应结果: {response.text}")
            if response.status_code == 200:
                print("恭喜！方案", i+1, "发送成功！")
                break
        except Exception as e:
            print(f"请求失败: {e}")

# --- 执行诊断 ---
if __name__ == "__main__":
    my_data = {
        "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
        "orderNo": "RCPLXZRW-202600000022",
        "issue": "【RCPLXZRW-202600000022】施婷杰发起的数据研发平台【JDBC入仓批量新增任务】审核工单",
        "dataMap": "{\"fileName\":\"批量新增任务_测试模板1条.xlsx\",\"sceneType\":\"jdbcInputBatchAddTask\",\"createdBy\":\"施婷杰\",\"batchTaskId\":376,\"scOwnerUid\":\"6260e238-93c5-4324-8d0f-e3ba17659a14\",\"taskId\":376,\"recordCnt\":1,\"scene\":\"批量新增任务\"}",
        "processInstId": "2f41787e-9148-41a2-a9ec-c3174c625e32",
        "orderInfos": "[{\"label\":\"任务ID\",\"value\":\"376\",\"key\":\"taskId\"},{\"label\":\"创建人\",\"value\":\"施婷杰\",\"key\":\"createdBy\"}]",
        "operatorUid": "6260e238-93c5-4324-8d0f-e3ba17659a14",
        "operator": "陈沈伟",
        "status": "STATUS_APPROVED"
    }

    mq_sender_diagnostic_skill(
        payload_data=my_data,
        queue="dataops.queue.receiveBatchOperationFlow",
        exchange="flowplus.exchange.workOrder2",
        routing_key="bg_jdbc_rc_plxz_rw.STATUS_APPROVED"
    )