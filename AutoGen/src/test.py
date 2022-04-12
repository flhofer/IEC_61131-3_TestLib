'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - Test module

Created May, 30, 2017

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

class Test:
    """Test object that contains information on a test POU""" 

    testName = ''
    fbName = ''
    instanceName = ''
    maxSteps = 1
    constants = []
    variables = []
    generators = []
    
    # From workbook -> may be removed in future
    varTypes = {}
    sequences = {}
    
    def __init__(self, testName = 'DummyTest', instanceName = 'TestInst', fbName=''):
        """Intialise new test object"""
        self.testName = testName 
        self.instanceName = instanceName
        self.fbName = fbName
    
    def _generateVars(self):
        """Generate -required- variable list to add to the test POU"""

        self.generators = []
        # Collector for the parametrized test values
        for sequence in self.sequences:
            generator = { 'Len' : 0, 'Name' : '', 'Value' : '', 'Test': 0}
            wasGenArr = False
            for i, varType in enumerate(self.varTypes[1]): 
                for varValues in sequence:
                    if varValues[1][i]['Type'].lower() == 'tuple':
                        generator['Value'] = 'rTuple'
                        wasGenArr = True
                        generator['Name'] = varType['Name']
                        generator['Value'] += ', ' + varValues[1][i]['Value']   
                        generator['Test'] = sequence
                        generator['Len']+=3
                    elif str(varValues[1][i]['Value']) != '' and varValues[1][i]['Type'].lower() == '' and wasGenArr == True:
                        generator['Value'] += ', ' + varValues[1][i]['Value']
                        generator['Len']+=2
                    else:
                        wasGenArr = False                    
            
            if generator['Len'] > 0:
                self.generators.append(generator)

        self.variables.append({ 'Name': 'ptrVars', 'Type': 'POINTER TO ' + self.testName + '_vars'})
        self.variables.append({ 'Name': 'i', 'Type': 'INT', 'Value' : "1"})
        if self.fbName != '':
            self.variables.append({ 'Name': self.instanceName,    'Type': self.fbName})
    
        for i, generator in enumerate(self.generators):
            self.variables.append({ 'Name': 'Array' + str(i+1), 'Type': 'ARRAY[1..' + str(generator['Len']) +'] OF REAL', 'Value' : generator['Value']})

        return self.variables

    def _generateConst (self):
        """Generate constant values for the test
        Generate values that represent test parameters and test size parameters
        to add to the test POU"""

        # Collector for the parametrized test values
        testvars = []
        for sequence in self.sequences:
            testvar = []
            wasFix = [False] * len(self.varTypes[1])
            for varValues in sequence:
                #TODO: change to list
                const = "( " + self.varTypes[0]['Name'] + " := " + str(int(varValues[0]))
                for i, varType in enumerate(self.varTypes[1]):
                    if str(varValues[1][i]['Value']) != '' and (varValues[1][i]['Type'].lower() == 'fix' or varValues[1][i]['Type'].lower() == '' and wasFix[i] == True):
                        const += ", " + varType['Name'] + " := " + str(varValues[1][i]['Value'])
                        wasFix[i] = True
                    else:
                        wasFix[i] = False
        
                for i, varType in enumerate(self.varTypes[2]):
                    if str(varValues[1][i]['Value']) != '':
                        const += ", " + varType['Name'] + " := " + str(varValues[2][i]['Value'])
                const += " )"
                    
                testvar.append(const)
    
            self.maxSteps = max(self.maxSteps, len(testvar))
            testvars.append(testvar)
        
        # Finally, return the constants for test function 
        self.constants.append({ 'Name': "NoOfTests",    'Type': "USINT", 'Value' : len(testvars)})
        self.constants.append({ 'Name': "NoOfInputs",    'Type': "USINT", 'Value' : self.maxSteps})
        self.constants.append({ 'Name': "TestVars",    'Type': "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars" + self.testName, 'Value' : testvars})
        #print constants
    
        return self.constants
        # fix len sequences to len array    
        
    def _updateStates(self):
        pass    
    
    def parseData(self):
        """Parses variables and sequence code to generate additional sequences from preset"""
        self._generateConst()
        self._generateVars()
        
        self._updateStates()
        pass
    
    