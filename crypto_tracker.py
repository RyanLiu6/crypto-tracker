import argparse

# Importing data
from src.models.coin import Coin


def parse_args():
    parser = argparse.ArgumentParser(description="cryptocurrency tracker")
    parser.add_argument("ticker", help="Ticker of cryptocurrency")
    parser.add_argument("input_file", help="A csv file containing information to process.")
    parser.add_argument("--output", default=None, dest="output_file",
                        help="Output filename. If not specified, will be generated based on ticker and time.")
    parser.add_argument("--currencies", nargs="+", default=None,
                        help="Additional currencies to process for")

    args = parser.parse_args()

    if args.currencies:
        print("Note: Additional currencies current do not work due to lack of data. Will be supported in a further update.")
        args.currencies = None

    return args.ticker, args.input_file, args.output_file, args.currencies


def process_request(ticker, input_file, output_file, currencies):
    """
    Processes input from a file specified by filename and creates a CSV file

    Args:
        filename: txt file that has data in specified format
    """
    coin = Coin(ticker=ticker, currencies=currencies, output=output_file)
    coin.process_data(input_file=input_file)
    coin.write_to_disk()

if __name__ == "__main__":
    ticker, input_file, output_file, currencies = parse_args()

    process_request(ticker, input_file, output_file, currencies)
