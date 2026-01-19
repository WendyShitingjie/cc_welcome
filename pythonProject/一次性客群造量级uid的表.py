import uuid
count = 5000001
# 生成100个标准格式的UUID作为uid
uids = [str(uuid.uuid4()) for _ in range(count)]

# 构建一次性插入多条记录的SQL语句，保持uid的原有格式
placeholders = ', '.join([f"('{uid}', 1)" for uid in uids])
insert_statement = f"INSERT INTO my_table (uid, val) VALUES {placeholders};"

print(insert_statement)



