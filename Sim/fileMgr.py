import os
import json

'''
    Name:   FindConfigFiles
    Desc:   Searches "/config" for .json files
    Param:  None
    Return: Returns a list of paths
'''
def FindConfigFiles():
	files = []
	for configFile in os.listdir("config"):
		if configFile.endswith(".json"):
			files.append(configFile)
	return files

'''
    Name:   OpenConfigFile
    Desc:   Opens config file and converts json to a dictionary
    Param:  Name of file including extension
    Return: Returns dictonary object of config file 
'''
def OpenConfigFile(filePath):
	try:
		fileObj = open(filePath, 'r')
		configDict = json.loads(fileObj.read())
		return configDict
	except IOError as error:
		print(error)

'''
    Name:   get_simDetails
    Desc:   Retrives simDetails from the dictonary 
    Param:  configuration dictonary
    Return: Returns dictonary object of simDetails
'''
def get_simDetails(configDict):
	simDetails = configDict["simDetails"]
	return simDetails

'''
    Name:   get_NAME
    Desc:   Retrives NAME data from the dictonary 
    Param:  configuration dictonary
    Return: Returns dictonary object of NAME data
'''
def get_NAME(configDict):
	NAME = configDict["NAME"]
	return NAME

'''
    Name:   get_PGUDict 
    Desc:   Retrives PGU dictonary from the dictonary 
    Param:  configuration dictonary
    Return: Returns dictonary object of PGU dictonary 
'''
def get_PGUDict (configDict):
	PGUDict = configDict["PGUDict"]
	return PGUDict

'''
    Name:   get_SPNDict 
    Desc:   Retrives SPN dictonary from the dictonary 
    Param:  PGU dictonary
    Return: Returns dictonary object of SPN disctonary 
'''
def get_SPNDict (PGUDict):
	SPNDict = PGUDict["SPNDict"]
	return SPNDict


