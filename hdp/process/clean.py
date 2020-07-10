import pandas as pd
import re
from scimath.units.api import UnitScalar
default_units = {'speed': 'km/h',
                 'distance': 'km',
                 'weight': 'kg',
                 'height': 'cm'}

units_conversions = {}


# Team 2
def convert_time(time: str, time_format: str = None, mode: str = 'flag') -> pd.Timedelta or str:
    """
        Converts string with time into pd.Timedelta object

        Parameters
        ----------
        time: string

        time_format: string
            if mode = flag : valid flags for pd.to_datetime function
            if mode = regex : raw string with regex. Each unit of time to be included in the result
                              should be named group of regex. One of the following values should be used as a key:
                              {'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks'}
                              Example of valid regex:
                              r"(?P<hours>[\d]{0,2})\:?(?P<minutes>[\d]{2})\:(?P<seconds>[\d]{2}).[\d]{3}"
            default = None : Default call of to_timedelta function without flags

        mode: string with value 'flag' or 'regex'
            flag for using flag mode (matching time using flags recognised by pd.to_datetime),
            regex for using regex patterns matching time

        Returns
        -------
        pd.Timedelta object if operation was successful, else returns time parameter as a string.
        """
    possible_keys = {'days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks'}
    if mode == 'flag':
        try:
            dt_time = pd.to_datetime(time, 'ignore', format=time_format)
            try:
                return pd.to_timedelta(dt_time)
            except ValueError:
                return pd.to_timedelta(str(dt_time.time()))
        except (TypeError, AttributeError):
            return str(time)

    elif mode == 'regex':
        if re_compiler(time_format) is True:
            try:
                time_dict = re.search(time_format, time).groupdict()
                time_dict = dict_comprehension(possible_keys, time_dict)
                return pd.Timedelta(**time_dict)
            except (AttributeError, KeyError):
                return str(time)
        else:
            return str(time)


# Team 2
def convert_date(date: str, date_format: str = None, mode: str = 'flag') -> pd.Timestamp or str:
    """
    Converts string with date into pd.Timestamp object

    Parameters
    ----------
    date : date in string format
    date_format: string
        if mode = flag : valid flags for pd.to_datetime function
        if mode = regex : raw string with regex. Each unit of date to be included in the result
                          should be named group of regex. One of the following values should be used as a key:
                          {'year', 'month', 'day', 'hour', 'minute', 'second', 'time_zone'}
                          Example of valid regex:
                          r"(?P<day>[\d]{2}) (?P<month>[\w]{3}) (?P<year>[\d]{2})"
        default = None : Default call of to_datetime function without flags
    mode : string
        flag for using flag mode (matching date using flags recognised by pd.to_datetime),
        regex for using regex patterns matching date
    Returns
    -------
    pd.Timestamp object if operation was successful, else returns date parameter as a string.

    """
    possible_keys = {'year', 'month', 'day', 'hour', 'minute', 'second', 'time_zone'}
    if mode == 'flag':
        try:
            return pd.to_datetime(date, 'ignore', format=date_format)
        except ValueError:
            return str(date)
    elif mode == 'regex':
        if re_compiler(date_format) is True:
            try:
                date_dict = re.search(date_format, date).groupdict()
                date_dict = dict_comprehension(possible_keys, date_dict)
                return pd.Timestamp(**date_dict)
            except (AttributeError, KeyError):
                return str(date)
        else:
            return str(date)


# Team 2
def convert_units(unit: str) -> float or str:
    """
    Convert units using UnitScalar object
    Parameters
    ----------
    unit : str representing value and units

    Returns
    -------
    float if operation was successful, else returns input parameter
    """
    pattern = r'''(?P<value>[\d]{1,}([.'"][\d]+)?)([ \t'"]*)(?P<unit>[^\s\d]+)([ \t'"]*)'''
    try:
        units_dict = re.search(pattern, unit).groupdict()
        scalar_unit = UnitScalar(units_dict['value'], units=units_dict['unit'])
        if scalar_unit.units.value == 1:
            return unit
        else:
            return float(scalar_unit) * scalar_unit.units.value
    except (AttributeError, TypeError):
        return unit


# Team 2
def clean_data(datatables: list, meta: list, clean_prop: list):
    def set_meta_obj(dt_list, meta_list):
        """
        Function to set right Metadata object as a DataTable.meta attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param meta_list: List of MetaData objects
        :type meta_list: list
        """
        for dt, meta in zip(dt_list, meta_list):
            dt.meta = meta

    def rename_columns(dt_list, cd_list):
        """
        Function to rename and drop columns according to CleanData.columns attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param cd_list: List of CleanData objects
        :type cd_list: list
        """
        for dt, cd in zip(dt_list, cd_list):
            for col in dt.dt.columns:
                if col not in cd.columns.keys():
                    dt.dt = dt.dt.drop(columns=col)
            dt.dt = dt.dt.rename(columns=cd.columns)

    def fill_values(dt_list, cd_list):
        """
        Function to fill missing values according to CleanData.missing_data attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param cd_list: List of CleanData objects
        :type cd_list: list
        """
        for dt, cd in zip(dt_list, cd_list):
            for col in dt.dt.columns:
                if not cd.missing_data[col]['permitted']:
                    if cd.missing_data[col]['fill_value'] is not None:
                        dt.dt[col] = dt.dt[col].fillna(value=cd.missing_data[col]['fill_value'])
                    elif cd.missing_data[col]['fill_method'] is not None:
                        dt.dt[col] = dt.dt[col].fillna(method=cd.missing_data[col]['fill_method'])
                    elif cd.missing_data[col]['fill_value'] is None and cd.missing_data[col]['fill_method'] is None:
                        dt.dt[col] = dt.dt[col].dropna()

    def set_index(dt_list, meta_list):
        """
        Function to set index according to Metada.index attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param meta_list: List of MetaData objects
        :type meta_list: list
        """
        for dt, meta in zip(dt_list, meta_list):
            dt.dt = dt.dt.set_index(meta.index)

    def set_datetime(dt_list, cd_list):
        """
        Function to set datetime values according to CleanData.date_time attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param cd_list: List of CleanData objects
        :type cd_list: list
        """
        for dt, cd in zip(dt_list, cd_list):
            for col in dt.dt.columns:
                if col in cd.date_time and cd.date_time[col] == 'datetime':
                    dt.dt[col] = dt.dt[col].apply(convert_date, args=(cd.patterns[col][0], cd.patterns[col][1]))
                elif col in cd.date_time and col not in cd.patterns:
                    dt.dt[col] = pd.to_datetime(dt.dt[col])

    def set_timedelta(dt_list, cd_list):
        """
        Function to set timedelta values according to CleanData.date_time attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param cd_list: List of CleanData objects
        :type cd_list: list
        """
        for dt, cd in zip(dt_list, cd_list):
            for col in dt.dt.columns:
                if col in cd.date_time and cd.date_time[col] == 'timedelta':
                    dt.dt[col] = dt.dt[col].apply(convert_time, args=(cd.patterns[col][0], cd.patterns[col][1]))
                elif col in cd.date_time and col not in cd.patterns:
                    dt.dt[col] = pd.to_timedelta(dt.dt[col])

    def set_categorical(dt_list, cd_list):
        """
        Function to change datatype according to CleanData.categorical attribute

        :param dt_list: List of Datatable objects
        :type dt_list: list

        :param cd_list: List of CleanData objects
        :type cd_list: list
        """
        for dt, cd in zip(dt_list, cd_list):
            for col in dt.dt.columns:
                if col in cd.categorical:
                    dt.dt[col] = dt.dt[col].astype('category')

    set_meta_obj(datatables, meta)
    rename_columns(datatables, clean_prop)
    fill_values(datatables, clean_prop)
    set_index(datatables, meta)
    set_datetime(datatables, clean_prop)
    set_timedelta(datatables, clean_prop)
    set_categorical(datatables, clean_prop)


def re_compiler(format: str) -> bool:
    """
    Checks if provided regex is valid

    Parameters
    ----------
    format: raw string with regex pattern

    Returns
    -------
    bool True if regex compiles, else False
    """

    try:
        re.compile(format)
        return True

    except re.error:
        return False


def get_month_number(value: str) -> int:
    """

    Parameters
    ----------
    value: string containing short or full month name - min 3 chars long

    Returns
    -------
    int representing month number
    """
    return {'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12
            }[value[:3].lower()]


def dict_comprehension(possible_keys: set, initial_dict: dict) -> dict:
    """

    Parameters
    ----------
    possible_keys: set with strings representing possible keys expected in the dictionary
    initial_dict: dictionary created using groupdict method on re.search object

    Returns
    -------
    dictionary validated for containing relevant keys

    """
    for k, v in initial_dict.copy().items():
        try:
            initial_dict[k] = int(v)
        except ValueError:
            initial_dict[k] = get_month_number(v)
    new_dict = {k if k in possible_keys else None: 0 if v == '' else int(v) for k, v in initial_dict.items()}
    if None in new_dict.keys():
        raise KeyError
    return new_dict
