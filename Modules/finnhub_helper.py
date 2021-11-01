import finnhub
from datetime import datetime


class Finnhub:
    def __init__(self, api_key) -> None:
        self.fh = finnhub.Client(api_key=api_key)

    def get_final_symbols_list(self, target_symbols):
        all_symbols_list = list()
        res = self.fh.crypto_symbols("BINANCE")
        for each in res:
            display = each["displaySymbol"]
            symbol = each["symbol"]
            base = display.split("/")[0]
            quote = display.split("/")[1]
            if quote == "USDT" and base in target_symbols:
                all_symbols_list.append(
                    {
                        "display": display,
                        "base": base,
                        "quote": quote,
                        "symbol": symbol,
                    }
                )
        return all_symbols_list

    def get_all_symbols(self, _quote):
        all_symbols_list = list()
        res = self.fh.crypto_symbols("BINANCE")
        for each in res:
            display = each["displaySymbol"]
            symbol = each["symbol"]
            base = display.split("/")[0]
            quote = display.split("/")[1]
            if quote == _quote:
                all_symbols_list.append(
                    {
                        "display": display,
                        "base": base,
                        "quote": quote,
                        "symbol": symbol,
                    }
                )
        return all_symbols_list

    def get_candles(self, symbol, frame, start, end):
        res = self.fh.crypto_candles(symbol, frame, start, end)
        if res["s"] == "no_data":
            return None
        data = list()
        for count in range(len(res["t"])):
            rowDate = datetime.fromtimestamp(res["t"][count])
            data.append(
                {
                    "ts": res["t"][count],
                    "date": rowDate,
                    "dateDay": rowDate.day,
                    "dateMonth": rowDate.month,
                    "dateYear": rowDate.year,
                    "dateHour": rowDate.hour,
                    "dateMinute": rowDate.minute,
                    "dateSeconds": rowDate.second,
                    "open": res["o"][count],
                    "close": res["c"][count],
                    "high": res["h"][count],
                    "low": res["l"][count],
                    "volume": res["v"][count],
                }
            )
        return data
