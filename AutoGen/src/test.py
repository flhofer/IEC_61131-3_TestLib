'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - Test module

Created May, 30, 2017

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''
from setuptools.dist import sequence

#TODO: mutate to data object/class
class Test:
    """Test object that contains information on a test POU""" 

    testName = ''
    fbName = ''
    instanceName = ''
    maxSteps = 1

    ''' Test data storage '''
    varDefs = { 'Time': {},  'Output': [], 'Input' : [] }
    initSequences = []  # TODO: for now only single Init
    runSequences = []

    ''' Parsing results '''
    constants = []
    variables = []
    generators = []
        
    def __init__(self, testName = 'DummyTest', instanceName = 'TestInst', fbName=''):
        """Intialise new test object"""
        self.testName = testName 
        self.instanceName = instanceName
        self.fbName = fbName
    
    def appendOutputType(self, varDesc ):
        """ Add a output variable to variable descriptors """
        self.varDefs['Output'].append(varDesc)
        
    def appendInputType(self, varDesc ):
        """ Add a input variable to variable descriptors """
        self.varDefs['Input'].append(varDesc)
    
    def setTimeType(self, timeDesc):
        """ Set the time base for the test """
        self.varDefs['Time'] = timeDesc

    def appendRunSequence(self, sequence):
        """ adds a Run-state Sequence to the list """
        self.runSequences.append(sequence)
        
    def _generateVars(self):
        """Generate -required- variable list to add to the test POU"""

        self.generators = []
        # Collector for the parametrized test values
        for sequence in self.runSequences:
            generator = { 'Len' : 0, 'Name' : '', 'Value' : '', 'Test': 0}
            wasGenArr = False
            for i, varType in enumerate(self.varDefs['Input']): 
                for varValues in sequence:
                    if varValues['Input'][i]['Mode'].lower() == 'tuple':
                        generator['Value'] = 'rTuple'
                        wasGenArr = True
                        generator['Name'] = varType['Name']
                        generator['Value'] += ', ' + varValues['Input'][i]['Value']   
                        generator['Test'] = sequence
                        generator['Len']+=3
                    elif str(varValues['Input'][i]['Value']) != '' and varValues['Input'][i]['Mode'].lower() == '' and wasGenArr == True:
                        generator['Value'] += ', ' + varValues['Input'][i]['Value']
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
        for sequence in self.runSequences:
            testvar = []
            wasFix = [False] * len(self.varDefs['Input'])
            for varValues in sequence:
                #TODO: change to list
                const = "( " + self.varDefs['Time']['Name'] + " := " + str(int(varValues['Time']))
                for i, varType in enumerate(self.varDefs['Input']):
                    if str(varValues['Input'][i]['Value']) != '' and (varValues['Input'][i]['Mode'].lower() == 'fix' or varValues['Input'][i]['Mode'].lower() == '' and wasFix[i] == True):
                        const += ", " + varType['Name'] + " := " + str(varValues['Input'][i]['Value'])
                        wasFix[i] = True
                        varType['Mode'] = 'fix' # TODO just temporary
                    else:
                        varType['Mode'] = varValues['Input'][i]['Mode']
                        wasFix[i] = False
        
                for i, varType in enumerate(self.varDefs['Output']):
                    if str(varValues['Input'][i]['Value']) != '':
                        const += ", " + varType['Name'] + " := " + str(varValues['Output'][i]['Value'])
                        varType['Mode'] = varValues['Output'][i]['Type']
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
        
    def _updateStates(self):
        pass    
    
    def parseData(self):
        """Parses variables and sequence code to generate additional sequences from preset"""

        self._generateConst()
        self._generateVars()
        self._updateStates()
     
        