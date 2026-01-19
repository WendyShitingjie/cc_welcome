import random
import string


def generate_combination():
    """
    生成1-10000的随机整数与随机小写字母的组合

    :return: 字符串格式的组合结果（如"732k"或"b491"）
    """
    # 生成1-1000的随机整数
    number = random.randint(1, 10000)

    # 生成随机小写字母
    letter = random.choice(string.ascii_lowercase)

    # 随机决定组合顺序（50%概率字母在前）
    if random.random() > 0.5:
        return f"{letter}{number}"
    else:
        return f"{number}{letter}"


# 示例输出
print("自动化测试随机名称"+generate_combination())  # 输出示例：'823x' 或 'r572'