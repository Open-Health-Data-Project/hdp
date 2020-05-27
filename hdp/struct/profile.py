from hdp.struct.datatable import *
from hdp.struct.cleandata import *


class Profile:
    name = ""
    extensions = []
    datatables = []
    cleandata = []
    images = []
    load_errors = {}

    def __init__(self, name=""):
        self.name = name

    def add_data(self, datatable, cleandata, extension, image=None, load_errors=None):
        if isinstance(datatable, DataTable) and isinstance(cleandata, CleanData) and isinstance(extension, str):
            self.extensions.append(extension)
            self.datatables.append(datatable)
            self.cleandata.append(cleandata)
        elif isinstance(datatable, list) and isinstance(cleandata, list) and isinstance(extension, list) and \
                len(datatable) == len(cleandata) and len(cleandata) == len(extension):
            self.extensions.extend(extension)
            self.datatables.extend(datatable)
            self.cleandata.extend(cleandata)
        if image is not None:
            if isinstance(image, list):
                self.images.extend(image)
            else:
                self.images.append(image)
        if load_errors is not None:
            self.load_errors = {**self.load_errors, **load_errors}

    def get_data(self):
        data = {}
        for extension, dt, cd in zip(self.extensions, self.datatables, self.cleandata):
            if extension not in data.keys():
                data[extension] = [[dt.to_pandas()] + [cd.to_dataframe()]]
            else:
                data[extension].append(dt.to_pandas() + [cd.to_dataframe()])
        data['images'] = self.images
        data['load_errors'] = self.load_errors
        return data


# Examples of usage
pr = Profile()
pr.add_data(dts, cds, ['csv', 'csv'], load_errors={r"C://example/example.file": "File not found"})
print(pr.get_data())
