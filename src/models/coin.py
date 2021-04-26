import csv

from datetime import datetime

from src.config import CARDANO
from src.models.data import Data, CardanoData
from src.api import BinanceClient, GeckoClient


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
                                       start_date=row[1],
                                       end_date=row[2],
                                       amount=float(row[3]),
                                       txn_fee=0,
                                       txn_type=row[4])

                    self.processed_data.append(data)
            else:
                for row in reader:
                    data = Data(date=row[0],
                                amount=float(row[1]),
                                txn_fee=float(row[2]),
                                txn_type=row[3])

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

    def write_to_disk(self):
        if not self.processed_data:
            raise ValueError("Data not yet processed!")

        with open(self.output, "w", newline="") as write_file:
            writer = csv.DictWriter(write_file, fieldnames=self.__get_fieldnames())

            writer.writeheader()

            for row in self.processed_data:
                writer.writerow(row.to_dict(ticker=self.ticker))


    """ ============================== Helpers ============================== """
    def __get_fieldnames(self):
        return self.processed_data[0].get_fields(ticker=self.ticker)
