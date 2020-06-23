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

    def add_data(self, datatables, load_params, extension, load_errors):
        cleandata_list = []
        for datatable in datatables:
            datatable.load_parameters = load_params
            cleandata_list.append(datatable.clean)
        self.datatables.extend(datatables)
        self.cleandata.extend(cleandata_list)
        if extension not in self.extensions:
            self.extensions.append(extension)
        self.load_errors.update(load_errors)

    def add_all_data(self, datatable, cleandata, extension, image=None, load_errors=None):
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
        data = {'name': self.name}
        for extension, dt in zip(self.extensions, self.datatables):
            if extension not in ('tcx', 'gpx', 'jpg'):
                data[dt.name] = dt.to_pandas()
            else:
                data['native_format'] = {}
                data['native_format'][dt.name + '.' + extension] = dt.to_pandas()
        data['images'] = self.images
        data['load_errors'] = pd.Series(self.load_errors).to_frame()
        return data


# Examples of usage
pr = Profile()
pr.add_all_data(dt, cd, 'csv', load_errors={r"C://example/example.file": "File not found"})
pr.name = "user1"
print(pr.get_data())
