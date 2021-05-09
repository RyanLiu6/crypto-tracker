from datetime import datetime, timedelta


def string_to_datetime(date_string):
    """
    Converts a date string of the format MM/DD/YYYY to a datetime object.

    Args:
        date_string: string representing datetime in mm/dd/yyyy and PDT or PST

    Returns:
        Datetime object representing input date
    """
    return datetime.strptime(date_string, "%m/%d/%Y")


def datetime_to_string(date_object):
    """
    Converts a datetime object to a date string of the format MM/DD/YYYY.

    Args:
        date_object: datetime object representing datetime

    Returns:
        String representing datetime object of the format MM/DD/YYYY
    """
    return date_object.strftime("%m/%d/%Y")


def datetime_range(start=None, end=None):
    """
    Yields a range of datetime iterable for processing a range of dates.

    Args:
        start: datetime object representing the start
        end: datetime object representing the end

    Yields:
        Iteratable containing datetime objects starting from start and ends on end
    """
    span = end - start
    for i in range(span.days + 1):
            yield start + timedelta(days=i)


def calculate_average(nums):
    """
    Calculates average for an input list of numbers.

    Args:
        nums: List of numbers

    Returns:
        Average of input list
    """
    return sum(nums) / len(nums)


def get_timestamp_milliseconds(date):
    """
    Gets timestamp, in milliseconds.

    Args:
        date: Datetime object to get timestamp for

    Returns:
        Timestamp in milliseconds
    """
    return int(datetime.timestamp(date))*1000
