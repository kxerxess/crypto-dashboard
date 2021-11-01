from Modules.mongo_helper import Mongo
import configparser

config = configparser.ConfigParser()
config.read("./common/settings.ini")

mongo_settings = {
    "host": config["mongo"]["host"],
    "port": config["mongo"]["port"],
    "username": config["mongo"]["username"],
    "password": config["mongo"]["password"],
    "db": config["mongo"]["db"],
}
mongo = Mongo(mongo_settings)

while True:
    base = input("Enter base:")
    quote = input("Enter base:")
    status = True if input("Y to ADD, N to REMOVE") == "Y" else False
    name = base + quote

    if mongo.update_target_status(name, status):
        print("Updated")
    else:
        print("Invalid")

    if input("Again?") == "Y":
        continue
    else:
        break
