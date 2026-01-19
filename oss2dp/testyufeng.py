import csv

# 定义CSV数据
data = [
    ["config_params", "basic_info"],
    [
        '{"version": "2.3.1","components": {"name": "parser","settings": {"encoding": "UTF-8","batch_size": 500}}}',
        '{"department": "devops", "env": "production"}'
    ]
]

file_path = "/Users/liyufeng/Desktop/ossTestFiles/jsonOutPut.csv"  # Linux/Mac

with open(file_path, 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file, delimiter='|')
    writer.writerows(data)

print("CSV文件已生成：jsonOutPut.csv")