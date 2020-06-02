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
        name = self.name
        dt_series = pd.Series({**{'name': self.name, 'path': self.path, 'frequency': self.frequency,
                               'row_full': self.row_full, 'category': self.category}, **self.problems,
                               **self.load_parameters})
        data = {name: self.df, name + '_columns_meta': self.meta.to_dataframe(), name + '_meta': dt_series,
                name + '_subcategories': {'table': self.subcategory.to_series()}, name + '_relations': {},
                name + '_clean': self.clean.to_dataframe()}
        for columns, subcategory in self.subcategories.items():
            data[name + '_subcategories'][columns] = subcategory.to_series()
        for num, relation in enumerate(self.relations):
            data[name + '_relations']['relation:' + str(num)] = relation.to_series()
        data[name + '_subcategories'] = pd.DataFrame(data[name + '_subcategories'])
        data[name + '_relations'] = pd.DataFrame(data[name + '_relations'])
        return data


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
dt.clean = cd



