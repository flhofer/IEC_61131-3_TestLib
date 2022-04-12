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
    
    def _readBaseParams(self):
        """Read header info and reset counters"""
        
        #Header information 
        self.testName = self.sheet.cell(0,1).value #TODO: fix Hard coded!
        self.fbName = self.sheet.cell(0,4).value
        self.instanceName = self.sheet.cell(0,6).value

        self.scanPos = 0
        
        # Find beginning of declaration tables
        while True:
            state = self.sheet.cell(self.scanPos,0).value
        
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
        self.sheet = self.wb.sheet_by_index(self.sheetno)
        self._readBaseParams()
        return self
    
    def getFunctionVars(self):
        """Collect the names and types of I/O vaiables in tables"""
        
        testTime = {"Name" : self.sheet.cell(self.scanPos,1).value, "Type": "DWORD"}

        # read actual line, field 2 on
        columns = self.sheet.row_values(self.scanPos, 2)
        
        inputs = []
        outputs= []
        outToIn = False
        coliterator = iter(columns)
        for field in coliterator:
            if field != None :
                if not field == "#":
                    newVar = {"Name" : field}
                    try: 
                        field = next(coliterator)
                    except:
                        print ("end of line!!")
                        
                    if field != None:
                        newVar["Type"] = field
                    
                    if not outToIn :
                        outputs.append(newVar.copy())
                    else:
                        inputs.append(newVar.copy())
                    newVar.clear()
                else:
                    if outToIn:
                        break
                    outToIn = True
        
        self.scanPos += 1 # next line, start to scan
        return [testTime, inputs, outputs]    
    
    def _scanLine(self, columns, typeDef):
        """Read a variable line and create time and I/O value list"""
        
        inputs = []
        outputs= []
        
        # Time value
        testTime = columns[0]
        
        i = 1
        for _ in typeDef[2]:
            var = {"Value": columns[i], "Type": columns[i+1]}
            outputs.append(var.copy())
            var.clear()
            i+= 2
        
        i+=1 # skip the line with hash
        for _ in typeDef[1]:
            var = {"Value": columns[i], "Type": columns[i+1]}
            inputs.append(var.copy())
            var.clear()
            i+= 2
            
        return [testTime, inputs, outputs]    
        
    def _readSequence(self, typeDef):
        """Read a test sequence in spreadsheet, group them into a value set"""
        
        sequence = []
        while (self.sheet.nrows > self.scanPos):
            if (self.sheet.cell(self.scanPos,1).value == ''):
                break
            newLine = self._scanLine(self.sheet.row_values(self.scanPos,1), typeDef)
            sequence.append(newLine)
            print ("New input found = " + str(newLine))
            self.scanPos += 1
            
        return sequence

    def readSequences(self, typeDef):
        """Read all sequences in a test configuration sheet"""
        
        sequences = []
        
        while (self.sheet.nrows > self.scanPos):
            newSequence = self._readSequence(typeDef)
            if newSequence != []:
                sequences.append(newSequence)
                print ("Sequence ", len(sequences))
                
            self.scanPos+=1 # skip empty line
        
        return sequences