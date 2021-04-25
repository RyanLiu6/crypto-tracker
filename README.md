
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

The script is relatively simple, and is accessed as:
```
usage: crypto_tracker.py [-h] [--output OUTPUT_FILE]
                         [--currencies CURRENCIES [CURRENCIES ...]]
                         ticker input_file

cryptocurrency tracker

positional arguments:
  ticker                Ticker of cryptocurrency
  input_file            A csv file containing information to process.

optional arguments:
  -h, --help            show this help message and exit
  --output OUTPUT_FILE  Output filename. If not specified, will be generated
                        based on ticker and time.
  --currencies CURRENCIES [CURRENCIES ...]
                        Additional currencies to process for
```

The input file is a csv of the following format:
```
data: comma separated values of (date, amount, txn_fee, txn_type) where:
- date: mm/dd/yyyy
- amount: float
- txn_fee: float
- txn_type: IN or OUT
```

If the ticker is ADA for Cardano, the will instead expect:
```
- epoch: integer
- start_date: mm/dd/yyyy
- end_date: mm/dd/yyyy
- amount: float
- txn_fee: float
- txn_type: IN or OUT
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
