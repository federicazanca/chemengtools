import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import xlrd
import os
import sys

suobk=xlrd.open_workbook("list1.xlsx")
suosh=suobk.sheet_by_index(0)
miobk=xlrd.open_workbook("list2.xlsx")
miosh=miobk.sheet_by_index(0)

for row in range(1, suosh.nrows):
    mofname=suosh.cell_value(row,0)
    for r in range(1, miosh.nrows):
        name=miosh.cell_value(r,0)
        if mofname==name:
            print(name)
    
    


   





