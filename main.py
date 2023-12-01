import pymysql
from configparser import ConfigParser
import sys
import get_data

# 开始程序
def main():
    # 输入密码
    password = input("请输入数据库密码: ")

    # 读取config.ini文件
    config = ConfigParser()
    config.read('config.ini')

    # 获取database配置
    host = config.get('database', 'host')
    port = config.getint('database', 'port')
    user = config.get('database', 'user')

    # 尝试创建数据库连接
    try:
        connection = pymysql.connect(host=host,
                                     port=port,
                                     user=user,
                                     password=password,
                                     database='jt_hq_data')  # 请替换为您的数据库名称
        print("数据库连接成功！")
        # 这里可以添加更多操作，例如查询、插入等

        # 关闭连接
        connection.close()
        df = get_data.getdata(password)
        print(df)

    except pymysql.MySQLError as e:
        print("数据库连接失败，请检查连接")
        print(f"错误信息: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
