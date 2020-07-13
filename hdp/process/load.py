from pathlib import Path
from typing import List, Tuple, Dict

from bs4 import BeautifulSoup
from bs4 import NavigableString, Tag

from hdp.struct.datatable import DataTable

import gpxpy
import pandas as pd


def _get_file_name(path):
    if isinstance(path, Path):
        name = path.name
    else:
        name = Path(str(path)).name
    return name


# Team 1
def clean_up(datatable_list):
    pass


def load_csv(csv_files: list, params: dict = {}):
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
def load_json(json_files: list, params: dict = {}):
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
def load_xlsx(xlsx_files: list, params: dict = {}):
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
def load_xls(xls_files: list, params: dict = {}):
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


def extract_tracks(gpx_parsed):
    track_list = list()
    if len(gpx_parsed.tracks) != 0:
        for track in gpx_parsed.tracks:
            for segment in track.segments:
                for point in segment.points:
                    track_dict = {"type": "Trackpoint", "longitude": point.longitude, "elevation": point.elevation,
                                  "latitude": point.latitude, "time": point.time if not "None" else None}
                    track_list.append(track_dict)
    return track_list


def extract_waypoints(gpx_parsed):
    track_list = list()
    for waypoint in gpx_parsed.waypoints:
        waypoint_dict = {}
        waypoint_dict["type"] = "Waypoint"
        waypoint_dict["longitude"] = waypoint.longitude
        waypoint_dict["elevation"] = waypoint.elevation
        waypoint_dict["latitude"] = waypoint.latitude
        track_list.append(waypoint_dict)
    return track_list


def get_gpx_metadata(gpx_parsed, file_name):
    """
    Gets metadata from gpx_file

    Parameters
    -----------
    gpx_parsed = .gpx file parsed using gpxpy.parse

    Returns
    -----------
    Dictionary with metadata.
    """
    # gpx_parsed = gpxpy.parse("")
    metadata = {}
    metadata["file_name"] = file_name
    metadata["start_time"], metadata["stop_time"] = gpx_parsed.get_time_bounds()
    lenght = gpx_parsed.length_2d()
    duration = pd.to_timedelta(gpx_parsed.get_duration(), unit="s")
    metadata["duration"] = duration
    moving = gpx_parsed.get_moving_data()
    if lenght is not None and duration is not None and duration.total_seconds() != 0:
        metadata["average_speed"] = lenght / duration.total_seconds()
    else:
        metadata["average_speed"] = None
    metadata["min_elevation"], metadata["max_elevation"] = gpx_parsed.get_elevation_extremes()
    metadata["length"] = lenght
    metadata["uphill_elevation"], metadata["downhill_elevation"] = gpx_parsed.get_uphill_downhill()
    return metadata


# Team 3
def load_gpx(gpx_files: list) -> Tuple[List[DataTable], Dict]:
    """
    Read list of gpx files

    Parameters
    ------------
    gpx_files: list of paths to .gpx files

    Returns
    -----------
    List with DataTable objects,DataFrame whose contain metadata and dictonary with exceptions whose occurred
    during read .gpx file
    """
    exception_dict = {}
    data_table_list = []
    metadata_pandas = DataTable()
    data_table = DataTable()
    metadata = []
    try:
        for path in gpx_files:
            name = _get_file_name(path)
            with (open(path, "r")) as file:
                gpx_parsed = gpxpy.parse(file)
            waypoints = extract_waypoints(gpx_parsed)
            tracks = extract_tracks(gpx_parsed)
            metadata.append(get_gpx_metadata(gpx_parsed, name))

            points = tracks + waypoints
            data_table.df = pd.DataFrame(points)
            data_table.name = name
            data_table.df.dropna(axis=1, how="all", inplace=True)
            data_table_list.append(data_table)
    except Exception as e:
        exception_dict[name] = str(e)
    else:
        data_table.name = name
        data_table_list.append(data_table)
    metadata_pandas = pd.DataFrame(metadata)
    metadata_pandas.append(metadata, ignore_index=True)
    return data_table_list, metadata_pandas.dropna(axis=0, how="all"), exception_dict


def extract_one_field_data(trackpoint) -> Dict:
    """
    :param trackpoint:
    :return: Not nested point values
    """
    point = {single_element.name: single_element.text
             for single_element in trackpoint.children
             if isinstance(single_element, Tag) and len(single_element.findChildren()) == 0}
    return point


def extract_nested_values(trackpoint) -> Dict:
    point = {}
    for element in trackpoint.children:
        if isinstance(element, Tag) and len(element.findChildren()) > 1:
            for value in element.children:
                if isinstance(value, NavigableString):
                    point[value.name] = value.string
                elif isinstance(value, Tag):
                    point[value.name] = value.text.strip()
    return point


# Team 3
def load_tcx(tcx_files: List) -> Tuple[List, Dict]:
    """
    Read list of tcx files
    :param tcx_files : List
        List of path to tcx
    :return:
    DataTable list:
        List of parsed DataTable objects with file name and DataFrame attributes filled.

pass
    Exceptions dictionary:
        Dictionary with files names as keys and exceptions strings as values.
        Contains only files where an exception occurred.
    """
    exceptions_dict = {}
    data_table_list = []
    for path in tcx_files:
        try:
            data_table = DataTable()
            activites = []
            name = _get_file_name(path)
            with (open(path, "r")) as file:
                activity = BeautifulSoup(file, "lxml")
            for trackpoint in activity.find_all("trackpoint"):
                point = extract_one_field_data(trackpoint)
                nested_data = extract_nested_values(trackpoint)
                point = {**point, **nested_data}
                activites.append(point)
            data_table.df = pd.DataFrame(activites)
        except Exception as e:
            exceptions_dict[name] = str(e)
        else:
            data_table.name = name
            data_table_list.append(data_table)
    return data_table_list, exceptions_dict


# Team 4
def load_jpg(jpg_files: list, params: dict = {}):
    pass
