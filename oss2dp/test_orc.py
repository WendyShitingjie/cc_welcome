import pyarrow as pa
import pyarrow.orc as orc
from datetime import datetime

# 定义标准测试Schema
schema = pa.schema([
    ('user_id', pa.int32()),        # 整型字段
    ('user_name', pa.string()),     # 字符串字段
    ('account_balance', pa.float64()),  # 浮点数字段
    ('last_login', pa.timestamp('ms')), # 时间戳字段
    ('is_active', pa.bool_())       # 布尔字段
])

# 生成测试数据（包含空值和边界值）
data = [
    (1001, "张三", 1500.50, datetime(2024, 3, 15, 14, 30), True),
    (1002, "李四_Test", None, datetime(2024, 2, 29, 23, 59), False),  # 空值测试
    (1003, "特殊@字符#测试", 999999.99, None, True),  # 空时间戳测试
    (1004, "", -500.0, datetime(1970, 1, 1), False)  # 空字符串和最小值测试
]

# 构建Arrow Table
table = pa.Table.from_arrays(
    [
        pa.array([x[0] for x in data]),
        pa.array([x[1] for x in data]),
        pa.array([x[2] for x in data]),
        pa.array([x[3] for x in data]),
        pa.array([x[4] for x in data])
    ],
    schema=schema
)

# 写入ORC文件（添加压缩）
orc.write_table(table, 'simple_test.orc', compression='SNAPPY')

