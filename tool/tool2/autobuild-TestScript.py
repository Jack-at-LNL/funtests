#! /usr/bin/python

## This script allows to create automaticaly a test bench application based on the ConfigFile.xls 
## Developed by Maurizio Montis (INFN Legnaro - Italy) and Jean-Francois DENIS (CEA - France)
## Mails: maurizio.montis@lnl.infn.it and jfdenis@cea.fr

import xlrd  	# Library for developers to extract data from Microsoft Excel (tm) spreadsheet files
import sys   	# This module provides access to some variables used by the interpreter
import shutil   # This module offers a number of high-level operations on files and collections of files. 
from string import Template

###############################################################################################
###############################################################################################
########################### PART1 : Creation of the context ###################################
###############################################################################################
###############################################################################################

###############################################################
########################## Variables ##########################
###############################################################

##### Dictionnary of Macro for generic script file
dictMacroScriptFile = dict(XX="",CMD_PV="",RDBK_PV="",BANDWIDTH="",SEVERITY="",CMD_VAL="",DELAY="",RDBK_VAL="",FAIL_MESS="",SUCC_MESS="",RESULT="")

################################################################
########### Check Command line arguments #######################
################################################################

NbArgs = len(sys.argv)
cmdargs = str(sys.argv)

##### Test thenumber of arguments
if (NbArgs !=2):
	     print "ERROR : You need to provide a configuration file in argument \n Example : ./autobuilt-TestScript.py ConfigFile.xlsx "
	     sys.exit(2)
else:
	#Test if the configuration file provided on command line is on the current directory
	ConfigFileName=str(sys.argv[1])
	try:
		with open(ConfigFileName): pass
	except IOError:
		print "ERROR : The file \""+ConfigFileName+"\" is not on this directory"
		sys.exit(2)
	#Selection of the configuration file provided on command line
	ConfigFile = xlrd.open_workbook(ConfigFileName)
	Sheet = ConfigFile.sheet_by_name(u'Feuil1')

#################################################################################
############ Extract all data from the ConfigFile.csv to put in 2D array ########
#################################################################################

#####  Initialisation of 2D array
ConfigFileArray = [[0]*Sheet.ncols for _ in range(Sheet.nrows)]

#####  Extracting value from ConfigFile.csv
for rownum in range(0,Sheet.nrows): 
	for colnum in range(0,Sheet.ncols): 
		ConfigFileArray[rownum][colnum]= Sheet.cell(rowx=rownum,colx=colnum).value

#####  Extract all PV name to add in a List
ListPV = list()

#####  Selection of the Cmd PV column
colCmdPV = Sheet.col_values(0)

#####  Extract value and add in a List
for rownum in range(1,Sheet.nrows) : 
	if len(colCmdPV[rownum])!=0 : ListPV.append(colCmdPV[rownum])

#####  Selection of the Rdbk PV column
colRdbkPV = Sheet.col_values(2)

#####  Extract value and add in a List
for rownum in range(1,Sheet.nrows):
	if len(colRdbkPV[rownum])!=0 : ListPV.append(colRdbkPV[rownum])

###############################################################################################
###############################################################################################
########################### PART2 : Creation of the final python script #######################
###############################################################################################
###############################################################################################

#####  Creation of the name of the generated file  
# => NOT GOOD!!!!
scriptFileName = ConfigFileName.replace('Config','TestScript')
scriptFileName = scriptFileName.replace('xls','py')

#####  Creation of the generated file by copying the skeleton.sh
shutil.copy2('ExternalModules/Skeleton.py',scriptFileName)

################################################################
########### Adding script to test the PV connection ############
################################################################

ListTmpLine = list()
ListTmpLine.append("")

##### Adding all PV to one list
ListTmpLine.append("# Creation of the list of all PV\n")
for i in range(len(ListPV)):ListTmpLine.append("listPvConnect.append('"+ListPV[i]+".VAL')\n")

##### Creation of the test connection loop
ListTmpLine.append("\n# Loop to test connection of all PV\n")
ListTmpLine.append("for i in range(len(listPvConnect)): \n\tif caget(listPvConnect[i]) ==  None : listPvDisconnect.append(\"'\"+listPvConnect[i]+\"'\")")

##### Concatenation of all ligne in only one line
LineScriptConnect="".join(ListTmpLine)

##### Detection of the party where you will put all tests
FinalScriptFile = open(scriptFileName, 'r+')
text = FinalScriptFile.read()
tag = ">>>>>>>>>>CONNECTION_SCRIPT<<<<<<<<<<"
IndexTag = text.index(tag)

##### moving the crusor to the good index
FinalScriptFile.seek(IndexTag)

##### Write script lines at the index position
FinalScriptFile.write(LineScriptConnect)

##### Writing the end of the file
FinalScriptFile.write(text[IndexTag+len(tag):])


################################################################
########### Adding generic script for each line ############
################################################################

#####  clearing the list
ListTmpLine = []

#####  Detection of the party where you will put all tests
FinalScriptFile = open(scriptFileName, 'r+')
text = FinalScriptFile.read()
tag = ">>>>>>>>>>UNITTEST_SCRIPT<<<<<<<<<<"
IndexTag = text.index(tag)

#####  moving the crusor to the good index
FinalScriptFile.seek(IndexTag)

#####  remplacing parameters with a template and a dictionnary
for line in range(1,len(ConfigFileArray)):
	FinalScriptFile.write("##################### Test line "+str(line)+" #########################\n")
	fichier = open("Modules/"+ConfigFileArray[1][7]+".py", "r" )
	ListTmpLine = "".join(fichier.readlines())
	lineScriptFInal=Template(ListTmpLine)
	dictMacroScriptFile['XX'] = line
	dictMacroScriptFile['CMD_PV'] = ConfigFileArray[line][0]
	dictMacroScriptFile['CMD_VAL'] = ConfigFileArray[line][1]
	dictMacroScriptFile['RDBK_PV'] = ConfigFileArray[line][2]
	dictMacroScriptFile['DELAY'] = ConfigFileArray[line][3]
	dictMacroScriptFile['RDBK_VAL'] = ConfigFileArray[line][4]
	dictMacroScriptFile['BANDWIDTH'] = ConfigFileArray[line][5]
	dictMacroScriptFile['SEVERITY'] = ConfigFileArray[line][6]
	dictMacroScriptFile['FAIL_MESS'] = ConfigFileArray[line][8]
	dictMacroScriptFile['SUCC_MESS'] = ConfigFileArray[line][9]
	dictMacroScriptFile['RESULT'] = ConfigFileArray[line][10]
	sizeTexte = len (lineScriptFInal.substitute(dictMacroScriptFile))
	FinalScriptFile.write(lineScriptFInal.substitute(dictMacroScriptFile))

#####  Writing the end of the file
FinalScriptFile.write(text[IndexTag+len(tag):])

FinalScriptFile.close()
