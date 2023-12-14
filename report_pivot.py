import pandas as pd


def calculate_mr_level(report_id):
    if report_id.startswith('SC'):
        return 0
    return (len(report_id) - 2) // 2  # 使用整数除法


def reportpivot(df_dict):
    maindf = df_dict['maindf']
    dimensiondf = df_dict['dimensiondf']
    itemID = df_dict['itemID']
    PitemID = df_dict['PitemID']
    col_pivot = df_dict['pivot_col']
    col_filter = df_dict['filter_col']

    # 创建一个字典用于存储每个sheetfilter对应的结果DataFrame
    sheets_result = {}

    # 获取唯一的过滤条件值
    sheet_filters = maindf[col_filter].drop_duplicates()

    # 对每个过滤条件进行操作
    for sheetfilter in sheet_filters:
        filter_maindf = maindf[maindf[col_filter] == sheetfilter]
        pivot_table = filter_maindf.pivot_table(index=[itemID, PitemID], columns=col_pivot, values='值', aggfunc='sum',
                                                fill_value=0).reset_index()
        pivot_table['mr_level'] = pivot_table[itemID].apply(calculate_mr_level)

        # 创建一个新的DataFrame用于存储聚合数据
        all_agg_data = pd.DataFrame()

        # 获取最大的mr_level
        max_level = int(pivot_table['mr_level'].max())
        for i in range(max_level, 0, -1):
            select_rows = pivot_table[pivot_table['mr_level'] == i]
            agg_data = select_rows.groupby(PitemID).sum().reset_index()
            agg_data[itemID] = agg_data[PitemID]
            agg_data[PitemID] = agg_data[itemID].str[:-2]
            agg_data['mr_level'] = i - 1
            all_agg_data = pd.concat([all_agg_data, agg_data], ignore_index=True)

        # 合并原始透视表和聚合数据
        pivot_table = pd.concat([pivot_table, all_agg_data], ignore_index=True)
        final_df = pd.merge(dimensiondf, pivot_table, left_on='mr_code', right_on=itemID, how='left').fillna(0)

        # 将当前过滤条件的结果存储在字典中
        sheets_result[sheetfilter] = final_df

    # 返回一个包含所有sheets结果的字典
    return sheets_result
