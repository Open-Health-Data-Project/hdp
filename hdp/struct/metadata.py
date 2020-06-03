import pandas as pd


class Metadata:
    column_full = {}  # How much data is not NaN in every column
    index = 'Unknown'  # Index column name
    units = {}  # Units of data in columns
    dtype = {}  # Data types of data in columns
    data_min = {}  # Minimum acceptable value in each column if necessary
    data_max = {}  # Maximum acceptable value in each column if necessary

    def to_dataframe(self):
        df = pd.DataFrame({'column_full': self.column_full, 'units': self.units, 'dtype': self.dtype,
                           'data_min': self.data_min, 'data_max': self.data_max}).transpose()
        df.loc['index', self.index] = True
        return df


md = Metadata()
# Examples of values for the attributes above:
md.category = 'Activity'
md.column_full = {"A": 0.5, "B": 0.9, "C": 0.8, "D": 1.0}
md.index = ["A", "B"]
md.units = {"A": None, "B": "m", "C": "m/s", "D": "kg"}
md.dtype = {"A": "str", "B": "int", "C": "float", "D": "int"}
md.data_min = {"A": None, "B": 0, "C": 0, "D": 100}
md.data_max = {"A": None, "B": 100, "C": 50, "D": 200}



