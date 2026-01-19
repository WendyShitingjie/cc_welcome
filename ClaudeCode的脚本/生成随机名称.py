import random
import string


def generate_random_name(length=8, include_digits=True, include_letters=True):
    """
    生成包含字母和数字的随机名称

    参数:
        length: 名称长度，默认8个字符
        include_digits: 是否包含数字，默认True
        include_letters: 是否包含字母，默认True

    返回:
        随机生成的名称字符串
    """
    characters = ''

    if include_letters:
        characters += string.ascii_letters  # 包含大小写字母

    if include_digits:
        characters += string.digits  # 包含数字0-9

    if not characters:
        raise ValueError("至少需要包含字母或数字")

    return ''.join(random.choices(characters, k=length))


def generate_random_name_with_pattern(letter_count=5, digit_count=3):
    """
    按指定模式生成随机名称：先字母后数字

    参数:
        letter_count: 字母个数，默认5个
        digit_count: 数字个数，默认3个

    返回:
        格式为"字母+数字"的随机名称
    """
    letters = ''.join(random.choices(string.ascii_letters, k=letter_count))
    digits = ''.join(random.choices(string.digits, k=digit_count))
    return letters + digits


def generate_random_name_mixed(length=8, min_letters=3, min_digits=2):
    """
    生成混合排列的随机名称，确保至少包含指定数量的字母和数字

    参数:
        length: 总长度，默认8个字符
        min_letters: 最少字母数，默认3个
        min_digits: 最少数字数，默认2个

    返回:
        随机混合排列的名称
    """
    if min_letters + min_digits > length:
        raise ValueError("最少字母数和数字数之和不能超过总长度")

    # 生成必需的字母和数字
    letters = random.choices(string.ascii_letters, k=min_letters)
    digits = random.choices(string.digits, k=min_digits)

    # 填充剩余位置
    remaining = length - min_letters - min_digits
    if remaining > 0:
        mixed = random.choices(string.ascii_letters + string.digits, k=remaining)
        all_chars = letters + digits + mixed
    else:
        all_chars = letters + digits

    # 随机打乱顺序
    random.shuffle(all_chars)
    return ''.join(all_chars)


def batch_generate_names(count=10, **kwargs):
    """
    批量生成随机名称

    参数:
        count: 生成数量，默认10个
        **kwargs: 传递给generate_random_name的其他参数

    返回:
        名称列表
    """
    return [generate_random_name(**kwargs) for _ in range(count)]


if __name__ == "__main__":
    print("=" * 50)
    print("随机名称生成器")
    print("=" * 50)

    # 示例1: 生成默认长度的随机名称
    print("\n1. 生成10个默认长度(8位)的随机名称:")
    for i, name in enumerate(batch_generate_names(10), 1):
        print(f"   {i}. {name}")

    # 示例2: 生成指定长度的随机名称
    print("\n2. 生成5个12位的随机名称:")
    for i, name in enumerate(batch_generate_names(5, length=12), 1):
        print(f"   {i}. {name}")

    # 示例3: 只包含小写字母和数字
    print("\n3. 生成5个只包含小写字母和数字的名称:")
    for i in range(5):
        chars = string.ascii_lowercase + string.digits
        name = ''.join(random.choices(chars, k=10))
        print(f"   {i+1}. {name}")

    # 示例4: 使用固定模式(字母+数字)
    print("\n4. 生成5个固定模式(5字母+3数字)的名称:")
    for i in range(5):
        name = generate_random_name_with_pattern(5, 3)
        print(f"   {i+1}. {name}")

    # 示例5: 混合模式，确保至少包含指定数量的字母和数字
    print("\n5. 生成5个混合模式(总长10位，至少4字母+3数字)的名称:")
    for i in range(5):
        name = generate_random_name_mixed(10, 4, 3)
        print(f"   {i+1}. {name}")

    # 示例6: 生成唯一名称集合
    print("\n6. 生成20个唯一的随机名称:")
    unique_names = set()
    while len(unique_names) < 20:
        unique_names.add(generate_random_name(10))

    for i, name in enumerate(sorted(unique_names), 1):
        print(f"   {i}. {name}")
