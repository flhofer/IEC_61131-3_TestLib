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
from ideInterface import CoDeSysConnect
from time import sleep

def main(argv):

	"""
	Main program
	
	Read test Workbook and generate test cases/import for the IEC61131-3
	""" 
	
	#TODO: hardcoded XLS
	workBook = Workbook('test_unit.xls')
	wbkiter = iter(workBook)
	
	testFiles = []
	#iterate though sheets
	for sheet in wbkiter:
				
		# TODO: create multiple tests per sheet, continue on next sheet with new file, use generator!
		test = sheet.readTest()		
		# parse data and prepare test structure
		test.parseData()
		
		with ExpWriter(fileName=test.testName) as testFile:
			testFile.writeTest(test)
			testFiles.append(testFile._fileName)
	
	#TODO: hardcoded target pro
	ide = CoDeSysConnect('..\Examples\Sample1.pro')
	ide.runTest(testFiles)
	sleep(30) #TODO: more precise timing needed between import/run and DDE
	
	ide.connect()
	sleep(3)
	print("Polling test results...")
	try:
		while True:
			ide.poll()
			sleep(1)
	except KeyboardInterrupt:
		pass

	print('Exit program')
	ide.waitIde()

if __name__ == "__main__":
	main(sys.argv[1:])
