# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library - Test module
#
# Created May, 30, 2017
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

class Test:
    """Test object that contains information on a test POU""" 

    testName = ''
    fbName = ''
    instanceName = ''
    constants = {}
    variables = {}
    
    # From workbook -> may be removed in future
    typeVar = {}
    steps = {}
    
    def __init__(self, testName = 'DummyTest', instanceName = 'TestInst', fbName=''):
        """Intialise new test object"""
        self.testName = testName 
        self.instanceName = instanceName
        self.fbName = fbName
    
    def _generateVars(self):
        """Generate -required- variable list to add to the test POU"""
    
        self.variables = {0:{ 'Name': 'ptrVars', 'Type': 'POINTER TO ' + self.testName + '_vars'}}
        self.variables[1] = { 'Name': 'i', 'Type': 'INT', 'Value' : "1"}
        if self.fbName != '':
            self.variables[2] = { 'Name': self.instanceName,    'Type': self.fbName}
    
        #TODO: add generation of Variables for testGenArray
        return self.variables

    def _generateConst (self):
        """Generate constant values for the test
        Generate values that represent test parameters and test size parameters
        to add to the test POU"""

        # Collector for the parametrized test values
        testvars = []
        seqlen = 0
        for s in self.steps:
            testvar = []
            wasFix = [False] * len(self.steps[s][0])
            for v in self.steps[s]:
                const = "( " + self.typeVar[0]['Name'] + " := " + str(int(self.steps[s][v][0]))
                for t in self.typeVar[1]:
                    if str(self.steps[s][v][1][t]['Value']) != '' and (self.steps[s][v][1][t]['Type'].lower() == 'fix' or self.steps[s][v][1][t]['Type'].lower() == '' and wasFix[t] == True):
                        const += ", " + self.typeVar[1][t]['Name'] + " := " + str((self.steps[s][v][1][t]['Value']))
                        wasFix[t] = True
                    else:
                        wasFix[t] = False
        
                for t in self.typeVar[2]:
                    if str(self.steps[s][v][1][t]['Value']) != '':
                        const += ", " + self.typeVar[2][t]['Name'] + " := " + str(self.steps[s][v][2][t]['Value'])
                const += " )"
                    
                testvar.append(const)
    
            seqlen = max(seqlen, len(testvar))
            testvars.append(testvar)
        
        # Finally, return the constants for test function 
        self.constants = {0:{ 'Name': "NoOfTests",    'Type': "USINT", 'Value' : len(testvars)}}
        self.constants[1] = { 'Name': "NoOfInputs",    'Type': "USINT", 'Value' : seqlen}
        self.constants[2] = { 'Name': "TestVars",    'Type': "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars" + self.testName, 'Value' : testvars}
        #print constants
    
        return self.constants
        # fix len steps to len array    
        
    def _updateStates(self):
        pass    
    
    def parseData(self):
        """Parses variables and sequence code to generate additional steps from preset"""
        self._generateConst()
        self._generateVars()
        
        self._updateStates()
        pass
    
    