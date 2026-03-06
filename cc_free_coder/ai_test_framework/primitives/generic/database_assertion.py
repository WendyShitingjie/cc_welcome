"""数据库断言原语（通用原语）"""
from typing import Any, Dict, List
import time
from ..base import ExecutionPrimitive, PrimitiveMetadata
from ...utils.database import DatabaseConnection, parse_table_name
import re


class AssertFieldEqualsPrimitive(ExecutionPrimitive):
    """
    断言字段值相等原语

    支持超时轮询功能：
    - 如果指定了timeout参数，会在超时时间内轮询查询，直到字段值匹配或超时
    - 可以通过poll_interval参数控制轮询间隔（默认2秒）
    - 适用于等待异步Job执行完成的场景
    """

    metadata = PrimitiveMetadata(
        name='assert_field_equals',
        category='assertion',
        description='断言数据库字段值等于期望值（支持超时轮询）',
        parameters=[
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名（如copilot.common_job_status）'
            },
            {
                'name': 'field',
                'type': 'str',
                'required': True,
                'description': '字段名'
            },
            {
                'name': 'where',
                'type': 'str',
                'required': True,
                'description': 'WHERE条件'
            },
            {
                'name': 'expected',
                'type': 'any',
                'required': True,
                'description': '期望值'
            },
            {
                'name': 'timeout',
                'type': 'int',
                'required': False,
                'description': '最大超时时间（秒），默认0表示不轮询，只查询一次'
            },
            {
                'name': 'poll_interval',
                'type': 'int',
                'required': False,
                'description': '轮询间隔（秒），默认2秒'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '详情'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行断言（支持超时轮询）"""
        self.validate_parameters(params)

        table = params['table']
        field = params['field']
        where = params['where']
        expected = params['expected']
        timeout = params.get('timeout', 0)  # 默认0表示不轮询
        poll_interval = params.get('poll_interval', 2)  # 默认2秒轮询一次

        # 解析表名
        db_name, table_name = parse_table_name(table)

        # 执行SQL查询（不再自动添加LIMIT 1，因为WHERE条件中可能已经包含了ORDER BY和LIMIT）
        sql = f"SELECT {field} FROM {db_name}.{table_name} WHERE {where}"

        # 如果没有设置超时，只查询一次
        if timeout <= 0:
            return self._check_once(db_name, sql, table, field, where, expected)

        # 如果设置了超时，进行轮询
        return self._check_with_polling(db_name, sql, table, field, where, expected, timeout, poll_interval)

    def _check_once(self, db_name: str, sql: str, table: str, field: str, where: str, expected: Any) -> Dict[str, Any]:
        """执行一次查询检查"""
        # 调试：打印SQL（只在第一次查询时打印）
        if not hasattr(self, '_sql_printed'):
            print(f"    🔍 执行SQL: {sql}")
            self._sql_printed = True

        try:
            results = DatabaseConnection.execute_query(db_name, sql)

            if not results:
                return {
                    'status': 'FAIL',
                    'reason': f'未找到符合条件的记录',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'sql': sql
                    }
                }

            actual = results[0][field]

            if actual == expected:
                return {
                    'status': 'PASS',
                    'reason': f'字段值匹配: {field} = {expected}',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'actual': actual,
                        'expected': expected
                    }
                }
            else:
                return {
                    'status': 'FAIL',
                    'reason': f'字段值不匹配: {field} = {actual}, 期望 {expected}',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'actual': actual,
                        'expected': expected
                    }
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'reason': f'查询失败: {str(e)}',
                'details': {
                    'table': table,
                    'field': field,
                    'where': where,
                    'sql': sql,
                    'error': str(e)
                }
            }

    def _check_with_polling(self, db_name: str, sql: str, table: str, field: str, where: str,
                            expected: Any, timeout: int, poll_interval: int) -> Dict[str, Any]:
        """轮询检查直到字段值匹配或超时"""
        start_time = time.time()
        elapsed = 0
        attempt = 0
        last_actual = None

        print(f"    ⏳ 开始轮询检查（最大超时: {timeout}秒，轮询间隔: {poll_interval}秒）...")

        while elapsed < timeout:
            attempt += 1
            elapsed = time.time() - start_time
            print(f"    🔍 第{attempt}次查询 (已等待{round(elapsed, 1)}秒)...")

            # 执行查询
            result = self._check_once(db_name, sql, table, field, where, expected)

            # 如果匹配成功，立即返回
            if result['status'] == 'PASS':
                result['details']['attempts'] = attempt
                result['details']['elapsed_time'] = round(elapsed, 2)
                print(f"    ✅ 字段值匹配成功！共尝试{attempt}次，耗时{round(elapsed, 2)}秒")
                return result

            # 记录最后一次的实际值
            if 'actual' in result.get('details', {}):
                last_actual = result['details']['actual']

            # 如果还有时间，继续等待
            remaining = timeout - elapsed
            if remaining > 0:
                sleep_time = min(poll_interval, remaining)
                if sleep_time > 0:
                    time.sleep(sleep_time)
            else:
                break

        # 超时失败
        elapsed = time.time() - start_time
        print(f"    ❌ 超时失败！共尝试{attempt}次，耗时{round(elapsed, 2)}秒")
        return {
            'status': 'FAIL',
            'reason': f'超时({timeout}秒)：字段值始终不匹配期望值',
            'details': {
                'table': table,
                'field': field,
                'where': where,
                'expected': expected,
                'last_actual': last_actual,
                'timeout': timeout,
                'attempts': attempt,
                'elapsed_time': round(elapsed, 2)
            }
        }


class AssertRecordCountPrimitive(ExecutionPrimitive):
    """断言记录数原语"""

    metadata = PrimitiveMetadata(
        name='assert_record_count',
        category='assertion',
        description='断言记录数等于期望值（支持超时轮询）',
        parameters=[
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名'
            },
            {
                'name': 'where',
                'type': 'str',
                'required': True,
                'description': 'WHERE条件'
            },
            {
                'name': 'expected',
                'type': 'int',
                'required': True,
                'description': '期望记录数'
            },
            {
                'name': 'timeout',
                'type': 'int',
                'required': False,
                'description': '最大超时时间（秒），默认0表示不轮询，只查询一次'
            },
            {
                'name': 'poll_interval',
                'type': 'int',
                'required': False,
                'description': '轮询间隔（秒），默认2秒'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '详情'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行断言（支持超时轮询）"""
        self.validate_parameters(params)

        table = params['table']
        where = params['where']
        expected = params['expected']
        timeout = params.get('timeout', 0)  # 默认0表示不轮询
        poll_interval = params.get('poll_interval', 2)  # 默认2秒轮询一次

        # 解析表名
        db_name, table_name = parse_table_name(table)

        # 执行SQL查询
        sql = f"SELECT COUNT(*) as count FROM {db_name}.{table_name} WHERE {where}"

        # 如果没有设置超时，只查询一次
        if timeout <= 0:
            return self._check_once(db_name, sql, table, where, expected)

        # 如果设置了超时，进行轮询
        return self._check_with_polling(db_name, sql, table, where, expected, timeout, poll_interval)

    def _check_once(self, db_name: str, sql: str, table: str, where: str, expected: int, print_sql: bool = True) -> \
    Dict[str, Any]:
        """执行一次查询检查"""
        # 调试：打印SQL（只在第一次或非轮询时打印）
        if print_sql:
            print(f"    🔍 执行SQL: {sql}")

        try:
            results = DatabaseConnection.execute_query(db_name, sql)
            actual = results[0]['count']

            # 调试：打印查询结果（只在非轮询时打印）
            if print_sql:
                print(f"    📊 查询结果: {actual} 条记录")

            if actual == expected:
                return {
                    'status': 'PASS',
                    'reason': f'记录数匹配: {actual} = {expected}',
                    'details': {
                        'table': table,
                        'where': where,
                        'actual': actual,
                        'expected': expected
                    }
                }
            else:
                return {
                    'status': 'FAIL',
                    'reason': f'记录数不匹配: {actual} != {expected}',
                    'details': {
                        'table': table,
                        'where': where,
                        'actual': actual,
                        'expected': expected
                    }
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'reason': f'查询失败: {str(e)}',
                'details': {
                    'table': table,
                    'where': where,
                    'sql': sql,
                    'error': str(e)
                }
            }

    def _check_with_polling(self, db_name: str, sql: str, table: str, where: str,
                            expected: int, timeout: int, poll_interval: int) -> Dict[str, Any]:
        """轮询检查直到记录数匹配或超时"""
        start_time = time.time()
        elapsed = 0
        attempt = 0
        last_actual = None

        print(f"    ⏳ 开始轮询检查（最大超时: {timeout}秒，轮询间隔: {poll_interval}秒）...")

        # 第一次查询前先打印SQL
        print(f"    🔍 执行SQL: {sql}")

        while elapsed < timeout:
            attempt += 1
            elapsed = time.time() - start_time
            print(f"    🔍 第{attempt}次查询 (已等待{round(elapsed, 1)}秒)...")

            # 执行查询（轮询时不打印SQL，避免重复）
            result = self._check_once(db_name, sql, table, where, expected, print_sql=False)

            # 如果匹配成功，立即返回
            if result['status'] == 'PASS':
                print(f"    ✅ 记录数匹配成功！共尝试{attempt}次，耗时{round(elapsed, 1)}秒")
                return result

            # 记录最后一次的实际值
            last_actual = result['details'].get('actual')

            # 如果还没超时，等待后继续
            if elapsed < timeout:
                time.sleep(poll_interval)

        # 超时失败
        print(f"    ❌ 超时失败！共尝试{attempt}次，耗时{round(elapsed, 2)}秒")
        return {
            'status': 'FAIL',
            'reason': f'超时({timeout}秒)：记录数始终不匹配期望值',
            'details': {
                'table': table,
                'where': where,
                'expected': expected,
                'last_actual': last_actual,
                'timeout': timeout,
                'attempts': attempt,
                'elapsed_time': round(elapsed, 2)
            }
        }


class AssertAllRecordsMatchPrimitive(ExecutionPrimitive):
    """
    断言所有记录匹配原语

    支持超时轮询功能：
    - 如果指定了timeout参数，会在超时时间内轮询查询，直到所有记录都匹配或超时
    - 可以通过poll_interval参数控制轮询间隔（默认2秒）
    - 适用于等待异步Job执行完成的场景
    """

    metadata = PrimitiveMetadata(
        name='assert_all_records_match',
        category='assertion',
        description='断言所有记录的某个字段都等于期望值（支持超时轮询）',
        parameters=[
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名'
            },
            {
                'name': 'field',
                'type': 'str',
                'required': True,
                'description': '字段名（支持JSON_EXTRACT表达式）'
            },
            {
                'name': 'where',
                'type': 'str',
                'required': True,
                'description': 'WHERE条件'
            },
            {
                'name': 'expected',
                'type': 'any',
                'required': True,
                'description': '期望值'
            },
            {
                'name': 'timeout',
                'type': 'int',
                'required': False,
                'description': '最大超时时间（秒），默认0表示不轮询，只查询一次'
            },
            {
                'name': 'poll_interval',
                'type': 'int',
                'required': False,
                'description': '轮询间隔（秒），默认2秒'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '详情'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行断言（支持超时轮询）"""
        self.validate_parameters(params)

        table = params['table']
        field = params['field']
        where = params['where']
        expected = params['expected']
        timeout = params.get('timeout', 0)  # 默认0表示不轮询
        poll_interval = params.get('poll_interval', 2)  # 默认2秒轮询一次

        # 解析表名
        db_name, table_name = parse_table_name(table)

        # 执行SQL查询（不再自动添加LIMIT，因为WHERE条件中可能已经包含了ORDER BY和LIMIT）
        # 如果field包含output_data，同时查询output_data字段用于调试
        if 'output_data' in field.lower():
            sql = f"SELECT {field}, output_data FROM {db_name}.{table_name} WHERE {where}"
        else:
            sql = f"SELECT {field} FROM {db_name}.{table_name} WHERE {where}"

        # 如果没有设置超时，只查询一次
        if timeout <= 0:
            return self._check_once(db_name, sql, table, field, where, expected)

        # 如果设置了超时，进行轮询
        return self._check_with_polling(db_name, sql, table, field, where, expected, timeout, poll_interval)

    def _check_once(self, db_name: str, sql: str, table: str, field: str, where: str, expected: Any) -> Dict[str, Any]:
        """执行一次查询检查"""
        try:
            results = DatabaseConnection.execute_query(db_name, sql)

            if not results:
                return {
                    'status': 'FAIL',
                    'reason': '未找到符合条件的记录',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'sql': sql
                    }
                }

            # 检查所有记录的字段值是否都等于expected
            mismatched = []
            for idx, record in enumerate(results):
                value = record.get(field)
                if value != expected:
                    # 调试：打印不匹配的记录详情
                    # print(f"    🔍 记录 {idx}: {field} = {value} (类型: {type(value).__name__})")
                    # # 如果是JSON_EXTRACT字段，打印完整的output_data
                    # if 'output_data' in field.lower():
                    #     output_data = record.get('output_data')
                    #     print(f"    📄 完整output_data: {output_data}")

                    mismatched.append({
                        'record_index': idx,
                        'actual': value,
                        'expected': expected
                    })

            if not mismatched:
                return {
                    'status': 'PASS',
                    'reason': f'所有{len(results)}条记录的{field}都等于{expected}',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'total_count': len(results),
                        'expected': expected
                    }
                }
            else:
                return {
                    'status': 'FAIL',
                    'reason': f'有{len(mismatched)}条记录的{field}不等于{expected}',
                    'details': {
                        'table': table,
                        'field': field,
                        'where': where,
                        'total_count': len(results),
                        'mismatched_count': len(mismatched),
                        'expected': expected,
                        'mismatched_records': mismatched[:5]  # 只显示前5个
                    }
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'reason': f'查询失败: {str(e)}',
                'details': {
                    'table': table,
                    'field': field,
                    'where': where,
                    'sql': sql,
                    'error': str(e)
                }
            }

    def _check_with_polling(self, db_name: str, sql: str, table: str, field: str, where: str,
                            expected: Any, timeout: int, poll_interval: int) -> Dict[str, Any]:
        """轮询检查直到所有记录都匹配或超时"""
        start_time = time.time()
        elapsed = 0
        attempt = 0
        last_mismatched_count = None

        print(f"    ⏳ 开始轮询检查（最大超时: {timeout}秒，轮询间隔: {poll_interval}秒）...")

        while elapsed < timeout:
            attempt += 1
            elapsed = time.time() - start_time
            print(f"    🔍 第{attempt}次查询 (已等待{round(elapsed, 1)}秒)...")

            # 执行查询
            result = self._check_once(db_name, sql, table, field, where, expected)

            # 如果匹配成功，立即返回
            if result['status'] == 'PASS':
                result['details']['attempts'] = attempt
                result['details']['elapsed_time'] = round(elapsed, 2)
                print(f"    ✅ 所有记录都匹配成功！共尝试{attempt}次，耗时{round(elapsed, 2)}秒")
                return result

            # 记录最后一次的不匹配数量
            if 'mismatched_count' in result.get('details', {}):
                last_mismatched_count = result['details']['mismatched_count']

            # 如果还有时间，继续等待
            remaining = timeout - elapsed
            if remaining > 0:
                sleep_time = min(poll_interval, remaining)
                if sleep_time > 0:
                    time.sleep(sleep_time)
            else:
                break

        # 超时失败
        elapsed = time.time() - start_time
        print(f"    ❌ 超时失败！共尝试{attempt}次，耗时{round(elapsed, 2)}秒")
        return {
            'status': 'FAIL',
            'reason': f'超时({timeout}秒)：仍有记录不匹配期望值',
            'details': {
                'table': table,
                'field': field,
                'where': where,
                'expected': expected,
                'last_mismatched_count': last_mismatched_count,
                'timeout': timeout,
                'attempts': attempt,
                'elapsed_time': round(elapsed, 2)
            }
        }


class AssertAllJsonFieldsNotNullPrimitive(ExecutionPrimitive):
    """断言所有记录的JSON字段非空原语"""

    metadata = PrimitiveMetadata(
        name='assert_all_json_fields_not_null',
        category='assertion',
        description='断言所有记录的JSON字段中的指定路径非空',
        parameters=[
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名'
            },
            {
                'name': 'json_field',
                'type': 'str',
                'required': True,
                'description': 'JSON字段名（如output_data）'
            },
            {
                'name': 'extract_fields',
                'type': 'list',
                'required': True,
                'description': 'JSON路径列表（如["$.character", "$.target"]）'
            },
            {
                'name': 'where',
                'type': 'str',
                'required': True,
                'description': 'WHERE条件'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '详情'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行断言"""
        self.validate_parameters(params)

        table = params['table']
        json_field = params['json_field']
        extract_fields = params['extract_fields']
        where = params['where']

        # 解析表名
        db_name, table_name = parse_table_name(table)

        # 构造SQL查询，检查所有JSON路径是否非空
        json_extracts = ', '.join([
            f"JSON_EXTRACT({json_field}, '{path}') as `{path}`"
            for path in extract_fields
        ])

        sql = f"SELECT {json_extracts} FROM {db_name}.{table_name} WHERE {where}"

        try:
            results = DatabaseConnection.execute_query(db_name, sql)

            if not results:
                return {
                    'status': 'FAIL',
                    'reason': '未找到符合条件的记录',
                    'details': {
                        'table': table,
                        'json_field': json_field,
                        'extract_fields': extract_fields,
                        'where': where
                    }
                }

            # 检查每条记录的每个JSON字段是否非空
            null_records = []
            for idx, record in enumerate(results):
                for path in extract_fields:
                    value = record.get(path)
                    if value is None or value == 'null':
                        null_records.append({
                            'record_index': idx,
                            'path': path,
                            'value': value
                        })

            if not null_records:
                return {
                    'status': 'PASS',
                    'reason': f'所有{len(results)}条记录的JSON字段{extract_fields}都非空',
                    'details': {
                        'table': table,
                        'json_field': json_field,
                        'extract_fields': extract_fields,
                        'where': where,
                        'total_records': len(results)
                    }
                }
            else:
                return {
                    'status': 'FAIL',
                    'reason': f'有{len(null_records)}个字段为空',
                    'details': {
                        'table': table,
                        'json_field': json_field,
                        'extract_fields': extract_fields,
                        'where': where,
                        'total_records': len(results),
                        'null_records': null_records[:10]  # 只显示前10个
                    }
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'reason': f'查询失败: {str(e)}',
                'details': {
                    'table': table,
                    'json_field': json_field,
                    'extract_fields': extract_fields,
                    'where': where,
                    'sql': sql,
                    'error': str(e)
                }
            }


class AssertAllFieldsNotNullPrimitive(ExecutionPrimitive):
    """断言所有记录的字段非空原语"""

    metadata = PrimitiveMetadata(
        name='assert_all_fields_not_null',
        category='assertion',
        description='断言所有记录的指定字段都非空',
        parameters=[
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名'
            },
            {
                'name': 'fields',
                'type': 'list',
                'required': True,
                'description': '字段名列表'
            },
            {
                'name': 'where',
                'type': 'str',
                'required': True,
                'description': 'WHERE条件'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '详情'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行断言"""
        self.validate_parameters(params)

        table = params['table']
        fields = params['fields']
        where = params['where']

        # 解析表名
        db_name, table_name = parse_table_name(table)

        # 构造SQL查询
        fields_str = ', '.join(fields)
        sql = f"SELECT {fields_str} FROM {db_name}.{table_name} WHERE {where}"

        try:
            results = DatabaseConnection.execute_query(db_name, sql)

            if not results:
                return {
                    'status': 'FAIL',
                    'reason': '未找到符合条件的记录',
                    'details': {
                        'table': table,
                        'fields': fields,
                        'where': where
                    }
                }

            # 检查每条记录的每个字段是否非空
            null_records = []
            for idx, record in enumerate(results):
                for field in fields:
                    value = record.get(field)
                    if value is None or value == '':
                        null_records.append({
                            'record_index': idx,
                            'field': field,
                            'value': value
                        })

            if not null_records:
                return {
                    'status': 'PASS',
                    'reason': f'所有{len(results)}条记录的字段{fields}都非空',
                    'details': {
                        'table': table,
                        'fields': fields,
                        'where': where,
                        'total_records': len(results)
                    }
                }
            else:
                return {
                    'status': 'FAIL',
                    'reason': f'有{len(null_records)}个字段为空',
                    'details': {
                        'table': table,
                        'fields': fields,
                        'where': where,
                        'total_records': len(results),
                        'null_records': null_records[:10]  # 只显示前10个
                    }
                }
        except Exception as e:
            return {
                'status': 'FAIL',
                'reason': f'查询失败: {str(e)}',
                'details': {
                    'table': table,
                    'fields': fields,
                    'where': where,
                    'sql': sql,
                    'error': str(e)
                }
            }


class AssertDatabaseRecordPrimitive(ExecutionPrimitive):
    """
    断言数据库记录多字段匹配原语 (增强版)

    功能特点：
    1. 智能字段匹配：支持 pi.status 自动识别为字典中的 status。
    2. 别名支持：支持在 YAML 中写 "pi.status AS pi_status"，解决多表字段重名冲突。
    3. 异步轮询：内置超时重试机制，适配后端异步回写场景。
    4. 类型容错：自动执行强转字符串比对，避免数字与字符串比对失败。
    """

    metadata = PrimitiveMetadata(
        name='assert_database_record',
        category='assertion',
        description='断言数据库记录的多个字段同时满足期望值（支持多表别名和超时轮询）',
        parameters=[
            {'name': 'table', 'type': 'str', 'required': True, 'description': '表名及关联逻辑(FROM后的内容)'},
            {'name': 'where', 'type': 'str', 'required': True, 'description': 'WHERE查询条件'},
            {'name': 'assertions', 'type': 'list', 'required': True,
             'description': '校验列表，支持别名：[{"field":"pi.status AS pi_status", "expected":0}]'},
            {'name': 'wait', 'type': 'int', 'required': False, 'description': '轮询等待时间(秒)'},
            {'name': 'poll_interval', 'type': 'int', 'required': False, 'description': '轮询间隔，默认2s'}
        ],

        returns={
            'status': 'PASS/FAIL',
            'reason': '失败或成功的简述',
            'details': '详细的字段比对结果'
        }
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        self.validate_parameters(params)

        table_expr = params['table']
        where_clause = params['where']
        assertions_config = params['assertions']
        timeout = params.get('wait', params.get('timeout', 0))
        poll_interval = params.get('poll_interval', 2)

        # 1. 预处理：解析字段名、别名和对应的字典 Key
        query_fields = []
        processed_items = []

        for asm in assertions_config:
            raw_field = asm['field']

            # 情况A: 用户显式使用了 AS 别名 (如 "ds.status AS ds_status")
            if ' AS ' in raw_field.upper():
                # 使用正则忽略大小写分割
                parts = re.split(r'\s+AS\s+', raw_field, flags=re.IGNORECASE)
                sql_part = raw_field  # 原始 SQL: "ds.status AS ds_status"
                dict_key = parts[1].strip()  # Python 取值 Key: "ds_status"

            # 情况B: 带有表前缀但没别名 (如 "pi.status")
            elif '.' in raw_field:
                sql_part = raw_field  # 原始 SQL: "pi.status"
                dict_key = raw_field.split('.')[-1]  # Python 取值 Key: "status"

            # 情况C: 普通字段
            else:
                sql_part = raw_field
                dict_key = raw_field

            query_fields.append(sql_part)
            processed_items.append({
                'key': dict_key,  # 用于从数据库结果字典里拿数据
                'expected': asm['expected'],
                'raw': raw_field  # 用于在日志里展示
            })

        # 2. 解析主库名（用于 DatabaseConnection 路由）
        # 即使 table 字段包含 JOIN 语句，我们取第一个词来识别数据库
        db_context_name = table_expr.split('.')[0].split()[0]

        # 3. 构造完整 SQL
        sql = f"SELECT {', '.join(query_fields)} FROM {table_expr} WHERE {where_clause}"

        # 4. 执行逻辑：单次或轮询
        if timeout <= 0:
            return self._check_once(db_context_name, sql, processed_items)

        return self._check_with_polling(db_context_name, sql, processed_items, timeout, poll_interval)

    def _check_once(self, db_name: str, sql: str, processed_items: List[Dict]) -> Dict[str, Any]:
        try:
            print(f"    🔍 执行SQL: {sql}")
            # 注意：DatabaseConnection 内部必须开启 autocommit 或执行 commit 刷新快照
            results = DatabaseConnection.execute_query(db_name, sql)

            if not results:
                return {'status': 'FAIL', 'reason': '未查询到符合条件的记录'}

            record = results[0]
            mismatches = []

            for item in processed_items:
                actual = record.get(item['key'])
                expected = item['expected']

                # ⭐ 核心逻辑：强转字符串比对，解决类型不一致问题
                if str(actual) != str(expected):
                    mismatches.append(f"字段 [{item['raw']}]: 实际={actual}, 期望={expected}")

            if not mismatches:
                return {'status': 'PASS', 'reason': '所有字段校验通过', 'details': record}
            else:
                return {'status': 'FAIL', 'reason': '字段值不匹配', 'details': "; ".join(mismatches)}

        except Exception as e:
            return {'status': 'FAIL', 'reason': f'执行异常: {str(e)}'}

    def _check_with_polling(self, db_name: str, sql: str, processed_items: List[Dict],
                            timeout: int, poll_interval: int) -> Dict[str, Any]:
        start_time = time.time()
        attempt = 0
        print(f"    ⏳ 开始轮询检查 (最大等待 {timeout}s)...")

        while (time.time() - start_time) < timeout:
            attempt += 1
            result = self._check_once(db_name, sql, processed_items)

            if result['status'] == 'PASS':
                print(f"    ✅ 第 {attempt} 次查询匹配成功！")
                return result

            time.sleep(poll_interval)

        return {'status': 'FAIL', 'reason': f'轮询 {timeout}s 后验证仍未通过', 'details': result.get('details')}
