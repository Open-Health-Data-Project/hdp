import pandas as pd


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
    hr_data = False
    wind_data = False
    altitude_data = False

    def to_series(self):
        data = {'enviroment': self.environment, 'category': self.category, 'kind': self.kind,
                'min_speed': self.min_speed, 'max_speed': self.max_speed, 'gps_data': self.gps_data,
                'hr_data': self.hr_data, 'wind_data': self.wind_data, 'altitude_data': self.altitude_data}
        return pd.Series(data)


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

