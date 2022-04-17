
# Cryptocurrency Tracker

Generates CSV files for cryptocurrency based on input. Supports any coin traded on Binance, with generic transaction data.

Specific support for:
1. Cardano (ADA)

and more to come if required!

In addition, this also supports Binance savings account along with airdrops.

## Usage
Before using the script, some credentials need to be created. Users will need to sign up for an account with [Binance](Binance.com) and generate both an API key and a Secret key. Afterwards, create an `.env` file like
```
API_KEY=some_key
SECRET_KEY=some_key
```

The script is two-tiered, with the base script being `crypto_rewards_tracker.py`
```
$ python crypto_rewards_tracker.py --help
Usage: crypto_rewards_tracker.py [OPTIONS] COMMAND [ARGS]...

  Cryptocurrency Rewards Tracker entrypoint.

  Args:     output_filename (str): Output file name, if not specified, will be
  generated     currencies (Tuple[str]): Tuple of additional currencies to
  process for

Options:
  --output PATH      Output filename, will be generated if not specified
  --currencies TEXT  Additional currencies to process for
  --help             Show this message and exit.

Commands:
  track-binance-rewards  Tracks Binance Airdrops and Savings.
  track-generic-rewards  Tracks generic crypto rewards from staking.
```

The specific commands for different types of rewards are `track-binance-rewards` and `track-generic-rewards`. To use, it will be something like
```
$ python crypto_rewards_tracker.py track-binance-rewards --help
```

If requiring an input file, the file is a csv of the following format:
```
data: comma separated values of (date, amount, txn_fee) where:
- date: mm/dd/yyyy
- amount: float
- txn_fee: float
```

If the ticker is ADA for Cardano, the will instead expect:
```
- epoch: integer
- start_date: mm/dd/yyyy
- end_date: mm/dd/yyyy
- amount: float
- txn_fee: float
```

## Examples
ADA
```
252,03/06/2021,03/11/2021,2,IN
253,03/11/2021,03/16/2021,3,IN
254,03/16/2021,03/21/2021,4,IN
255,03/21/2021,03/26/2021,3,IN
256,03/26/2021,03/31/2021,2,IN
257,03/31/2021,04/05/2021,3,IN
258,04/05/2021,04/10/2021,4,IN
259,04/10/2021,04/15/2021,3,IN
260,04/15/2021,04/20/2021,2,IN
```
