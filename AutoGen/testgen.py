#!/usr/bin/python

import xlrd
import os.path
import exp
import wbk

def generateConst ():
	testvars = []
	seqlen = 1
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
		
	constants = {1:{ 'Name': "NoOfTests", 'Type': "INT", 'Value' : len(testvars)}}
	constants[2] = { 'Name': "NoOfInputs", 'Type': "INT", 'Value' : seqlen}
	constants[3] = {'Name' : "TestVars", 'Type' : "ARRAY [1..NoOfTests,1..NoOfInputs] OF Vars"+testName, 'Value' : testvars}
	#print constants

	return constants
	# fix len steps to len array

def generateVars():
	
	variables = {1:{ 'Name': instanceName, 'Type': fbName}}
	variables[2] = { 'Name': 'ptrVars', 'Type': 'POINTER TO ' + testName + '_vars'}
	variables[3] = { 'Name': 'i', 'Type': 'INT', 'Value' : "1"}

	
	return variables


wb = xlrd.open_workbook(os.path.join('','test_unit.xlsx'))
wb.sheet_names()
sh = wb.sheet_by_index(0)

#header information
testName = sh.cell(0,1).value
fbName = sh.cell(0,4).value
instanceName = sh.cell(0,6).value

scanPos = 1

with open(testName + ".txt", "a") as testFile:
	# test file is open, create header and lets scan for data!e
	exp.createHeader(testFile, testName)
	
	while True:
		state = sh.cell(scanPos,0).value
		
		if state != "State":
			scanPos += 1
		else:
			break
	
	# found header, scan for labels.
	typeVar = wbk.getFunctionVars(sh.row_values(scanPos, 2))

	scanPos += 1 # next line, start to scan
	
	# build step dictionary
	cnt = 1
	steps = {}
	print scanPos
	#while sh.nrows > scanPos:
	steps[cnt] = wbk.readSequence(sh, scanPos, typeVar)
	print scanPos

	exp.writeConstatns(testFile, generateConst())
	exp.writeVariables(testFile, generateVars())
	exp.createStateMachine(testFile, testName, instanceName, typeVar)
	exp.createFooter(testFile)
	exp.createTestDUT(testFile, testName, typeVar)

testFile.close()

