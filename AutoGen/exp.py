# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library - EXP module
#
# Created May, 26, 2017
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

from builtins import list

if __name__ == '__main__':
    pass

class expWriter:
    
    def __init__ (self, fileName, testName):
        """Initialize EXP writer object"""
        try:
            self.testFile = open(fileName + ".txt", "a")
        except:
            print ("Unable to open file ' + fileName + ' for write")
            raise
        
        self.testName = testName

    def createHeader(self):
        """Create the EXP POU file header"""
        
        print ("EXP header opening " + self.testName + "...\n")
        header = "(* @NESTEDCOMMENTS := 'Yes' *)\n(* @PATH := '' *)\n(* @OBJECTFLAGS := '0, 8' *)\n(* @SYMFILEFLAGS := '2048' *)\n"
        header += "PROGRAM " + self.testName + "\n"
        self.testFile.write (header)
    
    def createFooter(self):
        """Create the EXP file footer"""
        
        print ("EXP POU footer closure...\n")
        # TODO: 
        self.testFile.write("END_PROGRAM\n")    
        
    def endDeclaration(self):
        """End of declaration header"""
         
        print ("EXP end declaration...\n")
        # TODO: 
        self.testFile.write("(* @END_DECLARATION := '0' *)\n")
    
    def writeConstatns(self, constants):
        """Write test values and size constants to file"""
        
        print ("export constants to EXP...\n")
        self.testFile.write("VAR CONSTANT\n")
        
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
                        
            self.testFile.write(text)
        self.testFile.write("END_VAR\n")
        
    def writeVariables(self, variables):
        """Write test variables needed for test execution"""
        
        print ("export variables to EXP...\n")
        self.testFile.write("VAR\n")
        
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
                        
            self.testFile.write(text)
        self.testFile.write("END_VAR\n")
        
    def createStateMachine(self, instanceName, typeVar):
        """Create test state machine, main test execution"""
        
        print ("Create state machine for testing...\n")
        self.testFile.write('    testInit(' + self.testName + ', NoOfTests)\n\n')
        self.testFile.write('    CASE _tls_ OF\n')
        self.testFile.write('    sT_INIT :    (* Reset *)\n')
        self.testFile.write('                SysMemSet (ADR(' + instanceName + '), 0, SIZEOF(' + instanceName + '));\n')
        self.testFile.write('                testParam(pSteps, SIZEOF(Tests_Values)/NoOfTests/SIZEOF(Tests_Values[_tlt_,1]));\n')
        self.testFile.write('\n')
        self.testFile.write('    sT_RUN:    (* test run *)\n')
        self.testFile.write('               ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
        
        self.testFile.write('               ' + instanceName + '(')
        
        for v in typeVar[1]:
            self.testFile.write('\n                    ' + typeVar[1][v]['Name'] + ' := ptTestVars^.' + typeVar[1][v]['Name'])
            
        self.testFile.write('\n                    );\n')
        self.testFile.write('\n')
        
        for v in typeVar[2]:
            self.testFile.write('               assertEqualsD (    Value1 := ' + instanceName + '.' + typeVar[2][v]['Name'] +',\n')
            self.testFile.write('                                  Value2 := ptTestVars^.' + typeVar[2][v]['Name'] + ',\n')
            self.testFile.write('                                  MaxCnt := 0, Delay := ptTestVars^.testTime);\n\n')
        
        self.testFile.write('    sTC_PASS: Pass := TRUE;\n    END_CASE\n')
        
    def createTestDUT(self, typeVar):
        """Create test variable data type for the test parameter table"""
        
        print ("Writing data type used for the test to file..")
    
        self.testFile.write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self.testFile.write("(* @PATH := '' *)\n")
        self.testFile.write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self.testFile.write("TYPE Vars" + self.testName + " :\n")
        self.testFile.write("STRUCT\n")
    
        self.testFile.write('    ' + typeVar[0]['Name'] + ' : ' + typeVar[0]['Type'] + ';\n')
        
        for v in typeVar[1]:
            self.testFile.write('\n    ' + typeVar[1][v]['Name'] + ' : ' + typeVar[1][v]['Type'] + ';')
    
        self.testFile.write('\n')
        for v in typeVar[2]:
            self.testFile.write('\n    ' + typeVar[2][v]['Name'] + ' : ' + typeVar[2][v]['Type'] + ';')
    
        self.testFile.write('\n')
    
        self.testFile.write("END_STRUCT\n")
        self.testFile.write("END_TYPE\n\n")
        self.testFile.write("(* @END_DECLARATION := '0' *)\n")
        
    def close(self):
        """Close test file"""
        self.testFile.close()
    