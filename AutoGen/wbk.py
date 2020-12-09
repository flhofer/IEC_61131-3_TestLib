# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library - Workbook module
#
# Created May, 30, 2017
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

import test

import xlrd
import os.path

class workbook:
    
    def __init__(self, bookfile):
        
        self.wb = xlrd.open_workbook(os.path.join('',bookfile))
        self.wb.sheet_names()
        self.sh = self.wb.sheet_by_index(0)

        #Header information
        testName = self.sh.cell(0,1).value
        fbName = self.sh.cell(0,4).value
        instanceName = self.sh.cell(0,6).value

        scanPos = 0
        
        # Find beginning of declaration tables
        while True:
            state = self.sh.cell(scanPos,0).value
        
            if state != "State":
                scanPos += 1
            else:
                break
    
    def getFunctionVars(self, columns):
        """Collect the names and types of I/O vaiables in tables"""
        
        inputs = {}
        outputs= {}
        number = 0
        outtoin = False
        coliter = iter(columns)
        for col in coliter:
            if col != None :
                if not col == "#":
                    var = {"Name" : col}
                    try: 
                        col = next(coliter)
                    except:
                        print ("end of line!!")
                        
                    if col != None:
                        var["Type"] = col
                    
                    if not outtoin :
                        outputs[number] = var.copy()
                    else:
                        inputs[number] = var.copy()
                    number += 1
                    var.clear()
                else:
                    if outtoin:
                        break
                    outtoin = True
                    number = 0
        
        testTime = {"Name" : "testtime", "Type": "DWORD"}
        self.scanPos += 1 # next line, start to scan
        return [testTime, inputs, outputs]    
    
    def scanLine(self, columns, typeDef):
        """Read a variable line and create time and I/O value list"""
        
        inputs = {}
        outputs= {}
        
        # Time value
        testTime = columns[0]
        
        i = 1
        cnt = 0
        for ntype in typeDef[2]:
            var = {"Value": columns[i], "Type": columns[i+1]}
            outputs [cnt]= var.copy()
            var.clear()
            i+= 2
            cnt+=1
        
        i+=1 # skip the line with hash
        cnt = 0
        for ntype in typeDef[1]:
            var = {"Value": columns[i]}
            inputs [cnt]= var.copy()
            var.clear()
            i+= 2
            cnt+=1
            
        return [testTime, inputs, outputs]    
        
    def readSequence(self, typeDef):
        """Read a test sequence in spreadsheet, group them into a value set"""
        
        while self.sh.nrows> self.scanPos :    
            sequence = {}
            self.scanPos += 1
            cnt = 0
            print (self.sh.nrows)
            while (self.sh.nrows > self.scanPos):
                if (self.sh.cell(self.scanPos,1).value == ''):
                    break
                sequence[cnt] = self.scanLine(self.sh.row_values(self.scanPos,1), typeDef)
                print ("New input found = " + str(sequence[cnt]))
                self.scanPos += 1
                cnt += 1
            
        return sequence
