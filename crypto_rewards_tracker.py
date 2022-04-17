#!/usr/bin/env python

import click

from typing import Tuple

# Importing data
from src.models.coin import Coin
from src.config import BINANCE_AIRDROP, BINANCE_SAVINGS


@click.group()
@click.pass_context
@click.option("--output", "output_filename", type=click.Path(), default=None,
    help="Output filename, will be generated if not specified")
@click.option("--currencies", multiple=True, default=None,
    help="Additional currencies to process for")
def cli(ctx: click.Context, output_filename: str, currencies: Tuple[str]):
    """
    Cryptocurrency Rewards Tracker entrypoint.

    Args:
        output_filename (str): Output file name, if not specified, will be generated
        currencies (Tuple[str]): Tuple of additional currencies to process for

    """
    # Ensure that ctx.obj exists and is a dict (in case `cli()` is called outside of main)
    ctx.ensure_object(dict)

    ctx.obj["OUTPUT_FILENAME"] = output_filename
    ctx.obj["CURRENCIES"] = list(currencies)


@cli.command()
@click.pass_context
@click.argument("ticker")
@click.argument("start_date")
@click.argument("end_date")
@click.option("--income_type", type=click.Choice([BINANCE_AIRDROP, BINANCE_SAVINGS]), default=BINANCE_AIRDROP,
    help="Income type for Binance, defaults to AIRDROP")
def track_binance_rewards(ctx: click.Context, ticker: str, start_date: str, end_date: str, income_type: str):
    """
    Tracks Binance Airdrops and Savings.

    The goal of this tool is to generate a CSV file for a given cryptocurrency that contains:
    - From start_date to end_date, on a per day basis, how many coins was earned
    - The average price of the coin on that day, in USD
    - The value gained on that day, in USD

    This will help keeping track of your gains and will make tax information much easier.

    Args:
        ctx (click.Context): Click context object
        ticker (str): Ticker of the cryptocurrency
        start_date (str): Start date to process from
        end_date (str): End date to process to
        income_type (str): Income type
    """
    coin = Coin(ticker=ticker, currencies=ctx.obj["CURRENCIES"], output_filename=ctx.obj["OUTPUT_FILENAME"])
    coin.process_income(income_type=income_type, start_date=start_date, end_date=end_date)
    coin.write_to_disk()


@cli.command()
@click.pass_context
@click.argument("ticker")
@click.argument("input_filename", type=click.Path())
def track_generic_rewards(ctx: click.Context, ticker: str, input_filename: str):
    """
    Tracks generic crypto rewards from staking.

    Args:
        ctx (click.Context): Click context object
        ticker (str): Ticker of the cryptocurrency
        input_filename (str): CSV file to read from that contains reward information
    """
    if ctx.obj["CURRENCIES"]:
        print("Note: Additional currencies are not supported at this moment.")

    coin = Coin(ticker=ticker, currencies=None, output_filename=ctx.obj["OUTPUT_FILENAME"])
    coin.process_data(input_filename=input_filename)
    coin.write_to_disk()


if __name__ == "__main__":
    cli()
