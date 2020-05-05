import pandas as pd
from enum import Enum


class Relation:
    pass


class Frequency(Enum):
    monthly = 'mo'
    weekly = 'w'
    daily = 'd'
    minute = 'min'
    second = 's'
    millisecond = 'ms'
    custom = 'cs'


class DataTable:
    dt = pd.DataFrame()
    relations = []
    units = {}
    frequency = Frequency.custom
    category = None
    row_full = True
    column_full = True




