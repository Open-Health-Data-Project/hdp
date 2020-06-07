# Team 5
import os
import pandas as pd
from pathlib import Path
from hdp.struct.profile import pr
# from PIL import Image


# def save_to_csv(profile, directory=Path(r"/data")):
#
#     def save_file(data, file_name, directory):
#         try:
#             # data.to_csv(f'{file_name}.csv', header=False, encoding='utf-8')
#             print(directory.joinpath(file_name + ".csv"))
#         except FileNotFoundError:
#             print("No such a directory: ", directory)
#
#     if isinstance(directory, str):
#         directory = Path(directory)
#     directory = directory.joinpath(profile["name"])
#     for name, file in profile.items():  # example1, roz...2, roz...n
#         directory_meta = directory.joinpath(name + "_metadata")
#         if name in ("name", "images", 'native_format'):
#             pass
#             # for image in file:
#             #     im = Image.open(fr'{image}')
#             #     im.save(f"{image}")  # function to save images
#         elif name == "load_errors":
#             save_file(file, name, directory)
#         else:
#             for key, data in file.items():
#                 file_name = str(name) + "_" + str(key)
#                 if key is "data":
#                     save_file(data, file_name, directory)
#                 else:
#                     save_file(data, file_name, directory_meta)
#
#     # with open('saved_files.txt', 'w') as f:
#     #    f.write(directory)
#     print(profile["name"] + "," + str(directory))


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


# save_to_csv(pr.get_data())
# print(open_csv("Example"))