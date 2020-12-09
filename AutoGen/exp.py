# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library - EXP module
#
# Created May, 26, 2017
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

from test import todo
from builtins import list

if __name__ == '__main__':
    pass

def createHeader (fileN, testName):
    """Create the EXP file header"""
    
    print ("EXP header opening " + testName + "...\n")
    header = "(* @NESTEDCOMMENTS := 'Yes' *)\n(* @PATH := '' *)\n(* @OBJECTFLAGS := '0, 8' *)\n(* @SYMFILEFLAGS := '2048' *)\n"
    header += "PROGRAM " + testName + "\n"
    fileN.write (header)

def createFooter (fileN):
    """Create the EXP file footer"""
    
    print ("EXP footer closure...\n")
    todo()
    fileN.write("END_PROGRAM\n")    
    
def endDeclaration (fileN):
    """End of declaration header"""
     
    print ("EXP end declaration...\n")
    todo()
    fileN.write("(* @END_DECLARATION := '0' *)\n")

def writeConstatns (fileN, constants):
    """Write test values and size constants to file"""
    
    print ("export constants to EXP...\n")
    fileN.write("VAR CONSTANT\n")
    
    for c in constants:
        text = "    " +  constants[c]['Name'] + " : " + constants[c]['Type'] + " := "
        if type(constants[c]['Value']) != list:
            text += str(constants[c]['Value']) + ";\n"
        else:
            i = 0
            for v in constants[c]['Value']:
                i+=1
                text += "\n        (* Test case" + str(i) + "*)\n"
                end = False
                for w in v:
                    if end:
                        text += ",\n"
                    text += "        " + w
                    end = True
                    
                text += ";\n"
                    
        fileN.write(text)
    fileN.write("END_VAR\n")
    
def writeVariables (fileN, variables):
    """Write test variables needed for test execution"""
    
    print ("export variables to EXP...\n")
    fileN.write("VAR\n")
    
    for c in variables:
        text = "    " +  variables[c]['Name'] + " : " + variables[c]['Type']
        
        if 'Value' in variables[c]:
            text += " := "
            if type(variables[c]['Value']) != list:
                text += str(variables[c]['Value'])
            else:
                i = 0
                for v in variables[c]['Value']:
                    i+=1
                    text += "\n        (* Test case" + str(i) + "*)"
                    end = False
                    for w in v:
                        if end:
                            text += ",\n"
                        text += "        " + w
                        end = True
                    
        text += ";\n"
                    
        fileN.write(text)
    fileN.write("END_VAR\n")
    
def createStateMachine(fileN, testName, instanceName, typeVar):
    """Create test state machine, main test execution"""
    
    print ("Create state machine for testing...\n")
    fileN.write('    testInit(' + testName + ', NoOfTests)\n\n')
    fileN.write('    CASE _tls_ OF\n')
    fileN.write('    sT_INIT :    (* Reset *)\n')
    fileN.write('                SysMemSet (ADR(' + instanceName + '), 0, SIZEOF(' + instanceName + '));\n')
    fileN.write('                testParam(pSteps, SIZEOF(Tests_Values)/NoOfTests/SIZEOF(Tests_Values[_tlt_,1]));\n')
    fileN.write('\n')
    fileN.write('    sT_RUN:    (* test run *)\n')
    fileN.write('               ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
    
    fileN.write('               ' + instanceName + '(')
    
    for v in typeVar[1]:
        fileN.write('\n                    ' + typeVar[1][v]['Name'] + ' := ptTestVars^.' + typeVar[1][v]['Name'])
        
    fileN.write('\n                    );\n')
    fileN.write('\n')
    
    for v in typeVar[2]:
        fileN.write('               assertEqualsD (    Value1 := ' + instanceName + '.' + typeVar[2][v]['Name'] +',\n')
        fileN.write('                                  Value2 := ptTestVars^.' + typeVar[2][v]['Name'] + ',\n')
        fileN.write('                                  MaxCnt := 0, Delay := ptTestVars^.testTime);\n\n')
    
    fileN.write('    sTC_PASS: Pass := TRUE;\n    END_CASE\n')
    
def createTestDUT(fileN, testName, typeVar):
    """Create test variable data type for the test parameter table"""
    
    print ("Writing data type used for the test to file..")

    fileN.write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
    fileN.write("(* @PATH := '' *)\n")
    fileN.write("(* @OBJECTFLAGS := '0, 8' *)\n")
    fileN.write("TYPE Vars" + testName + " :\n")
    fileN.write("STRUCT\n")

    fileN.write('    ' + typeVar[0]['Name'] + ' : ' + typeVar[0]['Type'] + ';\n')
    
    for v in typeVar[1]:
        fileN.write('\n    ' + typeVar[1][v]['Name'] + ' : ' + typeVar[1][v]['Type'] + ';')

    fileN.write('\n')
    for v in typeVar[2]:
        fileN.write('\n    ' + typeVar[2][v]['Name'] + ' : ' + typeVar[2][v]['Type'] + ';')

    fileN.write('\n')

    fileN.write("END_STRUCT\n")
    fileN.write("END_TYPE\n\n")
    fileN.write("(* @END_DECLARATION := '0' *)\n")
    