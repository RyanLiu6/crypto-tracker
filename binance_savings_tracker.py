import argparse

# Importing data
from src.models.coin import Coin
from src.config import BINANCE_AIRDROP, BINANCE_SAVINGS


def parse_args():
    parser = argparse.ArgumentParser(description="Binance Savings Tracker")
    parser.add_argument("ticker", help="Ticker of cryptocurrency")
    parser.add_argument("income_type", choices=[BINANCE_AIRDROP, BINANCE_SAVINGS],
                        help="Income type for Binance.")
    parser.add_argument("start_date", help="Start Date of transactions.")
    parser.add_argument("--output", default=None, dest="output_file",
                        help="Output filename. If not specified, will be generated based on ticker and time.")
    parser.add_argument("--currencies", nargs="+", default=None,
                        help="Additional currencies to process for")

    args = parser.parse_args()

    if args.currencies:
        print("Note: Additional currencies current do not work due to lack of data. Will be supported in a further update.")
        args.currencies = None

    return args.ticker, args.income_type, args.start_date, args.output_file, args.currencies


def process_request(ticker, income_type, start_date, output_file, currencies):
    """
    Processes input from a file specified by filename and creates a CSV file

    Args:
        filename: txt file that has data in specified format
    """
    coin = Coin(ticker=ticker, currencies=currencies, output=output_file)
    coin.process_income(income_type=income_type, start_date=start_date)
    coin.write_to_disk()


if __name__ == "__main__":
    args = parse_args()

    process_request(*args)
