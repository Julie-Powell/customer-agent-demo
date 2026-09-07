import pandas as pd
from analysis.read_data import load_data


def analyze_trend():

    df = load_data()

    # 按日期汇总
    daily = df.groupby("date").agg(
        consult_count=("consult_count", "sum"),
        satisfaction=("satisfaction", "mean"),
        response_time=("response_time", "mean")
    ).reset_index()


    return daily


if __name__ == "__main__":

    result = analyze_trend()

    print(result)