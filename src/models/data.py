from src.config import *


class Data():
    FIELDS = [DATE]

    def __init__(self, date, amount, txn_fee, txn_type):
        self.date = date
        self.amount = amount
        self.txn_fee = txn_fee
        self.txn_type = txn_type
        self.price_and_value = {}

    def to_dict(self):
        return {}


class CardanoData(Data):
    ADA_AMOUNT = AMOUNT.format(ticker="ADA")
    FIELDS = [EPOCH, START_DATE, END_DATE, ADA_AMOUNT, PRICE_USD, VALUE_USD]

    def __init__(self, epoch, start_date, end_date, amount, txn_fee, txn_type):
        super().__init__(date=end_date, amount=amount, txn_fee=txn_fee, txn_type=txn_type)

        self.epoch = epoch
        self.start_date = start_date
        self.end_date = end_date

    def to_dict(self):
        return {
            EPOCH: self.epoch,
            START_DATE: self.start_date,
            END_DATE: self.end_date,
            self.ADA_AMOUNT: self.amount,
            PRICE_USD: self.price_and_value[FIAT_USD]["price"],
            VALUE_USD: self.price_and_value[FIAT_USD]["value"],
        }
