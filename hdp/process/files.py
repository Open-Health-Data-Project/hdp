def load_csv(csv_files: list):
    pass


def load_txt(txt_files: list):
    pass


def load_xlsx(xlsx_files: list):
    pass


def load_xls(xls_files: list):
    pass


def load_gpx(gpx_files: list):
    pass


def load_tcx(tcx_files: list):
    pass


def load_jpg(jpg_files: list):
    pass


supported_formats = {'csv': load_csv,
                     'txt': load_txt,
                     'xlsx': load_xlsx,
                     'xls': load_xls,
                     'gpx': load_gpx,
                     'tcx': load_tcx,
                     'jpg': load_jpg}


def load_files(files_paths: list):
    pass
