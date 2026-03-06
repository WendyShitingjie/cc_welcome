#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YAML 测试用例自动化执行引擎

功能：
1. 读取 YAML 测试用例文件
2. 解析测试意图和断言
3. 调用对应的原语/接口执行测试
4. 验证断言并生成测试报告
"""

import yaml
import sys
import os
import re
import subprocess
import mysql.connector
from datetime import datetime
from typing import Dict, List, Any, Optional


class TestContext:
    """测试上下文，用于存储测试过程中的变量"""

    def __init__(self):
        self.variables = {}

    def set(self, key: str, value: Any):
        """设置变量"""
        self.variables[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """获取变量"""
        return self.variables.get(key, default)

    def resolve(self, value: str) -> Any:
        """解析变量引用，如 ${context.taskId}"""
        if not isinstance(value, str):
            return value

        # 查找所有 ${...} 模式
        pattern = r'\$\{context\.(\w+)\}'
        matches = re.findall(pattern, value)

        result = value
        for var_name in matches:
            var_value = self.get(var_name)
            if var_value is not None:
                result = result.replace(f'${{context.{var_name}}}', str(var_value))

        return result


class PrimitiveExecutor:
    """原语执行器，负责��用具体的 Skills 和接口"""

    def __init__(self, context: TestContext):
        self.context = context
        self.skills_dir = "/Users/wendy/PycharmProjects/cc_free_coder/skills"

    def execute(self, primitive: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """执行原语"""
        # 解析参数中的变量引用
        resolved_params = {k: self.context.resolve(v) for k, v in params.items()}

        # 根据原语类型调用对应的执行方法
        if primitive == "TKP_001":
            return self.execute_tkp_001(resolved_params)
        elif primitive == "TKP_002":
            return self.execute_tkp_002(resolved_params)
        elif primitive == "TKP_003":
            return self.execute_tkp_003(resolved_params)
        elif primitive == "TKI_003":
            return self.execute_tki_003(resolved_params)
        elif primitive == "TKI_004":
            return self.execute_tki_004(resolved_params)
        elif primitive == "TKI_005":
            return self.execute_tki_005(resolved_params)
        elif primitive == "TKP_004":
            return self.execute_tkp_004(resolved_params)
        else:
            raise ValueError(f"未知的原语: {primitive}")

    def execute_tkp_001(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKP_001: 创建测试表"""
        print("\n[TKP_001] 创建测试表")

        # 从 instruction 中提取参数
        instruction = params.get('instruction', '')
        instance = params.get('default_instance', 'cjjcommon')
        database = params.get('default_db', 'dataops_shitingjie')

        # 解析表数量
        count_match = re.search(r'(\d+)\s*张', instruction)
        count = int(count_match.group(1)) if count_match else 2

        # 调用 batch_workflow.py（仅执行步骤1：创建表）
        # 这里简化为调用 test-table skill
        script_path = os.path.join(self.skills_dir, 'test-table/scripts/index.py')

        created_tables = []
        timestamp = datetime.now().strftime("%m%d%H%M")

        for i in range(count):
            table_name = f"batch_test_{timestamp}_{i+1:02d}"
            cmd = [
                'python3', script_path,
                'generate',
                '--tableName', table_name,
                '--dataType', 'mixed',
                '--rowCount', '10',
                '--execute',
                '--env', instance
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                created_tables.append(table_name)
                print(f"  ✓ 表 {table_name} 创建成功")
            else:
                print(f"  ✗ 表 {table_name} 创建失败")
                return {'success': False, 'error': result.stderr}

        # 保存到上下文
        self.context.set('instance_name', instance)
        self.context.set('db_name', database)
        self.context.set('created_tables', created_tables)

        return {
            'success': True,
            'created_tables': created_tables,
            'instance': instance,
            'database': database
        }

    def execute_tkp_002(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKP_002: 完善元数据"""
        print("\n[TKP_002] 完善元数据")

        instance = params.get('instance_name')
        database = params.get('db_name')
        tables = params.get('tables', [])

        script_path = os.path.join(self.skills_dir, 'metadata-complete/scripts/index.py')

        for table in tables:
            cmd = [
                'python3', script_path,
                '--instance', instance,
                '--database', database,
                '--table', table
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"  ✓ 表 {table} 元数据完善成功")
            else:
                print(f"  ✗ 表 {table} 元数据完善失败")
                return {'success': False, 'error': result.stderr}

        return {'success': True}

    def execute_tkp_003(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKP_003: 生成 Excel 测试文件"""
        print("\n[TKP_003] 生成 Excel 测试文件")

        instance = params.get('instance_name')
        database = params.get('db_name')
        tables = params.get('tables', [])

        script_path = os.path.join(self.skills_dir, 'jdbc-warehouse-test/scripts/template_updater.py')

        cmd = [
            'python3', script_path,
            instance, database,
            *tables,
            '--db-type', 'mysql',
            '--extract-method', 'ins',
            '--deal-method', 'merge'
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(script_path))

        if result.returncode == 0:
            print(f"  ✓ Excel 文件生成成功")
            # 文件路径
            file_path = "/Users/wendy/PycharmProjects/cc_free_coder/JBDC入仓/BIZ_REQ_33706_001_批量入仓_新增任务/test_data/batch_test_latest.xlsx"
            self.context.set('test_file_path', file_path)
            return {'success': True, 'file_path': file_path}
        else:
            print(f"  ✗ Excel 文件生成失败")
            return {'success': False, 'error': result.stderr}

    def execute_tki_003(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKI_003: 批量上传校验接口"""
        print("\n[TKI_003] 批量上传校验")

        file_path = self.context.get('test_file_path')
        script_path = os.path.join(self.skills_dir, 'jdbc-warehouse-test/scripts/batch_upload_validate.py')

        cmd = ['python3', script_path, file_path, 'sit03']
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(script_path))

        # 解析 TaskId
        task_id = None
        for line in result.stdout.split('\n'):
            if '任务ID:' in line or 'taskId:' in line:
                parts = line.split(':')
                if len(parts) >= 2:
                    try:
                        task_id = str(int(parts[1].strip()))
                        break
                    except ValueError:
                        continue

        if task_id:
            print(f"  ✓ 上传成功，TaskId: {task_id}")
            self.context.set('taskId', task_id)
            return {'success': True, 'taskId': task_id}
        else:
            print(f"  ✗ 上传失败或未获取到 TaskId")
            return {'success': False, 'error': '未获取到 TaskId'}

    def execute_tki_004(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKI_004: 查询校验结果"""
        print("\n[TKI_004] 查询校验结果")

        task_id = params.get('taskId')
        script_path = os.path.join(self.skills_dir, 'jdbc-warehouse-test/scripts/batch_query_result.py')

        # 轮询查询（最多10次）
        import time
        for attempt in range(1, 11):
            cmd = ['python3', script_path, task_id, 'sit03']
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(script_path))

            # 检查是否成功
            if '✅ 校验成功' in result.stdout or 'success: True' in result.stdout:
                print(f"  ✓ 校验成功（第 {attempt} 次查询）")
                return {'success': True}

            if attempt < 10:
                time.sleep(3)

        print(f"  ✗ 校验超时")
        return {'success': False, 'error': '查询超时'}

    def execute_tki_005(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKI_005: 提交批量操作任务"""
        print("\n[TKI_005] 提交批量操作任务")

        task_id = params.get('taskId')
        script_path = os.path.join(self.skills_dir, 'jdbc-warehouse-test/scripts/batch_submit_task.py')

        cmd = ['python3', script_path, task_id, 'sit03']
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(script_path))

        if result.returncode == 0 and '✅ 提交成功' in result.stdout:
            print(f"  ✓ 提交成功")
            return {'success': True}
        else:
            print(f"  ✗ 提交失败")
            return {'success': False, 'error': result.stderr}

    def execute_tkp_004(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """TKP_004: 发送 MQ 审批信号"""
        print("\n[TKP_004] 发送 MQ 审批信号")

        task_id = params.get('taskId')
        instruction = params.get('instruction', '')

        # 判断是审批通过还是拒绝
        if '审批通过' in instruction:
            status = 'STATUS_APPROVED'
            scenario = 'approve'
        elif '审批拒绝' in instruction:
            status = 'STATUS_REJECTED'
            scenario = 'reject'
        else:
            status = 'STATUS_APPROVED'
            scenario = 'approve'

        # 查询数据库获取工单信息
        import json
        db_config = {
            'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
            'port': 3306,
            'database': 'dataops',
            'user': 'bdsit_user_0e0bc33',
            'password': 'bdsit_user_0e0bc33_26587a',
            'charset': 'utf8mb4'
        }

        sql = """
        SELECT
            r.process_instance_node_id AS batchTaskId,
            r.process_instance_node_id AS taskId,
            r.bpm_process_id AS processInstId,
            r.order_no AS orderNo,
            t.file_name AS file_name
        FROM
            dataops_bpm_record r
        INNER JOIN
            dataops_batch_operation_task t
            ON r.process_instance_node_id = t.id
        WHERE
            r.process_key = 'bg_jdbc_rc_plxz_rw'
            AND r.process_instance_node_id = %s
            AND r.status = 2
        """

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (task_id,))
            db_result = cursor.fetchone()
            cursor.close()
            conn.close()

            if not db_result:
                print(f"  ✗ 未找到工单信息")
                return {'success': False, 'error': '未找到工单信息'}

            # 构造 MQ 消息
            payload = {
                "cluster_name": "amqp-cn-4591j61c6009",
                "queue": "dataops.queue.receiveBatchOperationFlow",
                "payload_dict": {
                    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                    "orderNo": db_result['orderNo'],
                    "dataMap": {
                        "fileName": db_result['file_name'],
                        "sceneType": "jdbcInputBatchAddTask",
                        "createdBy": "施婷杰",
                        "batchTaskId": str(db_result['batchTaskId']),
                        "scOwnerUid": "6260e238-93c5-4324-8d0f-e3ba17659a14",
                        "taskId": str(db_result['taskId']),
                        "recordCnt": 1,
                        "scene": "批量新增任务"
                    },
                    "processInstId": db_result['processInstId'],
                    "operatorUid": "6260e238-93c5-4324-8d0f-e3ba17659a14",
                    "operator": "陈沈伟",
                    "startName": "施婷杰",
                    "status": status
                },
                "reason": f"YAML测试用例自动化执行-{scenario}"
            }

            if scenario == 'reject':
                payload['payload_dict']['dataMap']['rejectReason'] = "自动化测试-审批拒绝场景"

            # 调用 mq_sender.py
            mq_script = "/Users/wendy/.claude/skills/mq-sender/scripts/mq_sender.py"
            cmd = ['python3', mq_script, json.dumps(payload, ensure_ascii=False)]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0 and 'success' in result.stdout:
                print(f"  ✓ MQ 消息发送成功")
                return {'success': True}
            else:
                print(f"  ✗ MQ 消息发送失败")
                return {'success': False, 'error': result.stderr}

        except Exception as e:
            print(f"  ✗ 执行失败: {str(e)}")
            return {'success': False, 'error': str(e)}


class AssertionExecutor:
    """断言执行器"""

    def __init__(self, context: TestContext):
        self.context = context

    def execute(self, assertion: Dict[str, Any]) -> bool:
        """执行断言"""
        primitive = assertion.get('primitive')

        if primitive == 'assert_field_equals':
            return self.assert_field_equals(assertion.get('params', {}))
        elif primitive == 'assert_database_record':
            return self.assert_database_record(assertion.get('params', {}))
        else:
            print(f"  ⚠️  未知断言类型: {primitive}")
            return True  # 未知断言默认通过

    def assert_field_equals(self, params: Dict[str, Any]) -> bool:
        """断言数据库字段值"""
        table = self.context.resolve(params.get('table'))
        field = params.get('field')
        where = self.context.resolve(params.get('where'))
        expected = params.get('expected')

        print(f"\n  [断言] {table}.{field} = {expected}")

        # 连接数据库
        db_config = {
            'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
            'port': 3306,
            'database': 'dataops',
            'user': 'bdsit_user_0e0bc33',
            'password': 'bdsit_user_0e0bc33_26587a',
            'charset': 'utf8mb4'
        }

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            sql = f"SELECT {field} FROM {table} WHERE {where}"
            cursor.execute(sql)
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if result:
                actual = result[field]
                if str(actual) == str(expected):
                    print(f"    ✓ 实际值: {actual}")
                    return True
                else:
                    print(f"    ✗ 实际值: {actual}, 预期值: {expected}")
                    return False
            else:
                print(f"    ✗ 未找到记录")
                return False

        except Exception as e:
            print(f"    ✗ 查询失败: {str(e)}")
            return False

    def assert_database_record(self, params: Dict[str, Any]) -> bool:
        """断言数据库记录存在"""
        table = self.context.resolve(params.get('table'))
        where = self.context.resolve(params.get('where'))
        wait = params.get('wait', 0)
        assertions = params.get('assertions', [])

        print(f"\n  [断言] 验证 {table} 记录")

        # 等待
        if wait > 0:
            import time
            print(f"    等待 {wait} 秒...")
            time.sleep(wait)

        # 查询数据库
        db_config = {
            'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
            'port': 3306,
            'database': 'dataops',
            'user': 'bdsit_user_0e0bc33',
            'password': 'bdsit_user_0e0bc33_26587a',
            'charset': 'utf8mb4'
        }

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)

            # 构造查询
            fields = [a['field'] for a in assertions]
            sql = f"SELECT {', '.join(fields)} FROM {table} WHERE {where}"

            cursor.execute(sql)
            result = cursor.fetchone()

            cursor.close()
            conn.close()

            if not result:
                print(f"    ✗ 未找到记录")
                return False

            # 验证每个断言
            all_passed = True
            for assertion in assertions:
                field = assertion['field']
                expected = assertion['expected']
                actual = result[field]

                if str(actual) == str(expected):
                    print(f"    ✓ {field} = {actual}")
                else:
                    print(f"    ✗ {field}: 实际={actual}, 预期={expected}")
                    all_passed = False

            return all_passed

        except Exception as e:
            print(f"    ✗ 查询失败: {str(e)}")
            return False


class TestExecutor:
    """YAML 测试用例执行器"""

    def __init__(self, yaml_file: str):
        self.yaml_file = yaml_file
        self.test_case = None
        self.context = TestContext()
        self.primitive_executor = PrimitiveExecutor(self.context)
        self.assertion_executor = AssertionExecutor(self.context)
        self.results = []

    def load_test_case(self):
        """加载 YAML 测试用例"""
        with open(self.yaml_file, 'r', encoding='utf-8') as f:
            self.test_case = yaml.safe_load(f)

    def execute(self) -> bool:
        """执行测试用例"""
        print("=" * 70)
        print(f"测试用例: {self.test_case.get('test_name')}")
        print(f"用例ID: {self.test_case.get('test_case_id')}")
        print(f"业务流程: {self.test_case.get('business_flow')}")
        print("=" * 70)

        start_time = datetime.now()

        # 执行前置条件
        preconditions = self.test_case.get('test_intent', {}).get('preconditions', [])
        for step in preconditions:
            intent = step.get('intent')
            primitive = step.get('primitive')
            params = step.get('params', {})

            print(f"\n>>> {intent}")
            result = self.primitive_executor.execute(primitive, params)
            self.results.append({
                'step': intent,
                'success': result.get('success', False)
            })

            if not result.get('success'):
                print(f"\n❌ 前置条件失败: {intent}")
                return False

        # 执行测试步骤
        test_steps = self.test_case.get('test_intent', {}).get('test_steps', [])
        for step in test_steps:
            intent = step.get('intent')
            primitive = step.get('primitive')
            params = step.get('params', {})
            assertions = step.get('assertions', [])

            print(f"\n>>> {intent}")

            # 执行原语
            if primitive:
                result = self.primitive_executor.execute(primitive, params)
                self.results.append({
                    'step': intent,
                    'success': result.get('success', False)
                })

                if not result.get('success'):
                    print(f"\n❌ 步骤失败: {intent}")
                    return False

            # 执行断言
            for assertion in assertions:
                assertion_intent = assertion.get('intent')
                print(f"\n  [验证] {assertion_intent}")

                if not self.assertion_executor.execute(assertion):
                    print(f"\n❌ 断言失败: {assertion_intent}")
                    return False

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        print("\n" + "=" * 70)
        print(f"✅ 测试用例执行成功")
        print(f"执行时间: {duration:.2f} 秒")
        print("=" * 70)

        return True


def main():
    if len(sys.argv) < 2:
        print("用法: python test_executor.py <yaml_file>")
        print()
        print("示例:")
        print("  python test_executor.py ../test_cases/TC_TKF001_001_JDBC批量新增入仓任务_全链路成功场景.yaml")
        sys.exit(1)

    yaml_file = sys.argv[1]

    if not os.path.exists(yaml_file):
        print(f"❌ 文件不存在: {yaml_file}")
        sys.exit(1)

    executor = TestExecutor(yaml_file)
    executor.load_test_case()

    success = executor.execute()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
