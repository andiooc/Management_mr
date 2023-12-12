import pandas as pd
# import output
def calculate_mr_level(row):
    report_id = row['管报ID']  # 获取行索引中的 '管报ID' 值
    if report_id.startswith('SC'):
        mylevel = 0
    else:
        mylevel = (len(report_id) - 2) / 2
    return mylevel
def reportpivot(df_dict):
    maindf = df_dict['maindf']
    dimensiondf = df_dict['dimensiondf']
    itemID = df_dict['itemID']
    PitemID = df_dict['PitemID']
    col_pivot = df_dict['pivot_col']
    row_pivot = df_dict['pivot_row']
    col_filter = df_dict['filter_col']
    sheet_filter = maindf[col_filter].drop_duplicates().values.tolist()

    for sheetfilter in sheet_filter:
        filter_maindf = maindf.loc[maindf[col_filter].str.contains(sheetfilter)]
        pivot_table=filter_maindf.pivot_table(index=[itemID, PitemID], columns=col_pivot, values='值', aggfunc='sum', fill_value=0).reset_index()
        pivot_table['mr_level'] = pivot_table.apply(calculate_mr_level, axis=1)

        max_level = int(pivot_table['mr_level'].max())
        for i in range(max_level,0,-1):
            select_rows = pivot_table[pivot_table['mr_level'] == i]
            agg_data = select_rows.groupby('父ID').sum().reset_index().drop('管报ID', axis=1)
            agg_data.rename(columns={'父ID': '管报ID'}, inplace = True)
            agg_data['父ID'] = agg_data['管报ID'].str[:-2]
            agg_data['mr_level'] = i-1
            agg_data.reset_index(inplace=True)
            agg_data = agg_data[pivot_table.columns]
            pivot_table = pd.concat([pivot_table,agg_data], ignore_index= True)


        final_df = pd.merge(dimensiondf, pivot_table, left_on='mr_code', right_on='管报ID', how='left').fillna(0)

    # for index, row in final_df.iterrows():
    #     if row['mr_level'] == max_level - 1:
    #         parent_code = row['mr_code']
    #         numeric_subset = final_df[final_df['mr_parentcode'] == parent_code].select_dtypes(include=['number'])
    #         parent_sum = numeric_subset.sum()
    #         final_df.loc[index, numeric_subset.columns] = parent_sum


        return final_df

