import csv

from collections.abc import Sequence
from typing import List, Dict, Iterator

from datetime import datetime, timedelta


def string_to_datetime(date_string: str) -> datetime:
    """
    Converts a date string of the format MM/DD/YYYY to a datetime object.

    Args:
        date_string (str): string representing datetime in mm/dd/yyyy and PDT or PST

    Returns:
        datetime: Datetime object representing input date
    """
    return datetime.strptime(date_string, "%m/%d/%Y")


def datetime_to_string(date_object: datetime) -> str:
    """
    Converts a datetime object to a date string of the format MM/DD/YYYY.

    Args:
        date_object (datetime): datetime object representing datetime

    Returns:
        str: String representing datetime object of the format MM/DD/YYYY
    """
    return date_object.strftime("%m/%d/%Y")


def timestamp_to_datetime(timestamp: float) -> datetime:
    """
    Custom conversion of timestamp in seconds to datetime object.

    Specifically, this sets everything to be 00:00:00.

    Args:
        timestamp (float): timestamp in seconds

    Returns:
        datetime: Datetime object representing timestamp such that we are at 00:00:00
    """
    date = datetime.fromtimestamp(timestamp // 1000)
    date = date.replace(hour=0, minute=0, second=0, microsecond=0)

    return date


def datetime_range(start: datetime=None, end: datetime=None) -> Iterator:
    """
    Yields a range of datetime iterable for processing a range of dates.

    Args:
        start (datetime): Datetime object representing the start
        end (datetime): Datetime object representing the end

    Yields:
        Iterator: Iteratable containing datetime objects starting from start and ends on end
    """
    span = end - start
    for i in range(span.days + 1):
            yield start + timedelta(days=i)


def calculate_average(nums: List[int]) -> float:
    """
    Calculates average for an input list of numbers.

    Args:
        nums (List[int]): List of numbers

    Returns:
        float: Average of input list
    """
    return sum(nums) / len(nums)


def get_timestamp_milliseconds(date: datetime) -> float:
    """
    Gets timestamp, in milliseconds.

    Args:
        date (datetime): Datetime object to get timestamp for

    Returns:
        float: Timestamp in milliseconds
    """
    return int(datetime.timestamp(date))*1000


def write_csv_to_file(field_names: Sequence, output_prefix: str, data_to_write: List[Dict]) -> None:
    """
    Writes data to a CSV.

    Args:
        field_names (Sequence): Field names of the CSV file
        output_prefix (str): Prefix of the output CSV file name - the name is postfixed
            with the current time in milliseconds
        data_to_write (List[Dict]): Data to write, list of dictionaries where each dictionary
            has every element of field_names as keys
    """
    output_file_name = f"{output_prefix}_{get_timestamp_milliseconds(date=datetime.now())}.csv"
    with open(output_file_name, "w", newline="") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=field_names)

        writer.writeheader()

        for row in data_to_write:
            writer.writerow(row)

    print(f"CSV File written to {output_file_name}")
