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
        
        for i in range(0, indent, 1):
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

        for c in test.constants:
            text = c['Name'] + " : " + c['Type'] + " := "
            if type(c['Value']) != list:
                self._write(text + str(c['Value']) + ";\n")
            else:
                # constant is a list
                self._write(text+"\n")
                self._indent+=1
                text = ''
                i = 0
                
                for i, v in enumerate(c['Value']):
                    if i:  
                        self._write(text+',\n')
                        text = ''
                    if type(v) != list: # char array, actually
                        text += v
                    else:
                        # constant is a list of lists
                        if c['Name'] == 'TestVars':
                            self._write('\n')
                            self._write("(* Test case " + str(i+1) + " *)\n")
                        
                        for j, w in enumerate(v):
                            if j: 
                                self._write(text+',\n')
                                text = ''
                            text += w
                        
                        if test.maxSteps-len(v) > 0:
                            self._write(text+',\n')
                            text = (str(test.maxSteps-len(v)) + "( testtime :=  0 )")
                            
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

        for c in test.variables:
            self._write(c['Name'] + " : " + c['Type'], indent=1)
            
            if 'Value' in c:
                self._write(" := ", indent=0);
                if type(c['Value']) != list:
                    self._write(str(c['Value']), indent=0)
                else:
                    i = 0
                    self._write('\n',indent=0)
                    for v in c['Value']:
                        i+=1
                        self._write("(* Test case" + str(i) + "*)")
                        
                        end = False
                        for w in v:
                            if end:
                                self._write(",\n",indent=0)
                            self._write(w)
                            end = True
                        
            self._write(";\n", indent=0)
        self._indent=0                       
        self._write("END_VAR\n")

        
    def _createStateMachine(self, test):
        """Create test state machine, main test execution"""
        
        print ("Create state machine for testing...\n")
        self._indent = 1;
        self._write("testInit('" + test.testName + "', NoOfTests)\n\n")
        self._write('CASE _tls_ OF\n')
        self._write('sT_INIT:    (* Reset *)\n')
        self._indent = 4;
        self._write('SysMemSet (ADR(' + test.instanceName + '), 0, SIZEOF(' + test.instanceName + '));\n')

        sel = False
        for i, s in enumerate (test.steps):
            if len(s) < test.maxSteps:
                if sel:
                    self._write('ELSIF _tst_ = ' + str(i) + 'THEN\n')
                else:
                    self._write('IF _tst_ = ' + str(i) + 'THEN\n')
                    
                self._write('testParam(pSteps, '+ str(test.maxSteps) +');\n', self._indent+1)
                self._indent-=1
        if sel:
            self._write('ELSE\n');
            self._indent+=1
        self._write('testParam(pSteps, '+ str(test.maxSteps) +');\n')
        if sel:
            self._indent-=1
        
        self._write('\n', indent=0)
        self._write('sT_RUN:    (* test run *)\n', indent=1)
        self._write('ptTestVars := ADR(Tests_Values[_tlt_,_tlp_]);\n')
        
        self._write(test.instanceName + '(\n')
        
        for v in test.typeVar[1]:
            self._write(v['Name'] + ' := ptTestVars^.' + v['Name'] + '\n', indent=5)
            
        self._write(');\n', indent=5)
        self._write('\n', indent=0)
        
        for v in test.typeVar[2]:
            line = ''
            if v['Type'] == 'BOOL':
                line = 'assertEquals'
            else:
                line = 'assertEqualsD'
            line += ' (    Value1 := ' + test.instanceName + '.' + v['Name'] +',\n'
            self._write(line)
            self._write('Value2 := ptTestVars^.' + v['Name'] + ',\n', indent=9)
            line = 'Mode := '
            
#            if v.mode[0] == '=' or v.mode[0] == 'VFY':           
            line += 'mVFY'
#            elif v.mode[0] == 'BFRNG':
#                line += 'mBFRNG, '
#                line += str(v.mode[1])
            line += ', Delay := ptTestVars^.testTime);\n\n'
            self._write(line, indent=9)
        
        self._write('sTC_PASS: Pass := TRUE;\n    END_CASE\n', indent=1)
        self._indent=0
        
    def _createTestDUT(self, typeVar, testName):
        """Create test variable data type for the test parameter table"""
        
        print ("Writing data type used for the test to file..")
    
        #TODO: parameter writer
        self._write("(* @NESTEDCOMMENTS := 'Yes' *)\n")
        self._write("(* @PATH := '' *)\n")
        self._write("(* @OBJECTFLAGS := '0, 8' *)\n")
        self._write("TYPE Vars" + testName + " :\n")
        self._write("STRUCT\n")
        
        self._indent=1
        
        self._write(typeVar[0]['Name'] + ' : ' + typeVar[0]['Type'] + ';\n')
        self._write('(* Inputs *)\n')
        for v in typeVar[1]:
            self._write(v['Name'] + ' : ' + v['Type'] + ';\n')
    
        self._write('(* Expected outputs *)\n')
        for v in typeVar[2]:
            self._write(v['Name'] + ' : ' + v['Type'] + ';\n')
    
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
        self._createTestDUT(test.typeVar, test.testName)
      
class XmlWriter(ExportWriter):
    """XML style export writer"""
    #TODO: implement XML writing 
    pass
