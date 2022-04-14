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
from settings import *
from textwrap import indent
from samba.provision.sambadns import SecureTimeProperty

if __name__ == '__main__':
    pass

class ExportWriter:
    """Common test export-import writer class"""
    
    def __init__(self, fileName, extension='.txt'):
        """Initialize instance and open output file"""
        try:
            self.testFile = open(fileName + extension, "w", encoding="utf-8")
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
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
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
            text = constant[VAR_NAME] + " : " + constant[VAR_TYPE] + " := "
            if type(constant[VAR_VALUE]) != list:
                self._write(text + str(constant[VAR_VALUE]) + ";\n")
            else:
                # constant is a list
                self._write(text+"\n")
                self._indent+=1
                text = ''
                i = 0
                
                for i, value in enumerate(constant[VAR_VALUE]):
                    if i:  
                        self._write(text+',\n')
                        text = ''
                    if type(value) != list: # char array, actually
                        text += value
                    else:
                        # constant is a list of lists
                        if constant[VAR_NAME] == 'TestVars':
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
            self._write(variable[VAR_NAME] + " : " + variable[VAR_TYPE], indent=1)
            
            if VAR_VALUE in variable:
                self._write(" := ", indent=0);
                if type(variable[VAR_VALUE]) != list:
                    self._write(str(variable[VAR_VALUE]), indent=0)
                else:
                    i = 0
                    self._write('\n',indent=0)
                    for value in variable[VAR_VALUE]:
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

    def _writeStateHeader(self, state):
        ''' Writes the case steatement constant and indent '''
        self._write(STATES[state] + ':    (* State '+  state + ' *)\n', indent = 1)
        self._indent = 4;

    def _writeStateCode(self, test, state):
        ''' Write the code for the state found in input'''
                
        for stateCode in test.stateCode:
            if stateCode[CODE_STATE] == STATES[state]:
                self._writeStateHeader(state)
                for line in stateCode[CODE_CODE]:
                    if line[TEST_TIME] != 0:
                        self._write('testParam(pWTIME, ' + str(line[TEST_TIME])+ ');\n')
                    self._write(line[CODE_LINE] + '\n')
                    
                return True
        return False
                            
    def _createStateMachine(self, test):
        """Create test state machine, main test execution"""
        
        print ("Create state machine for testing...\n")

        self._indent = 1;
        self._write("testInit('" + test.testName[:TEST_NAME_MAX] + "', NoOfTests)\n\n")
        self._write('CASE _tls_ OF\n')

        ''' Write State Code '''

        for state in STATES:
            #NOTE > this needs Python 3.6 or higher, ordered dictionaries
            
            header = self._writeStateCode(test, state)
        
            ''' Some additional key states '''
            if state == 'Init' and test.maxSteps > 1:
                ''' Init State '''
                if not header:
                    self._writeStateHeader(state)

                #        if test.fbName != '' : # if there is an instance -> clear
                #            self._write('SysMemSet (ADR(' + test.instanceName + '), 0, SIZEOF(' + test.instanceName + '));\n')
                
                # Write step length only if needed
                selSteps = False
                for i, sequence in enumerate (test.runSequences):
                    if len(sequence) < test.maxSteps:
                        text = ''
                        if selSteps:
                            text = 'ELS'
    
                        selSteps = True
                        text += 'IF _tlt_ = ' + str(i+1) + ' THEN\n'
                        self._write(text)
                        self._write('testParam(pSTEPS, '+ str(len(sequence)) +');\n', self._indent+1)
                if selSteps:
                    self._write('ELSE\n');
                    self._indent+=1
                self._write('testParam(pSteps, '+ str(test.maxSteps) +');\n')
                if selSteps:
                    self._indent-=1
                            
                self._write('\n', indent=0)
        
            if state == 'Run':
                ''' RUN STATE ''' 
                if not header:
                    self._writeStateHeader(state)

                self._write('ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
        
                self._write(test.instanceName + '(\n')
        
                self._indent+=1
                for varType in test.varDefs[TEST_INPUT]:
                    text = varType[VAR_NAME] + ' := '
                    #TODO: for now only supports one generator per variable per test
                    generator = next((item for item in test.generators if item[VAR_NAME] == varType[VAR_NAME]), None)
                    if generator:
                        text += 'SEL( _tlt_ <> ' + str(generator[VAR_TEST]) + ', testGenArray(ADR(' + generator[VAR_REF] + '),SIZEOF(' + generator[VAR_REF] + ')),\n'
                        self._write(text)
                        self._indent+=1
                        text = ''
                    text += 'ptTestVars^.' + varType[VAR_NAME]
                    if generator:
                        text += ')'
                    text += '\n'
                    self._write(text)
                    if generator:
                        self._indent-=1
    
                self._write(');\n')
                self._write('\n', indent=0)
                self._indent-=1
                
                for varType in test.varDefs[TEST_OUTPUT]:
                    line = ''
                    if varType[VAR_TYPE] == 'BOOL':
                        line = 'assertEquals '
                    elif varType[VAR_TYPE] == 'STRUCT':
                        line = 'assertEqualsO'
                    else:
                        line = 'assertEqualsD'
                    line += ' ( Value1 := ' + test.instanceName + '.' + varType[VAR_NAME] +',\n'
                    self._write(line)
                    self._write('Value2 := ptTestVars^.' + varType[VAR_NAME] + ',\n', indent=8)
                    line = 'Mode := '
                    
                    varMode = varType[VAR_TEST].split(",")
                    if varMode[0] in MODES:
                        
                        line += varMode[0]
                        if len(varMode) > 1:
                            line += ' + ' + varMode[1]
                    else:
                        line += 'mVFY' 
                    line += ', Delay := ptTestVars^.testTime);\n\n'
                    self._write(line, indent=8)
            
            if state == 'Case Pass':
                ''' TEST CASE PASS STATE '''
                if not header:
                    self._writeStateHeader(state)
                
                self._write('Pass := TRUE;\n')

        self._write(' END_CASE\n', indent=1)
            
        self._indent=0
        
    def _createTestDUT(self, varDefs, testName):
        """Create test variable data type for the test parameter table"""
        
        print ("Writing data type used for the test to file..")
    
        #TODO: parameter writer
        self._write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self._write("(* @PATH := '' *)\n")
        self._write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self._write("TYPE Vars" + testName + " :\n")
        self._write("STRUCT\n")
        
        self._indent=1
        
        self._write(varDefs[TEST_TIME][VAR_NAME] + ' : ' + varDefs[TEST_TIME][VAR_TYPE] + ';\n')
        self._write('(* Inputs *)\n')
        for varType in varDefs[TEST_INPUT]:
            self._write(varType[VAR_NAME] + ' : ' + varType[VAR_TYPE] + ';\n')
    
        self._write('(* Expected outputs *)\n')
        for varType in varDefs[TEST_OUTPUT]:
            self._write(varType[VAR_NAME] + ' : ' + varType[VAR_TYPE] + ';\n')
    
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
        self._createTestDUT(test.varDefs, test.testName)
      
class XmlWriter(ExportWriter):
    """XML style export writer"""
    #TODO: implement XML writing 
    pass
