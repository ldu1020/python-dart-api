import pandas as pd
import re

data2 = pd.read_excel('./삼성전자/2020년03월삼성전자.xlsx',sheet_name="손익계산서")
sheets = pd.ExcelFile('./삼성전자/2020년03월삼성전자.xlsx')

def re_name_column_period(data):
    for idx,column in enumerate(data.columns):
        period_header_bool = data[column].astype(str).str.contains('제\s?\d*\s?기')
        period_name_df = data[column][period_header_bool]
        period_name_arr = list(period_name_df.to_dict().values())
        if period_name_arr.__len__() > 0:
            data.rename(columns={column:period_name_arr[0]}, inplace = True)
    return data

def re_name_column_account_name(data):
    for idx,column in enumerate(data.columns):
        is_name_bool = data[column].astype(str).str.contains('\w*?자산\w*?|\w*?매출\w*?|\w*?부채\w*?')
        is_name_bool_arr = is_name_bool.to_list()
        is_name_column = True in is_name_bool_arr
        if is_name_column:
            data.rename(columns={column:'계정명'},inplace=True)
    return data

def remove_un_necessary_indexes(data):
    un_necessary_indexes = []
    max_value_in_un_necessary = 0
    for idx,column in enumerate(data.columns):
        period_header_bool = data[column].astype(str).str.contains('제\s?\d*\s?기')
        not_using_rows_indexes = data[column][period_header_bool].index
        if not_using_rows_indexes.__len__() > 0:
            for index in not_using_rows_indexes: 
                un_necessary_indexes.append(index)
                
    if un_necessary_indexes.__len__() > 0:
        for value in un_necessary_indexes:
            if value > max_value_in_un_necessary : max_value_in_un_necessary = value
    
    return data[max_value_in_un_necessary+1:]


def remove_un_necessary_columns(data):
    for column in data.columns:
        if re.match('Unnamed:\s?\w*?|계정명',column):
            data.drop([column], axis=1,inplace=True)
    return data

data2 = re_name_column_period(data2)
data2 = re_name_column_account_name(data2)
data2 = remove_un_necessary_indexes(data2)
data2 = data2.set_index(data2['계정명'])
data2 = remove_un_necessary_columns(data2)


# print(data2)

