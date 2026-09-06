import sqlite3
import pandas as pd


def load_data():

    conn = sqlite3.connect(
        "database/customer.db"
    )

    df = pd.read_sql(
        "SELECT * FROM customer_metrics",
        conn
    )

    conn.close()

    return df



def analyze_metrics():

    df = load_data()


    # 按日期汇总
    daily = df.groupby("date").agg(
        consult_count=("consult_count", "sum"),
        satisfaction=("satisfaction", "mean"),
        response_time=("response_time", "mean")
    ).reset_index()


    # 最近一天
    latest = daily.iloc[-1]


    # 前一天
    previous = daily.iloc[-2]


    # 计算变化
    consult_change = (
        (latest["consult_count"] - previous["consult_count"])
        / previous["consult_count"]
        * 100
    )


    satisfaction_change = (
        latest["satisfaction"] - previous["satisfaction"]
    )


    response_change = (
        latest["response_time"] - previous["response_time"]
    )


    alerts = []


    if consult_change > 10:
        alerts.append(
            f"咨询量增长 {consult_change:.1f}%"
        )


    if satisfaction_change < -3:
        alerts.append(
            f"满意度下降 {abs(satisfaction_change):.1f} 个百分点"
        )


    if response_change > 3:
        alerts.append(
            f"平均响应时间增加 {response_change:.1f}"
        )


    result = {
        "日期": latest["date"],
        "咨询量": int(latest["consult_count"]),
        "咨询量变化": round(consult_change, 1),
        "满意度": round(latest["satisfaction"], 1),
        "满意度变化": round(satisfaction_change, 1),
        "平均响应时间": round(latest["response_time"], 1),
        "异常": alerts
    }


    return result



if __name__ == "__main__":

    result = analyze_metrics()

    print("========== 客服业务监测 ==========")

    for key, value in result.items():
        print(f"{key}：{value}")