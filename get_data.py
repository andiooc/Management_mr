import configparser
import pandas as pd
from sqlalchemy import create_engine

# 读取配置文件
def getdata(sqlpassword):
    # 保护性赋值
    sql_query = dimension_query = pivot_col = pivot_row = filter_col = d_ID = d_PID = f_value = None
    # 输入日期范围
    lower_date_input = str(input("请输入起始日期（YYYY-MM）或输入N: ") )+ '-01'
    if lower_date_input.lower() == "n":
        lower_date = ""
    else:
        lower_date = f" and mr_period >= '{lower_date_input}'"

    upper_date_input = str(input("请输入结束日期（YYYY-MM）或输入N: ")) + '-01'
    if upper_date_input.lower() == "n":
        upper_date = ""
    else:
        upper_date = f" and mr_period <= '{upper_date_input}'"

    # 输入选择的国家
    countryselect_input = input("请输入选择的国家或输入N: ")
    if countryselect_input.lower() == "n":
        countryselect = ""
    else:
        countryselect = f" and db_nation_shortname = '{countryselect_input}'"

    pivot_input = str(input("聚合维度方式：1.列为月份，sheet为国家；2.列为国家，sheet为月份 "))
    if pivot_input not in ("1","2"):
        pivot_input ="1"



    report_config = configparser.ConfigParser()
    report_config.read('report_config.ini', encoding="UTF-8")

    config = configparser.ConfigParser()
    config.read('config.ini', encoding="UTF8")

    # 获取所有的报表名称
    report_names = [report_config[section]['name'] for section in report_config.sections()]
    print("可用的报表名称：", report_names)

    # 用户输入报表名称
    while True:
        user_input = input("请输入报表名称：").strip()
        if user_input not in report_names:
            print("未找到该报表，请重新输入。")
            retry = input("是否重新输入报表名称？(y/n): ").strip().lower()
            if retry != 'y':
                return None
        else:
            break

    # 找到用户输入对应的section
    section_found = False
    for section in report_config.sections():
        if report_config[section]['name'] == user_input:
            sql_query = report_config[section]['readsql_select'] + f""" where '管报ID' is not null {lower_date} {upper_date} {countryselect} """ + report_config[section]['readsql_groupby']
            dimension_query = report_config[section]['r_dimension']
            pivot_col = report_config[section]['pivot_col'+pivot_input]
            pivot_row = report_config[section]['pivot_row' + pivot_input]
            filter_col = report_config[section]['filter_col'+pivot_input]
            d_ID = report_config[section]['f_item_ID']
            d_PID = report_config[section]['f_item_PID']
            f_value = report_config[section]['f_value']
            section_found = True
            break

    if not section_found:
        print("配置文件中未找到对应的报表配置。")
        return None

    # 假设配置文件中还包含数据库连接信息
    db_config = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'port': int(config['database']['port']),
        'database': "jt_hq_data",
        'password': sqlpassword
    }

    try:
        # 连接数据库
        engine = create_engine(
            f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}")

        # 构建SQL查询


        # 使用pandas的read_sql方法读取数据
        df = pd.read_sql(sql_query, con=engine)
        dimension_df = pd.read_sql(dimension_query,con=engine)
    except Exception as e:
        print(f"数据库查询失败: {e}")
        return None
    df_dict = {
        'maindf':df,
        'dimensiondf':dimension_df,
        'pivot_col':pivot_col,
        'pivot_row':pivot_row,
        'filter_col':filter_col,
        'itemID':d_ID,
        'PitemID':d_PID,
        'df_value':f_value

    }

    return df_dict
