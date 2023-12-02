import tkinter as tk
from tkinter import messagebox
import configparser
from sqlalchemy import create_engine
import pymysql

# 读取数据库配置
config = configparser.ConfigParser()
config.read('config.ini', encoding="UTF8")
db_config = config['database']

# 创建用户界面
root = tk.Tk()
root.title('管理报表客户端')

# 用户输入框
server_entry = tk.Entry(root)
server_entry.insert(0, db_config['host'])

port_entry = tk.Entry(root)
port_entry.insert(0, db_config['port'])

username_entry = tk.Entry(root)
username_entry.insert(0, db_config['user'])

password_entry = tk.Entry(root, show='*')

# 测试数据库连接
def test_connection():
    try:
        connection = pymysql.connect(host=server_entry.get(),
                                     port=int(port_entry.get()),
                                     user=username_entry.get(),
                                     password=password_entry.get(),
                                     database='jt_hq_data')
        print("数据库连接成功！")

        # 关闭连接
        connection.close()

        conn = create_engine(
            f"mysql+pymysql://{username_entry.get()}:{password_entry.get()}@{server_entry.get()}:{port_entry.get()}/{'jt_hq_data'}"
        )

        messagebox.showinfo('成功', '连接成功')
        # 更新config
        config.set('database', 'username', username_entry.get())
        with open('database.ini', 'w') as configfile:
            config.write(configfile)
        # 置灰输入框
        server_entry.config(state='readonly', foreground='gray')
        port_entry.config(state='readonly', foreground='gray')
        username_entry.config(state='readonly', foreground='gray')
        password_entry.config(state='readonly', foreground='gray')
        test_btn.config(state='disabled', foreground='gray')  # 置灰测试连接按钮
        execute_btn.config(state='normal')  # 启用执行按钮
    except Exception as e:
        messagebox.showerror('失败', str(e))

# 布局
server_entry.pack()
port_entry.pack()
username_entry.pack()
password_entry.pack()

# 测试连接按钮
test_btn = tk.Button(root, text='测试连接', command=test_connection)
test_btn.pack()

# 读取报表配置
report_config = configparser.ConfigParser()
report_config.read('report_config.ini', encoding="UTF8")

# 用户选择报表
def select_report():
    selected_report = report_var.get()
    aimfile = report_config[selected_report]['aimfile']
    # 这里可以继续读取aimfile并处理

# 单选按钮
report_var = tk.StringVar()
for section in report_config.sections():
    rb = tk.Radiobutton(root, text=section, variable=report_var, value=section, command=select_report)
    rb.pack()

# 执行功能
def execute_function():
    # 在这里添加执行功能的代码
    pass

# 执行按钮
execute_btn = tk.Button(root, text='执行', command=execute_function, state='disabled')
execute_btn.pack()

root.mainloop()
