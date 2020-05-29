import pandas as pd
from hdp.struct.datatable import DataTable
from pathlib import Path


def _get_file_name(path):
    if isinstance(path, Path):
        name = path.name
    else:
        name = Path(str(path)).name
    return name


# Team 1
def clean_up(datatable_list):
    # usuwanie kolumn z Nan
    df_without_missing = df.dropna(how='all', axis=0) #po kolumnach
    df_without_missing = df.dropna(how='all', axis=1)  # po wierszach

    # sprawdzanie typów danych
    columns_object_str = {}
    for i in df_without_missing:
        type = df_without_missing.dtypes()
    if type == 'object' or 'str':
        columns_object_str[i] = type

    # datetime jako index
    index_col = 'kolumna_z_datą'

    # czy indeks jest unikalny (nie jestem pewna, czy to)
    not_unique_index = {}
    for index in df_without_missing:
        if index = pd.Series.is_unique(index):
            break
    else:
    not_unique_index = 'NAZWA KOLUMNY'  # nie wiem, jak to zapisać


# ile procent nie jest Nan
count = df_without_missing.notnull().sum(axis=0)  # suma wierszy z wartosciami
count_row = df_without_missing.shape[0]  # suma wszystkich wierszy, moze byc tez len(df.index)
not_null = (count / count_row) * 100  # procent wierszy z wartosciami


def load_csv(csv_files: list, params: dict):
    """
    Read list of CSV files.

    Parameters
    ----------
    csv_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_csv function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    data_table_list = []
    exceptions = {}
    for path in csv_files:
        data_table = DataTable()
        name = _get_file_name(path)
        try:
            data_table.df = pd.read_csv(path, **params)
        except Exception as exc:
            exceptions[name] = str(exc)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions


# Team 1
def load_json(json_files: list, params: dict):
    """
    Read list of JSON files.

    Parameters
    ----------
    json_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_json function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    data_table_list = []
    exceptions = {}
    for path in json_files:
        data_table = DataTable()
        name = _get_file_name(path)
        try:
            data_table.df = pd.read_json(path, **params)
        except Exception as exc:
            exceptions[name] = str(exc)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions


# Team 1
def load_xlsx(xlsx_files: list, params: dict):
    """
    Read list of xlsx files.

    Parameters
    ----------
    xlsx_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_excel function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    data_table = DataTable()

    for path in xlsx_files:
        try:
            data_table.df = pd.read_excel(path, **params)
            name = _get_file_name(path)

        except Exception as e:
            exceptions_dict[name] = str(e)

        else:
            data_table.name = name
            data_table_list.append(data_table)

    return data_table_list, exceptions_dict


# Team 1
def load_xls(xls_files: list, params: dict):
    """
    Read list of xls files.

    Parameters
    ----------
    xls_files: list of paths
        Path objects from pathlib and string convertible
        paths are supported.

    params: dict
        Parameters to pass to Pandas read_excel function.

    Returns
    -------
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    data_table = DataTable()

    for path in xls_files:
        try:
            data_table.df = pd.read_excel(path, **params)
            name = _get_file_name(path)

        except Exception as e:
            exceptions_dict[name] = str(e)

        else:
            data_table.name = name
            data_table_list.append(data_table)

    return data_table_list, exceptions_dict


# Team 3
def load_gpx(gpx_files: list, params: dict):
    pass


# Team 3
def load_tcx(tcx_files: list, params: dict):
    pass


# Team 4
def load_jpg(jpg_files: list, params: dict):
    pass
