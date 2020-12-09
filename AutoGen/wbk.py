'''
Created on May 30, 2017

@author: florian
'''
import test

def getFunctionVars(columns):
    inputs = {}
    outputs= {}
    number = 1
    outtoin = False
    coliter = iter(columns)
    for col in coliter:
        if col != None :
            if not col == "#":
                var = {"Name" : col}
                try: 
                    col = coliter.next()
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
                number = 1
    
    testTime = {"Name" : "testtime", "Type": "DWORD"}
    return [testTime, inputs, outputs]    

def scanLine(columns, typeDef):
    inputs = {}
    outputs= {}
    number = 1

    testTime = columns[0]
    
    i = 1
    cnt = 1
    for type in typeDef[2]:
        var = {"Value": columns[i], "Type": columns[i+1]}
        outputs [cnt]= var.copy()
        var.clear()
        i+= 2
        cnt+=1
    
    i+=1 # skip the line with hash
    cnt = 1
    for type in typeDef[1]:
        var = {"Value": columns[i]}
        inputs [cnt]= var.copy()
        var.clear()
        i+= 2
        cnt+=1
        
    return [testTime, inputs, outputs]    
    
def readSequence(sh, scanPos, typeDef):
    while sh.nrows> scanPos :    
        sequence = {}
        scanPos += 1
        cnt = 1
        print (sh.nrows)
        while (sh.nrows > scanPos):
            if (sh.cell(scanPos,1).value == ''):
                break
            sequence[cnt] = scanLine(sh.row_values(scanPos,1), typeDef)
            print ("New input found = " + str(sequence[cnt]))
            scanPos += 1
            cnt += 1
        
    return sequence
