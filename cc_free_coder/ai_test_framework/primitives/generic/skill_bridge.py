"""
Skill 桥接原语 (TKP 专属版)

功能：
1. 专门处理以 TKP_ 开头的物理组件。
2. 动态映射到 /skills 目录下的 Python 脚本执行。
3. 自动同步执行结果到 Context 上下文。

位置：ai_test_framework/primitives/generic/skill_bridge.py
"""

import os
import re
import json
import yaml
import subprocess
from typing import Any, Dict, Optional
from pathlib import Path
from ..base import ExecutionPrimitive, PrimitiveMetadata
import mysql.connector


class SkillBridgePrimitive(ExecutionPrimitive):
    """
    Skill 桥接原语
    """

    metadata = PrimitiveMetadata(
        name='skill_bridge',  # 执行器 executor.py 通过此名称 get()
        category='skill',  # 原语类型标记为 skill
        description='桥接执行本地 Python Skill 脚本',
        parameters=[
            {
                'name': 'component_id',
                'type': 'str',
                'required': True,
                'description': '组件ID（必须以 TKP_ 开头）'
            }
        ],
        returns={
            'status': 'SUCCESS/FAIL',
            'data': '执行详情',
            'message': '描述信息'
        }
    )

    def __init__(self):
        super().__init__()
        # 1. 路径初始化
        self.project_root = Path(__file__).resolve().parents[3]
        self.skills_dir = self.project_root / "skills"
        # 组件 MD 所在目录
        self.components_dir = self.project_root / "JBDC入仓" / "BIZ_REQ_33706_001_批量入仓_新增任务" / "components"

        self._component_cache = {}

    def execute(self, context, component_id: str, **params) -> Dict[str, Any]:
        """主执行入口"""
        try:
            # 路由检查
            if not component_id.startswith('TKP_'):
                return {'status': 'FAIL', 'message': f'SkillBridge 不处理非 TKP 原语: {component_id}'}

            print(f"\n[SkillBridge] ⚡ 桥接执行: {component_id}")

            # 1. 解析组件 MD 获取 associated_skill
            metadata = self._load_metadata(component_id)
            if not metadata:
                return {'status': 'FAIL', 'message': f'未找到组件 {component_id} 的 MD 定义'}

            skill_name = metadata.get('associated_skill')
            if not skill_name:
                return {'status': 'FAIL', 'message': f'组件 {component_id} 未定义 associated_skill'}

            # 2. 查找并调用处理器 (Handler)
            handler = self._get_handler(component_id)
            result = handler(skill_name, context, params)

            # 3. 如果成功，自动同步 Context 变量
            if result.get('status') == 'SUCCESS' and result.get('context_updates'):
                for key, value in result['context_updates'].items():
                    context.set(key, value)
                    print(f"   ✓ [Context] 更新变量: {key}")

            return result

        except Exception as e:
            return {'status': 'FAIL', 'message': f'桥接异常: {str(e)}'}

    def _get_handler(self, component_id: str):
        """路由映射表：将组件 ID 绑定到具体的方法"""
        handlers = {
            'TKP_001': self._handle_tkp_001_test_table,  # 造数
            'TKP_002': self._handle_tkp_002_metadata_complete,  # 元数据
            'TKP_003': self._handle_tkp_003_excel_gen,  # 生成Excel
            'TKP_004': self._handle_tkp_004_mq_sender,  # 发送MQ

            # --- 🚀 未来扩展示例 ---
            # 'TKP_005': self._handle_tkp_005_new_skill_sample,
        }

        func = handlers.get(component_id)
        if not func:
            raise NotImplementedError(f"组件 {component_id} 的桥接逻辑尚未实现")
        return func

    # -------------------------------------------------------------------------
    # 核心处理方法 (具体的 Skill 桥接)
    # -------------------------------------------------------------------------

    def _handle_tkp_001_test_table(self, skill, context, params):
        """TKP_001 桥接：物理表造数"""
        # 从 params 或 instruction 中提取业务逻辑
        env = params.get('default_instance', 'cjjcommon')
        instruction = params.get('instruction', '')
        count = int(re.search(r'(\d+)', instruction).group(1)) if re.search(r'(\d+)', instruction) else 1

        script = self.skills_dir / skill / "scripts" / "index.py"
        created_tables = []
        from datetime import datetime
        ts = datetime.now().strftime("%m%d%H%M")

        for i in range(count):
            table_name = f"batch_test_{ts}_{i + 1:02d}"
            # 物理调用子进程
            cmd = ['python3', str(script), 'generate', '--tableName', table_name, '--execute', '--env', env]
            cp = subprocess.run(cmd, capture_output=True, text=True)
            if cp.returncode == 0:
                created_tables.append(table_name)
            else:
                return {'status': 'FAIL', 'message': f'造数失败: {cp.stderr}'}

        return {
            'status': 'SUCCESS',
            'context_updates': {
                'created_tables': created_tables,
                'instance_name': env,
                'db_name': params.get('default_db', 'dataops_shitingjie')
            }
        }

    def _handle_tkp_002_metadata_complete(self, skill, context, params):
        """TKP_002 桥接：元数据补全"""
        tables = params.get('tables') or context.get('created_tables')
        instance = params.get('instance_name') or context.get('instance_name')

        script = self.skills_dir / skill / "scripts" / "index.py"
        for table in tables:
            cmd = ['python3', str(script), '--instance', instance, '--database', 'dataops_shitingjie', '--table', table]
            subprocess.run(cmd, check=True)

        return {'status': 'SUCCESS', 'message': f'已补全 {len(tables)} 张表的元数据'}

    def _handle_tkp_003_excel_gen(self, skill, context, params):
        """TKP_003 桥接：Excel 模板生成"""
        tables = params.get('tables') or context.get('created_tables')
        instance = params.get('instance_name') or context.get('instance_name')

        script = self.skills_dir / skill / "scripts" / "template_updater.py"
        cmd = ['python3', str(script), instance, 'dataops_shitingjie', *tables, '--db-type', 'mysql']

        # template_updater 通常在当前目录生成文件，注意设置 cwd
        cp = subprocess.run(cmd, capture_output=True, text=True, cwd=script.parent)

        if cp.returncode == 0:
            file_path = self.project_root / "JBDC入仓" / "BIZ_REQ_33706_001_批量入仓_新增任务" / "test_data" / "batch_test_latest.xlsx"
            return {
                'status': 'SUCCESS',
                'context_updates': {'test_file_path': str(file_path)},
                'message': 'Excel文件已生成'
            }
        return {'status': 'FAIL', 'message': '生成Excel失败'}

        # -------------------------------------------------------------------------
        # TKP_004 (mq-sender) 深度优化：完全基于协议文档
        # -------------------------------------------------------------------------

    def _handle_tkp_004_mq_sender(self, skill, context, params):
        """TKP_004: MQ 审批信号发送 (优化正则版)"""
        import mysql.connector

        task_id = params.get('taskId') or context.get('taskId')
        instruction = params.get('instruction', '')
        status = 'STATUS_REJECTED' if '拒绝' in instruction else 'STATUS_APPROVED'

        # 1. ⭐ 更加强大的正则匹配逻辑
        ref_path = self.skills_dir / skill / "references" / "JDBC批量入仓_新增任务审批_消息构造协议.md"
        mq_config = {"cluster": "", "queue": ""}

        if ref_path.exists():
            with open(ref_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # 解释：匹配 "Queue"，忽略前后可能存在的星号、空格和反引号，提取核心字符串
                q_match = re.search(r'Queue[*\s]*[:：][*\s`]*([a-zA-Z0-9._\-]+)', content, re.IGNORECASE)
                c_match = re.search(r'Cluster[*\s]*[:：][*\s`]*([a-zA-Z0-9._\-]+)', content, re.IGNORECASE)

                if q_match: mq_config["queue"] = q_match.group(1)
                if c_match: mq_config["cluster"] = c_match.group(1)

        # 增加一个二次确认的打印，方便你调试
        print(f"      📖 协议解析结果: Cluster={mq_config['cluster']}, Queue={mq_config['queue']}")

        if not mq_config["queue"]:
            return {'status': 'FAIL', 'message': f'从协议文档解析 Queue 失败，请检查文档格式'}

        # 2. 数据库查询逻辑 (保持不变)
        db_info = {
            'host': 'bigdata-biz.db.ali-bj-bdsit01.shuheo.net',
            'database': 'dataops',
            'user': 'bdsit_user_0e0bc33',
            'password': 'bdsit_user_0e0bc33_26587a'
        }

        try:
            conn = mysql.connector.connect(**db_info)
            cursor = conn.cursor(dictionary=True)
            sql = """
                SELECT r.bpm_process_id AS processInstId, r.order_no AS orderNo, t.file_name AS file_name
                FROM dataops_bpm_record r
                INNER JOIN dataops_batch_operation_task t ON r.process_instance_node_id = t.id
                WHERE r.process_key = 'bg_jdbc_rc_plxz_rw' AND r.process_instance_node_id = %s AND r.status = 2
            """
            cursor.execute(sql, (task_id,))
            db_res = cursor.fetchone()
            cursor.close()
            conn.close()

            if not db_res:
                return {'status': 'FAIL', 'message': f'未找到 taskId={task_id} 的待审批工单'}

            # 3. 构造报文并执行 (cluster_name 对应协议中的 Cluster)
            payload = {
                "cluster_name": mq_config["cluster"],
                "queue": mq_config["queue"],
                "payload_dict": {
                    "startUid": "71e8b23d-45e2-497a-b247-f5b807fb4f65",
                    "orderNo": db_res['orderNo'],
                    "dataMap": {
                        "fileName": db_res['file_name'],
                        "sceneType": "jdbcInputBatchAddTask",
                        "batchTaskId": str(task_id),
                        "taskId": str(task_id),
                        "scene": "批量新增任务"
                    },
                    "processInstId": db_res['processInstId'],
                    "status": status
                }
            }

            script = self.skills_dir / skill / "scripts" / "mq_sender.py"
            cmd = ['python3', str(script), json.dumps(payload, ensure_ascii=False)]
            cp = subprocess.run(cmd, capture_output=True, text=True)

            if cp.returncode == 0 and "success" in cp.stdout.lower():
                print(f"      ✅ MQ 信号发送成功: {status}")
                return {'status': 'SUCCESS'}
            else:
                return {'status': 'FAIL', 'message': f'MQ脚本返回错误: {cp.stdout or cp.stderr}'}

        except Exception as e:
            return {'status': 'FAIL', 'message': f'MQ 处理异常: {str(e)}'}
    # -------------------------------------------------------------------------
    # 💡 扩展样例：如何增加一个新的 Skill (TKP_005)
    # -------------------------------------------------------------------------
    def _handle_tkp_xxx_new_skill_sample(self, skill, context, params):
        """
        扩展步骤：
        1. 在 _get_handler 的 handlers 字典中添加 'TKP_005': self._handle_tkp_005_xxx
        2. 实现本方法：
           - 从 params 获取 YAML 里的参数
           - 从 context 获取之前步骤存下的变量
           - 使用 subprocess 调用对应的 skill 脚本
           - 返回结果字典，如有需要更新的变量放入 context_updates
        """
        # 示例逻辑
        # arg1 = params.get('some_param')
        # cmd = ['python3', str(self.skills_dir / skill / 'xxx.py'), arg1]
        # subprocess.run(cmd)
        return {'status': 'SUCCESS', 'message': '新组件执行成功'}

    # -------------------------------------------------------------------------
    # 内部工具
    # -------------------------------------------------------------------------

    def _load_metadata(self, cid: str) -> Optional[Dict]:
        """读取 MD 头部 YAML 定义"""
        if cid in self._component_cache:
            return self._component_cache[cid]

        target_files = list(self.components_dir.glob(f"{cid}_*.md"))
        if not target_files:
            return None

        with open(target_files[0], 'r', encoding='utf-8') as f:
            match = re.search(r'^---\s*\n(.*?)\n---', f.read(), re.DOTALL | re.MULTILINE)
            if match:
                data = yaml.safe_load(match.group(1))
                self._component_cache[cid] = data
                return data
        return None


# 单例导出
skill_bridge = SkillBridgePrimitive()
