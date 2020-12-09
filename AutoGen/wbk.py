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

def getFunctionVars(columns):
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
    return [testTime, inputs, outputs]    

def scanLine(columns, typeDef):
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
    
def readSequence(sh, scanPos, typeDef):
    """Read a test sequence in spreadsheet, group them into a value set"""
    
    while sh.nrows> scanPos :    
        sequence = {}
        scanPos += 1
        cnt = 0
        print (sh.nrows)
        while (sh.nrows > scanPos):
            if (sh.cell(scanPos,1).value == ''):
                break
            sequence[cnt] = scanLine(sh.row_values(scanPos,1), typeDef)
            print ("New input found = " + str(sequence[cnt]))
            scanPos += 1
            cnt += 1
        
    return sequence
