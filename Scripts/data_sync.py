import pandas as pd
from datetime import datetime
import time
from tqdm import tqdm
from Modules.finnhub_helper import Finnhub
from Modules.mongo_helper import Mongo


class data_sync:
    def __init__(self, mongo_settings, fh_api_key) -> None:
        self.fh = Finnhub(api_key=fh_api_key)
        self.mongo = Mongo(mongo_settings)
        self.data_path = "../Data/"

    def sync_daily_data(self):

        mongo = self.mongo
        fh = self.fh
        data_path = self.data_path

        for each in tqdm(list(mongo.get_target_symbols())):

            end = int(datetime.now().timestamp())

            name = each["name"]
            start = each["dailySync"]
            symbol = each["symbol"]

            try:
                df = pd.read_csv(data_path + name + "_1D.csv")
                exists = True
            except:
                df = None
                exists = False
            try:
                data = fh.get_candles(symbol, "D", start, end)
            except:
                time.sleep(60)
                data = fh.get_candles(symbol, "D", start, end)

            if not data:
                continue

            dfNew = pd.DataFrame(data)
            if exists:
                df = df.append(dfNew)
            else:
                df = dfNew.copy()
            df = df.drop_duplicates(subset=["ts"], keep="last")
            last_ts = int(df.iloc[-1]["ts"])
            df.to_csv(data_path + name + "_1D.csv", index=False)

            mongo.update_symbol_sync(symbol, "dailySync", last_ts)

            time.sleep(0.1)

    def sync_hourly_data(self):

        mongo = self.mongo
        fh = self.fh
        data_path = self.data_path

        for each in tqdm(list(mongo.get_target_symbols())):

            end = int(datetime.now().timestamp())

            name = each["name"]
            start = each["hourlySync"]
            symbol = each["symbol"]

            try:
                df = pd.read_csv(data_path + name + "_1H.csv")
                exists = True
            except:
                df = None
                exists = False
            try:
                data = fh.get_candles(symbol, "60", start, end)
            except:
                time.sleep(60)
                data = fh.get_candles(symbol, "60", start, end)

            if not data:
                continue

            dfNew = pd.DataFrame(data)
            if exists:
                df = df.append(dfNew)
            else:
                df = dfNew.copy()
            df = df.drop_duplicates(subset=["ts"], keep="last")
            last_ts = int(df.iloc[-1]["ts"])
            df.to_csv(data_path + name + "_1D.csv", index=False)

            mongo.update_symbol_sync(symbol, "hourlySync", last_ts)

            time.sleep(0.1)
