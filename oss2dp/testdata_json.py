import json

data = [
    {
        "product_id": "A001",
        "name": "无线鼠标",
        "specs": {
            "color": "黑色",
            "dpi": [800, 1600, 2400],
            "interface": ["USB", "蓝牙"]
        },
        "stock": 150
    },
    {
        "product_id": "B002",
        "name": "机械键盘",
        "specs": None,  # 测试空值
        "stock": 0
    }
]

with open('products.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


