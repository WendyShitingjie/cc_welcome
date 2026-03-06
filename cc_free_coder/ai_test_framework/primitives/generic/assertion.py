"""校验原语（通用原语）"""
from typing import Any, Dict
from ..base import ExecutionPrimitive, PrimitiveMetadata


class AssertEqualsPrimitive(ExecutionPrimitive):
    """相等断言原语"""

    metadata = PrimitiveMetadata(
        name='assert_equals',
        category='assertion',
        description='断言两个值相等',
        parameters=[
            {
                'name': 'actual',
                'type': 'any',
                'required': True,
                'description': '实际值（支持表达式如${user.user_id}）'
            },
            {
                'name': 'expected',
                'type': 'any',
                'required': True,
                'description': '期望值'
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

        # 解析实际值（支持表达式）
        actual = params['actual']
        if isinstance(actual, str) and actual.startswith('${'):
            actual = context.get(actual)

        expected = params['expected']

        if actual == expected:
            return {
                'status': 'PASS',
                'reason': f'断言通过: {actual} == {expected}',
                'details': {
                    'actual': actual,
                    'expected': expected
                }
            }
        else:
            return {
                'status': 'FAIL',
                'reason': f'断言失败: {actual} != {expected}',
                'details': {
                    'actual': actual,
                    'expected': expected
                }
            }


class AssertBusinessRulePrimitive(ExecutionPrimitive):
    """业务规则断言原语"""

    metadata = PrimitiveMetadata(
        name='assert_business_rule',
        category='assertion',
        description='根据业务规则验证结果',
        parameters=[
            {
                'name': 'rule_id',
                'type': 'str',
                'required': True,
                'description': '业务规则ID（如BR_001）'
            },
            {
                'name': 'context_data',
                'type': 'dict',
                'required': False,
                'description': '上下文数据（不传则使用当前上下文）'
            }
        ],
        returns={
            'status': 'PASS/FAIL',
            'details': '校验详情'
        },
        related_business_rules=['BR_001']
    )

    def execute(self, context, **params) -> Dict[str, Any]:
        """执行业务规则校验"""
        self.validate_parameters(params)

        rule_id = params['rule_id']
        context_data = params.get('context_data') or context.variables

        # 根据规则ID执行不同的校验逻辑
        if rule_id == 'BR_001':
            return self._validate_br001(context_data, context)
        else:
            raise ValueError(f"未实现的业务规则: {rule_id}")

    def _validate_br001(self, data: Dict, context) -> Dict[str, Any]:
        """
        验证BR_001：剧本生成规则

        规则要求：
        1. 剧本必须包含：沟通对象、沟通身份、沟通策略
        2. 根据用户特征验证策略合理性
        """
        # 获取剧本内容
        script_content = data.get('ai_script', {}).get('value', {}).get('script_content', '')

        if not script_content:
            return {
                'status': 'FAIL',
                'reason': '剧本内容为空',
                'details': {}
            }

        # 基础结构校验
        required_parts = ['沟通对象', '沟通身份', '沟通策略']
        missing_parts = []

        for part in required_parts:
            if part not in script_content:
                missing_parts.append(part)

        if missing_parts:
            return {
                'status': 'FAIL',
                'reason': f"剧本缺少必要部分: {', '.join(missing_parts)}",
                'details': {
                    'required': required_parts,
                    'missing': missing_parts
                }
            }

        # 业务逻辑校验
        user = data.get('current_user', {}).get('value', {})
        overdue_days = user.get('overdue_days', 0)

        validation_details = []

        # 规则1：逾期天数影响策略
        if overdue_days <= 7:
            if '提醒' not in script_content and '帮助' not in script_content:
                validation_details.append({
                    'rule': '首次逾期应侧重提醒和帮助',
                    'status': 'FAIL',
                    'actual': '剧本中未包含"提醒"或"帮助"'
                })
            else:
                validation_details.append({
                    'rule': '首次逾期应侧重提醒和帮助',
                    'status': 'PASS'
                })

        # 汇总结果
        failed_rules = [d for d in validation_details if d['status'] == 'FAIL']

        if failed_rules:
            return {
                'status': 'FAIL',
                'reason': f"有{len(failed_rules)}条业务规则校验失败",
                'details': validation_details
            }
        else:
            return {
                'status': 'PASS',
                'reason': '所有业务规则校验通过',
                'details': validation_details
            }

