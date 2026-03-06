"""数据库操作原语（通用原语）"""
from typing import Any, Dict, List
from ..base import ExecutionPrimitive, PrimitiveMetadata
from ...utils.database import DatabaseConnection


class DatabaseInsertPrimitive(ExecutionPrimitive):
    """数据库插入原语"""

    metadata = PrimitiveMetadata(
        name='database_insert',
        category='database',
        description='向数据库表插入数据',
        parameters=[
            {
                'name': 'database',
                'type': 'str',
                'required': True,
                'description': '数据库名称'
            },
            {
                'name': 'table',
                'type': 'str',
                'required': True,
                'description': '表名'
            },
            {
                'name': 'data',
                'type': 'dict or list',
                'required': True,
                'description': '要插入的数据（单条记录用dict，多条记录用list）'
            }
        ],
        returns={
            'inserted_count': '插入的记录数'
        },
        examples=[
            {
                'description': '插入单条记录',
                'code': '''database_insert(
    database="copilot",
    table="common_job_status",
    data={
        "job_name": "AiScriptUidPullJob",
        "business_type": "postLoan",
        "status": "FAIL",
        "complete_count": 2
    }
)'''
            },
            {
                'description': '插入多条记录',
                'code': '''database_insert(
    database="copilot",
    table="ai_script_recommendation_log",
    data=[
        {"source": "postLoan", "execute_status": "INIT"},
        {"source": "postLoan", "execute_status": "INIT"}
    ]
)'''
            }
        ]
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行数据库插入"""
        self.validate_parameters(params)

        database = params['database']
        table = params['table']
        data = params['data']

        # 统一处理为列表
        if isinstance(data, dict):
            data_list = [data]
        elif isinstance(data, list):
            data_list = data
        else:
            raise ValueError(f"data参数必须是dict或list类型，实际类型: {type(data)}")

        if not data_list:
            return {
                'status': 'SUCCESS',
                'inserted_count': 0,
                'message': '没有数据需要插入'
            }

        inserted_count = 0

        for record in data_list:
            try:
                # 构建INSERT语句
                columns = list(record.keys())
                placeholders = ', '.join(['%s'] * len(columns))
                column_names = ', '.join(columns)

                sql = f"""
                    INSERT INTO {database}.{table} ({column_names})
                    VALUES ({placeholders})
                """

                values = tuple(record[col] for col in columns)

                # 执行插入
                DatabaseConnection.execute_update(database, sql, values)
                inserted_count += 1

            except Exception as e:
                print(f"    ⚠️  插入记录失败: {e}")
                print(f"    记录: {record}")
                # 继续处理下一条记录

        return {
            'status': 'SUCCESS' if inserted_count > 0 else 'FAIL',
            'inserted_count': inserted_count,
            'message': f'成功插入 {inserted_count}/{len(data_list)} 条记录'
        }

