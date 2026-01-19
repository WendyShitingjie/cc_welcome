# Python数据生成示例
import json
from datetime import datetime

data = {
    "transaction_id": "TX20240315001",
    "config_params": {
        "version": "2.3.1",
        "components": [
            {"name": "parser", "settings": {"encoding": "UTF-8", "batch_size": 500}},
            {"name": "logger", "levels": ["INFO", "WARN", "ERROR"]}
        ]
    },
    "basic_info": {"department": "devops", "env": "production"}
}

with open('mixed_data.txt', 'w') as f:
    f.write(f"timestamp: {datetime.utcnow().isoformat()}Z\n")
    f.write(f"config_params: {json.dumps(data['config_params'], indent=2)}\n")
    f.write(f"basic_info: {json.dumps(data['basic_info'])}\n")