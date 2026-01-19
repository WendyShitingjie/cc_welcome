import pandas as pd


def convert_separator(input_file, output_file, new_sep):
    # 显式指定原始分隔符（避免自动检测失败）
    df = pd.read_csv(input_file, sep=',')  # 强制指定逗号分隔

    # 处理含分隔符的内容
    df.to_csv(output_file,
              sep=new_sep,
              index=False,
              encoding='utf-8-sig',
              quotechar='"',  # 包裹含分隔符的字段
              escapechar='\\'  # 转义特殊字符
              )
convert_separator('users.csv', 'users1.csv', '*')
