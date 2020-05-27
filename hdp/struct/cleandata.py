import pandas as pd


class CleanData:
    columns = {}
    patterns = {}
    missing_data = {}
    date_time = {}
    categorical = []
    column_info = {}

    def to_dataframe(self):
        df = pd.DataFrame(columns=[value for value in self.columns.values()])

        for key, value in self.columns.items():
            df.loc['columns', value] = key

        for key, value in self.patterns.items():
            df.loc['patterns:0', key] = value[0]
            df.loc['patterns:1', key] = value[1]

        for key, value in self.missing_data.items():
            for k, v in value.items():
                df.loc['missing_data:' + k, key] = v

        for key, value in self.date_time.items():
            df.loc['date_time', key] = value

        for key in self.categorical:
            df.loc['categorical', key] = True

        for key, value in self.column_info.items():
            df.loc['column_info', key] = value
        return df


cd = CleanData()

# Examples of attributes formats:
cd.columns = {'a': 'A', 'b': 'B', 'c': 'C', 'd': 'D'}
cd.patterns = {'A': [None, None], 'B': [r'/d/d:/d/d:/d/d', 'regex']}
cd.missing_data = {'A': {'permitted': True, 'fill_value': 'a', 'fill_method': 'ffill'},
                'B': {'permitted': False, 'fill_value': None, 'fill_method': None},
                'C': {'permitted': True, 'fill_value': 1.0, 'fill_method': 'bfill'},
                'D': {'permitted': False, 'fill_value': None, 'fill_method': None}}
cd.date_time = {'A': 'datetime', 'C': 'timedelta'}
cd.categorical = ['B', 'D']
cd.column_info = {'A': 0.9, 'B': 0.8, 'C': 1.0, 'D': 0.1}
# a, b, c, d - initial column names, A, B, C, D - column names after change

# Two copies of CleanData object used only for testing
cds = [cd, cd]