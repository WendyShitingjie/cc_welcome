import pika
import json

# RabbitMQ 连接参数
rabbitmq_host = 'localhost'  # 替换为你的 RabbitMQ 服务器地址
rabbitmq_port = 5672         # 默认端口
rabbitmq_user = 'guest'      # 默认用户名
rabbitmq_password = 'guest'  # 默认密码
queue_name = 'dataops.queue.receiveDataLakeDataSourceFlow'  # 替换为你实际使用的队列名称

# 创建连接
credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbitmq_host,
    port=rabbitmq_port,
    credentials=credentials
))
channel = connection.channel()

# 声明队列（如果队列不存在，则创建）
channel.queue_declare(queue=queue_name, durable=True)

# 构造消息内容
message = {
    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
    "orderNo": "CSRE-202400000423",
    "taskid": 1214
}

# 将消息转换为 JSON 字符串
message_json = json.dumps(message)

# 发送消息到队列
channel.basic_publish(
    exchange='',
    routing_key=queue_name,
    body= message_json,
    properties=pika.BasicProperties(
        delivery_mode=2,  # 消息持久化
    )
)

print(f" [x] Sent message: {message_json}")

# 关闭连接
connection.close()

