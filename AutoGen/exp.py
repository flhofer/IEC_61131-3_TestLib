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
from textwrap import indent

if __name__ == '__main__':
    pass

class ExportWriter:
    """Common test export-import writer class"""
    
    def __init__(self, fileName, testName, extension='.txt'):
        """Initialize instance and open output file"""
        try:
            self.testFile = open(fileName + extension, "w")
        except:
            print ("Unable to open file ' + fileName + ' for write")
            raise FileNotFoundError

        self.testName = testName
        self.indent = 0;

    def _write(self, text, indent=-1):
        """Write contents to file with indentation"""
        
        if -1 == indent:    # no parameter, write with instance indent 
            indent = self.indent
        
        for i in range(0, indent, 1):
            self.testFile.write("    ")
            
        self.testFile.write(text)
        
    def close(self):
        """Close test file"""
        self.testFile.close()
                    
class ExpWriter(ExportWriter):
    
    def __init__(self, fileName, testName, extension='.exp'):
        super().__init__(fileName, testName, extension)
    
    def createHeader(self):
        """Create the EXP POU file header"""
        
        print ("EXP header opening " + self.testName + "...\n")
        header = "(* @NESTEDCOMMENTS := 'Yes' *)\n(* @PATH := '' *)\n(* @OBJECTFLAGS := '0, 8' *)\n(* @SYMFILEFLAGS := '2048' *)\n"
        header += "PROGRAM " + self.testName + "\n"
        self._write(header)
    
    def createFooter(self):
        """Create the EXP file footer"""
        
        print ("EXP POU footer closure...\n")
        self._write("END_PROGRAM\n")    
        
    def endDeclaration(self):
        """End of declaration header"""
         
        print ("EXP end declaration...\n")
        self._write("(* @END_DECLARATION := '0' *)\n")
    
    def writeConstatns(self, constants):
        """Write test values and size constants to file"""
        
        print ("export constants to EXP...\n")
        self._write("VAR CONSTANT\n")
        
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
                        
            self._write(text)
        self._write("END_VAR\n")
        
    def writeVariables(self, variables):
        """Write test variables needed for test execution"""
        
        print ("export variables to EXP...\n")
        self._write("VAR\n")
        
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
                        
            self._write(text)
        self._write("END_VAR\n")
        
    def createStateMachine(self, instanceName, typeVar):
        """Create test state machine, main test execution"""
        
        print ("Create state machine for testing...\n")
        self.indent = 1;
        self._write('testInit(' + self.testName + ', NoOfTests)\n\n')
        self._write('CASE _tls_ OF\n')
        self._write('sT_INIT:    (* Reset *)\n')
        self.indent = 4;
        self._write('SysMemSet (ADR(' + instanceName + '), 0, SIZEOF(' + instanceName + '));\n')
        self._write('testParam(pSteps, SIZEOF(TestVars)/NoOfTests/SIZEOF(Tests_Values[_tlt_,1]));\n')
        self._write('\n', indent=0)
        self._write('sT_RUN:    (* test run *)\n', indent=1)
        self._write('ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
        
        self._write(instanceName + '(\n')
        
        for v in typeVar[1]:
            self._write(typeVar[1][v]['Name'] + ' := ptTestVars^.' + typeVar[1][v]['Name'] + '\n', indent=5)
            
        self._write(');\n', indent=5)
        self._write('\n', indent=0)
        
        for v in typeVar[2]:
            self._write('assertEqualsD (    Value1 := ' + instanceName + '.' + typeVar[2][v]['Name'] +',\n')
            self._write('Value2 := ptTestVars^.' + typeVar[2][v]['Name'] + ',\n', indent=9)
            self._write('MaxCnt := 0, Delay := ptTestVars^.testTime);\n\n', indent=9)
        
        self._write('sTC_PASS: Pass := TRUE;\n    END_CASE\n', indent=1)
        self.indent=0
        
    def createTestDUT(self, typeVar):
        """Create test variable data type for the test parameter table"""
        
        print ("Writing data type used for the test to file..")
    
        self._write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self._write("(* @PATH := '' *)\n")
        self._write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self._write("TYPE Vars" + self.testName + " :\n")
        self._write("STRUCT\n")
        
        self.indent=1
        
        self._write(typeVar[0]['Name'] + ' : ' + typeVar[0]['Type'] + ';\n')
        self._write('(* Inputs *)\n')
        for v in typeVar[1]:
            self._write(typeVar[1][v]['Name'] + ' : ' + typeVar[1][v]['Type'] + ';\n')
    
        self._write('(* Expected outputs *)\n')
        for v in typeVar[2]:
            self._write(typeVar[2][v]['Name'] + ' : ' + typeVar[2][v]['Type'] + ';\n')
    
        self.indent=0
        self._write("END_STRUCT\n")
        self._write("END_TYPE\n\n")
        self._write("(* @END_DECLARATION := '0' *)\n")
            
class XmlWriter(ExportWriter):
    """XML style export writer"""
    #TODO: implement XML writing 
    pass
