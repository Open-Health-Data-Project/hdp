from enum import Enum


class Frequency(Enum):
    monthly = 'mo'
    weekly = 'w'
    daily = 'd'
    minute = 'min'
    second = 's'
    millisecond = 'ms'
    custom = 'cs'


class Metadata:
    category = None  # General type of data for example Health, Food, Activity, Environment, Sleep etc. as string
    frequency = Frequency.custom  # Time period between rows
    row_full = 1.0  # If every unit of time available in the data as percent of values
    column_full = {}  # How much data is not NaN in every column
    index = 'Unknown'  # Index column name
    units = {}  # Units of data in columns
    dtype = {}  # Data types of data in columns
    data_min = {}  # Minimum acceptable value in each column if necessary
    data_max = {}  # Maximum acceptable value in each column if necessary


# Examples of values for the attributes above:
category = 'Activity'

frequency = Frequency.daily
row_full = 0.9
column_full = {"A": 0.5, "B": 0.9, "C": 0.8, "D": 1.0}
index = "A"
units = {"A": None, "B": "m", "C": "m/s", "D": "kg"}
dtype = {"A": "str", "B": "int", "C": "float", "D": "int"}
data_min = {"A": None, "B": 0, "C": 0, "D": 100}
data_max = {"A": None, "B": 100, "C": 50, "D": 200}

