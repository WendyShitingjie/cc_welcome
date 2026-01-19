import json

# 文件路径
file_path = 'tezheng.json'
consistent_count = 0
inconsistent_count = 0

with open(file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# 遍历字典，检查每个值中clc和rt的时间戳是否一致
for key, value in data.items():
    if key not in ["total_count", "error_count"]:
        # 提取clc和rt的时间部分
        clc_time_str = value.split("clc:")[1].split(" rt:")[0]
        rt_time_str = value.split("rt:")[1]

        # 比较clc和rt的时间戳
        if clc_time_str == rt_time_str:
            consistent_count += 1
        else:
            inconsistent_count += 1
            print(f"不一致的条目: {key}, old: {clc_time_str}, new: {rt_time_str}")


print(f"\n一致的数量: {consistent_count}")
print(f"不一致的数量: {inconsistent_count}")
