import csv
from datetime import datetime

headers = ['id', 'name', 'salary', 'department', 'hire_date']
data = [
    [1, '张三', 8500.50, '技术部', '2023-01-15'],
    [2, '李四(Amy)', 9200.0, '财务部', '2022-07-23'],
    [3, '王五', None, '市场部', '2024-03-01'],  # 包含空值
    [4, 'Emma "Smith"', 7800.75, 'HR', '2021-12-31']
]

with open('employees.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(data)