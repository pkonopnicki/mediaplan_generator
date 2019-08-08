import itertools
import pandas as pd

input_file = 'input.xlsx'
output_file = 'output.xlsx'

df = pd.read_excel(input_file)
output_df = pd.DataFrame()

# Creating combinations of the input variables


def give_all_combinations():
    first_col = df.columns[0]
    first_col_unique = df[first_col].unique()
    global output_df
    for val in first_col_unique:
        df1 = df.loc[df[first_col] == val]

        value_list = [df1[x].dropna().unique() for x in df1.columns]

        data = [e for e in itertools.product(*value_list)]

        df1 = pd.DataFrame(data, columns=df1.columns)
        output_df = output_df.append(df1, ignore_index=True)

# Adding starting and ending date from the dictionary


def add_date():
    input_file_dates_dictionary = 'dictionary/dates.xlsx'
    df_dates_dictionary = pd.read_excel(input_file_dates_dictionary)
    try:
        start_date = df_dates_dictionary["Start Date"][0]
        output_df["Start Date"] = start_date.date()
    except:
        output_df["Start Date"] = None
    try:
        end_date = df_dates_dictionary["End Date"][0]
        output_df["End Date"] = end_date.date()
    except:
        output_df["End Date"] = None

# Adding buy model based on a dictionary


def add_buymodel():
    global output_df
    input_file_buymodel_dictionary = 'dictionary/buymodel.xlsx'
    df_buymodel_dictionary = pd.read_excel(input_file_buymodel_dictionary)
    output_df['Vendor_left'] = output_df['Vendor']
    output_df['Vendor_left'] = output_df['Vendor_left'].str.lower()
    output_df['Vendor_left'] = output_df['Vendor_left'].str.replace(' ', '')
    df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor']
    df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor_right'].str.lower()
    df_buymodel_dictionary['Vendor_right'] = df_buymodel_dictionary['Vendor_right'].str.replace(' ', '')
    output_df = pd.merge(output_df, df_buymodel_dictionary, left_on='Vendor_left',
                         right_on='Vendor_right', suffixes=('', '_right_join'), how='left')
    output_df = output_df.drop(columns=['Vendor_left', 'Vendor_right_join', 'Vendor_right'])


# Adding budget with multiple granularity option


def add_budget():
    global output_df
    input_file_budget_dictionary = 'dictionary/budget.xlsx'
    df_budget_dictionary = pd.read_excel(input_file_budget_dictionary)

    list_basic = ['Vendor', 'Country']
    list_left = ['Vendor_left', 'Country_left']
    list_right = ['Vendor_right', 'Country_right']
    list_join_right = [el + "_join" for el in list_right]
    list_join = list_left + list_right + list_join_right

    output_df[list_left] = output_df[list_basic]
    df_budget_dictionary[list_right] = df_budget_dictionary[list_basic]
    output_df = pd.merge(output_df, df_budget_dictionary, left_on=list_left,
                         right_on=list_right, suffixes=('', '_right_join'), how='left')
    output_df = output_df.drop(columns=list_join)
    output_df.loc[output_df.duplicated(subset=list_basic), "Budget"] = 0


# use all methods and save output


give_all_combinations()
add_date()
add_buymodel()
add_budget()


output_df.to_excel(output_file, index=False)

