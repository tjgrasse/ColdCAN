import fileMgr as fM
	
'''		
    Name: 	label
    Desc:   This function verifies that the label value is a string and less than 30 char
    Param:  obj -  either and SPN or PGN
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def label(obj, flag):
	label = obj["Label"]
	if ((type(label) == str) and (len(label) < 30)):
		return
	else:
		print("label value is incorrect for id " + str(obj['id']))
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
		print("simVisible value is incorrect for id" + str(obj['id']))
		flag[0] = False
		return


'''
    Name: 	rate
    Desc:   This function verifies that the rate value is within range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level
    Return: None
    ref: https://stackoverflow.com/questions/41609813/python-how-to-judge-whether-a-variable-is-boolean-type
'''
def rate(PGU, flag):
	rate = PGU["rate"]
	if rate > 0 and rate < 10000:			#TODO: determine spec max
		return
	else:
		print("rate value is incorrect for PGN " + str(PGU['id']))
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
	if dataLngth > 0 and dataLngth <= 64:
		return
	else:
		print("dataLngthvalue is incorrect for PGN/SPN " + str(obj['id']))
		flag[0] = False
		return


'''
    Name: 	dp
    Desc:   This function verifies that the dp value is bool
    Param:  PGU - PGU Dictonary
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def dp(PGU, flag):
	dp = PGU["dp"]
	if (dp == 1 or dp == 0):
			return
	else:
		print("dp value is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	PDUF
    Desc:   This function verifies that the PDUF value is in range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def PDUF(PGU, flag):
	PDUF = PGU["PDUF"]
	if PDUF >= 0 and PDUF <= 255:
		return
	else:
		print("PDUF value is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	PDUS
    Desc:   This function verifies that the PDUS value is in range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level
    Return: None
'''
def PDUS(PGU, flag):
	PDUS = PGU["PDUS"]
	if PDUS >= 0 and PDUS <= 255:
		return
	else:
		print("PDUS value is incorrect for PGN " + str(PGU['id']))
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
	if sa >= 0 and sa <= 255:
		return
	else:
		print("sa value is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	priority
    Desc:   This function verifies that the priority value is in range
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level    
    Return: None
'''
def priority(PGU, flag):
	priority = PGU["priority"]
	if priority >= 0 and priority <= 7:
		return
	else:
		print("priority value is incorrect for PGN " + str(PGU['id']))
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
	if PGN >= 0 and PGN <= 65535:
		return
	else:
		print("PGN value is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	PGUKeyCount
    Desc:   This function verifies that the PGUKeyCount is 11
    Param:  PGU -  PGU Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def PGUKeyCount(PGU, flag):
	if len(PGU) == 11:
		return
	else:
		print("PGU key count is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
		return


'''
    Name: 	SPNKeyCount
    Desc:   This function verifies that the SPNKeyCount is 13
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def SPNKeyCount(SPN, flag):
	if len(SPN) == 13:
		return
	else:
		print(len(SPN))
		print("SPN key count is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	simMutable
    Desc:   This function verifies that the simMutable is bool 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
    ref: https://stackoverflow.com/questions/41609813/python-how-to-judge-whether-a-variable-is-boolean-type
'''
def simMutable(SPN, flag):
	simMutable = SPN["simMutable"]
	if isinstance(simMutable, bool):
		return
	else:
		print("simMutable value is incorrect for SPN" + str(SPN['id']))
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
	if isinstance(resolution, int):									#TODO: determine spec range
		return
	else:
		print("resolution value is incorrect for SPN " + str(SPN['id']))
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
	resolution = SPN["resolution"]
	if isinstance(resolution, int):									#TODO: determine spec range
		return									
	else:
		print("resolution value is incorrect for SPN " + str(SPN['id']))
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
		print("startBit value is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	initialValue
    Desc:   This function verifies that the initialValue is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level   
    Return: None
'''
def initialValue(SPN, flag):
	initialValue = SPN["initialValue"]
	
	if initialValue >= SPN["loLimit"] and initialValue <= SPN["hiLimit"]:
		return
	else:
		print("initialValue value is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
		return


'''
    Name: 	loLimit
    Desc:   This function verifies that the loLimit is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level  
    Return: None
'''
def loLimit(SPN, flag):
	loLimit = SPN["loLimit"]
	
	if isinstance(loLimit, int):				#TODO: improve the logic to completely verify 
		return
	else:
		print("loLimit value is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
		return


'''
   	Name: 	hiLimit
    Desc:   This function verifies that the hiLimit is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level 
    Return: None
'''
def hiLimit(SPN, flag):
	hiLimit = SPN["hiLimit"]
	
	if isinstance(hiLimit, int):				#TODO: improve the logic to completely verify 
		return
	else:
		print("hiLimit value is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
		return


'''		
   	Name: 	typeSPN
    Desc:   This function verifies that the typeSPN is in range 
    Param:  SPN -  SPN Dictonary
			flag - a bool flag to transfer errors to the UI level 
    Return: None
'''
def typeSPN(SPN, flag):
	typeSPN = SPN["type"]
	if ((type(typeSPN) == str) and (len(typeSPN) < 30)):
		return
	else:
		print("type value is incorrect for SPN" + str(SPN['id']))
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
		print("unit value is incorrect for SPN" + str(SPN['id']))
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
	if SPNid >= 0 and SPNid <= 524287:
		return
	else:
		print("SPN value is incorrect for SPN " + str(SPN['id']))
		flag[0] = False
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
		rate(PGU, flag)
		dataLngth(PGU, flag)
		dp(PGU, flag)
		PDUF(PGU, flag)
		PDUS(PGU, flag)
		sa(PGU, flag)
		priority(PGU, flag)
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
		for k,v in SPNDict.items():
			SPN = SPNDict[k]
			SPNKeyCount(SPN, flag)
			label(SPN, flag)
			simVisible(SPN, flag)
			simMutable(SPN, flag)
			dataLngth(SPN, flag)
			resolution(SPN, flag)
			offset(SPN, flag)
			startBit(SPN, flag)
			initialValue(SPN, flag)
			loLimit(SPN, flag)
			hiLimit(SPN, flag)
			typeSPN(SPN, flag)
			unit(SPN, flag)
			spn(SPN, flag)
	except:
		print("SPNDict object is incorrect for PGN " + str(PGU['id']))
		flag[0] = False
