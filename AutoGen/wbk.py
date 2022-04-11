# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library - Workbook module
#
# Created May, 30, 2017
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

import xlrd
import os.path

class Workbook:
    
    def __readBaseParams(self):
        """Read header info and reset counters"""
        
        #Header information
        self.testName = self.sh.cell(0,1).value
        self.fbName = self.sh.cell(0,4).value
        self.instanceName = self.sh.cell(0,6).value

        self.scanPos = 0
        
        # Find beginning of declaration tables
        while True:
            state = self.sh.cell(self.scanPos,0).value
        
            if state != "State":
                self.scanPos += 1
            else:
                break    
    
    def __init__(self, bookfile):
        """Create new instance, open bookfile and start reading info"""

        try:
            self.wb = xlrd.open_workbook(os.path.join('', bookfile))
        except:
            print ("Unable to open file ' + fileName + ' for write")
            raise
        
        print (self.wb.sheet_names())
        self.sheetno = -1
            
    def __iter__(self):
        """Implement the iterator interface"""
        return self

    def __next__(self):
        """Iterate to next sheet"""
        self.sheetno+=1
        if self.wb.nsheets <= self.sheetno:
            raise StopIteration
        self.sh = self.wb.sheet_by_index(self.sheetno)
        self.__readBaseParams()
        return self
    
    def getFunctionVars(self):
        """Collect the names and types of I/O vaiables in tables"""
        
        # read actual line, column 2 on
        columns = self.sh.row_values(self.scanPos, 2)
        
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
            var = {"Value": columns[i], "Type": columns[i+1]}
            inputs [cnt]= var.copy()
            var.clear()
            i+= 2
            cnt+=1
            
        return [testTime, inputs, outputs]    
        
    def readSequence(self, typeDef):
        """Read a test sequence in spreadsheet, group them into a value set"""
        
        sequence = {}
        cnt = 0
        while (self.sh.nrows > self.scanPos):
            if (self.sh.cell(self.scanPos,1).value == ''):
                break
            sequence[cnt] = self.scanLine(self.sh.row_values(self.scanPos,1), typeDef)
            print ("New input found = " + str(sequence[cnt]))
            self.scanPos += 1
            cnt += 1
            
        return sequence

    def readSequences(self, typeDef):
        """Read all sequences in a test configuration sheet"""
        
        cnt = 0
        steps = {}
        
        while (self.sh.nrows > self.scanPos):
            print ("Sequence ", cnt)
            steps[cnt] = self.readSequence(typeDef)
            if steps[cnt] == {}:
                del steps[cnt]
            else:
                cnt+=1
            self.scanPos+=1 # skip empty line
        
        return steps