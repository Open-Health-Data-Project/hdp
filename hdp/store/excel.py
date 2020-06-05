# Team 5
import pandas as pd
from hdp.struct.profile import Profile


def profile_file(name):
    with open('profile.txt', 'w') as profile:
        profile.write('Profile: ' + name + '\n')
        profile.write('Directory: ' + '\n')
        profile.write('Files: ' + '\n')


def save_to_excel(datatable, directory=None):
    for key, file in datatable.items():
        if key is 'load_errors':
            error = pd.Series(file, dtype='str')
            error.to_excel(key + '.xlsx')
        else:
            for i in file:
                if isinstance(file[i], pd.DataFrame) or isinstance(file[i], pd.Series):
                    file[i].to_excel(i + '.xlsx')
                    with open('profile.txt', 'a') as profile:
                        profile.write(i + '.xlsx\n')


def open_excel(file, directory=None):
    df = pd.read_excel(file)
    print(df)


pr = Profile()
print('*' * 40)
profile_file(pr.name)
save_to_excel(pr.get_data())
