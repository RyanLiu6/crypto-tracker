from src.config import *


class Data():
    def __init__(self, date, amount, txn_fee, txn_type):
        self.date = date
        self.amount = amount
        self.txn_fee = txn_fee
        self.txn_type = txn_type
        self.price_and_value = {}

    def get_fields(self, ticker):
        return [DATE, AMOUNT.format(ticker=ticker), TXN_FEE.format(currency=ticker), PRICE_USD, VALUE_USD, TXN_FEE.format(currency=FIAT_USD)]

    def to_dict(self, ticker):
        amount_field = AMOUNT.format(ticker=ticker)
        ticker_fee_field = TXN_FEE.format(currency=ticker)
        usd_fee_field = TXN_FEE.format(currency=FIAT_USD)

        price = self.price_and_value[FIAT_USD]["price"]

        return {
            DATE: self.date,
            amount_field: self.amount,
            ticker_fee_field: self.txn_fee,
            PRICE_USD: price,
            VALUE_USD: self.price_and_value[FIAT_USD]["value"],
            usd_fee_field: self.txn_fee * price
        }


class CardanoData(Data):
    def __init__(self, epoch, start_date, end_date, amount, txn_fee, txn_type):
        super().__init__(date=end_date, amount=amount, txn_fee=txn_fee, txn_type=txn_type)

        self.epoch = epoch
        self.start_date = start_date
        self.end_date = end_date

    def get_fields(self, ticker):
        return [EPOCH, START_DATE, END_DATE, AMOUNT.format(ticker=ticker), PRICE_USD, VALUE_USD]

    def to_dict(self, ticker=CARDANO):
        amount_field = AMOUNT.format(ticker=ticker)

        return {
            EPOCH: self.epoch,
            START_DATE: self.start_date,
            END_DATE: self.end_date,
            amount_field: self.amount,
            PRICE_USD: self.price_and_value[FIAT_USD]["price"],
            VALUE_USD: self.price_and_value[FIAT_USD]["value"],
        }
