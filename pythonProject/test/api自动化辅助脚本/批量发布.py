# 表名
table_name = "stj_large_amount_keys"

# 字段列表
fields = [
    "id INT AUTO_INCREMENT PRIMARY KEY COMMENT '主键'",
    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'",
    "updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'",
    "created_by VARCHAR(20) DEFAULT NULL COMMENT '创建人'",
    "updated_by VARCHAR(20) DEFAULT NULL COMMENT '更新人'"
]

# 添加150个字段
for i in range(1, 151):
    fields.append(f"field{i} VARCHAR(20) DEFAULT NULL COMMENT '字段{i}的描述'")

# 生成DDL语句
ddl_statement = f"CREATE TABLE {table_name} (\n"
ddl_statement += ",\n".join(fields)
ddl_statement += "\n);"

# 输出DDL语句
print(ddl_statement)