import openpyxl
import pandas as pd

dictionary = [{
        'vendor': 'vendor1',
        'option_list': [{
            'col1_name': 'Column1',
            'col1_options': ['option1', 'option2', 'option3']
            }, {
            'col2_name': 'Column2',
            'col2_options': ['small']
            },  {
            'col3_name': 'Column3',
            'col3_options': ['yellow', 'black', 'green']
            }
        ]
    },  {
        'vendor': 'vendor2',
        'option_list': [{
            'col1_name': 'Column1',
            'col1_options': ['option3']
            }, {
            'col2_name': 'Column2',
            'col2_options': ['small', 'medium', 'large']
            }, {
            'col3_name': 'Column3',
            'col3_options': ['yellow', 'green']
            }
        ]
    }]

df = pd.DataFrame.from_dict(for vendor in dictionary:)
print(df)