"""原语库初始化

三层原语架构：
1. 通用原语层 (Generic Primitives) - 高度抽象，跨业务复用
2. 业务原语层 (Business Primitives) - 针对特定业务，封装业务逻辑
3. 基础设施层 (Infrastructure) - 数据库连接、HTTP客户端等
"""

# 导入注册表
from .primitive_registry import PrimitiveRegistry, primitive_registry

# 导入注册函数
from .primitives_config import register_all_primitives

__all__ = [
    'PrimitiveRegistry',
    'primitive_registry',
    'register_all_primitives'
]
