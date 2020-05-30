# Team 5
import pandas as pd


def save_file(file_name, directory):    # probably temporary function
    directory = directory.strip("/")
    try:
        data.to_csv(f'{directory}/{file_name}.csv', encoding='utf-8')
    except FileNotFoundError:
        print("No such a directory: ", directory)


def save_to_csv(datatable, directory=None):
    for key, file in datatable.items():  # rozszerzenie_1, roz...2, roz...n
        print(key)
        for items in file:      # all files
            for item in items:  # content of files
                if type(item) is list:
                    for i in item:      # all data from dataframes and series
                        print("  Lista:", i)
                        if isinstance(i, dict):
                            for k, v in i.items():
                                print("        Dict:", k, v)
                                # if directory is None and isinstance(v, pd.DataFrame) or isinstance(v, pd.Series):
                                #     v.to_csv(f'{file_name}.csv', encoding='utf-8')
                                # else:
                                #     save_file(file_name, directory)
                        else:
                            print("        Else:", i)
                else: 
                    print("  ", item)
                    continue


def open_csv():
    pass


pseudodata = {
    'exercise': [
        [
            'file.cs',
            [
                {'dt': ['dane DF'],
                 'meta': ['obiekt Metadata DF']
                 },
                {
                    'dt_meta': ['rest of data SR'],
                    'opcjonalne': ['dane opcjonalne']
                }
            ],
            ['obiekt Cleandata DF']
        ],
    ]
}

save_to_csv(pseudodata)
