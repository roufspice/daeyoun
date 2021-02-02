import os

import tablib

def create_tablib_to_xlsx():
    pass
    databook = tablib.Databook()

    for i in range(1,10):
        dataset = tablib.Dataset(title=f'{str(i)}_sheet_name',
                                 headers=['IDX','NAME','ADDRESS'])
        dataset.append([
            100,
            'test_name',
            'test_address'
        ])

        databook.add_sheet(dataset)

    directory = os.path.join(os.getcwd())
    with open(os.path.join(directory, f'test_sample.xlsx'), 'wb') as f:
        f.write(databook.export(format='xlsx'))



if __name__ == '__main__':
    create_tablib_to_xlsx()

