import pandas as pd
import re
default_units = {'speed': 'km/h',
                 'distance': 'km',
                 'weight': 'kg',
                 'height': 'cm'}

units_conversions = {}


# Team 2
def convert_time(time: str, format: str = None, mode: str = 'flag'):
    """
    Converts string with time into pd.Timestamp object

    :param time: string with time, it can contain date, however it will be removed
    :param format: string with flag valid for pd.to_datetime function - if mode = flag,
    raw string with regex if mode = regex, default = None
    :param mode: string with value 'flag' or 'regex'
    - flag for using flag mode (matching time using flags recognised by pd.to_datetime,
    - regex for using regex patterns matching time
    :return: pd.Timestamp object if operation was successful else returns param time as a string
    """
    if mode == 'flag':
        try:
            dt_time = pd.to_datetime(time.split(' ')[-1].split('.')[0], 'ignore', format=format)  # Removing date
            # and microseconds
            try:
                return pd.to_timedelta(dt_time)
            except ValueError:
                return pd.to_timedelta(dt_time.time().__str__())
        except (TypeError, AttributeError):
            return str(time)

    elif mode == 'regex':
        try:
            re.compile(format)
            is_valid = True
        except re.error:
            is_valid = False
        if is_valid:
            try:
                return pd.to_timedelta(re.search(format, time).string.split('.')[0])  # Removing microseconds
            except AttributeError:
                return str(time)
        else:
            return str(time)


# Team 2
def convert_date(date: str, format, mode: str):
    pass


# Team 2
def convert_units(datatables: list):
    pass


# Team 2
def clean_data(datatables: list, meta: list, columns: dict, date_time: list):
    pass


