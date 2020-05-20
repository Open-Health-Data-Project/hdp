class Subcategory:
    table = True
    columns = []  # Subcategory is many-to-one relation, so many columns from DataTable object can be assigned to
    # one subcategory. In some cases it could be also many-to-many relation, because one column can have multiple
    # categories


class PhysicalActivity(Subcategory):
    environment = 'Unknown'  # Possible: outdoor, indoor
    category = 'Unknown'  # Possible: weight_training, stretching, dynamic_inplace, dynamic_transportation, static
    kind = 'Unknown'  # Examples: walking, running, cycling, hiking, swimming, skiing, kayaking etc.
    min_speed = 0
    max_speed = 0
    gps_data = False
    bpm_data = False
    wind_data = False
    altitude_data = False


class Nutrients(Subcategory):
    pass


class Sleep(Subcategory):
    pass


class Appearance(Subcategory):
    pass


class PhysicalData(Subcategory):
    pass


class EnvironmentData(Subcategory):
    pass


class MedicalData(Subcategory):
    pass


class EntertainmentData(Subcategory):
    pass
