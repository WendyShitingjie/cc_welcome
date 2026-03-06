"""参数解析器 - 支持变量引用和函数调用"""
import re
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List


class ParamResolver:
    """参数解析器

    支持的语法：
    1. 变量引用: ${context.batch_no} - 引用上下文中的变量
    2. 函数调用: ${uuid()} - 调用内置函数
    3. 数组引用: ${context.uids[0]} - 引用数组元素
    4. 嵌套引用: ${context.users[0].uid} - 引用嵌套对象
    """

    # 内置函数
    BUILTIN_FUNCTIONS = {
        'uuid': lambda: str(uuid.uuid4()).replace('-', ''),
        'batch_no': lambda: datetime.now().strftime('%Y%m%d') + '001',
        'serial_id': lambda: f"serial_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:8]}",
        'timestamp': lambda: datetime.now().strftime('%Y%m%d%H%M%S'),
        'date': lambda: datetime.now().strftime('%Y-%m-%d'),
        'time': lambda: datetime.now().strftime('%H:%M:%S'),
    }

    # 带参数的内置函数
    BUILTIN_FUNCTIONS_WITH_ARGS = {
        'timestamp_minus_minutes': lambda minutes: (datetime.now() - timedelta(minutes=int(minutes))).strftime(
            '%Y-%m-%d %H:%M:%S'),
        'timestamp_minus_hours': lambda hours: (datetime.now() - timedelta(hours=int(hours))).strftime(
            '%Y-%m-%d %H:%M:%S'),
        'timestamp_minus_days': lambda days: (datetime.now() - timedelta(days=int(days))).strftime('%Y-%m-%d %H:%M:%S'),
        'timestamp_plus_minutes': lambda minutes: (datetime.now() + timedelta(minutes=int(minutes))).strftime(
            '%Y-%m-%d %H:%M:%S'),
        'timestamp_plus_hours': lambda hours: (datetime.now() + timedelta(hours=int(hours))).strftime(
            '%Y-%m-%d %H:%M:%S'),
        'timestamp_plus_days': lambda days: (datetime.now() + timedelta(days=int(days))).strftime('%Y-%m-%d %H:%M:%S'),
    }

    def __init__(self, context):
        """初始化参数解析器

        Args:
            context: ExecutionContext对象
        """
        self.context = context

    def resolve(self, params: Any) -> Any:
        """解析参数（递归处理）

        Args:
            params: 参数（可以是dict、list、str等）

        Returns:
            解析后的参数
        """
        if isinstance(params, dict):
            return {k: self.resolve(v) for k, v in params.items()}
        elif isinstance(params, list):
            return [self.resolve(item) for item in params]
        elif isinstance(params, str):
            return self._resolve_string(params)
        else:
            return params

    def _resolve_string(self, value: str) -> Any:
        """解析字符串中的变量引用和函数调用

        支持的格式：
        - ${context.batch_no} - 引用上下文变量
        - ${uuid()} - 调用函数
        - ${context.uids[0]} - 引用数组元素
        - "prefix_${uuid()}_suffix" - 字符串拼接

        Args:
            value: 字符串值

        Returns:
            解析后的值
        """
        # 查找所有 ${...} 模式
        pattern = r'\$\{([^}]+)\}'
        matches = list(re.finditer(pattern, value))

        if not matches:
            return value

        # 如果整个字符串就是一个变量引用，直接返回值（保持原始类型）
        if len(matches) == 1 and matches[0].group(0) == value:
            expr = matches[0].group(1)
            return self._evaluate_expression(expr)

        # 否则进行字符串替换
        result = value
        for match in reversed(matches):  # 从后往前替换，避免索引变化
            expr = match.group(1)
            resolved_value = self._evaluate_expression(expr)
            # 转换为字符串进行替换
            result = result[:match.start()] + str(resolved_value) + result[match.end():]

        return result

    def _evaluate_expression(self, expr: str) -> Any:
        """计算表达式

        Args:
            expr: 表达式（如 "context.batch_no" 或 "uuid()" 或 "timestamp_minus_minutes(5)" 或 "owner_id"）

        Returns:
            计算结果
        """
        expr = expr.strip()

        # 1. 函数调用: uuid() 或 timestamp_minus_minutes(5)
        if '(' in expr and ')' in expr:
            func_name = expr.split('(')[0].strip()

            # 1.1 无参数函数
            if func_name in self.BUILTIN_FUNCTIONS:
                return self.BUILTIN_FUNCTIONS[func_name]()

            # 1.2 带参数函数
            elif func_name in self.BUILTIN_FUNCTIONS_WITH_ARGS:
                # 提取参数: timestamp_minus_minutes(5) -> "5"
                args_str = expr[expr.index('(') + 1:expr.rindex(')')].strip()
                if not args_str:
                    raise ValueError(f"函数 {func_name} 需要参数")
                # 支持多个参数（用逗号分隔）
                args = [arg.strip().strip('"\'') for arg in args_str.split(',')]
                return self.BUILTIN_FUNCTIONS_WITH_ARGS[func_name](*args)

            else:
                raise ValueError(f"未知函数: {func_name}")

        # 2. 上下文变量引用: context.batch_no 或 context.uids[0]
        if expr.startswith('context.'):
            path = expr[8:]  # 去掉 "context."
            return self._get_context_value(path)

        # 3. 简单变量引用（从上下文中直接读取）: owner_id, graph_code 等
        # 尝试从上下文中获取该变量
        value = self.context.get(expr)
        if value is not None:
            return value

        # 4. 响应字段引用: response.code
        if expr.startswith('response.'):
            path = expr[9:]  # 去掉 "response."
            response = self.context.get('response')
            if response:
                # 支持嵌套路径: response.data.value
                parts = path.split('.')
                current = response
                for part in parts:
                    if isinstance(current, dict):
                        current = current.get(part)
                    else:
                        current = None
                        break
                if current is not None:
                    return current

        # 5. 直接返回字符串
        return expr

    def _get_context_value(self, path: str) -> Any:
        """从上下文中获取值（支持嵌套路径和数组索引）

        Args:
            path: 路径（如 "batch_no" 或 "uids[0]" 或 "users[0].uid"）

        Returns:
            值
        """
        # 解析路径: batch_no 或 uids[0] 或 users[0].uid
        parts = re.split(r'\.|\[', path)

        # 从context.variables中获取第一个key的值
        first_key = parts[0]
        current = self.context.get(first_key)

        if current is None:
            raise ValueError(f"上下文中不存在变量: context.{first_key}")

        # 处理后续路径
        for part in parts[1:]:
            if not part:
                continue

            # 处理数组索引: "0]"
            if part.endswith(']'):
                index = int(part[:-1])
                current = current[index]
            else:
                # 处理对象属性
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    current = getattr(current, part, None)

            if current is None:
                raise ValueError(f"上下文中不存在路径: context.{path}")

        return current

