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
def load_files(files_paths: list, load_params: dict):

    def load(_format, _files, _save):
        _result = supported_formats[_format](_files, load_params[_format])
        results[_save].extend(_result[0])
        if len(_result[1]) != 0:
            results['load_errors'][_format] = _result[1]

    if isinstance(files_paths[0], Path):
        files_paths = [str(file) for file in files_paths]
    results = {'datatables': [], 'jpg': [], 'load_errors': {}, 'problems': [], 'column_info': []}
    supported_files = {}

    for file in files_paths:
        try:
            file_ext = file.split('.')[1]
        except IndexError:
            results['load_errors'].setdefault('unsupported_files', []).append(file)
            continue

        if file_ext in supported_formats.keys():
            supported_files.setdefault(file_ext, []).append(file)
        else:
            results['load_errors'].setdefault('unsupported_files', []).append(file)

    for key, value in supported_files.items():
        if key not in ('gpx', 'tcx', 'jpg'):
            load(key, value, 'datatables')

    results['datatables'], results['problems'], results['column_info'] = clean_up(results['datatables'])

    for key, value in supported_files.items():
        if key in ('gpx', 'tcx'):
            load(key, value, 'datatables')

    if 'jpg' in supported_files.keys():
        load('jpg', supported_files['jpg'], 'jpg')

    return results
