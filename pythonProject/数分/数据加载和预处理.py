import random
import string

def generate_random_string(length):
    letters = string.ascii_lowercase  # 获取所有小写字母
    result = ''.join(random.choice(letters) for _ in range(length))  # 随机选择字母并组合成指定长度的字符串
    return result

random_string = generate_random_string(5)
print(random_string)