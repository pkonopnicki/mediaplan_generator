import itertools
import pandas as pd

input_file = 'input.xlsx'
output_file = 'output.xlsx'

df = pd.read_excel(input_file)

#Creating combinations of the input variables
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
#output_df.insert(1,'PKPartnerName', '')

#Adding buy model based on a dictionary

input_file_buymodel_dictionary = 'dictionary/buymodel.xlsx'
df_buymodel_dictionary = pd.read_excel(input_file_buymodel_dictionary)

output_df['Vendor_left'] = output_df['Vendor']
output_df['Vendor_left'] = output_df['Vendor_left'].str.lower()
output_df['Vendor_left'] = output_df['Vendor_left'].str.replace(' ','')

df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor']
df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor_right'].str.lower()
df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor_right'].str.replace(' ','')

merge_df = pd.merge(output_df,df_buymodel_dictionary, left_on='Vendor_left', right_on='Vendor_right', suffixes=('','_right_join'), how='left')
merge_df = merge_df.drop(columns = ['Vendor_left','Vendor_right_join','Vendor_right'])

merge_df.to_excel(output_file, index=False)