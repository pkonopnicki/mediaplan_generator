from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View
import openpyxl
import pandas as pd

# Create your views here.


def index(request):
    if "GET" == request.method:
        return render(request, 'index.html', {})
    elif 'excel_upload' in request.POST:
        excel_file = request.FILES["excel_file"]

        excel_data = pd.read_excel(excel_file, sheetname=0)

        column_names = excel_data.columns.tolist()
        vendor_column = excel_data[column_names[0]].dropna().tolist()

        vendor_len = len(vendor_column)
        column_len = len(column_names)
        col_n = '_'.join(str(e) for e in column_names)

        columns_list = []
        for i in range(1, len(column_names)):
            columns_dictionary = {
                "column_name": excel_data.columns[i],
                "column_options": excel_data[column_names[i]].dropna().tolist()
            }
            columns_list.append(columns_dictionary)

        vendor_list = []
        for i in range(0, len(vendor_column)):
            vendor_dictionary = {
                "vendor_id": str(i),
                "vendor_name": vendor_column[i],
                "option_list": columns_list
            }
            vendor_list.append(vendor_dictionary)

        ctx = {
            'vendor_list': vendor_list,
            'vendor_len': vendor_len,
            'column_len': column_len,
            'column_names': col_n,
        }

        return render(request, 'index.html', ctx)

    elif 'go_next' in request.POST:

        vendor_count = request.POST.get("vendor count")
        column_count = request.POST.get("column count")
        column_names_concat = request.POST.get("column names")
        column_names = column_names_concat.split("_")

        vendor_list = []
        for j in range(0, int(vendor_count)):
            columns_list = []
            for i in range(1, int(column_count)):
                columns_dictionary = {
                    "column_name": column_names[i],
                    "column_options": request.POST.getlist("{} {}".format(column_names[i], str(j)))
                }
                columns_list.append(columns_dictionary)

            vendor_dictionary = {
                "vendor_name": request.POST.get("vendor {}".format(str(j))),
                "option_list": columns_list
            }
            vendor_list.append(vendor_dictionary)

        print(vendor_list)

        return HttpResponseRedirect('/')