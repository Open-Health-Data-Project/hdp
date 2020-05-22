import pandas as pd
from hdp.struct.datatable import DataTable


# Team 1
def clean_up(datatable_list):
    pass


# Team 1
def load_csv(csv_files: list):
    data_table_list = []
    exceptions = {}
    for path in csv_files:
        data_table = DataTable()
        try:
            data_table.df = pd.read_csv(path)
        except FileNotFoundError:
            exceptions[path] = "File does not exist"
        except ValueError:
            exceptions[path] = "Invalid path or object not string"
        except Exception as exc:
            exceptions[path] = str(exc)
        else:
            data_table.name = path
            data_table_list.append(data_table)

    return data_table_list, exceptions


# Team 1
def load_json(txt_files: list):
    exception_dict = dict()
    data_table_list = list()
    data = str()
    for path in txt_files:
        try:
            with(open(path, "r")) as file:
                for line in file:
                    data += line.strip()
            data_table=pd.read_json(data,orient="index")
            data_table.name=path
            data_table_list.append(pd.read_json(data,orient="index"))
        except ValueError:
            exception_dict = {path: "ValueError"}
    return data_table_list, exception_dict

# Team 1
def load_xlsx(xlsx_files: list):
    pass


# Team 1
def load_xls(xls_files: list):
    pass


# Team 3
def load_gpx(gpx_files: list):
    pass


# Team 3
def load_tcx(tcx_files: list):
    pass


# Team 4
def load_jpg(jpg_files: list):
    pass
