import pandas as pd
import numpy as np

print("=" * 60)
print("Pandas 入门 Demo - 快速上手指南")
print("=" * 60)

# ============================================================
# 1. 创建 DataFrame（类似 Excel 表格）
# ============================================================
print("\n【1. 创建 DataFrame】")
print("-" * 60)

# 方法1: 通过字典创建
data = {
    '姓名': ['张三', '李四', '王五', '赵六', '钱七'],
    '年龄': [25, 30, 35, 28, 32],
    '城市': ['北京', '上海', '广州', '深圳', '杭州'],
    '工资': [8000, 12000, 15000, 10000, 11000]
}

df = pd.DataFrame(data)
print("创建的 DataFrame:")
print(df)

# ============================================================
# 2. 查看数据基本信息
# ============================================================
print("\n【2. 查看数据基本信息】")
print("-" * 60)

print(f"\n数据形状（行数, 列数）: {df.shape}")
print(f"总行数: {len(df)}")
print(f"列名: {list(df.columns)}")

print("\n前3行数据:")
print(df.head(3))

print("\n数据类型:")
print(df.dtypes)

print("\n数据统计摘要:")
print(df.describe())

# ============================================================
# 3. 选择数据
# ============================================================
print("\n【3. 选择和筛选数据】")
print("-" * 60)

# 选择单列
print("\n选择'姓名'列:")
print(df['姓名'])

# 选择多列
print("\n选择'姓名'和'工资'列:")
print(df[['姓名', '工资']])

# 选择行（通过索引）
print("\n选择第2到4行:")
print(df[1:4])

# 条件筛选
print("\n筛选工资大于10000的员工:")
high_salary = df[df['工资'] > 10000]
print(high_salary)

print("\n筛选年龄在30岁以上且工资大于10000的员工:")
condition = (df['年龄'] >= 30) & (df['工资'] > 10000)
print(df[condition])

# ============================================================
# 4. 添加和修改数据
# ============================================================
print("\n【4. 添加和修改数据】")
print("-" * 60)

# 添加新列
df['部门'] = ['技术部', '销售部', '技术部', '市场部', '技术部']
print("\n添加'部门'列后:")
print(df)

# 基于现有列计算新列
df['年薪'] = df['工资'] * 12
print("\n添加'年薪'列后:")
print(df)

# 修改某个值
df.loc[0, '工资'] = 8500
print("\n修改张三的工资后:")
print(df)

# ============================================================
# 5. 数据分组和聚合
# ============================================================
print("\n【5. 数据分组和聚合】")
print("-" * 60)

print("\n按部门统计平均工资:")
dept_avg = df.groupby('部门')['工资'].mean()
print(dept_avg)

print("\n按部门统计人数和平均工资:")
dept_stats = df.groupby('部门').agg({
    '姓名': 'count',
    '工资': 'mean'
}).rename(columns={'姓名': '人数', '工资': '平均工资'})
print(dept_stats)

# ============================================================
# 6. 排序
# ============================================================
print("\n【6. 数据排序】")
print("-" * 60)

print("\n按工资降序排列:")
df_sorted = df.sort_values('工资', ascending=False)
print(df_sorted[['姓名', '工资']])

print("\n按年龄升序，工资降序排列:")
df_sorted2 = df.sort_values(['年龄', '工资'], ascending=[True, False])
print(df_sorted2[['姓名', '年龄', '工资']])

# ============================================================
# 7. 常用统计函数
# ============================================================
print("\n【7. 常用统计函数】")
print("-" * 60)

print(f"平均工资: {df['工资'].mean():.2f}")
print(f"工资中位数: {df['工资'].median()}")
print(f"最高工资: {df['工资'].max()}")
print(f"最低工资: {df['工资'].min()}")
print(f"工资总和: {df['工资'].sum()}")
print(f"工资标准差: {df['工资'].std():.2f}")

# ============================================================
# 8. 处理缺失值
# ============================================================
print("\n【8. 处理缺失值】")
print("-" * 60)

# 创建带缺失值的数据
df_with_na = df.copy()
df_with_na.loc[1, '工资'] = np.nan
df_with_na.loc[3, '年龄'] = np.nan

print("\n带缺失值的数据:")
print(df_with_na)

print(f"\n各列缺失值数量:")
print(df_with_na.isnull().sum())

print("\n删除包含缺失值的行:")
print(df_with_na.dropna())

print("\n用平均值填充工资的缺失值:")
df_filled = df_with_na.copy()
df_filled['工资'].fillna(df_filled['工资'].mean(), inplace=True)
print(df_filled[['姓名', '工资']])

# ============================================================
# 9. 保存和读取文件
# ============================================================
print("\n【9. 保存和读取文件】")
print("-" * 60)

# 保存为CSV
csv_file = '/Users/wendy/PycharmProjects/ClaudeCode的脚本/员工数据.csv'
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"\n数据已保存到: {csv_file}")

# 读取CSV
df_loaded = pd.read_csv(csv_file)
print("\n从CSV文件读取的数据:")
print(df_loaded)

# 保存为Excel（需要安装 openpyxl: pip install openpyxl）
try:
    excel_file = '/Users/wendy/PycharmProjects/ClaudeCode的脚本/员工数据.xlsx'
    df.to_excel(excel_file, index=False, sheet_name='员工信息')
    print(f"\n数据已保存到: {excel_file}")
except ImportError:
    print("\n提示: 保存Excel需要安装 openpyxl，运行: pip install openpyxl")

# ============================================================
# 10. 实用小技巧
# ============================================================
print("\n【10. 实用小技巧】")
print("-" * 60)

# 列重命名
df_renamed = df.rename(columns={'姓名': 'name', '年龄': 'age'})
print("\n重命名列后:")
print(df_renamed.head())

# 删除列
df_dropped = df.drop(['年薪'], axis=1)
print("\n删除'年薪'列后:")
print(df_dropped.head())

# 去重
print("\n'部门'列的唯一值:")
print(df['部门'].unique())
print(f"部门数量: {df['部门'].nunique()}")

# 值计数
print("\n各部门人数统计:")
print(df['部门'].value_counts())

print("\n" + "=" * 60)
print("Demo 结束！你已经掌握了 Pandas 的基本操作 🎉")
print("=" * 60)
