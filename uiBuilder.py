import fileMgr as fM
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pubsub import pub
import pprint
import configVerif as cv
import conversion as con

class simulatorWindow:
	
	def __init__(self, parent, configDict):
		self.parent = parent
		self.configDict = configDict
		self.PGUDict = fM.get_PGUDict(configDict)
		self.simDetails = fM.get_simDetails(configDict)
		self.mainFrame = None
		self.initData = None

	'''
    	Name:   initMainSimWindow
    	Desc:   initialize main window by bulind main composition frame and calling builder functions.  
    	Param:  Class variables: parent and PGUDict
    	Return: None
    	Ref: 	Event binding to allow a click anywhere in the UI to de-focus the entry is based off 
    			information found at the following link:
				https://stackoverflow.com/questions/24072567/remove-focus-from-entry-widget/24072653#24072653
	'''
	def initMainSimWindow(self):
		self.parent.title("J1939 Simulator")
		
		self.mainFrame = ttk.Frame(self.parent, padding=(10,10))
		self.mainFrame.pack()
		
		if cv.verifPGN(fM.get_PGUDict(self.configDict)):
			titleFont = tkFont.Font(family="Helvetica",size=36,weight="bold")
			self.titleFrame = ttk.Frame(self.mainFrame, padding=(30,0))
			ttk.Label(self.titleFrame, text='J1939 Simulator Sender', font = titleFont).pack(expand=1, fill=tk.X)
			self.titleFrame.pack()
			self.parent.bind_all("<1>", lambda event:event.widget.focus_set())
			self.__SimTitle()
			self.__BuildPGURows()
			self.__BuildStopStart()
		else:
			titleFont = tkFont.Font(family="Helvetica",size=18,weight="bold")
			self.titleFrame = ttk.Frame(self.mainFrame, padding=(30,0))
			ttk.Label(self.titleFrame, text='Configuration file error, please check error log.', font = titleFont).pack(expand=1, fill=tk.X)
			self.titleFrame.pack()
		


	'''
	    Name: 	SimTitle  
	    Desc: 	Add the user selected short description to th UI   
	    Param:  None
	    Return: None
	'''
	def __SimTitle(self):
		titleFont = tkFont.Font(family="Helvetica",size=16,weight="bold")
		
		titleFrame = ttk.Frame(self.mainFrame, padding=(5,5))
		titleFrame.pack()
		
		titleValLbl = ttk.Label(self.mainFrame, text= self.simDetails["title"], font= titleFont, padding=(30,10))
		titleValLbl.config(anchor="center")
		titleValLbl.pack()


	'''
    	Name: 	BuildPGURows   
	    Desc: 	Loops through PGUDict to build PGU frames and calls SPN bulder  
	    Param:  Class variables: parent and PGUDict
	    Return: None
	'''
	def __BuildPGURows(self):
		lblFrmFont = tkFont.Font(family="Helvetica",size=10)
		self.__initSimMsg(self.PGUDict)
		for PGNKey in self.PGUDict.keys():
			if self.PGUDict[PGNKey]["simVisible"] == True:
				PGUFrame = tk.LabelFrame(self.mainFrame, text= self.PGUDict[PGNKey]["Label"] + " - " + str(self.PGUDict[PGNKey]["id"]), font=lblFrmFont)
				PGUFrame.pack()
				self.__BuildSPNs(self.PGUDict[PGNKey], PGUFrame)


	'''
    	Name:  	BuildSPNs 
    	Desc:  	Builds the individual SPN widgets, which are cunstructed from a human 
    			readable value and a set of buttons for changeing the value by calling 
    			a function to build the value and another to build the buttons. 
    	Param:  PGU - dictonary object contians PGU and SPN data, 
    			PGUFrame - tkinter frame to contian PGU
    	Return: None
	'''
	def __BuildSPNs(self, PGU, PGUFrame):
		lblFrmFont = tkFont.Font(family="Helvetica",size=10)
		for SPNkey in PGU["SPNDict"].keys():
			if PGU["SPNDict"][SPNkey]["simVisible"] == True:
				SPNFrame = tk.LabelFrame(PGUFrame, text=  PGU["SPNDict"][SPNkey]["Label"] + " - " + str(SPNkey), font=lblFrmFont)
				SPNFrame.pack(padx=5, pady=10, side=tk.LEFT, fill=tk.Y)
				self.__BuildParamValue(PGU["SPNDict"][SPNkey], SPNFrame)
				self.__BuildModEntry(PGU["SPNDict"][SPNkey], SPNFrame, PGU)


	'''
    	Name:  	BuildParamValue 
	    Desc:   Initializes the display value and stores the widget object for future modification.  
    	Param:  SPN - dictonary object contians SPN data, 
    			SPNFrame - tkinter frame to contain SPN
    	Return: None
	'''
	def __BuildParamValue(self, SPN, SPNFrame):
		valueFont = tkFont.Font(family="Helvetica",size=18,weight="bold")
		valueFrame = ttk.Frame(SPNFrame, padding=(20,5))
		valueFrame.pack()
		dispVal = self.__initDispVal(SPN)
		SPN["UI_Objects"]["dispValLbl"] = ttk.Label(SPNFrame, text= dispVal, font= valueFont)
		SPN["UI_Objects"]["dispValLbl"].config(anchor="center")
		SPN["UI_Objects"]["dispValLbl"].pack()


	'''
    	Name:  	initDispVal 
	    Desc:   Initializes diplay valu formated string.  
    	Param:  SPN - dictonary object contians SPN data 
    	Return: None
	'''
	def __initDispVal(self, SPN):	
		temp = {"UI_Objects": {"currentVal": SPN["initialValue"]}} 
		SPN.update(temp)
		return str(SPN["initialValue"]) + ' ' + SPN["unit"]


	'''
		Name:  	updateDispVal 
	    Desc:   Initializes diplay valu formated string.  
    	Param:  SPN - dictonary object contians SPN data 
    	Return: None
	'''
	def __updateDispVal(self, SPN, val):
		SPN["UI_Objects"]["currentVal"] = float(val)
		return str(val) + ' ' + SPN["unit"]


	'''
    	Name: 	BuildModEntry
    	Desc:   Creates the SPN modifier entry window in the SPN widget
    	Param:  SPN - dictonary object contians SPN data,
    			SPNFrame - tkinter frame to contain SPN,
    			PGU - dictonary object contians PGU data
    	Return: None
	'''	
	def __BuildModEntry(self, SPN, SPNFrame, PGU):
		if SPN["simMutable"] == True:
			modFont = tkFont.Font(family="Helvetica",size=14,weight="bold")
			entryframe= ttk.Frame(SPNFrame, padding=(5,5))
			entryframe.pack()
			SPN["UI_Objects"]["entryVal"] = tk.StringVar()
			SPN["UI_Objects"]["entry"] = tk.Entry(entryframe, textvariable=SPN["UI_Objects"]["entryVal"])
			SPN["UI_Objects"]["entry"].grid(row=1, column=1, sticky="ew")
			SPN["UI_Objects"]["entry"].bind("<1>", lambda event: self.__EntryUpdateBinding(SPN, SPNFrame, PGU))


	'''
    	Name: 	EntryUpdateBinding
    	Desc:   Creates the SPN modifier entry event bindings
    	Param:  SPN - dictonary object contians SPN data,
    			SPNFrame - tkinter frame to contain SPN,
    			PGU - dictonary object contians PGU data
    	Return: None
	'''	
	def __EntryUpdateBinding(self, SPN, SPNFrame, PGU):
		SPN["UI_Objects"]["entry"].config(foreground='black')
		SPNFrame.configure(bd=4)
		SPN["UI_Objects"]["entry"].bind("<Return>", lambda event: self.parent.focus_set())
		SPN["UI_Objects"]["entry"].bind("<FocusOut>", lambda event: self.__EntryUpdateAccept(SPN, SPNFrame, PGU))


	'''
    	Name: 	EntryUpdateAccept
    	Desc:   Verifies user entry and provides feedback in the case of invalid entry. 
    	Param:  SPN - dictonary object contians SPN data,
    			SPNFrame - tkinter frame to contain SPN,
    			PGU - dictonary object contians PGU data
    	Return: None
	'''	
	def __EntryUpdateAccept(self, SPN, SPNFrame, PGU):
		SPNFrame.configure(bd=2)
		newEntry = SPN["UI_Objects"]["entry"].get()
		
		if con.StrIsFloat(newEntry) and float(newEntry) >= SPN["loLimit"] and float(newEntry) <= SPN["hiLimit"]:
			SPN["UI_Objects"]["currentVal"] = float(newEntry)				
			if SPN["resolution"] < 1:
				newEntry = round(float(newEntry), 2)										
			newEntry = str(newEntry)  + ' ' + SPN["unit"]
			SPN["UI_Objects"]["dispValLbl"].config(text=newEntry)
			self.__SPNUpdateMsg(PGU, SPN, SPN["UI_Objects"]["currentVal"])
			SPN["UI_Objects"]["entry"].delete(0, 'end')
		else:
			SPN["UI_Objects"]["entry"].config(foreground='red')


	'''
	    Name: BuildStopStart  
	    Desc: Create the start and stop simulation buttons in the mainFrame of the UI   
	    Param:  None
	    Return: None
	'''
	def __BuildStopStart(self):
		startstopFont = tkFont.Font(family="Helvetica",size=14,weight="bold")
		
		buttonFrame = ttk.Frame(self.mainFrame, padding=(5,5))
		buttonFrame.pack()

		startStopBtn = tk.Button(buttonFrame, text="START", command= lambda: self.__StartSim(startStopBtn), font= buttonFrame, activebackground= 'green', background= 'green', width= 5)
		startStopBtn.grid(row=1, column=1, sticky="ew")
		

	'''
	    Name: StartSim  
	    Desc: 
	    Param:  None
	    Return: None
	'''
	def __StartSim(self, startStopBtn):
		startStopBtn.config(text= "STOP")
		startStopBtn.config(background= 'red', activebackground= 'red')
		startStopBtn.config(command= lambda: self.__StopSim(startStopBtn))
		self.__StartSimMsg


	'''
	    Name: StartSim  
	    Desc: 
	    Param:  None
	    Return: None
	'''
	def __StopSim(self, startStopBtn):
		startStopBtn.config(text= "START")
		startStopBtn.config(background= 'green', activebackground= 'green')
		startStopBtn.config(command= lambda: self.__StartSim(startStopBtn))
		self.__StopSimMsg


	'''
	    Name: 	StartSim  
	    Desc:   Passes a message down to start the sender
	    Param:  None
	    Return: None
	'''
	def __StartSimMsg(self):
		message = dict(status="start")
		pub.sendMessage('BusStatus', payload=message)


	'''
	    Name: 	StopSim
	    Desc:   Passes a message down to stop the sender 
	    Param:  None
	    Return: None
	'''
	def __StopSimMsg(self):
		message = dict(status="stop")
		pub.sendMessage('BusStatus', payload=message)


	'''
	    Name: 	UpdateDictComposer
	    Desc:   Builds update message with new value to pub/sub to builder layer
	    Param:  SPN - dictonary object contians SPN data, 
	    		PGU - dictonary object contians PGU data,
	    		newValue - new SPN value to be updated
	    Return: tempDict - a formatted and filtered update dictonary
	    Ref: https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression-in-python-taking-union-o
	'''
	def __UpdateDictComposer(self, PGU, SPN, newValue):
		PGNMsg = self.__PGNDictComposer(PGU)
		SPNMsg = self.__SPNDictComposer(SPN, newValue)
		SPNArry = {"SPNArry": [SPNMsg['SPN']]}
		tempDict = {**PGNMsg, **SPNArry}
		return tempDict


	'''
	    Name: 	PGNDictComposer
	    Desc:   Builds PGN protion of the update message to pub/sub to builder layer
	    Param:  PGU - dictonary object contians PGU data,
	    Return: {"PGN": filteredDict} - a formatted and filtered PGN portion of the update dictonary
	'''
	def __PGNDictComposer(self, PGU):
		filterSet = ["id","priority","dp","sa","rate"]
		filteredDict = {}
		
		for k,v in PGU.items():
			if k in filterSet:
				filteredDict[k] = v

		return {"PGN": filteredDict}
	

	'''
	    Name: 	SPNDictComposer
	    Desc:   Builds SPN protion of the update message to pub/sub to builder layer
	    Param:  SPN - dictonary object contians SPN data,
	    Return: {"SON": filteredDict} - a formatted and filtered SPN portion of the update dictonary
	'''
	def __SPNDictComposer(self, SPN, currentVal = None):
		filterSet = ["id","dataLngth","resolution","offset","startBit"]
		filteredDict = {}
		
		for k,v in SPN.items():
			if k in filterSet:
				filteredDict[k] = v
		
		if currentVal == None:
			filteredDict["currentVal"] = con.MetricToRaw(float(SPN["initialValue"]), SPN["resolution"], SPN["offset"])
		else:	
			filteredDict["currentVal"] = con.MetricToRaw(float(currentVal), SPN["resolution"], SPN["offset"]) 
			
		return {"SPN": filteredDict}


	'''
	    Name: 	SPNUpdateMsg
	    Desc:   Passes a message down to update a specific SPN 
	    Param:  SPN - dictonary object contians SPN data, 
	    		PGU - dictonary object contians PGU data,
	    		newValue - new SPN value to be updated
	    Return: None
	'''
	def __SPNUpdateMsg(self, PGU, SPN, newValue):
		message = self.__UpdateDictComposer(PGU, SPN, newValue)
		pub.sendMessage('SPNValueUpdate', payload=message)


	'''
	    Name: 	intDictComposer
	    Desc:   Builds init message with new value to pub/sub to builder layer
	    Param:  PGUDict - dictonary object contianing all PGU data
	    Return: initData - a formatted and filtered initialization dictonary
	    		[{spn:{}, pgn[]}, {spn:{}, pgn[]}]
				An array of dictionaries that each contain the PGN dict and an array of SPN discts
	'''
	def __intDictComposer(self, PGUDict):
		initData = [] 
		for PGNKey in self.PGUDict.keys():
			temp = self.__PGNDictComposer(PGUDict[PGNKey])
			temp["SPNArry"] = []
			for SPNKey in PGUDict[PGNKey]["SPNDict"].keys():
				tmpSPN = self.__SPNDictComposer(PGUDict[PGNKey]["SPNDict"][SPNKey])
				temp["SPNArry"].append(tmpSPN['SPN'])
			initData.append(temp)	
		return initData


	'''
	    Name: 	initSimMsg
	    Desc:   Passes a message down to initialize a specific SPN    
	    Param:  PGUDict - dictonary object contianing all PGU data
	    Return: None
	'''
	def __initSimMsg(self, PGUDict):
		message = self.__intDictComposer(PGUDict)
		pub.sendMessage('initSim', payload=message)