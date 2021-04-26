from pytz import utc
from datetime import datetime

from dotenv import dotenv_values
from binance.client import Client
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter

from src.config import FIAT_USD


class BinanceClient:
    def __init__(self):
        config = dotenv_values(".env")

        self.client = Client(api_key=config["API_KEY"], api_secret=config["SECRET_KEY"])
        self.converter = CurrencyConverter('http://www.ecb.int/stats/eurofxref/eurofxref-hist.zip')

    def get_average_price_for_date(self, ticker, date, currencies=None):
        """
        Given a ticker, returns the historical average price for a specific date.

        Args:
            ticker: string representing cryptocurrency
            date: string representing datetime in mm/dd/yyyy and PDT or PST
            currencies: list of currencies to convert to

        Returns:
            A dictionary containg the average price of cryptocurrency in USD, along with
            any other currencies specified. Would be in the format of
            {
                "USD": some_value,
                "EUR": some_value (using conversion value from that day)
            }
        """
        symbol = f"{ticker}USDT"

        pacific_start = datetime.strptime(date, "%m/%d/%Y")
        pacific_end = pacific_start.replace(hour=23, minute=59, second=59, microsecond=999999)

        utc_start = pacific_start.astimezone(utc)
        utc_end = pacific_end.astimezone(utc)

        start_timestamp_seconds = int(datetime.timestamp(utc_start))
        end_timestamp_seconds = int(datetime.timestamp(utc_end))

        start_timestamp = start_timestamp_seconds*1000
        end_timestamp = end_timestamp_seconds*1000

        klines = self.client.get_historical_klines(symbol=symbol,
                                                   interval=Client.KLINE_INTERVAL_1HOUR,
                                                   start_str=start_timestamp,
                                                   end_str=end_timestamp)

        # Have to manually process out entries that are past end date because ???
        values = []
        for line in klines:
            if line[6] > end_timestamp:
                continue
            else:
                # result is array of OHLCV starting with timestamp of open - we will use Open and Close values for best representation
                open_price = float(line[1])
                close_price = float(line[4])
                values.append(self.__calculate_average([open_price, close_price]))

        mid_day = utc_start.replace(hour=utc_start.hour + 12)
        prices = { FIAT_USD: self.__calculate_average(values) }

        if currencies:
            for currency in currencies:
                prices[currency] = self.converter.convert(prices[FIAT_USD], FIAT_USD, currency, date=mid_day)

        return prices

    def __calculate_average(self, nums):
        return sum(nums) / len(nums)


class GeckoClient:
    def __init__(self):
        self.client = CoinGeckoAPI()
        self.converter = CurrencyConverter('http://www.ecb.int/stats/eurofxref/eurofxref-hist.zip')

    def get_average_price_for_date(self, ticker, date, currencies=None):
        """
        Given a ticker, returns the historical average price for a specific date.

        Args:
            ticker: string representing cryptocurrency
            date: string representing datetime in mm/dd/yyyy and PDT or PST
            currencies: list of currencies to convert to

        Returns:
            A dictionary containg the average price of cryptocurrency in USD, along with
            any other currencies specified. Would be in the format of
            {
                "USD": some_value,
                "EUR": some_value (using conversion value from that day)
            }
        """
        pacific_time = datetime.strptime(date, "%m/%d/%Y")
        utc_time = pacific_time.astimezone(utc)
        cg_time = pacific_time.strftime("%d-%m-%Y")

        result = self.client.get_coin_history_by_id(id=ticker, date=cg_time)

        prices = { FIAT_USD: result["market_data"]["current_price"]["usd"] }

        if currencies:
            for currency in currencies:
                prices[currency] = result["market_data"]["current_price"][currency.lower()]

        return prices
