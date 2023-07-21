import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell
import xlrd
import os
import sys


class MOF:
    def __init__(self,name):
        self.name = name
        self.prop = []
    def line(self, sheet, column):
        for r in range(1,sheet.nrows):
            mofname = sheet.cell_value(r,column)
            if self.name.upper()== mofname.upper():
                
                return r
                break
        return -1
    def value(self, sheet, row):
        val = []
        for c in range(1,sheet.ncols):
            if row > -1:
                self.prop.append(sheet.cell_value(row,c))
            else:
                self.prop.append("not found")
    def criteri(self, row):
        if row > -1:
            self.prop.append("yes") #1 = yes
        else:
            self.prop.append("no") #0 = no

structPropBk = xlrd.open_workbook("structural.xlsx")
structPropShList = structPropBk.sheets()

criteriBk = xlrd.open_workbook("criteri.xlsx")
criteriSh = criteriBk.sheet_by_index(0)

elencoBk = xlrd.open_workbook("dosat_15_02_22.xlsx")
elencoSh = elencoBk.sheet_by_index(0)

metalBk = xlrd.open_workbook("metalli.xlsx")
metalSh = metalBk.sheet_by_index(0)

densityBk = xlrd.open_workbook("metal_density.xlsx")
densitySh = densityBk.sheet_by_index(0)

geompropBk = xlrd.open_workbook("all_mofs_reference.xlsx")
geompropSh = geompropBk.sheet_by_index(0)

HSEBk = xlrd.open_workbook("HSE results.xlsx")
HSESh = HSEBk.sheet_by_index(0)

targetBk = xlsxwriter.Workbook("DATA.xlsx")
targetSh = targetBk.add_worksheet()
            
targetSh.write(xl_rowcol_to_cell(0,0), "MOF_name")
targetSh.write(xl_rowcol_to_cell(0,1), "Dos at Fermi energy, eln/cell")
targetSh.write(xl_rowcol_to_cell(0,2), "Band_gap")
targetSh.write(xl_rowcol_to_cell(0,5), "Type")
targetSh.write(xl_rowcol_to_cell(0,3), "Dos at VBM, eln/cell")
targetSh.write(xl_rowcol_to_cell(0,4), "Dos at CBM, eln/cell")
targetSh.write(xl_rowcol_to_cell(0,6), "LCD")
targetSh.write(xl_rowcol_to_cell(0,7), "PLD, Å")
targetSh.write(xl_rowcol_to_cell(0,8), "Density (g/cm3)")
targetSh.write(xl_rowcol_to_cell(0,9), "Accessible Surface Area (m2/cm3)")
targetSh.write(xl_rowcol_to_cell(0,10), "Accessible Surface Area (m2/g)")
targetSh.write(xl_rowcol_to_cell(0,11), "Volume Fraction")
targetSh.write(xl_rowcol_to_cell(0,12), "Criteria#")
targetSh.write(xl_rowcol_to_cell(0,13), "Multiplier_Sum")
targetSh.write(xl_rowcol_to_cell(0,14), "Space_group#")
targetSh.write(xl_rowcol_to_cell(0,15), "Space_group")
targetSh.write(xl_rowcol_to_cell(0,16), "Temp")
targetSh.write(xl_rowcol_to_cell(0,17), "Zprime")
targetSh.write(xl_rowcol_to_cell(0,18), "Year")
targetSh.write(xl_rowcol_to_cell(0,19), "Metal")
targetSh.write(xl_rowcol_to_cell(0,20), "Metal 2")
targetSh.write(xl_rowcol_to_cell(0,21), "Metal 3")
targetSh.write(xl_rowcol_to_cell(0,22), "Metals number")
targetSh.write(xl_rowcol_to_cell(0,23), "Cell volume")
targetSh.write(xl_rowcol_to_cell(0,24), "Metal density")
targetSh.write(xl_rowcol_to_cell(0,25), "Crit: metal")
targetSh.write(xl_rowcol_to_cell(0,26), "Crit: redox match")
targetSh.write(xl_rowcol_to_cell(0,27), "Crit: redox active linker")
targetSh.write(xl_rowcol_to_cell(0,28), "Crit: pi-pi stacking")
targetSh.write(xl_rowcol_to_cell(0,29), "Crit: level 1")
a = 0
for i, Sh in enumerate(structPropShList):
    targetSh.write(xl_rowcol_to_cell(0,30 + i), Sh.name)
    a = a+1
targetSh.write(xl_rowcol_to_cell(0,30+a), "HSE band gap")


#cycle per each mof
for readline in range(1,elencoSh.nrows):
    print(readline)
    #get mof name and calculation results
    readmof = MOF(str(elencoSh.cell_value(readline,0)))
    print(readmof.name)
    targetSh.write(xl_rowcol_to_cell(readline,0), readmof.name)
    readmof.value(elencoSh, readline)
    #get geometric properties and number of criteria matched
    lineGeomprop = readmof.line(geompropSh,0)
    readmof.value(geompropSh, lineGeomprop)
    #get metal type
    lineMet =  readmof.line(metalSh,0)
    readmof.value(metalSh, lineMet)
    #get metal density and volume
    lineDens =  readmof.line(densitySh,0)
    readmof.value(densitySh, lineDens)
    #get what of the 4 criteria each mof matches
    criterio1 = readmof.line(criteriSh,0)
    criterio2 = readmof.line(criteriSh,1)
    criterio3 = readmof.line(criteriSh,2)
    criterio4 = readmof.line(criteriSh,3)
    criterio5 = readmof.line(criteriSh,4)
    readmof.criteri(criterio1)
    readmof.criteri(criterio2)
    readmof.criteri(criterio3)           
    readmof.criteri(criterio4)
    readmof.criteri(criterio5)
    #get structural properties
    for i, Sh in enumerate(structPropShList):
        structProp = readmof.line(Sh,0)
        readmof.criteri(structProp)
    #get HSE band gap
    lineHse =  readmof.line(HSESh,0)
    readmof.value(HSESh, lineHse)    
    
    #write all the data for this mof in the excel file
    for c in range(len(readmof.prop)):
        targetSh.write(xl_rowcol_to_cell(readline,c+1), readmof.prop[c])
targetBk.close()
          



        
    
    
        
        
