#1/usr/bin/env python

import csv
import click

from typing import Dict

from src.utils import write_csv_to_file


@click.command()
@click.argument("binance_data")
def clean_binance_csv(binance_data: str) -> None:
    """
    Generates a CSV file, based on input parameter binance_data.

    This will remove any rows whose operation is not:
    1. Deposit
    2. Withdraw
    3. Buy
    4. Sell
    5. Fee
    6. Transaction Related
    7. Small assets exchange *

    This really targets Savings and Staking, as that is calculated with
    this calculator, and therefore is not applicable in that data.

    Args:
        binance_data (str): Input Binance data
    """
    operations_to_keep = [
        "Deposit",
        "Withdraw",
        "Buy",
        "Sell",
        "Fee",
        "Transaction Related",
    ]

    operations_to_keep_match = [
        "Small assets exchange"
    ]

    to_write = []
    with open(binance_data, "r", newline="") as read_file:
        reader = csv.DictReader(read_file, skipinitialspace=True, delimiter=",", quotechar="|")
        field_names = reader.fieldnames

        for row in reader:
            operation = row["Operation"].strip()

            # Direct match
            if operation in operations_to_keep:
                to_write.append(row)

            # Startswith match - could be done with Regex
            for item in operations_to_keep_match:
                if operation.startswith(item):
                    to_write.append(row)

    write_csv_to_file(field_names=field_names, output_prefix="binance_data", data_to_write=to_write)


if __name__ == "__main__":
    clean_binance_csv()
