import tkinter as tk
from tkinter import messagebox
import configparser
from sqlalchemy import create_engine  # 或者其他数据库连接库

# 读取数据库配置
config = configparser.ConfigParser()
config.read('config.ini')
db_config = config['database']

# 创建用户界面
root = tk.Tk()
root.title('报表客户端')

# 用户输入框
server_entry = tk.Entry(root)
server_entry.insert(0, db_config['host'])
server_entry.config(state='readonly')

port_entry = tk.Entry(root)
port_entry.insert(0, db_config['port'])
port_entry.config(state='readonly')


username_entry = tk.Entry(root)
username_entry.insert(0, db_config['user'])

password_entry = tk.Entry(root, show='*')

# 测试数据库连接
def test_connection():
    try:
        conn = create_engine(
        f"mysql+pymysql://{username_entry.get()}:{password_entry.get()}@{server_entry.get()}:{port_entry.get()}/{'jt_hq_data'}"
        )

        messagebox.showinfo('成功', '连接成功')
        # 更新config
        config.set('database', 'username', username_entry.get())
        with open('database.ini', 'w') as configfile:
            config.write(configfile)
        # 置灰输入框
        username_entry.config(state='readonly')
        password_entry.config(state='readonly')
    except Exception as e:
        messagebox.showerror('失败', str(e))

# 测试连接按钮
test_btn = tk.Button(root, text='测试连接', command=test_connection)

# 布局
server_entry.pack()
port_entry.pack()
username_entry.pack()
password_entry.pack()
test_btn.pack()

# 读取报表配置
report_config = configparser.ConfigParser()
report_config.read('reportconfig.ini')

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

root.mainloop()
