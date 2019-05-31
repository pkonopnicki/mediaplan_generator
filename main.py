import itertools
import pandas as pd

input_file = 'input.xlsx'
output_file = 'output.xlsx'

df = pd.read_excel(input_file)

first_col = df.columns[0]
first_col_unique = df[first_col].unique()

output_df = pd.DataFrame()

for val in first_col_unique:
    df1 = df.loc[df[first_col] == val]

    value_list = [df1[x].dropna().unique() for x in df1.columns]

    data = [e for e in itertools.product(*value_list)]

    df1 = pd.DataFrame(data, columns=df1.columns)
    output_df = output_df.append(df1, ignore_index=True)

#Insert additional empty column if needed
#output_df.insert(1, 'PKPartnerName', '')
output_df.to_excel(output_file, index=False)
