import pyorc

# 读取ORC文件基础示例
with open("testOrc.orc", "rb") as f:
    reader = pyorc.Reader(f)

    # 打印sch
    #
    # ema信息
    print("Schema:", reader.schema)

    # 提取字段列表
    columns = reader.schema.fields
    print("Columns:", [col.name for col in columns])

    # 逐行读取数据
    for row in reader:
        print(row)  # 输出元组格式数据

# 结合pandas使用（推荐方式）
import pandas as pd

with open("testOrc.orc.orc", "rb") as f:
    reader = pyorc.Reader(f)
    df = pd.DataFrame(reader)
    print(df.head())