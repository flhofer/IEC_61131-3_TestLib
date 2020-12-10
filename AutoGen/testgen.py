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

def generateConst (steps):
	"""Generate constant values for the test
	Generate values that represent test parameters and test size parameters
	to add to the test POU"""

	# Collector for the parametrized test values
	testvars = []
	seqlen = 0
	for s in steps:
		testvar = []
		for v in steps[s]:
			const = "( " + typeVar[0]['Name'] + " := " + str(int(steps[s][v][0]))
			for t in typeVar[1]:
				const += ", " + typeVar[1][t]['Name'] + " := " + str((steps[s][v][1][t]['Value']))
	
			for t in typeVar[2]:
				const += ", " + typeVar[2][t]['Name'] + " := " + str(steps[s][v][2][t]['Value'])
			const += " )"
				
			testvar.append(const)

		seqlen = max(seqlen, len(testvar))
		testvars.append(testvar)
	
	# Finally, return the constants for test function 
	constants = {0:{ 'Name': "NoOfTests",	'Type': "USINT", 'Value' : len(testvars)}}
	constants[1] = { 'Name': "NoOfInputs",	'Type': "USINT", 'Value' : seqlen}
	constants[2] = { 'Name': "TestVars",	'Type': "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars" + wbk.testName, 'Value' : testvars}
	#print constants

	return constants
	# fix len steps to len array

def generateVars():
	"""Generate -required- variable list to add to the test POU"""
	
	variables = {0:{ 'Name': wbk.instanceName,	'Type': wbk.fbName}}
	variables[1] = { 'Name': 'ptrVars', 	'Type': 'POINTER TO ' + wbk.testName + '_vars'}
	variables[2] = { 'Name': 'i', 			'Type': 'INT', 'Value' : "1"}
	
	return variables

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
	
	# test file is open, create header and lets scan for data!e
	testFile.createHeader()
		
	# found header, scan for labels.
	typeVar = wbk.getFunctionVars()
	
	# build step dictionary
	steps = wbk.readSequences(typeVar)
		
	testFile.writeConstatns(generateConst(steps))
	testFile.writeVariables(generateVars())
	testFile.endDeclaration()
	testFile.createStateMachine(wbk.instanceName, typeVar)
	testFile.createFooter()
	testFile.createTestDUT(typeVar)

	testFile.close()
