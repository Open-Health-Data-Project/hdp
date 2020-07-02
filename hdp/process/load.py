import pandas as pd
from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag
from typing import List,Tuple,Dict
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
    pass


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
            data_table.path = path
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
def load_tcx(tcx_files: List) -> Tuple[List,Dict]:
    # def extract_trackpoints(activity):
    #     for trackpoint in activity
    exceptions_dict = {}
    data_table_list = []
    data_table = DataTable()
    activites = []
    for path in tcx_files:
        try:
            name = _get_file_name(path)
            with (open(path, "r")) as file:
                activity = BeautifulSoup(file, "lxml")
            for trackpoint in activity.find_all("trackpoint"):
                point = {
                    element.name: element.text
                    for element in trackpoint.children
                    if isinstance(element, Tag) and len(element.findChildren()) == 0
                }
                for element in trackpoint.children:
                    if isinstance(element, Tag) and len(element.findChildren()) > 1:
                        for value in element.children:
                            if isinstance(value, NavigableString):
                                point[value.name] = value.string
                            elif isinstance(value, Tag):
                                point[value.name] = value.text.strip()
                activites.append(point)
            data_table.df = pd.DataFrame(activites)
        except Exception as e:
            exceptions_dict[name] = str(e)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions_dict


# Team 4
def load_jpg(jpg_files: list, params: dict):
    pass

a,b = load_tcx(["test.tcx"])
print(a[0].df)
