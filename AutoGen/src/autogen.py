#!/usr/bin/python

'''
-----------------------------------------------------------
Test Generator for the IEC61131-3 Test library

(C) 2017-2020 Hofer Florian, Bolzano, ITALY

Released under GNU Public License (GPL)
email info@florianhofer.it
-----------------------------------------------------------
'''

from exp import ExpWriter
from wbk import Workbook
import sys

def main(argv):

	"""
	Main program
	
	Read test Workbook and generate test cases/import for the IEC61131-3
	""" 
	
	workBook = Workbook('test_unit.xlsx')
	wbkiter = iter(workBook)
	
	#iterate though sheets
	for sheet in wbkiter:
				
		# TODO: create multiple tests per sheet, continue on next sheet with new file, use generator!
		test = sheet.readTest()		
		# parse data and prepare test structure
		test.parseData()
		
		with ExpWriter(fileName=test.testName) as testFile:
			testFile.writeTest(test)

if __name__ == "__main__":
	main(sys.argv[1:])
