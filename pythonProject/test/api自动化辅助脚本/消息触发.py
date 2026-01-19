import json
from kafka import KafkaConsumer
import requests

# 配置Kafka消费者
kafka_bootstrap_servers = 'localhost:9092'  # 替换为你的Kafka服务器地址
kafka_topic = 'flowplus.exchange.workOrder2'  # 替换为你的Kafka主题

# 配置/delete接口的URL
delete_url = 'http://dataops.apps01.ali-bj-sit03.shuheo.net/dataops/etlx/delete'  # 替换为实际的URL

# 创建Kafka消费者
consumer = KafkaConsumer(
    kafka_topic,
    bootstrap_servers=kafka_bootstrap_servers,
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

def delete_data(message):
    # 提取消息内容
    start_uid = message.get('startUid')
    order_no = message.get('orderNo')
    task_id = message.get('taskid')

    # 构建请求参数
    payload = {
        "startUid": start_uid,
        "orderNo": order_no,
        "taskId": task_id
    }

    # 发送DELETE请求
    try:
        response = requests.delete(delete_url, json=payload)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出异常
        print(f"数据删除成功: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"数据删除失败: {e}")

# 消费Kafka消息
for message in consumer:
    print(f"接收到的消息: {message.value}")
    delete_data(message.value)
```
