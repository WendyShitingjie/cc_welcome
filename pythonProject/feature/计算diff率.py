import pandas as pd
file_path = 'diff2.csv'  # 请替换为你的CSV文件路径
df = pd.read_csv(file_path)

# 步骤2: 计数
total_count = len(df)  # 总行数
diff_count = df['ym_adt_initiate_no_urge_v5_Comparison'].eq('diff').sum()  # 假设需要分析的列名为'column_name'

# 步骤3: 计算比例
diff_percentage = (diff_count / total_count) * 100  # 转换为百分比

print(f"'diff'的占比为: {diff_percentage}%")
