import pandas as pd


# Team 1
def clean_up(datatable_list):
    pass


# Team 1
def load_csv(csv_files: list):
    pass


# Team 1
PATHS=["sample.json"]
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
print(load_json(PATHS))

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
