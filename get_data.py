import configparser
import pandas as pd
from sqlalchemy import create_engine

# 读取配置文件
def getdata(sqlpassword):
    # 保护性赋值
    factdata = main_dimension = m_d_lan_cn = m_d_lan_en = org_dimension = None


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
            factdata = report_config[section]['factdata']
            main_dimension = report_config[section]['main_dimension']
            m_d_lan_cn = report_config[section]['m_d_lan_cn']
            m_d_lan_en = report_config[section]['m_d_lan_en']
            org_dimension = report_config[section]['org_dimension']
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
        sql_query = f"SELECT * FROM {factdata} "

        # 使用pandas的read_sql方法读取数据
        df = pd.read_sql(sql_query, con=engine)
    except Exception as e:
        print(f"数据库查询失败: {e}")
        return None

    return df
