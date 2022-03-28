import math

from pytz import utc
from datetime import datetime, timedelta

from dotenv import dotenv_values
from binance.client import Client
from pycoingecko import CoinGeckoAPI
from currency_converter import CurrencyConverter

from src.config import FIAT_USD, BINANCE_AIRDROP, BINANCE_SAVINGS
from src.utils import calculate_average, get_timestamp_milliseconds


class BinanceClient:
    def __init__(self):
        config = dotenv_values(".env")

        self.client = Client(api_key=config["API_KEY"], api_secret=config["SECRET_KEY"])
        self.converter = CurrencyConverter('http://www.ecb.int/stats/eurofxref/eurofxref-hist.zip')

    def is_ticker_on_binance(self, ticker):
        symbol = f"{ticker}USDT"

        result = self.client.get_symbol_info(symbol=symbol)

        return True if result else False

    def get_average_price_for_date(self, ticker, date, currencies=None):
        """
        Given a ticker, returns the historical average price for a specific date.

        Args:
            ticker: string representing cryptocurrency
            date: datetime object
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

        pacific_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

        utc_start = date.astimezone(utc)
        utc_end = pacific_end.astimezone(utc)

        start_timestamp = get_timestamp_milliseconds(utc_start)
        end_timestamp = get_timestamp_milliseconds(utc_end)

        klines = self.client.get_historical_klines(symbol=symbol,
                                                   interval=Client.KLINE_INTERVAL_1HOUR,
                                                   start_str=start_timestamp,
                                                   end_str=end_timestamp)

        values = []
        for line in klines:
            # result is array of OHLCV starting with timestamp of open - we will use Open and Close values for best representation
            open_price = float(line[1])
            close_price = float(line[4])
            values.append(calculate_average([open_price, close_price]))

        mid_day = utc_start.replace(hour=utc_start.hour + 12)
        prices = { FIAT_USD: calculate_average(values) }

        if currencies:
            for currency in currencies:
                prices[currency] = self.converter.convert(prices[FIAT_USD], FIAT_USD, currency, date=mid_day)

        return prices

    def get_saving_data(self, ticker, start_date, end_date=datetime.now()):
        """
        Gets savings data for specific ticker for a date range.

        From the API: The time between startTime and endTime cannot be longer than 30 days.
        Therefore, we

        Since API can only return 100 results at max, assume that each day has one savings transaction.
        Thus, we make X amount of API calls, where X = ((end_date - start_date) / 100 ) + 1

        From the API: The time between startTime and endTime cannot be longer than 30 days

        Args:
            ticker: string representing cryptocurrency
            start_date: datetime object
            end_date: datetime object. Defaults to datetime.now().
        """
        days_in_between = (end_date - start_date).days + 1
        iterations = math.ceil(days_in_between / 30)

        results = []
        for i in range(iterations):
            request_start_date = start_date + timedelta(days=i*30)
            request_end_date = request_start_date + timedelta(days=30)

            print(request_start_date, request_end_date)

            request_params = {
                "lendingType": "DAILY",
                "asset": ticker,
                "size": 100,
                "startTime": get_timestamp_milliseconds(request_start_date),
                "endTime": get_timestamp_milliseconds(request_end_date)
            }

            sub_results = self.client.get_lending_interest_history(**request_params)
            results.extend(sub_results)

        results.sort(key=lambda x: x["time"])

        return results

    def get_dividend_data(self, ticker, start_date, end_date=datetime.now()):
        """
        Gets dividends data for specific ticker for a date range.

        Since API can only return 500 results at max, assume that each day has one savings transaction.
        Thus, we make X amount of API calls, where X = ((end_date - start_date) / 500 ) + 1

        Args:
            ticker: string representing cryptocurrency
            start_date: datetime object
            end_date: datetime object. Defaults to datetime.now()
        """
        days_in_between = (end_date - start_date).days + 1
        iterations = math.ceil(days_in_between / 100)

        results = []
        for i in range(iterations):
            request_start_date = start_date + timedelta(days=i*500)
            request_end_date = request_start_date + timedelta(days=500)

            request_params = {
                "asset": ticker,
                "limit": 500,
                "startTime": get_timestamp_milliseconds(request_start_date),
                "endTime": get_timestamp_milliseconds(request_end_date)
            }

            sub_results = self.client.get_asset_dividend_history(**request_params)
            results.extend(sub_results["rows"])

        results.sort(key=lambda x: x["divTime"])

        return results

    def __income_helper(self, ticker, start_date, limit, request_dict, savings=True):
        """
        Helper function for both savings and dividends as they are
        almost the same.

        Args:
            ticker: string representing cryptocurrency
            start_date: datetime object
            limit: Limit of each API call
            request_dict: dictionary containing specific request data

        Returns:
            List of savings or dividend transactions
        """
        end_date = datetime.now()
        days_in_between = (end_date - start_date).days + 1
        iterations = math.ceil(days_in_between / limit)

        results = []
        for i in range(iterations):
            request_start_date = start_date + timedelta(days=i*limit)
            request_end_date = request_start_date + timedelta(days=limit)

            request_dict["startTime"] = get_timestamp_milliseconds(start_date)
            request_dict["endTime"] = get_timestamp_milliseconds(end_date)

            if savings:
                sub_results = self.client.get_lending_interest_history(**request_dict)
            else:
                sub_results = self.client.get_asset_dividend_history(**request_dict)["rows"]

            results.extend(sub_results)

        if savings:
            sort_key = "time"
        else:
            sort_key = "divTime"

        results.sort(key=lambda x: x[sort_key])

        return results


class GeckoClient:
    def __init__(self):
        self.client = CoinGeckoAPI()
        self.converter = CurrencyConverter('http://www.ecb.int/stats/eurofxref/eurofxref-hist.zip')

    def get_average_price_for_date(self, ticker, date, currencies=None):
        """
        Given a ticker, returns the historical average price for a specific date.

        Args:
            ticker: string representing cryptocurrency
            date: datetime object
            currencies: list of currencies to convert to

        Returns:
            A dictionary containg the average price of cryptocurrency in USD, along with
            any other currencies specified. Would be in the format of
            {
                "USD": some_value,
                "EUR": some_value (using conversion value from that day)
            }
        """
        utc_time = date.astimezone(utc)
        cg_time = date.strftime("%d-%m-%Y")

        coin_id = self.__get_coin_id(ticker=ticker)
        result = self.client.get_coin_history_by_id(id=coin_id, date=cg_time)

        prices = { FIAT_USD: result["market_data"]["current_price"]["usd"] }

        if currencies:
            for currency in currencies:
                prices[currency] = result["market_data"]["current_price"][currency.lower()]

        return prices

    def __get_coin_id(self, ticker):
        coins = self.client.get_coins_list()

        for coin in coins:
            if coin["symbol"] == ticker.lower():
                return coin["id"]

        return None
