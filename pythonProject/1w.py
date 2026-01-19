import uuid
import csv
# 定义输出文件名
filename = "output500wnew.csv"

# 创建csv writer对象
with open(filename, 'w', newline='') as csvfile:
    fieldnames = ['uid', 'key']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 生成并写入1万条UUID记录
    for _ in range(5000000):
        row = {'uid': str(uuid.uuid4()), 'key': 1}
        writer.writerow(row)