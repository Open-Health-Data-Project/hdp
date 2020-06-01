from hdp.struct.metadata import Metadata
from hdp.struct.metadata import md
from hdp.struct.categories import *
from hdp.struct.cleandata import *
from enum import Enum


class Frequency(Enum):
    monthly = 'mo'
    weekly = 'w'
    daily = 'd'
    minute = 'min'
    second = 's'
    millisecond = 'ms'
    custom = 'cs'


class Relation:  # Relation many-to-many
    dt_to = None  # Target table name - string
    col_from = []  # Names of columns from this DataTable - string list
    col_to = []  # Names of columns from target DataTable - string list

    def to_series(self):
        return pd.Series({'dt_to': self.dt_to, 'col_from': self.col_from, 'col_to': self.col_to})


class DataTable:
    name = ""
    path = r""
    frequency = Frequency.custom  # Time period between rows
    row_full = 1.0  # If every unit of time available in the data as percent of values
    category = None  # General type of data for example Health, Food, Activity, Environment, Sleep etc. as string
    df = pd.DataFrame()
    meta = Metadata()
    clean = CleanData()
    subcategory = PhysicalActivity()  # One subcategory for the whole table, if it's common for every column
    subcategories = {}  # Subcategories for subset of rows if necessary
    relations = []
    problems = {}
    load_parameters = {}

    def to_pandas(self):
        df_dict = {'dt': self.df, 'meta': self.meta.to_dataframe()}
        dt_series = pd.Series({**{'name': self.name, 'path': self.path, 'frequency': self.frequency,
                               'row_full': self.row_full, 'category': self.category}, **self.problems,
                               **self.load_parameters})
        series_dict = {'dt_meta': dt_series, 'subcategory': self.subcategory.to_series()}
        for columns, subcategory in self.subcategories.items():
            series_dict[columns] = subcategory.to_series()
        for num, relation in enumerate(self.relations):
            series_dict['relation:' + str(num)] = relation.to_series()
        return [df_dict, series_dict]


# Examples:
rel = Relation()
rel.dt_to = 'activity_1'
rel.col_from = ['A', 'B']
rel.col_to = ['E', 'F', 'G']

dt = DataTable()
dt.name = "Example"
dt.path = r"C://example/activity.csv"
dt.frequency = Frequency.daily
dt.category = "Activity"
dt.df = pd.DataFrame(columns=['A', 'B', 'C', 'D'], data=[[1, 2, 3, 4], [6, 7, 8, 9]])
dt.meta = md
dt.subcategory = PhysicalActivity()
dt.subcategories = {("A", "B", "C"): PhysicalActivity(), ("D"): PhysicalActivity()}
dt.relations = [rel]
dt.problems = {'A': 5, 'B': 'Example', 'C:dtype': 'str', 'possible_indexes': ('C', 'D'), 'not_unique_index': 'A'}

# Two copies of the same DataTable used only for testing
dts = [dt, dt]



