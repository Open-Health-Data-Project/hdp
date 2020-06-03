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
        if re_compiler(format) is True:
            try:
                return pd.to_timedelta(re.search(time_format, time).group())  # Removing microseconds
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
    :param format: raw string with regex pattern
    :return: bool True if regex compiles, else False
    """

    try:
        re.compile(format)
        return True

    except re.error:
        return False
