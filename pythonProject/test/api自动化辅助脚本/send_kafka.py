from kafka import KafkaProducer
import json

# Kafka broker地址
bootstrap_servers = ['172.20.143.170:9092', '172.20.143.169:9092', '172.20.143.171:9092']

# Kafka主题
topic_name = 'flowplus.exchange.workOrder2'

# 要发送的消息内容
message_data = {
    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
    "orderNo": "CSRE-202400000423",
    "issue": "【CSRE-202400000423】施婷杰2024-11-18发起的【离线抽数任务删除申请工单】流程",
    "dataMap": "{\"instanceName\":\"cjjcommon\",\"etlxFields\":\"已经完善元数据\",\"schedulerRate\":\"日\",\"dbName\":\"dataops_shitingjie\",\"requirement\":\"自动化测试需求目的\",\"applicant\":\"施婷杰\",\"tableName\":\"stj_auto_api_test_only_complete\",\"scene\":\"delTaskAfterPublishSuccess\",\"userJourney\":\"T00000006\",\"schedulerTime\":\"03:34\",\"techOwner\":\"施婷杰\",\"dataLakeConfig\":\"http://moka.dmz.sit.caijj.net/analytoolui/#/edit-task?id=1211\",\"metaDataPath\":\"http://moka.dmz.sit.caijj.net/midwareui/#/mysql-metadata\",\"businessOwner\":\"施婷杰\",\"dataSource\":\"input_mysql_cjjcommon_dataops_shitingjie\",\"dataSourceType\":\"mysql\",\"isMetaDataPerfect\":true}",
    "activityName": "数仓负责人审核",
    "activityDefId": "obj_caee368ae7a00001451ae500a8c012a7",
    "operator": "何胜",
    "startName": "施婷杰",
    "status": "STATUS_APPROVING"
}

# 将消息内容序列化为JSON字符串
message_json = json.dumps(message_data)

# 创建Kafka生产者
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: x.encode('utf-8')  # 将消息内容编码为UTF-8字节串
)

# 发送消息到Kafka主题
producer.send(topic_name, message_json)

# 关闭生产者以释放资源
producer.close()

print(f"Message sent to {topic_name}: {message_json}")