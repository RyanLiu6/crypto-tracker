import csv

from datetime import datetime

from src.api import BinanceClient, GeckoClient
from src.models.data import Data, CardanoData, SavingsData
from src.utils import string_to_datetime, datetime_range, timestamp_to_datetime
from src.config import CARDANO, VECHAIN, VETHOR, BINANCE_AIRDROP, BINANCE_SAVINGS


class Coin():
    def __init__(self, ticker, currencies, output=None):
        self.ticker = ticker
        self.currencies = currencies
        self.processed_data = []

        self.gecko = GeckoClient()
        self.binance = BinanceClient()

        if not output:
            identifier = str(int(datetime.now().timestamp())*1000)
            self.output = f"{self.ticker}_{identifier}.csv"
        else:
            self.output = output

    def process_data(self, input_file):
        with open(input_file, newline="") as read_file:
            reader = csv.reader(read_file, skipinitialspace=True, delimiter=",", quotechar="|")

            if self.ticker == CARDANO:
                for row in reader:
                    data = CardanoData(epoch=row[0],
                                       start_date=string_to_datetime(row[1]),
                                       end_date=string_to_datetime(row[2]),
                                       amount=float(row[3]),
                                       txn_fee=0)

                    self.processed_data.append(data)
            elif self.ticker == VETHOR:
                row = next(reader)
                start_date = string_to_datetime(row[0])
                end_date = string_to_datetime(row[1])
                vtho_per_day = float(row[2])

                for date in datetime_range(start=start_date, end=end_date):
                    data = Data(date=date,
                                amount=vtho_per_day,
                                txn_fee=0)

                    self.processed_data.append(data)
            else:
                for row in reader:
                    data = Data(date=string_to_datetime(row[0]),
                                amount=float(row[1]),
                                txn_fee=float(row[2]))

                    self.processed_data.append(data)

        for row in self.processed_data:
            if self.binance.is_ticker_on_binance(ticker=self.ticker):
                prices = self.binance.get_average_price_for_date(ticker=self.ticker, date=row.date, currencies=self.currencies)
            else:
                prices = self.gecko.get_average_price_for_date(ticker=self.ticker, date=row.date, currencies=self.currencies)

            for currency, price in prices.items():
                row.price_and_value[currency] = {
                    "price": price,
                    "value": row.amount * price
                }

    def process_income(self, income_type, start_date):
        start_date = string_to_datetime(start_date)

        if income_type == BINANCE_SAVINGS:
            results = self.binance.get_saving_data(ticker=self.ticker, start_date=start_date)
            for res in results:
                data = SavingsData(amount=float(res["interest"]),
                                   date=timestamp_to_datetime(res["time"]))

                self.processed_data.append(data)
        elif income_type == BINANCE_AIRDROP:
            results = self.binance.get_dividend_data(ticker=self.ticker, start_date=start_date)
            for res in results:
                data = SavingsData(amount=float(res["amount"]),
                                   date=timestamp_to_datetime(res["divTime"]))
                self.processed_data.append(data)

        for row in self.processed_data:
            prices = self.binance.get_average_price_for_date(ticker=self.ticker, date=row.date, currencies=self.currencies)

            for currency, price in prices.items():
                row.price_and_value[currency] = {
                    "price": price,
                    "value": row.amount * price
                }

    def write_to_disk(self):
        if not self.processed_data:
            raise ValueError("Data not yet processed!")

        with open(self.output, "w", newline="") as write_file:
            writer = csv.DictWriter(write_file, fieldnames=self.__get_fieldnames())

            writer.writeheader()

            for row in self.processed_data:
                writer.writerow(row.to_dict(ticker=self.ticker))

        print(f"CSV File written to {self.output}")


    """ ============================== Helpers ============================== """
    def __get_fieldnames(self):
        return self.processed_data[0].get_fields(ticker=self.ticker)
