import pandas as pd


# 假设 maindf 是您的主要 DataFrame，并且已经包含了上面的数据
# 假设 dimensiondf 是您的维度 DataFrame

# 为了避免递归，我们可以创建一个字典来存储每个ID及其子ID的累积总和
def calculate_values_non_recursive(df):
    # 初始化一个字典来存储每个ID的值累积
    value_dict = {}
    for index, row in df.iterrows():
        value_dict[row['管报ID']] = 0
        value_dict[row['父ID']] = 0
    # 将每个ID的值存入字典
    for index, row in df.iterrows():
        value_dict[row['管报ID']] += row['值']

    # 从底层向上累加值
    for _, row in df.iterrows():
        current_id = row['管报ID']
        parent_id = row['父ID']
        # 只要存在父ID，就累加当前ID的值到其父ID
        while pd.notnull(parent_id) and parent_id in value_dict:
            value_dict[parent_id] += value_dict[current_id]
            # 为了避免死循环，需要找到新的父ID
            if parent_id in df['管报ID'].values:
                current_id = parent_id
                parent_id = df.loc[df['管报ID'] == current_id, '父ID'].values[0]
            else:
                break

def reportpivot(df_dict):
    # 先拷贝一份数据
    maindf = df_dict['maindf']
    dimensiondf = df_dict['dimensiondf']
    df = maindf.copy()

    # 计算非递归的值
    calculate_values_non_recursive(df)

    # 创建透视表
    pivot_table = df.pivot_table(index='管报ID', columns='国家名称', values='值', aggfunc='sum').fillna(0)

    # 重置索引，以便合并
    pivot_table.reset_index(inplace=True)

    # 合并透视表与dimensiondf
    final_df = pd.merge(dimensiondf, pivot_table, left_on='mr_code', right_on='管报ID', how='left').fillna(0)

    # 删除额外的'管报ID'列，因为'mr_code'已提供相同的信息
    final_df.drop(columns=['管报ID'], inplace=True)

    return final_df

