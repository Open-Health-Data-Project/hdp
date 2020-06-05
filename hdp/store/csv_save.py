# Team 5
import os
import pandas as pd
from PIL import Image


def save_to_csv(datatable, directory=None):

    def save_file(data, file_name, directory):
        directory = directory.strip("/")
        try:
            data.to_csv(f'{directory}/{file_name}.csv', encoding='utf-8')
        except FileNotFoundError:
            print("No such a directory: ", directory)


    for name, file in datatable.items():  # example1, roz...2, roz...n
        if name == "images":
            pass
            # for image in file:
            #     im = Image.open(fr'{image}')
            #     im.save(f"{image}")  # function to save images
        elif name == "load_errors":
            path = f'{list(datatable.keys())[0]}_load_errors.csv'
            if directory:
                directory = directory.strip("/")
                path = rf'{directory}/{path}'
            with open(path, 'w') as f:          # tu bedzie zapisywał pd.series (poprawię)
                for error, error_desc in file.items():
                    f.write(f"{error};{error_desc};\n")
        else:
            for key, values in file.items():  # all datas from dictionary
                file_name = str(name) + "_" + str(key)
                for item in values:
                    if isinstance(item, pd.DataFrame) or isinstance(item, pd.Series):
                        if directory:
                            save_file(item, file_name, directory)
                        else:
                            item.to_csv(f'{file_name}.csv', encoding='utf-8')
                    else:
                        print("Unknown or incorrect format!")
    with open('saved_files.txt', 'w') as f:
        f.write(directory)


def open_csv(profile):
    data = {profile : {}}
    with open('saved_files.txt', 'r') as f:
        path = f.read().strip() + "/"
        file_list = os.listdir(path)
        for file in file_list:
            full_filename = os.path.splitext(file)
            if profile in file and os.path.splitext(file)[1] == ".csv":
                filename = full_filename[0].lstrip(profile)
                filename = filename.lstrip("_")
                if filename == 'load_errors':
                    print("Zapis do pd.series")
                else:
                    try:
                        data[profile][filename] = pd.read_csv(f"{path + file}")
                    except:
                        print("Error!")
    return data
