# Team 5
import os.path
import os
import pandas as pd
from pathlib import Path
from hdp.struct.profile import Profile

pr = Profile()


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
    # profile = pr.get_data()
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
    with open('saved{}_files.txt'.format('_'+mode), 'w') as f:
        f.write(profile['name'] + '\n')
        f.write(str(directory))
    # print(str(directory))
    # print(profile)
    # print(profile.keys())


def _read_files(profile_name, mode):
    with open('saved_{}_files.txt'.format(mode), 'r+') as f:
        for line in f:
            if line.startswith(profile_name):
                directory = next(f) + r'\\'
                # print(directory)
                return directory


def read_data(profile_name, file_name, mode):
    if mode == 'excel':
        path = _read_files(profile_name, 'excel') + file_name
        if os.path.isfile(path):
            df = pd.read_excel(path, sheet_name=None)
            print(df)
    elif mode == 'csv':
        path = _read_files(profile_name, 'csv') + file_name
        if os.path.isfile(path):
            df = pd.read_csv(path)
            print(df)
        else:
            for key in pr.get_data().keys():
                if key == 'name' or key == 'images' or key == 'load_errors':
                    continue
                else:
                    path = _read_files(profile_name, 'csv') + key + r'_metadata\\' + file_name
                    if os.path.isfile(path):
                        df = pd.read_csv(path)
                        print(df)
    elif mode == 'json':
        path = _read_files(profile_name, 'json') + file_name
        if os.path.isfile(path):
            df = pd.read_json(_read_files(profile_name, 'json') + file_name)
            print(df)
        else:
            for key in pr.get_data().keys():
                if key == 'name' or key == 'images' or key == 'load_errors':
                    continue
                else:
                    path = _read_files(profile_name, 'json') + key + r'_metadata\\' + file_name
                    if os.path.isfile(path):
                        df = pd.read_csv(path)
                        print(df)


save_data(pr.get_data(), 'csv')
read_data(pr.name, 'Example_clean.json', 'json')
