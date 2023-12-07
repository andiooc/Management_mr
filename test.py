import pandas as pd

# 创建示例DataFrame
data = {'ID': [1, 2, 3, 4],
        'ParentID': ['-', 1, 1, 5],
        'col1': [0, 1, 1, 1],
        'col2': [0, 1, 1, 1],
        'col3': [0, 1, 1, 12],
        'level': [1, 2, 2, 2]}
df = pd.DataFrame(data)
print(df)

# 循环处理
for i in range(1, df['level'].max() + 1):
    selected_rows = df[df['level'] == i]  # 选择level字段等于i的行
    aggregated_data = selected_rows.groupby('ParentID').sum().drop('ID', axis=1)  # 根据ParentID列进行数据汇总
    print(f"When level = {i}:")
    print(aggregated_data)