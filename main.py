import pandas as pd
from Modules.finnhub_helper import Finnhub
from Modules.mongo_helper import Mongo
from Scripts.data_sync import data_sync
import configparser
from datetime import datetime
import time

data_path = "../Data/"

config = configparser.ConfigParser()
config.read("./common/settings.ini")

emailId = config["user"]["emailId"]

fh_api_key = config["finnhub"]["api_key"]
fh = Finnhub(api_key=fh_api_key)

mongo_settings = {
    "host": config["mongo"]["host"],
    "port": config["mongo"]["port"],
    "username": config["mongo"]["username"],
    "password": config["mongo"]["password"],
    "db": config["mongo"]["db"],
}
mongo = Mongo(mongo_settings)
ds = data_sync(mongo_settings, fh_api_key)

hour_count = 0
while True:
    if hour_count % 24 == 0:
        data_sync.sync_daily_data()
        print("Daily Synced")
    data_sync.sync_hourly_data()
    print("Hourly Synced")
    time.sleep(3600)
