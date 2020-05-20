import pandas as pd
from hdp.struct.metadata import Metadata
from hdp.struct.categories import *


class Relation:  # Relation many-to-many
    dt_to = None  # Target table name - string
    col_from = []  # Names of columns from this DataTable - string list
    col_to = []  # Names of columns from target DataTable - string list


class DataTable:
    name = None
    dt = pd.DataFrame()
    meta = Metadata()
    subcategory = None  # One subcategory for the whole table, if it's common for every column
    subcategories = {}  # Subcategories for subset of rows if necessary
    relations = []


# Examples:
subcategory = PhysicalActivity()
subcategories = {["A", "B", "C"]: PhysicalActivity(), ["D"]: Sleep()}
