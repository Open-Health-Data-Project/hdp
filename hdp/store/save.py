# Team 5
import os
import pandas as pd
from pathlib import Path


def _save_file(data, file_name, directory, mode, save_params):
    if not directory.exists():
        directory.mkdir(parents=True)
    if mode is 'csv':
        data.to_csv(directory.joinpath(file_name + ".csv"), header=False, encoding='utf-8', **save_params)
    elif mode is 'json':
        data.to_json(directory.joinpath(file_name + ".json"), **save_params)
    print(directory.joinpath(file_name + "." + mode))


def save_to_excel(name, spreadsheet, directory, save_params):
    if not directory.exists():
        directory.mkdir(parents=True)
    if name is 'load_errors':
        spreadsheet.to_excel(directory.joinpath('load_errors.xlsx'), **save_params)
    else:
        writer = pd.ExcelWriter(directory.joinpath(name + ".xlsx"))
        for key, data in spreadsheet.items():
            data.to_excel(writer, key, **save_params)
        writer.save()


def save_data(profile, mode, directory=Path(r"data/"), save_params=None):
    profile = profile.get_data()
    if save_params is None:
        save_params = {}
    if isinstance(directory, str):
        directory = Path(directory)
    if directory.is_absolute():
        directory = directory.joinpath(profile["name"])
    else:
        directory = Path(os.path.expanduser(r'~/Documents/Open Health Data Project'))\
            .joinpath(directory.joinpath(profile["name"]))
    if mode is not 'database':
        directory = directory.joinpath(mode)
        for name, file in profile.items():  # example1, roz...2, roz...n
            directory_meta = directory.joinpath(name + "_metadata")
            if name in ("name", "images", 'native_format'):
                pass
            else:
                if mode is not 'excel':
                    if name == "load_errors":
                        _save_file(file, name, directory, mode, save_params)
                    else:
                        for key, data in file.items():
                            file_name = str(name) + "_" + str(key)
                            if key is "data":
                                _save_file(data, file_name, directory, mode, save_params)
                            else:
                                _save_file(data, file_name, directory_meta, mode, save_params)
                else:
                    save_to_excel(name, file, directory, save_params)
    # with open('saved_files.txt', 'w') as f:
    #    f.write(directory)
    print(str(directory))


def read_data():
    pass
