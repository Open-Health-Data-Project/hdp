import pandas as pd
import re
default_units = {'speed': 'km/h',
                 'distance': 'km',
                 'weight': 'kg',
                 'height': 'cm'}

units_conversions = {}


# Team 2
def convert_time(time: str, time_format: str = None, mode: str = 'flag'):
    """
        Converts string with time into pd.Timedelta object

        Parameters
        ----------
        time: string

        time_format: string
            It could contain valid flag for pd.to_datetime function - if mode = flag or
            raw string with regex - if mode = regex, default = None

        mode: string with value 'flag' or 'regex'
            Flag for using flag mode (matching time using flags recognised by pd.to_datetime,
            regex for using regex patterns matching time

        Returns
        -------
        pd.Timedelta object
            If operation was successful else returns time parameter unchanged.
        """
    if mode == 'flag':
        try:
            dt_time = pd.to_datetime(time, 'ignore', format=time_format)
            return pd.to_timedelta(str(dt_time.time()))
        except (TypeError, AttributeError):
            return str(time)

    elif mode == 'regex':
        try:
            re.compile(time_format)
            is_valid = True
        except re.error:
            is_valid = False
        if is_valid:
            try:
                return pd.to_timedelta(re.search(time_format, time).string.split('.')[0])  # Removing microseconds
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


