import pymysql
import random
import string
from datetime import datetime
import json

config = {
    'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
    'user': 'bdsit_user_datagovernor',
    'password': 'bdsit_user_datagovernor_26587a',
    'database': 'datagovernor',
    'charset': 'utf8mb4'
}


def generate_random_email():
    prefix_length = random.randint(4, 12)
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=prefix_length))
    return f'{prefix}@128.com'[:20]


def generate_random_password():
    chars = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choices(chars, k=random.randint(8, 16)))


def generate_json_content():
    return {
        f"key{random.randint(1, 100)}": {
            "subkey": ''.join(random.choices(string.ascii_lowercase, k=5)),
            "value": random.randint(1, 1000)
        }
    }


def main():
    connection = None  # 初始化connection变量
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        insert_data = []
        for _ in range(15):
            email = generate_random_email()
            password = generate_random_password()
            json_content = generate_json_content()

            insert_data.append((
                email,
                json.dumps(json_content),
                password,
                'feihu3',
                'feihu',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'hello',
                f'add{random.randint(1, 99)}',
                'hello'
            ))

        sql = """
        INSERT INTO datagovernor_small_data_test_forysss 
        (email, content, password, created_by, updated_by, created_at, updated_at, GIBGI, test_ky99,ext_1)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.executemany(sql, insert_data)
        connection.commit()
        print(f"成功插入{cursor.rowcount}条数据")

    except Exception as e:
        print(f"操作失败：{str(e)}")
        if connection:  # 确保connection存在时才回滚
            connection.rollback()
    finally:
        if connection and connection.open:  # 双重验证
            connection.close()
            print("数据库连接已关闭")


if __name__ == "__main__":
    main()