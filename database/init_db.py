import sqlite3
import pandas as pd


# 创建数据库
conn = sqlite3.connect("database/customer.db")


# 读取 CSV
df = pd.read_csv("data/customer.csv")


# 写入数据库
df.to_sql(
    "customer_metrics",
    conn,
    if_exists="replace",
    index=False
)


conn.close()


print("数据库创建完成")