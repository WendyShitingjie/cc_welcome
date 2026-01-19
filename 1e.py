import uuid
import mysql.connector
import time
import random
from decimal import Decimal
from datetime import datetime, timedelta, date

# 数据库配置（请修改为实际配置）
config = {
    'host': 'sitpublic.tidb.ali-bj-sit01.shuheo.net',
    'port': 4000,
    'user': 'user_for_dp',
    'password': 'your_password',
    'database': 'dataops',
    'autocommit': False,
    'charset': 'utf8mb4'
}


def generate_valid_uuid():
    """生成符合RFC 4122标准的UUID字符串"""
    return str(uuid.uuid4())  # 直接使用uuid库生成标准格式


def generate_random_data():
    """生成单条随机测试数据"""
    # 基础日期范围（过去3年）
    base_date = date.today() - timedelta(days=3 * 365)
    max_date = date.today()

    # 主数据生成
    data = {
        'uid': generate_valid_uuid(),  # 标准UUID格式
        'latest_preloan_apply_time': random_datetime(base_date, max_date) if random.random() > 0.3 else None,
        'first_loan_amount_by_blbtchhl': random_decimal(1000, 50000) if random.random() > 0.4 else None,
        'first_loan_order_init_total_stage_by_blbtchhl': random.randint(3, 36) if random.random() > 0.5 else None,
        'first_preloan_date': random_date(base_date, max_date) if random.random() > 0.3 else None,
        'current_day_apply_order_flag': str(random.randint(0, 1)) if random.random() > 0.2 else None,
        'first_loan_order_no_by_blbtchhl': ('ORD_' + ''.join(
            random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=12))) if random.random() > 0.6 else None,
        'first_loan_order_product_code_by_blbtchhl': random.choice(['BL', 'BT', 'CH', 'HL', None]),
        'current_day_first_preloan_apply_time': random_datetime(max_date, max_date) if random.random() > 0.7 else None,
        'total_success_loan_times_by_blbtchhl': random.randint(0, 20) if random.random() > 0.4 else None,
        'current_day_reloan_amount_by_blbtchhl': random_decimal(500, 20000) if random.random() > 0.6 else None,
        'settled_customer_max_settle_up_date_by_blbtchhl': random_date(base_date,
                                                                       max_date) if random.random() > 0.5 else None,
        'overdue_principal_by_ch': random_decimal(0, 5000) if random.random() > 0.5 else None,
        'overdue_principal_by_bl': random_decimal(0, 10000) if random.random() > 0.5 else None,
        'total_overdue_amount_by_bt': random_decimal(0, 8000) if random.random() > 0.5 else None,
        'current_overdue_days_by_ch': random.randint(0, 90) if random.random() > 0.4 else None,
        'order_max_settle_up_date_by_blbtchhl': random_date(base_date, max_date) if random.random() > 0.5 else None,
        'light_max_overdue_days': random.randint(0, 180) if random.random() > 0.6 else None,
        'cut_day_unpaid_total_amount_by_ch': random_decimal(0, 3000) if random.random() > 0.5 else None,
        'cut_day_unpaid_total_amount_by_bt': random_decimal(0, 5000) if random.random() > 0.5 else None
    }

    # 逻辑关联字段处理
    if data['first_preloan_date'] and data['order_max_settle_up_date_by_blbtchhl']:
        # 确保结清日期不早于借款日期
        if data['order_max_settle_up_date_by_blbtchhl'] < data['first_preloan_date']:
            data['order_max_settle_up_date_by_blbtchhl'] = data['first_preloan_date'] + timedelta(
                days=random.randint(30, 365))

    return data


def random_date(start_date, end_date):
    """生成指定范围内的随机日期"""
    days_diff = (end_date - start_date).days
    random_days = random.randint(0, days_diff)
    return start_date + timedelta(days=random_days)


def random_datetime(start_date, end_date):
    """生成指定范围内的随机日期时间"""
    random_date = random_date(start_date, end_date)
    return datetime.combine(random_date, datetime.min.time()) + timedelta(
        seconds=random.randint(0, 86399)
    )


def random_decimal(min_val, max_val, decimal_places=2):
    """生成随机Decimal值"""
    value = round(random.uniform(min_val, max_val), decimal_places)
    return Decimal(str(value))


def batch_insert(total_records=10000, batch_size=500):
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        print(f"⏳ 开始生成并插入 {total_records} 条测试数据 (分 {total_records // batch_size} 批)...")
        start_time = time.time()

        # 准备插入SQL（完整字段）
        insert_query = """
        INSERT INTO `stj_output_dwa_f_user_transaction_info_20` (
            `uid`, `latest_preloan_apply_time`, `first_loan_amount_by_blbtchhl`,
            `first_loan_order_init_total_stage_by_blbtchhl`, `first_preloan_date`,
            `current_day_apply_order_flag`, `first_loan_order_no_by_blbtchhl`,
            `first_loan_order_product_code_by_blbtchhl`, `current_day_first_preloan_apply_time`,
            `total_success_loan_times_by_blbtchhl`, `current_day_reloan_amount_by_blbtchhl`,
            `settled_customer_max_settle_up_date_by_blbtchhl`, `overdue_principal_by_ch`,
            `overdue_principal_by_bl`, `total_overdue_amount_by_bt`, `current_overdue_days_by_ch`,
            `order_max_settle_up_date_by_blbtchhl`, `light_max_overdue_days`,
            `cut_day_unpaid_total_amount_by_ch`, `cut_day_unpaid_total_amount_by_bt`
        ) VALUES (
            %(uid)s, %(latest_preloan_apply_time)s, %(first_loan_amount_by_blbtchhl)s,
            %(first_loan_order_init_total_stage_by_blbtchhl)s, %(first_preloan_date)s,
            %(current_day_apply_order_flag)s, %(first_loan_order_no_by_blbtchhl)s,
            %(first_loan_order_product_code_by_blbtchhl)s, %(current_day_first_preloan_apply_time)s,
            %(total_success_loan_times_by_blbtchhl)s, %(current_day_reloan_amount_by_blbtchhl)s,
            %(settled_customer_max_settle_up_date_by_blbtchhl)s, %(overdue_principal_by_ch)s,
            %(overdue_principal_by_bl)s, %(total_overdue_amount_by_bt)s, %(current_overdue_days_by_ch)s,
            %(order_max_settle_up_date_by_blbtchhl)s, %(light_max_overdue_days)s,
            %(cut_day_unpaid_total_amount_by_ch)s, %(cut_day_unpaid_total_amount_by_bt)s
        )
        """

        # 分批生成和插入
        for batch_num in range(0, total_records, batch_size):
            current_batch_size = min(batch_size, total_records - batch_num)
            batch_data = [generate_random_data() for _ in range(current_batch_size)]

            # 执行批量插入
            cursor.executemany(insert_query, batch_data)
            conn.commit()

            print(f"✅ 批次 {batch_num // batch_size + 1} 完成: {current_batch_size}条记录")

        # 性能统计
        elapsed = time.time() - start_time
        print(f"\n🎉 数据插入完成! 共 {total_records} 条记录")
        print(f"⏱️ 总耗时: {elapsed:.2f}秒 | 平均速度: {total_records / elapsed:.0f}条/秒")

    except mysql.connector.Error as err:
        print(f"❌ 数据库错误: {err}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
    except Exception as e:
        print(f"❌ 系统错误: {e}")
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("🔌 数据库连接已关闭")


# 主程序
if __name__ == "__main__":
    # 执行数据插入
    batch_insert(total_records=10000, batch_size=500)

    # 验证UUID格式示例
    print("\nUUID格式验证示例:")
    for _ in range(3):
        sample_uuid = generate_valid_uuid()
        print(f"  {sample_uuid} (长度: {len(sample_uuid)} 字符)")