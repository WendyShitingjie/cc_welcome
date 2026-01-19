import pymysql
import uuid
import random
import json
from datetime import datetime, timedelta

# 数据库配置
config = {
    'host': 'sitpublic.tidb.ali-bj-sit01.shuheo.net',
    'user': 'sit_user_64edae8',
    'password': 'sit_user_64edae8_68b2cb',
    'database': 'featurestore',
    'port': 4000,
    'charset': 'utf8mb4'
}


def generate_account_data(num_records=20):
    """生成符合实际业务场景的账户数据"""
    accounts = []
    business_types = ['ENJOY_PAY', 'LOAN_REPAYMENT', 'INVESTMENT', 'WITHDRAWAL', 'TRANSFER']
    channels = ['hbxzxzx', 'mobile_bank', 'web_portal', 'atm', 'branch']
    account_types = ['M', 'C', 'D', 'S', 'I']  # 根据样例中的account_type

    for _ in range(num_records):
        # 核心字段
        account_id = str(uuid.uuid4())  # 完整的UUID格式
        uid = str(uuid.uuid4())
        node_id = random.choice(['DEBIT_NODE', 'CREDIT_NODE']) + str(random.randint(1000, 9999))

        # 账户编号 - 符合样例格式
        year = random.randint(2019, 2025)
        month = str(random.randint(1, 12)).zfill(2)
        day = str(random.randint(1, 28)).zfill(2)
        account_no = f"{random.choice(['01', '02', '03'])}{year}{month}{day}{str(random.randint(1000, 9999)).zfill(4)}"

        # 时间字段 - 创建合理的时序关系
        created_at = datetime.now() - timedelta(days=random.randint(1, 365 * 3))
        activated_at = created_at + timedelta(minutes=random.randint(1, 60))
        expired_at = activated_at + timedelta(days=random.randint(180, 730)) if random.random() > 0.7 else None
        updated_at = activated_at + timedelta(days=random.randint(1, 1000))

        # 构建extra_info - 可能为NULL或JSON
        if random.random() > 0.3:
            extra_info = json.dumps({
                "institution": f"ORG{random.randint(100, 999)}",
                "product": f"P{random.randint(1000, 9999)}",
                "level": random.randint(1, 5)
            })
        else:
            extra_info = None

        accounts.append((
            account_id,  # account_id
            node_id,  # node_id
            random.choice(account_types),  # account_type
            uid,  # uid
            account_no,  # account_no
            str(random.randint(1, 100)).zfill(3),  # match_no (3位数字)
            random.choice(business_types),  # business_type
            random.choice(channels),  # channel
            'ACTIVE' if random.random() > 0.2 else 'INACTIVE',  # activated_status
            None,  # name (样例为NULL)
            None,  # short_name (样例为NULL)
            None,  # account_category (样例为NULL)
            None,  # canceled_at (样例为NULL)
            extra_info,  # extra_info
            activated_at,  # activated_at
            expired_at,  # expired_at
            random.randint(0, 10)  # version
        ))
    return accounts


def insert_accounts_batch():
    """向account表插入批次数据"""
    try:
        connection = pymysql.connect(**config)
        cursor = connection.cursor()

        # 生成10条记录
        accounts = generate_account_data(10)

        # 构建SQL（排除自增id和生成列）
        sql = """
        INSERT INTO account (
            account_id, node_id, account_type, uid, account_no, 
            match_no, business_type, channel, activated_status, 
            name, short_name, account_category, canceled_at, 
            extra_info, activated_at, expired_at, version
        ) VALUES (
            %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s, 
            %s, %s, %s, %s
        )
        """

        # 执行批量插入
        cursor.executemany(sql, accounts)
        connection.commit()
        print(f"✅ 成功插入 {len(accounts)} 条账户记录")

        return True
    except pymysql.Error as e:
        print(f"❌ 插入失败: {e}")
        if 'connection' in locals() and connection:
            connection.rollback()
        return False
    finally:
        if 'connection' in locals() and connection:
            connection.close()


if __name__ == "__main__":
    insert_accounts_batch()