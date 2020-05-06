from hdp.process.load import *

supported_formats = {'csv': load_csv,
                     'txt': load_txt,
                     'xlsx': load_xlsx,
                     'xls': load_xls,
                     'gpx': load_gpx,
                     'tcx': load_tcx,
                     'jpg': load_jpg}


def load_files(files_paths: list):
    pass
