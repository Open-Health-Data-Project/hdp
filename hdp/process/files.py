from hdp.struct.profile import Profile
from hdp.process.load import *
from pathlib import Path

supported_formats = {'csv': load_csv,
                     'json': load_json,
                     'xlsx': load_xlsx,
                     'xls': load_xls,
                     'gpx': load_gpx,
                     'tcx': load_tcx,
                     'jpg': load_jpg}


# Team 1
def load_files(files_paths: list, load_params: dict, profile: Profile):
    """
        Read list of files supported by application.

        Parameters
        ----------
        files_paths: list of paths
            Path objects from pathlib and string convertible
            paths are supported.

        load_params: dict
            Parameters to pass to read functions.

        profile: Profile
            Profile object to save data.

        Returns
        -------
        Profile
            Profile object with loaded data.
        """
    def load(_format, _files):
        datatables, load_errors = supported_formats[_format](_files, load_params[_format])
        if _format not in ('gpx', 'tcx'):
            datatables = clean_up(datatables)
        profile.add_data(datatables, load_params[_format], _format, load_errors)

    if isinstance(files_paths[0], str):
        files_paths = [Path(file) for file in files_paths]
    results = {'datatables': [], 'jpg': [], 'load_errors': {}, 'problems': [], 'column_info': []}
    supported_files = {}

    for file in files_paths:
        try:
            file_ext = file.suffix.replace('.', '')
        except IndexError:
            results['load_errors'].setdefault('unsupported_files', []).append(file)
            continue

        if file_ext in supported_formats.keys():
            supported_files.setdefault(file_ext, []).append(file)
        else:
            results['load_errors'].setdefault('unsupported_files', []).append(file)

    for key, value in supported_files.items():
        if key not in ('gpx', 'tcx', 'jpg'):
            load(key, value)

    for key, value in supported_files.items():
        if key in ('gpx', 'tcx'):
            load(key, value)

    if 'jpg' in supported_files.keys():
        profile.images = load_jpg(supported_files['jpg'], load_params['jpg'])

    return profile
