# Team 5
import pandas as pd
from hdp.struct.profile import Profile

# df1 = pd.DataFrame([['a', 'b'], ['c', 'd']])
# df2 = pd.DataFrame([['1', '2'], ['6', '8']])


def save_to_excel(name, datatable, directory=None):
    for key, file in datatable.items():
        for items in file:
            for item in items:
                if type(item) is list:
                    for i in item:
                        if isinstance(i, dict):
                            for k, v in i.items():
                                if directory is None and isinstance(v, pd.DataFrame) or isinstance(v, pd.Series):
                                    v.to_excel(name + '_' + '.xlsx', encoding='utf-8')
                else:
                    continue


def open_excel(file, directory=None):
    df = pd.read_excel(file)
    print(df)


# pseudodata = {'rozszerzenie_1': [
#   [
#     'file.cs',
#     [
#       {
#         'dt': df2,
#         'meta': df1
#       },
#       {
#         'dt_meta': df1,
#         'subcategory': df1,
#         'relation:0': df1,
#         'relation:n': df1
#       }
#     ],
#     df1
#   ],
# ]
# }
pr = Profile()
print(pr.get_data())
save_to_excel('excercise', pr.get_data())
open_excel('excercise_.xlsx')
