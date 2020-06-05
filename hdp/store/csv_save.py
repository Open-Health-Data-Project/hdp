# Team 5
import os
import pandas as pd
# from PIL import Image


def save_to_csv(datatable, directory=None):

    def save_file(data, file_name, directory=None):
        try:
            if directory:
                directory = directory.strip("/")
                data.to_csv(f'{directory}/{file_name}.csv', header=False, encoding='utf-8')
            else:
                data.to_csv(f'{file_name}.csv', header=False, encoding='utf-8')
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
            file = pd.Series(file)
            save_file(file, path, directory)
        else:
            for key, values in file.items():  # all datas from dictionary
                file_name = str(name) + "_" + str(key)
                for item in values:
                    if isinstance(item, pd.DataFrame) or isinstance(item, pd.Series):
                        save_file(item, file_name, directory)
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
                    data[profile][filename] = pd.read_csv(f"{path + file}", index_col=1, header=None, encoding='utf-8')
                else:
                    try:
                        data[profile][filename] = pd.read_csv(f"{path + file}", index_col=1, header=None, encoding='utf-8')
                    except:
                        print("Error!")
    return data


# pseudodata = {
#     'Example': {
#         'plik1': ['dane DF'],
#         'meta': ['obiekt Metadata DF'],
#         'dt_meta': [pd.Series([11, 33, 55, 66], index=["abc","cde","cft","kol"])],
#         'opcjonalne': [pd.Series([122, 667, 445, 336], index=["abc55","cd55e","c55ft","k55ol"])],
#         'Example_clean': ['obiekt Cleandata DF']
#     },
#     'images': ['2321.jpg', '2er.JPG', 'dfs.IMG', 'ffvbc.gif', 'the.png', 'rtttt.gpx'],
#     'load_errors': {r"C://example/example.file": "File not found",
#               r"C://example/example.file1": "File not found",
#              r"C://example/example.file2": "File not found",
#              r"C://example/example.file3": "File not found"}
# }
#
# save_to_csv(pseudodata, directory=r"e:/Python/pliki/")
# print(open_csv("Example"))