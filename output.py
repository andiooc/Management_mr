import datetime
import pandas as pd

def txtoutput(dfs_dict):
    # 创建一个Excel writer对象
    with pd.ExcelWriter(f'C:/Users/00399597/Desktop/测试{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}.xlsx') as writer:
        # 遍历字典中的每个DataFrame
        for sheet_name, df in dfs_dict.items():
            # 将DataFrame写入到Excel的不同sheet中
            df.to_excel(writer, sheet_name=str(sheet_name), index=False)