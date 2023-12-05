
import datetime
def txtoutput(df):
    df.to_excel(f'C:/Users/00399597/Desktop/测试{datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")}.xlsx')