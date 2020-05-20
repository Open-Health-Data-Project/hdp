class CleanData:
    columns = {}
    patterns = {}
    missing_data = {}
    date_time = {}
    categorical = []


# Examples of attributes formats:
columns = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
patterns = {"A": [None, None], "B": [r"/d/d:/d/d:/d/d", "regex"]}
missing_data = {"A": {'permitted': True, 'fill_value': "a", 'fill_method': 'ffill'},
                "B": {'permitted': False, 'fill_value': None, 'fill_method': None},
                "C": {'permitted': True, 'fill_value': 1.0, 'fill_method': 'bfill'},
                "D": {'permitted': False, 'fill_value': None, 'fill_method': None}}
date_time = {"A": 'datetime', "C": 'timedelta'}
categorical = ["B", "D"]
# a, b, c, d - initial column names, A, B, C, D - column names after change
