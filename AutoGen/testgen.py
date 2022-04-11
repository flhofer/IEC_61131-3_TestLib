#!/usr/bin/python

# -----------------------------------------------------------
# Test Generator for the IEC61131-3 Test library
#
# (C) 2017-2020 Hofer Florian, Bolzano, ITALY
# Released under GNU Public License (GPL)
# email info@florianhofer.it
# -----------------------------------------------------------

from exp import ExpWriter
from wbk import Workbook
from test import Test
import sys

def main(argv):

	"""
	Main program
	
	Read test Workbook and generate test cases/import for the IEC61131-3
	""" 
	
	wb = Workbook('test_unit.xlsx')
	
	wbkiter = iter(wb)
	
	#iterate though sheets
	for wbk in wbkiter:
				
		# TODO: create multiple tests per sheet, continue on next sheet with new file	
		testFile = ExpWriter(testName=wbk.testName, fileName=wbk.testName)

		test = Test(wbk.testName, wbk.instanceName, wbk.fbName)
		# found header, scan for labels.
		test.setTestVars(wbk.getFunctionVars()) 
		# build step dictionary
		test.setSteps(wbk.readSequences(test.getTestVars()))
		
		# test file is open, create header and lets scan for data!e
		testFile.createHeader()
			
		
			
		testFile.writeConstants(test.generateConst())
		testFile.writeVariables(test.generateVars())
		testFile.endDeclaration()
		testFile.createStateMachine(wbk.instanceName, test.getTestVars())
		testFile.createFooter()
		testFile.createTestDUT(test.getTestVars())
	
		testFile.close()

if __name__ == "__main__":
	main(sys.argv[1:])
