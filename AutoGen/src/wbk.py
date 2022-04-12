'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - Workbook module

Created May, 30, 2017

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

import xlrd
import os.path

class Workbook:
    
    def _readBaseParams(self):
        """Read header info and reset counters"""
        
        #Header information 
        self.testName = self._sheet.cell(0,1).value #TODO: fix Hard coded!
        self.fbName = self._sheet.cell(0,4).value
        self.instanceName = self._sheet.cell(0,6).value

        self._scanPos = 0
        
        # Find beginning of declaration tables
        while True:
            state = self._sheet.cell(self._scanPos,0).value
        
            if state != "State":
                self._scanPos += 1
            else:
                break    
    
    def __init__(self, bookfile):
        """Create new instance, open bookfile and start reading info"""

        try:
            self._workBook = xlrd.open_workbook(os.path.join('', bookfile))
        except:
            print ("Unable to open file ' + fileName + ' for write")
            raise
        
        print (self._workBook.sheet_names())
        self._sheetNo = -1
            
    def __iter__(self):
        """Implement the iterator interface"""
        return self

    def __next__(self):
        """Iterate to next _sheet"""
        self._sheetNo+=1
        if self._workBook.nsheets <= self._sheetNo:
            raise StopIteration
        self._sheet = self._workBook.sheet_by_index(self._sheetNo)
        self._readBaseParams()
        return self
    
    def getFunctionVars(self):
        """Collect the names and types of I/O vaiables in tables"""
        
        testTime = {"Name" : self._sheet.cell(self._scanPos,1).value, "Type": "DWORD"}

        # read actual line, field 2 on
        columns = self._sheet.row_values(self._scanPos, 2)
        
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
        
        self._scanPos += 1 # next line, start to scan
        return [testTime, inputs, outputs]    
    
    def _scanLine(self, columns, typeDef):
        """Read a variable line and create time and I/O value list"""
        
        inputs = []
        outputs= []
        
        # Time value
        testTime = columns[0]
        
        i = 1
        for _ in typeDef[2]:
            varValue = {"Value": columns[i], "Type": columns[i+1]}
            outputs.append(varValue.copy())
            varValue.clear()
            i+= 2
        
        i+=1 # skip the line with hash
        for _ in typeDef[1]:
            varValue = {"Value": columns[i], "Mode": columns[i+1]}
            inputs.append(varValue.copy())
            varValue.clear()
            i+= 2
            
        return [testTime, inputs, outputs]    
        
    def _readRunSequence(self, typeDef):
        """Read a test sequence in spreadsheet, group them into a value set"""
        
        sequence = []
        while (self._sheet.nrows > self._scanPos):
            if (self._sheet.cell(self._scanPos,1).value == ''):
                break
            newLine = self._scanLine(self._sheet.row_values(self._scanPos,1), typeDef)
            sequence.append(newLine)
            print ("New input found = " + str(newLine))
            self._scanPos += 1
            
        return sequence

    def readSequences(self, typeDef):
        """Read all sequences in a test configuration _sheet"""
        
        sequences = []
        
        while (self._sheet.nrows > self._scanPos):
            newSequence = self._readRunSequence(typeDef)
            if newSequence != []:
                sequences.append(newSequence)
                print ("Sequence ", len(sequences))
                
            self._scanPos+=1 # skip empty line
        
        return sequences