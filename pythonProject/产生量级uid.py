import uuid
import random

# 定义数据总量
data_amount = 10

# 初始化数据列表
data_list = []

# 生成数据
for _ in range(data_amount):
    # 生成32位UUID（实际是去掉"-")，然后格式化为"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    formatted_uuid = str(uuid.uuid4()).replace('-', '')

    # 假设第二个字段是随机整数，可以根据需求修改这部分逻辑
    second_field = random.randint(0, 10000)

    # 构造每一条数据
    data_entry = (formatted_uuid, second_field)
    data_list.append(data_entry)

# 打印或保存数据
for entry in data_list:
    print(f'("{entry[0]}", "{entry[1]}"),')  # 以逗号分隔的形式打印，方便插入数据库等操作


