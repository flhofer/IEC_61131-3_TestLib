'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library - settings

Created Apr, 12, 2022

(C) 2017-2020 Hofer Florian, Bolzano, ITALY
Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

TEST_NAME_MAX = 10


''' Constants for data/dictionary use '''
TEST_INPUT = 'Input'
TEST_OUTPUT = 'Output'
TEST_TIME = 'Time'
VAR_NAME = 'Name'
VAR_VALUE = 'Value'
VAR_TYPE = 'Type'
VAR_TEST = 'Test'
VAR_MODE = 'Mode'
CODE_LINE = 'Line'
CODE_STATE = 'State'
CODE_CODE = 'Code'

''' Constants for Test's internal use ''' 
MODES = { 'VFY' : 'mVFY', 'AT': 'mAT', 'BFRNG': 'mBFRNG', 'ATRNG': 'mATRNG', 'AFRNG' : 'mAFRNG'}

STATES = { 
    # Test Case preparation 
    'Case Init' : 'sTC_INIT', 'Case Wait' : 'sTC_WAIT', 'Case Start' : 'sTC_START', 'Case Run' : 'sTC_RUN',   
    # Test execution 
    #'sTC_ND', 
    'Init' : 'sT_INIT', 'Wait' : 'sT_WAIT', 'Start' : 'sT_START', 'Run' :  'sT_RUN', 'Abort' : 'sT_ABORT', 
    'Stop' : 'sT_STOP', 'End' : 'sT_END', 'Deinit' : 'sT_DEINIT', 'Pass' :  'sT_PASS', 'Fail' : 'sT_FAIL',
    'Error' : 'sT_ERROR',
    #Test case ending
    'Case Abort' : 'sTC_ABORT', 'Case Stop' : 'sTC_STOP', 'Case End' : 'sTC_END', 'Case Deinit' : 'sTC_DEINIT',
    'Case Pass' : 'sTC_PASS', 'Case Fail' : 'sTC_FAIL', 'Case Error' : 'sTC_ERROR'
    }
