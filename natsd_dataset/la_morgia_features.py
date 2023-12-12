import glob
import datetime
import os
import numpy as np
import pandas as pd

path = "data/*.csv"


def std_rush_order_feature(df_buy, time_freq, rolling_freq):
    # print(
    #    "????????????????????????std_rush_order_feature???????????????????????????????????????"
    # )
    df_buy = df_buy.groupby(df_buy.index).count()
    # print("DF_BUY")
    # print(df_buy.head())
    df_buy[df_buy == 1] = 0
    # print(df_buy.head())
    df_buy[df_buy > 1] = 1
    # print(df_buy.head())
    buy_volume = df_buy.groupby(pd.Grouper(freq=time_freq))["btc_volume"].sum()
    # print(f"Buy volume: {buy_volume}")
    buy_count = df_buy.groupby(pd.Grouper(freq=time_freq))["btc_volume"].count()
    # print(f"Buy Count: {buy_count}")
    buy_volume.drop(buy_volume[buy_count == 0].index, inplace=True)
    buy_volume.dropna(inplace=True)
    # print("Buy Volumqe: ", buy_volume)
    rolling_diff = buy_volume.rolling(window=rolling_freq).std()
    # print("Rolling_Diff: ", rolling_diff)
    results = rolling_diff.pct_change()
    # print("RESULTS: ", results)
    # print(
    #    "????????????????????????std_rush_order_feature???????????????????????????????????????"
    # )
    return results


def avg_rush_order_feature(df_buy, time_freq, rolling_freq):
    df_buy = df_buy.groupby(df_buy.index).count()
    df_buy[df_buy == 1] = 0
    df_buy[df_buy > 1] = 1
    buy_volume = df_buy.groupby(pd.Grouper(freq=time_freq))["btc_volume"].sum()
    buy_count = df_buy.groupby(pd.Grouper(freq=time_freq))["btc_volume"].count()
    buy_volume.drop(buy_volume[buy_count == 0].index, inplace=True)
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=rolling_freq).mean()
    results = rolling_diff.pct_change()
    return results


def std_trades_feature(df_buy_rolling, rolling_freq):
    buy_volume = df_buy_rolling["price"].count()
    buy_volume.drop(buy_volume[buy_volume == 0].index, inplace=True)
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=rolling_freq).std()
    results = rolling_diff.pct_change()
    return results


def std_volume_feature(df_buy_rolling, rolling_freq):
    buy_volume = df_buy_rolling["btc_volume"].sum()
    buy_volume.drop(buy_volume[buy_volume == 0].index, inplace=True)
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=rolling_freq).std()
    results = rolling_diff.pct_change()
    return results


def avg_volume_feature(df_buy_rolling, rolling_freq):
    buy_volume = df_buy_rolling["btc_volume"].sum()
    buy_volume.drop(buy_volume[buy_volume == 0].index, inplace=True)
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=rolling_freq).mean()
    results = rolling_diff.pct_change()
    return results


def std_price_feature(df_buy_rolling, rolling_freq):
    buy_volume = df_buy_rolling["price"].mean()
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=rolling_freq).std()
    results = rolling_diff.pct_change()
    return results


def avg_price_feature(df_buy_rolling):
    buy_volume = df_buy_rolling["price"].mean()
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=10).mean()
    results = rolling_diff.pct_change()
    return results


def avg_price_max(df_buy_rolling):
    buy_volume = df_buy_rolling["price"].max()
    buy_volume.dropna(inplace=True)
    rolling_diff = buy_volume.rolling(window=10).mean()
    results = rolling_diff.pct_change()
    return results


def chunks_time(df_buy_rolling):
    # compute any kind of aggregation
    buy_volume = df_buy_rolling["price"].max()
    buy_volume.dropna(inplace=True)
    # the index contains time info
    return buy_volume.index


def build_features(file, coin, time_freq, rolling_freq, index):
    df = pd.read_csv(file)
    df["time"] = pd.to_datetime(df["timestamp"].astype(np.int64), unit="ms")
    df = df.reset_index().set_index("time")

    df_buy = df[df["side"] == "buy"]
    df_buy_grouped = df_buy.groupby(pd.Grouper(freq=time_freq))
    # print("df_buy_grouped")
    # print(df_buy_grouped.head())

    date = chunks_time(df_buy_grouped)
    # print(f"DATE: {date}")
    # print(f"INDEX: {index}")

    # print(
    #    f"STD_RUSH_ORDER: { std_rush_order_feature(df_buy, time_freq, rolling_freq).values}"
    # )
    # print(
    #    f"AVG_RUSH_ORDER: {avg_rush_order_feature(df_buy, time_freq, rolling_freq).values}"
    # )

    results_df = pd.DataFrame(
        {
            "date": date,
            "pump_index": index,
            "std_rush_order": std_rush_order_feature(
                df_buy, time_freq, rolling_freq
            ).values,
            "avg_rush_order": avg_rush_order_feature(
                df_buy, time_freq, rolling_freq
            ).values,
            "std_trades": std_trades_feature(df_buy_grouped, rolling_freq).values,
            "std_volume": std_volume_feature(df_buy_grouped, rolling_freq).values,
            "avg_volume": avg_volume_feature(df_buy_grouped, rolling_freq).values,
            "std_price": std_price_feature(df_buy_grouped, rolling_freq).values,
            "avg_price": avg_price_feature(df_buy_grouped),
            "avg_price_max": avg_price_max(df_buy_grouped).values,
            "hour_sin": np.sin(2 * np.pi * date.hour / 23),
            "hour_cos": np.cos(2 * np.pi * date.hour / 23),
            "minute_sin": np.sin(2 * np.pi * date.minute / 59),
            "minute_cos": np.cos(2 * np.pi * date.minute / 59),
        }
    )
    pd.set_option("display.max_columns", None)
    # print("results_df")
    # print(results_df.head())

    results_df["symbol"] = coin
    results_df["gt"] = 0
    return results_df.dropna()


def build_features_multi(time_freq, rolling_freq, csv_path):
    files = glob.glob(path)
    # print(f"Files: {files}")
    all_results_df = pd.DataFrame()
    count = 0
    pumps = pd.read_csv(csv_path)
    pumps = pumps[pumps["exchange"] == "binance"]
    print("PUMPS")
    print(pumps.head())
    for f in files:
        print(f)
        coin_date, time = os.path.basename(f[: f.rfind(".")]).split(" ")
        coin, date = coin_date.split("_")

        skip_pump = (
            len(
                pumps[
                    (pumps["symbol"] == coin)
                    & (pumps["date"] == date)
                    & (pumps["hour"] == time.replace(".", ":"))
                ]
            )
            == 0
        )
        # print(f"Skip pump: {skip_pump}")
        if skip_pump:
            continue

        # print(f"SET INDEX: {count}")
        results_df = build_features(f, coin, time_freq, rolling_freq, count)
        # print("RESULTS DF")
        # print(results_df.head())

        date_datetime = datetime.datetime.strptime(date + " " + time, "%Y-%m-%d %H.%M")

        # We consider 24 hours before and 24 hours after the pump
        results_df = results_df[
            (results_df["date"] >= date_datetime - datetime.timedelta(minutes=2))
            & (results_df["date"] <= date_datetime + datetime.timedelta(minutes=2))
        ]

        all_results_df = pd.concat([all_results_df, results_df])
        count += 1

        # print("GT 1")
        # print(results_df[results_df["gt"] == 1].head())
        # print(
        #    " ----------------------------------------------------------------------------------- "
        # )

    print("HI")
    if not os.path.exists("features/"):
        os.makedirs("features/")

    all_results_df.to_csv(
        "features/features_{}.csv".format(time_freq), index=False, float_format="%.3f"
    )


def compute_features():
    build_features_multi(time_freq="25S", rolling_freq=10)
    build_features_multi(time_freq="15S", rolling_freq=10)
    build_features_multi(time_freq="5S", rolling_freq=20)


if __name__ == "__main__":
    start = datetime.datetime.now()
    compute_features()
    print(datetime.datetime.now() - start)
