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

''' Constants for Test's internal use ''' 
MODES = { 'VFY' : 'mVFY', 'AT': 'mAT', 'BFRNG': 'mBFRNG', 'ATRNG': 'mATRNG', 'AFRNG' : 'mAFRNG'}
