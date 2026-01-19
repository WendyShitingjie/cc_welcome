
with open('test3h.txt', 'r') as file:
    lines = file.readlines()

selected_lines = [line.strip() for line in lines if line.strip().endswith(",2")]
# 输出匹配结果
for line in selected_lines:
    print(line)