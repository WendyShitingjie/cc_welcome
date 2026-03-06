"""原语注册表"""
from typing import Dict, List, Type
from .base import ExecutionPrimitive


class PrimitiveRegistry:
    """原语注册表"""

    _instance = None
    _primitives: Dict[str, ExecutionPrimitive] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def register(self, primitive_class: Type[ExecutionPrimitive]):
        """
        注册原语

        Args:
            primitive_class: 原语类
        """
        primitive = primitive_class()
        self._primitives[primitive.metadata.name] = primitive

    def get(self, name: str) -> ExecutionPrimitive:
        """
        获取原语

        Args:
            name: 原语名称

        Returns:
            ExecutionPrimitive: 原语实例
        """
        if name not in self._primitives:
            raise ValueError(f"原语不存在: {name}")
        return self._primitives[name]

    def list_all(self) -> List[Dict]:
        """列出所有原语"""
        return [
            {
                'name': p.metadata.name,
                'category': p.metadata.category,
                'description': p.metadata.description
            }
            for p in self._primitives.values()
        ]

    def list_by_category(self, category: str) -> List[Dict]:
        """按分类列出原语"""
        return [
            {
                'name': p.metadata.name,
                'description': p.metadata.description
            }
            for p in self._primitives.values()
            if p.metadata.category == category
        ]


# 全局注册表实例
primitive_registry = PrimitiveRegistry()

