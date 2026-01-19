import uuid


def generate_insert_sql(table_name, count, val_column1, val_column2):
    # 生成指定数量的UUID
    uids = [str(uuid.uuid4()) for _ in range(count)]

    # 构建SQL插入语句的每一部分
    values_clauses = []
    for uid in uids:
        values_clauses.append(f"('{uid}', '{val_column1}', '{val_column2}')")

    # 拼接完整的SQL插入语句，表名作为参数传入
    insert_statement = f"INSERT INTO {table_name} (uid, val_column1, val_column2) VALUES {', '.join(values_clauses)};"

    return insert_statement


# 设置参数
dp_space_name ="ads_tmp_usrgrp_sit" #一次性客群的dp表项目名称
table_name = dp_space_name+"."+"stjtest一次性客群表"

count = 10
val_column1 = "1"
val_column2 = "上海"

# 生成并打印SQL插入脚本
sql_script = generate_insert_sql(table_name, count, val_column1, val_column2)
print(sql_script)