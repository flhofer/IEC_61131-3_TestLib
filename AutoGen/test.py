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
    
    typeVar = {}
    steps = {}
    
    def __init__(self, testName = 'DummyTest', instanceName = 'TestInst', fbName=''):
        """Intialise new test object"""
        self.testName = testName 
        self.instanceName = instanceName
        self.fbName = fbName
    
    def generateVars(self):
        """Generate -required- variable list to add to the test POU"""
    
        variables = {0:{ 'Name': self.instanceName,    'Type': self.fbName}}
        variables[1] = { 'Name': 'ptrVars', 'Type': 'POINTER TO ' + self.testName + '_vars'}
        variables[2] = { 'Name': 'i', 'Type': 'INT', 'Value' : "1"}
    
        return variables

    def generateConst (self):
        """Generate constant values for the test
        Generate values that represent test parameters and test size parameters
        to add to the test POU"""

        # Collector for the parametrized test values
        testvars = []
        seqlen = 0
        for s in self.steps:
            testvar = []
            for v in self.steps[s]:
                const = "( " + self.typeVar[0]['Name'] + " := " + str(int(self.steps[s][v][0]))
                for t in self.typeVar[1]:
                    const += ", " + self.typeVar[1][t]['Name'] + " := " + str((self.steps[s][v][1][t]['Value']))
        
                for t in self.typeVar[2]:
                    const += ", " + self.typeVar[2][t]['Name'] + " := " + str(self.steps[s][v][2][t]['Value'])
                const += " )"
                    
                testvar.append(const)
    
            seqlen = max(seqlen, len(testvar))
            testvars.append(testvar)
        
        # Finally, return the constants for test function 
        constants = {0:{ 'Name': "NoOfTests",    'Type': "USINT", 'Value' : len(testvars)}}
        constants[1] = { 'Name': "NoOfInputs",    'Type': "USINT", 'Value' : seqlen}
        constants[2] = { 'Name': "TestVars",    'Type': "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars" + self.testName, 'Value' : testvars}
        #print constants
    
        return constants
        # fix len steps to len array    

    def setTestVars(self, typeVar):
        self.typeVar = typeVar
    
    def getTestVars(self):
        return self.typeVar
        
    def setSteps(self, steps):
        self.steps = steps
        
    def getSteps(self):
        return self.steps