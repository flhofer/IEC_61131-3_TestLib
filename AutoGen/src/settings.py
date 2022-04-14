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
VAR_REF = 'Ref'
CODE_LINE = 'Line'
CODE_STATE = 'State'
CODE_CODE = 'Code'

''' Constants for Test's internal use ''' 
MODES = { 'VFY' : 'mVFY', 'AT': 'mAT', 'BFRNG': 'mBFRNG', 'ATRNG': 'mATRNG', 'AFRNG' : 'mAFRNG'}
'''
    mEQ            : DWORD := 16#0000000;
    mLT            : DWORD := 16#1000000;
    mGT            : DWORD := 16#2000000;
    mLEQ        : DWORD := 16#3000000;
    mGEQ        : DWORD := 16#4000000;
    mBTW        : DWORD := 16#5000000; (* not implemented yet *)
    mVFY        : DWORD := 16#00000000;
    mBEFORE        : DWORD := 16#10000000;
    mAFTER        : DWORD := 16#20000000;
    mAT            : DWORD := 16#30000000;
    mBFRNG        : DWORD := 16#50000000;
    mAFTRNG        : DWORD := 16#60000000;
    mATRNG        : DWORD := 16#70000000;
'''    

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
