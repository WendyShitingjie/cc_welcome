"""意图解析引擎"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel
import json


class ParsedIntent(BaseModel):
    """解析后的意图"""
    primitive: str  # 原语名称
    parameters: Dict[str, Any]  # 参数
    business_rules: List[str] = []  # 关联的业务规则
    data_models: List[str] = []  # 关联的数据模型
    reasoning: str = ""  # 推理过程


class IntentParser:
    """意图解析引擎"""

    def __init__(self, llm_client, knowledge_base):
        """
        初始化意图解析器

        Args:
            llm_client: LLM客户端
            knowledge_base: 知识库
        """
        self.llm = llm_client
        self.kb = knowledge_base

    def parse(self, test_intent: Dict[str, Any]) -> ParsedIntent:
        """
        解析测试意图

        Args:
            test_intent: 测试意图字典，包含:
                - intent: 意图描述
                - business_context: 业务上下文（可选）
                - primitive: 指定的原语（可选）
                - params: 参数（可选）

        Returns:
            ParsedIntent: 解析后的意图
        """
        # 如果已经指定了原语，直接返回
        if 'primitive' in test_intent:
            return ParsedIntent(
                primitive=test_intent['primitive'],
                parameters=test_intent.get('params', {}),
                business_rules=test_intent.get('business_rules', []),
                data_models=test_intent.get('data_models', [])
            )

        # 否则使用AI解析
        return self._parse_with_ai(test_intent)

    def _parse_with_ai(self, test_intent: Dict[str, Any]) -> ParsedIntent:
        """使用AI解析意图"""

        # 1. 构建提示词
        prompt = self._build_prompt(test_intent)

        # 2. 调用LLM
        llm_response = self.llm.chat(prompt)

        # 3. 解析LLM响应
        parsed = self._parse_llm_response(llm_response)

        # 4. 验证和补全
        validated = self._validate_and_enrich(parsed)

        return validated

    def _build_prompt(self, test_intent: Dict[str, Any]) -> str:
        """构建LLM提示词"""

        # 加载相关知识
        b_tree = self.kb.query_b_tree(test_intent.get('business_flow'))
        a_tree = self.kb.query_a_tree(test_intent.get('business_flow'))
        primitives = self.kb.get_all_primitives()

        prompt = f"""
你是一个测试意图解析专家。请根据以下信息解析测试意图：

【测试意图】
{test_intent['intent']}

【业务上下文】
{test_intent.get('business_context', '无')}

【业务知识】
业务流程: {b_tree.get('flow_name', '未知')}
业务规则: {b_tree.get('rules', [])}

【系统知识】
实现方式: {a_tree.get('implementation', '未知')}
数据模型: {a_tree.get('data_models', [])}

【可用原语】
{self._format_primitives(primitives)}

请分析并输出：
1. 应该使用哪个原语？
2. 原语需要哪些参数？
3. 涉及哪些业务规则？
4. 涉及哪些数据模型？

输出格式（JSON）：
{{
    "primitive": "原语名称",
    "parameters": {{"参数名": "参数值"}},
    "business_rules": ["规则ID"],
    "data_models": ["模型ID"],
    "reasoning": "推理过程"
}}
"""
        return prompt

    def _format_primitives(self, primitives: List[Dict]) -> str:
        """格式化原语列表"""
        result = []
        for p in primitives:
            result.append(f"- {p['name']}: {p['description']}")
        return "\n".join(result)

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """解析LLM响应"""
        try:
            # 尝试提取JSON
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
            return json.loads(json_str)
        except Exception as e:
            raise ValueError(f"无法解析LLM响应: {e}\n响应内容: {response}")

    def _validate_and_enrich(self, parsed: Dict[str, Any]) -> ParsedIntent:
        """验证并补全解析结果"""

        # 1. 验证原语是否存在
        primitive = self.kb.get_primitive(parsed['primitive'])
        if not primitive:
            raise ValueError(f"原语不存在: {parsed['primitive']}")

        # 2. 验证参数是否完整
        required_params = primitive.get('required_parameters', [])
        for param in required_params:
            if param not in parsed['parameters']:
                # 尝试从上下文推断
                inferred = self._infer_parameter(param, parsed)
                if inferred:
                    parsed['parameters'][param] = inferred
                else:
                    raise ValueError(f"缺少必填参数: {param}")

        return ParsedIntent(**parsed)

    def _infer_parameter(self, param: str, parsed: Dict) -> Optional[Any]:
        """推断参数值"""
        # 简化实现
        return None

