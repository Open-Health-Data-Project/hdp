# Team 5
import os.path, time
import os
import pandas as pd
from pathlib import Path
from hdp.struct.profile import Profile


pr = Profile()
pr.name = 'Tomasz'


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
        writer = pd.ExcelWriter(directory.joinpath(name + "_data.xlsx"))
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
    with open('{}saved{}_files.txt'.format(pr.name + '_', '_'+mode), 'w') as f:
        f.write(profile['name'] + '\n')
        f.write(str(directory))
    # print(str(directory))
    # print(profile)
    # print(profile.keys())


def _read_directory_files(profile_name, mode):
    """Reading directory path from profile file"""
    with open('{}_saved_{}_files.txt'.format(pr.name, mode), 'r+') as f:
        for line in f:
            if line.startswith(profile_name):
                directory = next(f) + r'\\'
                # print(directory)
                return directory


def _read_files(profile_name, file, mode):
    """Reading data from saved profile data frames"""
    if mode == 'json':
        path = _read_directory_files(profile_name, 'json') + file + '.json'
        df_data = pd.read_json(path)
        print(df_data)
    elif mode == 'csv':
        path = _read_directory_files(profile_name, 'csv') + file + '.csv'
        df_data = pd.read_csv(path)
        print(df_data)
    elif mode == 'excel':
        path = _read_directory_files(profile_name, 'excel') + file + '.xlsx'
        df_data = pd.read_excel(path, sheet_name='data')
        print(df_data)


def _modify_time(profile_name, file, mode):
    """Reading file modification time"""
    if mode == 'excel':
        modify_time = time.ctime(os.path.getmtime(_read_directory_files(profile_name, mode)
                                                  + file + '.xlsx'))
    else:
        modify_time = time.ctime(os.path.getmtime(_read_directory_files(profile_name, mode)
                                                  + file + '.' + mode))
    return modify_time


def _file_list(profile_name):
    file_set = set()
    mode_list = ('excel', 'csv', 'json')
    for mode in mode_list:
        if _check_file_directory(profile_name, mode) is True:
            for file in os.listdir(_read_directory_files(profile_name, mode)):
                if '_data' in file:
                    file = file.rsplit('.', 1)[0]
                    if file not in file_set:
                        file_set.add(file)
    return file_set


def _check_file_directory(profile_name, mode):
    if os.path.isfile('{}_saved_{}_files.txt'.format(profile_name, mode)):
        return True
    else:
        return False


def _error_message(profile_name):
    if _check_file_directory(profile_name, 'csv') is False:
        print('No csv file directory path.')
    if _check_file_directory(profile_name, 'json') is False:
        print('No json file directory path.')
    if _check_file_directory(profile_name, 'excel') is False:
        print('No excel file directory path.')


def read_data(profile_name):
    file_check_set = set()
    excel_modify_time = 'Sat 0'
    json_modify_time = 'Sat 0'
    csv_modify_time = 'Sat 0'
    i = 0
    for file in _file_list(profile_name):
        if _check_file_directory(profile_name, 'excel') is True and os.path.isfile(_read_directory_files(profile_name, 'excel') + file + '.xlsx')\
                and file not in file_check_set:
            excel_modify_time = _modify_time(profile_name, file, 'excel')
            i += 1
        if _check_file_directory(profile_name, 'csv') is True and os.path.isfile(_read_directory_files(profile_name, 'csv') + file + '.csv')\
                and file not in file_check_set:
            csv_modify_time = _modify_time(profile_name, file, 'csv')
            i += 1
        if _check_file_directory(profile_name, 'json') is True and os.path.isfile(_read_directory_files(profile_name, 'json') + file + '.json') and\
                file not in file_check_set:
            json_modify_time = _modify_time(profile_name, file, 'json')
            i += 1
        if i >= 2:
            if excel_modify_time > json_modify_time and excel_modify_time > csv_modify_time\
                    and file not in file_check_set and os.path.isfile(_read_directory_files(profile_name, 'excel')
                                                                      + file + '.xlsx'):
                _read_files(profile_name, file, 'excel')
                file_metadata_list = pd.ExcelFile(_read_directory_files(profile_name, 'excel')
                                                  + file + '.xlsx')
                print(file_metadata_list.sheet_names)
                print('1' + file)
                file_check_set.add(file)
            elif json_modify_time > excel_modify_time and json_modify_time > csv_modify_time\
                    and file not in file_check_set and os.path.isfile(_read_directory_files(profile_name, 'json')
                                                                      + file + '.json'):
                _read_files(profile_name, file, 'json')
                file_metadata_list = os.listdir(_read_directory_files(profile_name, 'json') +
                                                file.replace('data', 'metadata'))
                print(file_metadata_list)
                print('2' + file)
                file_check_set.add(file)
            elif csv_modify_time > excel_modify_time and csv_modify_time > json_modify_time\
                    and file not in file_check_set and os.path.isfile(_read_directory_files(profile_name, 'csv')
                                                                      + file + '.csv'):
                _read_files(profile_name, file, 'csv')
                file_metadata_list = os.listdir(_read_directory_files(profile_name, 'csv') +
                                                file.replace('data', 'metadata'))
                print(file_metadata_list)
                print('3' + file)
                file_check_set.add(file)
        if file not in file_check_set:
            if _check_file_directory(profile_name, 'excel') and _check_file_directory(profile_name, 'json') and\
                    _check_file_directory(profile_name, 'csv') is True:
                if not os.path.isfile(_read_directory_files(profile_name, 'excel') + file + '.xlsx') and\
                        not os.path.isfile(_read_directory_files(profile_name, 'json') + file + '.json'):
                    _read_files(profile_name, file, 'csv')
                    file_metadata_list = os.listdir(_read_directory_files(profile_name, 'csv') +
                                                    file.replace('data', 'metadata'))
                    print(file_metadata_list)
                    print('4' + file)
                    file_check_set.add(file)
                if not os.path.isfile(_read_directory_files(profile_name, 'csv') + file + '.csv') and\
                        not os.path.isfile(_read_directory_files(profile_name, 'json') + file + '.json'):
                    _read_files(profile_name, file, 'excel')
                    file_metadata_list = pd.ExcelFile(_read_directory_files(profile_name, 'excel')
                                                      + file + '.xlsx')
                    print(file_metadata_list.sheet_names)
                    print('5' + file)
                    file_check_set.add(file)
                if not os.path.isfile(_read_directory_files(profile_name, 'excel') + file + '.xlsx') and\
                        not os.path.isfile(_read_directory_files(profile_name, 'csv') + file + '.csv'):
                    _read_files(profile_name, file, 'json')
                    file_metadata_list = os.listdir(_read_directory_files(profile_name, 'json'))
                    print(file_metadata_list)
                    print('6' + file)
                    file_check_set.add(file)
            else:
                _error_message(profile_name)


# save_data(pr.get_data(), 'csv')
read_data(pr.name)
