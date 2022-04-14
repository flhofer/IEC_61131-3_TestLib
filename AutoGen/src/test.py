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
from settings import *

#TODO: mutate to data object/class
class Test:
    """Test object that contains information on a test POU""" 

    testName = ''
    fbName = ''
    instanceName = ''
    maxSteps = 1

    ''' Test data storage '''
    varDefs = { TEST_TIME: {},  TEST_OUTPUT: [], TEST_INPUT : [] }
    stateCode = []  # TODO: for now only single Init
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
        self.varDefs[TEST_OUTPUT].append(varDesc)
        
    def appendInputType(self, varDesc ):
        """ Add a input variable to variable descriptors """
        self.varDefs[TEST_INPUT].append(varDesc)
    
    def setTimeType(self, timeDesc):
        """ Set the time base for the test """
        self.varDefs[TEST_TIME] = timeDesc

    def appendRunSequence(self, sequence):
        """ adds a Run-state Sequence to the list """
        self.runSequences.append(sequence)
        
    def appendStateCode(self, state, codeLines):
        """ appends to the registry of code to insert to a State """
        self.stateCode.append({ CODE_STATE: state, CODE_CODE : codeLines })
        
    def _generateVars(self):
        """Generate -required- variable list to add to the test POU"""

        self.generators = []
        # Collector for the parametrized test values
        for s, sequence in enumerate(self.runSequences):
            generator = { 'Len' : 0, VAR_NAME : '', VAR_VALUE : '', 'Test': 0}
            wasGenArr = False
            for i, varType in enumerate(self.varDefs[TEST_INPUT]): 
                for varValues in sequence:
                    if varValues[TEST_INPUT][i][VAR_MODE] in GEN_MODES:
                        generator[VAR_VALUE] = GEN_MODES[varValues[TEST_INPUT][i][VAR_MODE]]
                        wasGenArr = True
                        generator[VAR_NAME] = varType[VAR_NAME]
                        generator[VAR_VALUE] += ', ' + varValues[TEST_INPUT][i][VAR_VALUE]   
                        generator[VAR_TEST] = s+1
                        generator['Len']+= len(varValues[TEST_INPUT][i][VAR_VALUE].split(','))
                    elif str(varValues[TEST_INPUT][i][VAR_VALUE]) != '' and varValues[TEST_INPUT][i][VAR_MODE].lower() == '' and wasGenArr == True:
                        generator[VAR_VALUE] += ', ' + varValues[TEST_INPUT][i][VAR_VALUE]
                        generator['Len']+= len(varValues[TEST_INPUT][i][VAR_VALUE].split(','))
                    else:
                        wasGenArr = False                    
            
            if generator['Len'] > 0:
                self.generators.append(generator)

        self.variables.append({ VAR_NAME: 'ptrVars', VAR_TYPE: 'POINTER TO Vars_' + self.testName })
        if self.fbName != '':
            self.variables.append({ VAR_NAME: self.instanceName,    VAR_TYPE: self.fbName})
    
        for i, generator in enumerate(self.generators):
            generator[VAR_REF] = 'Array' + str(i+1)
            self.variables.append({ VAR_NAME: generator[VAR_REF], VAR_TYPE: 'ARRAY[0..' + str(generator['Len']) +'] OF REAL', VAR_VALUE : generator[VAR_VALUE]})

        return self.variables

    def _generateConst (self):
        """Generate constant values for the test
        Generate values that represent test parameters and test size parameters
        to add to the test POU"""

        # Collector for the parametrized test values
        testvars = []
        for sequence in self.runSequences:
            testvar = []
            wasFix = [False] * len(self.varDefs[TEST_INPUT])
            for varValues in sequence:
                #TODO: change to list
                const = "( " + self.varDefs[TEST_TIME][VAR_NAME] + " := " + str(int(varValues[TEST_TIME]))
                for i, varType in enumerate(self.varDefs[TEST_INPUT]):
                    if str(varValues[TEST_INPUT][i][VAR_VALUE]) != '' and (varValues[TEST_INPUT][i][VAR_MODE].lower() == 'fix' or varValues[TEST_INPUT][i][VAR_MODE].lower() == '' and wasFix[i] == True):
                        const += ", " + varType[VAR_NAME] + " := " + str(varValues[TEST_INPUT][i][VAR_VALUE])
                        wasFix[i] = True
                        varType[VAR_MODE] = 'fix' # TODO just temporary
                    else:
                        if varValues[TEST_INPUT][i][VAR_MODE] != '':
                            varType[VAR_MODE] = varValues[TEST_INPUT][i][VAR_MODE] 
                        wasFix[i] = False
        
                for i, varType in enumerate(self.varDefs[TEST_OUTPUT]):
                    if str(varValues[TEST_OUTPUT][i][VAR_VALUE]) != '':
                        const += ", " + varType[VAR_NAME] + " := " + str(varValues[TEST_OUTPUT][i][VAR_VALUE])
                        if varValues[TEST_OUTPUT][i][VAR_TEST] != '':
                            varType[VAR_TEST] = varValues[TEST_OUTPUT][i][VAR_TEST]
                const += " )"
                    
                testvar.append(const)
    
            self.maxSteps = max(self.maxSteps, len(testvar))
            testvars.append(testvar)
        
        # Finally, return the constants for test function 
        self.constants.append({ VAR_NAME: "NoOfTests",    VAR_TYPE: "USINT", VAR_VALUE : len(testvars)})
        self.constants.append({ VAR_NAME: "NoOfInputs",    VAR_TYPE: "USINT", VAR_VALUE : self.maxSteps})
        self.constants.append({ VAR_NAME: "TestVars",    VAR_TYPE: "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars" + self.testName, VAR_VALUE : testvars})
        #print constants
    
        return self.constants  
        
    def _updateStates(self):
        pass    
    
    def parseData(self):
        """Parses variables and sequence code to generate additional sequences from preset"""

        self._generateConst()
        self._generateVars()
        self._updateStates()
     
        