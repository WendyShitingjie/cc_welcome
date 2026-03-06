#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
查看表的元数据信息
"""

import pymysql

config = {
    'host': 'cjjcommon.db.ali-bj-sit01.shuheo.net',
    'port': 3306,
    'user': 'sit_shitingjie',
    'password': 'sit_user_115e27b_932c93',
    'database': 'dataops_shitingjie',
    'charset': 'utf8mb4'
}

def view_table_metadata(table_name):
    """查看表的元数据"""
    connection = pymysql.connect(**config)
    cursor = connection.cursor()

    # 查看表注释
    cursor.execute(f"""
        SELECT TABLE_COMMENT
        FROM information_schema.TABLES
        WHERE TABLE_SCHEMA = '{config['database']}'
        AND TABLE_NAME = '{table_name}'
    """)
    table_comment = cursor.fetchone()

    print(f"\n{'='*80}")
    print(f"表名: {table_name}")
    print(f"表注释: {table_comment[0] if table_comment and table_comment[0] else '(无)'}")
    print(f"{'='*80}\n")

    # 查看字段注释
    cursor.execute(f"""
        SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT
        FROM information_schema.COLUMNS
        WHERE TABLE_SCHEMA = '{config['database']}'
        AND TABLE_NAME = '{table_name}'
        ORDER BY ORDINAL_POSITION
    """)

    columns = cursor.fetchall()

    print(f"字段元数据信息:")
    print(f"{'-'*80}")
    print(f"{'字段名':<20} {'类型':<20} {'允许NULL':<10} {'注释':<30}")
    print(f"{'-'*80}")

    for col in columns:
        col_name, col_type, is_null, col_key, col_default, col_comment = col
        comment_display = col_comment if col_comment else '(无)'
        print(f"{col_name:<20} {col_type:<20} {is_null:<10} {comment_display:<30}")

    print(f"{'-'*80}\n")

    cursor.close()
    connection.close()

if __name__ == "__main__":
    view_table_metadata('0418bugfuxianccc')
