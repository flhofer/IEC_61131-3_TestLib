'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - EXP module

Created May, 26, 2017

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

from builtins import list
from settings import TEST_NAME_MAX

if __name__ == '__main__':
    pass

class ExportWriter:
    """Common test export-import writer class"""
    
    def __init__(self, fileName, extension='.txt'):
        """Initialize instance and open output file"""
        try:
            self.testFile = open(fileName + extension, "w")
        except:
            print ("Unable to open file ' + fileName + ' for write")
            raise FileNotFoundError

        self._indent = 0;

    def _write(self, text, indent=-1):
        """Write contents to file with indentation"""
        
        if -1 == indent:    # no parameter, write with instance _indent 
            indent = self._indent
        
        for _ in range(0, indent, 1):
            self.testFile.write("    ")
            
        self.testFile.write(text)
        
    def close(self):
        """Close test file"""
        self.testFile.close()
                    
class ExpWriter(ExportWriter):
    
    def __init__(self, fileName, extension='.exp'):
        super().__init__(fileName, extension)
    
    def _createHeader(self, testName):
        """Create the EXP POU file header"""
        #TODO: parameter writer
        print ("EXP header opening " + testName + "...\n")
        self._write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self._write("(* @PATH := '' *)\n")
        self._write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self._write("(* @SYMFILEFLAGS := '2048' *)\n")
        self._write("PROGRAM " + testName + "\n")
    
    def _createFooter(self):
        """Create the EXP file footer"""
        #TODO: parameter writer
       
        print ("EXP POU footer closure...\n")
        self._write("END_PROGRAM\n")    
        
    def _endDeclaration(self):
        """End of declaration header"""
        #TODO: parameter writer
        
        print ("EXP end declaration...\n")
        self._write("(* @END_DECLARATION := '0' *)\n")
    
    def _writeConstants(self, test):
        """Write test values and size constants to file"""
        
        print ("export constants to EXP...\n")
        self._write("VAR CONSTANT\n")
        
        self._indent+=1

        for constant in test.constants:
            text = constant['Name'] + " : " + constant['Type'] + " := "
            if type(constant['Value']) != list:
                self._write(text + str(constant['Value']) + ";\n")
            else:
                # constant is a list
                self._write(text+"\n")
                self._indent+=1
                text = ''
                i = 0
                
                for i, value in enumerate(constant['Value']):
                    if i:  
                        self._write(text+',\n')
                        text = ''
                    if type(value) != list: # char array, actually
                        text += value
                    else:
                        # constant is a list of lists
                        if constant['Name'] == 'TestVars':
                            self._write('\n')
                            self._write("(* Test case " + str(i+1) + " *)\n")
                        
                        for j, valueItem in enumerate(value):
                            if j: 
                                self._write(text+',\n')
                                text = ''
                            text += valueItem
                        
                        if test.maxSteps-len(value) > 0:
                            self._write(text+',\n')
                            #TODO: use time variable name
                            text = (str(test.maxSteps-len(value)) + "( testtime :=  0 )")
                            
                self._write(text+';\n')
                self._indent-=1
        self._indent-=1

        self._write("END_VAR\n")
        
    def _writeVariables(self, test):
        """Write test variables needed for test execution"""
        
        print ("export variables to EXP...\n")
        
        # Default pass return variable
        self._write("VAR_OUTPUT\n")
        self._write("Pass: BOOL;\n", indent=1)
        self._write("END_VAR\n")

        self._write("VAR\n")
        self._indent=2

        for variable in test.variables:
            self._write(variable['Name'] + " : " + variable['Type'], indent=1)
            
            if 'Value' in variable:
                self._write(" := ", indent=0);
                if type(variable['Value']) != list:
                    self._write(str(variable['Value']), indent=0)
                else:
                    i = 0
                    self._write('\n',indent=0)
                    for value in variable['Value']:
                        i+=1
                        self._write("(* Test case" + str(i) + "*)")
                        
                        end = False
                        for valueItem in value:
                            if end:
                                self._write(",\n",indent=0)
                            self._write(valueItem)
                            end = True
                        
            self._write(";\n", indent=0)
        self._indent=0                       
        self._write("END_VAR\n")

        
    def _createStateMachine(self, test):
        """Create test state machine, main test execution"""
        
        print ("Create state machine for testing...\n")
        self._indent = 1;
        self._write("testInit('" + test.testName[:TEST_NAME_MAX] + "', NoOfTests)\n\n")
        self._write('CASE _tls_ OF\n')
        self._write('sT_INIT:    (* Reset *)\n')
        self._indent = 4;
        self._write('SysMemSet (ADR(' + test.instanceName + '), 0, SIZEOF(' + test.instanceName + '));\n')

        if test.maxSteps:
            # Write steplenght only if needed
            selSteps = False
            for i, sequence in enumerate (test.sequences):
                if len(sequence) < test.maxSteps:
                    text = ''
                    if selSteps:
                        text = 'ELS'

                    selSteps = True
                    text += 'IF _tst_ = ' + str(i) + ' THEN\n'
                    self._write(text)
                    self._write('testParam(pSteps, '+ str(len(sequence)) +');\n', self._indent+1)
            if selSteps:
                self._write('ELSE\n');
                self._indent+=1
            self._write('testParam(pSteps, '+ str(test.maxSteps) +');\n')
            if selSteps:
                self._indent-=1
        
        self._write('\n', indent=0)
        self._write('sT_RUN:    (* test run *)\n', indent=1)
        self._write('ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
        
        self._write(test.instanceName + '(\n')
        
        for varType in test.varTypes[1]:
            self._write(varType['Name'] + ' := ptTestVars^.' + varType['Name'] + '\n', indent=5)
            
        self._write(');\n', indent=5)
        self._write('\n', indent=0)
        
        for varType in test.varTypes[2]:
            line = ''
            if varType['Type'] == 'BOOL':
                line = 'assertEquals'
            else:
                line = 'assertEqualsD'
            line += ' (    Value1 := ' + test.instanceName + '.' + varType['Name'] +',\n'
            self._write(line)
            self._write('Value2 := ptTestVars^.' + varType['Name'] + ',\n', indent=9)
            line = 'Mode := '
            
#            if varType.mode[0] == '=' or varType.mode[0] == 'VFY':           
            line += 'mVFY'
#            elif varType.mode[0] == 'BFRNG':
#                line += 'mBFRNG, '
#                line += str(varType.mode[1])
            line += ', Delay := ptTestVars^.testTime);\n\n'
            self._write(line, indent=9)
        
        self._write('sTC_PASS: Pass := TRUE;\n    END_CASE\n', indent=1)
        self._indent=0
        
    def _createTestDUT(self, varTypes, testName):
        """Create test variable data type for the test parameter table"""
        
        print ("Writing data type used for the test to file..")
    
        #TODO: parameter writer
        self._write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self._write("(* @PATH := '' *)\n")
        self._write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self._write("TYPE Vars" + testName + " :\n")
        self._write("STRUCT\n")
        
        self._indent=1
        
        self._write(varTypes[0]['Name'] + ' : ' + varTypes[0]['Type'] + ';\n')
        self._write('(* Inputs *)\n')
        for varType in varTypes[1]:
            self._write(varType['Name'] + ' : ' + varType['Type'] + ';\n')
    
        self._write('(* Expected outputs *)\n')
        for varType in varTypes[2]:
            self._write(varType['Name'] + ' : ' + varType['Type'] + ';\n')
    
        self._indent=0
        self._write("END_STRUCT\n")
        self._write("END_TYPE\n\n")
        self._write("(* @END_DECLARATION := '0' *)\n")
    
    def writeTest(self, test):
        
        self._createHeader(test.testName)
        self._writeConstants(test)
        self._writeVariables(test)
        self._endDeclaration()
        self._createStateMachine(test)
        self._createFooter()
        self._createTestDUT(test.varTypes, test.testName)
      
class XmlWriter(ExportWriter):
    """XML style export writer"""
    #TODO: implement XML writing 
    pass
