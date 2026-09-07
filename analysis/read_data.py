import pandas as pd


def load_data():

    df = pd.read_csv(
        "data/customer.csv"
    )

    return df


if __name__ == "__main__":

    df = load_data()

    print("客服数据读取成功！")
    print(df)