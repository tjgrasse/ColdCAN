import fileMgr as fM
import logging as log
import conversion as con
	
'''		
    Name: 	label
    Desc:   This function verifies that the label value is a string and less than 30 cha
    Param:  obj -  either and SPN or PGN
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def label(obj, flag):
	label = obj["Label"]
	if ((type(label) == str) and (len(label) < 30)):
		return
	else:
		log.error("label value is incorrect for id %s. Limit legth to 30 chars.", str(obj['id']))
		flag[0] = False
		return


'''
    Name: 	simVisible
    Desc:   This function verifies that the simVisible value is bool
    Param:  obj -  either and SPN or PGN
			flag - a bool flag to transfer errors to the UI level
    Return: None
    ref: https://stackoverflow.com/questions/41609813/python-how-to-judge-whether-a-variable-is-boolean-type
'''
def simVisible(obj, flag):
	simVisible = obj["simVisible"]
	if isinstance(simVisible, bool):
		return
	else:
		log.error("simVisible value is incorrect for id %s. Value should be bool.", str(obj['id']))
		flag[0] = False
		return


'''
    Name: 	dataLngth
    Desc:   This function verifies that the dataLngth value is within range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def dataLngth(obj, flag):
	dataLngth = obj["dataLngth"]
	if dataLngth > 0 and dataLngth <= 64 and isinstance(dataLngth, int):
		return
	else:
		log.error("dataLngthvalue is incorrect for PGN/SPN %s. Value should be bits between 1 - 64", str(obj['id']))
		flag[0] = False
		return


'''
    Name: 	sa
    Desc:   This function verifies that the sa value is in range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
'''
def sa(PGU, flag):
	sa = PGU["sa"]
	if sa >= 0 and sa <= 255 and isinstance(sa, int):
		return
	else:
		log.error("sa value is incorrect for PGN %s. Value should be between 0 - 255.", str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	PGN
    Desc:   This function verifies that the priority value is in range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def PGN(PGU, flag):
	PGN = PGU["id"]
	if PGN >= 0 and PGN <= 65535 and isinstance(PGN, int):
		return
	else:
		log.error("PGN value is incorrect for PGN %s. Value should be between 0 - 65535.", str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	PGUKeyCount
    Desc:   This function verifies that the PGUKeyCount is 5
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def PGUKeyCount(PGU, flag):
	if len(PGU) == 5:
		return
	else:
		log.error("PGU key count is incorrect for PGN %s. 5 entries should exist in the dictonary.", str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	SPNKeyCount
    Desc:   This function verifies that the SPNKeyCount is 8
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def SPNKeyCount(SPN, flag):
	if len(SPN) == 8:
		return
	else:
		log.error("SPN key count is incorrect for SPN %s. 8 entries should exist in the dictonary.", str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	resolution
    Desc:   This function verifies that the resolution is int 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level    
    Return: None
'''
def resolution(SPN, flag):
	resolution = SPN["resolution"]
	if isinstance(resolution, float):									
		return
	elif isinstance(resolution, int):									
		return
	else:
		log.error("resolution value is incorrect for SPN %s. Value should be float.", str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	offset
    Desc:   This function verifies that the offset is int 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
'''
def offset(SPN, flag):
	offset = SPN["offset"]
	if isinstance(offset, int):									
		return									
	else:
		log.error("offset value is incorrect for SPN %s. Value should be int.", str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	startBit
    Desc:   This function verifies that the startBit is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
'''
def startBit(SPN, flag):
	startBit = SPN["startBit"]
	if startBit >= 0 and startBit <= 63:
		return
	else:
		log.error("startBit value is incorrect for SPN %s. Value should be between 0 - 63.", str(SPN['id']))
		flag[0] = False
		return


'''		
   	Name: 	unit
    Desc:   This function verifies that the unit is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level 
    Return: None
'''
def unit(SPN, flag):
	unit = SPN["unit"]
	if ((type(unit) == str) and (len(unit) < 6)):
		return
	else:
		log.error("unit value is incorrect for SPN %s. Value should be string and 5 char max.", str(SPN['id']))
		flag[0] = False
		return


'''
   	Name: 	spn
    Desc:   This function verifies that the spn is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level 
    Return: None
'''
def spn(SPN, flag):
	SPNid = SPN["id"]
	if SPNid >= 0 and SPNid <= 524287 and isinstance(SPNid, int):
		return
	else:
		log.error("SPN value is incorrect for SPN %s. Value should be between 0 - 524287.", str(SPN['id']))
		flag[0] = False
		return


'''
   	Name: 	DataspaceCheck
    Desc:   Check to verify that each SPN uses a valid section of the PGN data frame. 
    Param:  SPN -  SPN Dictonary
    		bitAry - this is an array passed from the SPN check loop to represent each SPN's space in the frame. 
			flag - a bool flag to transfer errors to the UI level 
    Return: None
'''
def DataspaceCheck(SPN, bitAry, flag):
	maxDataSpace = 2**SPN["dataLngth"] - 1

	if sum(bitAry[SPN["startBit"]:SPN["startBit"] + SPN["dataLngth"]]) == 0:
		endBoundry = SPN["startBit"] + SPN["dataLngth"] + 1
		if endBoundry <= 65:
			bitAry[SPN["startBit"] : endBoundry] = [1] * SPN["dataLngth"]
		else:
			log.error("SPN overruns data space. SPN: %s.", str(SPN['id']))
			flag[0] = False
			return
	else:
		log.error("SPN %s coflicts with another SPN's data space.", str(SPN['id']))				
		flag[0] = False
		return

	return


'''		
   	Name: 	verifPGN
    Desc:   This function verifies that the entire PGNDict is properly formatted
    Param:  PGUDict -  entire PGU Dictonary
    Return: None
'''
def verifPGN(PGUDict):
	flag = [True]
	for k,v in PGUDict.items():
		PGU = PGUDict[k]
		PGUKeyCount(PGU, flag)
		label(PGU, flag)
		simVisible(PGU, flag)
		sa(PGU, flag)
		PGN(PGU, flag)
		SPNDict(PGU, flag)
	return flag[0]


'''
   	Name: 	SPNDict
    Desc:   This function verifies that the entire PGNDict is properly formatted
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
'''
def SPNDict(PGU, flag):
	try:
		SPNDict = PGU["SPNDict"]
		bitAry = [0] * 64
		for k,v in SPNDict.items():
			SPN = SPNDict[k]
			SPNKeyCount(SPN, flag)
			label(SPN, flag)
			simVisible(SPN, flag)
			dataLngth(SPN, flag)
			resolution(SPN, flag)
			offset(SPN, flag)
			startBit(SPN, flag)
			unit(SPN, flag)
			spn(SPN, flag)
			DataspaceCheck(SPN, bitAry, flag)
	except:
		log.error("SPNDict object is incorrect for PGN %s.", str(PGU['id']))
		flag[0] = False
