import fileMgr as fM
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from pubsub import pub
from pprint import pprint
from tkinter import filedialog 
import os
import configVerif as cv
import decimal

class simulatorWindow:
	
	def __init__(self, parent):
		self.parent = parent
		self.configDict = None
		self.PGUDict = None
		self.simDetails = None
		self.mainFrame = None
		self.initData = None
		self.isLogging = None
		self.logPath = None

	'''
    	Name:   initMainSimWindow
    	Desc:   initialize main window by building main composition frame and calling config explorer function.  
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
		
		titleFont = tkFont.Font(family="Helvetica",size=36,weight="bold")
		self.titleFrame = ttk.Frame(self.mainFrame, padding=(30,0))
		ttk.Label(self.titleFrame, text='J1939 Simulator Receiver', font = titleFont).pack(expand=1, fill=tk.X)
		self.titleFrame.pack()
		

		buttonFont = tkFont.Font(size=14,weight="bold")
		self.buttonFrame = ttk.Frame(self.mainFrame, padding=(100,40))
		self.configButton = tk.Button(self.buttonFrame, text = "Choose Configuration File", font = buttonFont, command= lambda: self.__BrowseConfig(self.mainFrame, self.configButton))
		self.configButton.pack()
		self.buttonFrame.pack()




	'''
	    Name: 	__BrowseConfig 
	    Desc: 	Creates file explorer for user to select config file.
    	Param:  mainFrame - tkinter frame to contain the window frame, 
    			configButton - tkinter button object
	    Return: None
	    Ref: https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
	'''
	def __BrowseConfig(self, mainFrame, configButton):
		configFileName = filedialog.askopenfilename(initialdir = os.getcwd() + '/config', title = "Select a Configuration File", filetypes = [("JSON files", "*.json")])
		if configFileName:
			self.configDict = fM.OpenConfigFile(configFileName)
			self.PGUDict = fM.get_PGUDict(self.configDict)
			self.simDetails = fM.get_simDetails(self.configDict)
			self.buttonFrame.destroy()
			self.__ChooseLogging(mainFrame)

	'''
	    Name: 	__ChooseLogging 
	    Desc: 	Builds propmt for user to select logging during session
	    Param:  mainFrame - tkinter frame to contain the window frame
	    Return: None 
	'''
	def __ChooseLogging(self, mainFrame):
		titleFont = tkFont.Font(family="Helvetica",size=14)
		self.promptFrame = ttk.Frame(self.mainFrame, padding=(30,20))
		ttk.Label(self.promptFrame, text='Would you like to store the results of this session?', font = titleFont).pack(expand=1, fill=tk.X)
		
		buttonFont = tkFont.Font(size=14,weight="bold")
		self.buttonFrame = ttk.Frame(self.promptFrame, padding=(0,10))
		self.yesButton = tk.Button(self.buttonFrame, text = "Yes", font = buttonFont, command= lambda: self.__YesLogging(self.mainFrame, self.promptFrame))
		self.yesButton.grid(row=1, column=1, sticky="ew", padx = 5)
		self.noButton = tk.Button(self.buttonFrame, text = "No", font = buttonFont, command= lambda: self.__NoLogging(self.mainFrame, self.promptFrame))
		self.noButton.grid(row=1, column=2, sticky="ew", padx = 5)
		
		self.buttonFrame.pack()
		self.promptFrame.pack()
	'''
	    Name: 	__YesLogging	 
	    Desc: 	Calls logging file path eplorer and hands down the logging request to lower layer 
	    Param:  mainFrame - tkinter frame to contain the window frame,
	    		promptFrame - tkinter frame to contain the prompt
	    Return: None
	'''
	def __YesLogging(self, mainFrame, promptFrame):
		logFileName = filedialog.asksaveasfilename(initialdir = os.getcwd(), title = "SAVE LOG AS", filetypes = [("ASC File", "*.asc")])
		if logFileName:
			self.isLogging = True
			self.logPath = logFileName
			self.promptFrame.destroy()
			self.__PopulateSim(mainFrame)

	'''
	    Name: 	__NoLogging 
	    Desc: 	Clears window to load main UIand  hands down the logging request to lower layer 
	    Param:  mainFrame - tkinter frame to contain the window frame,
	    		promptFrame - tkinter frame to contain the prompt
	    Return: None
	    Ref: 
	'''
	def __NoLogging(self, mainFrame, promptFrame):
			self.isLogging = False
			self.logPath = ""
			self.promptFrame.destroy()
			self.__PopulateSim(mainFrame)

	'''
	    Name: 	__PopulateSim 
	    Desc: 	initialize main window by building main composition frame and calling builder functions.
	    Param:  mainFrame - tkinter frame to contain the window frame 
	    Return: None
	'''
	def __PopulateSim(self, mainFrame):
		if cv.verifPGN(fM.get_PGUDict(self.configDict)):
			self.parent.bind_all("<1>", lambda event:event.widget.focus_set())
			self.__SimTitle()
			self.__BuildPGURows()
			self.__BuildStopStart()
			pub.subscribe(self.__UpdateValue, "UpdateValue")

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
		temp = {"UI_Objects": {}} 
		SPN.update(temp)
		return str("-- " + SPN["unit"])


	'''
		Name:  	updateDispVal 
	    Desc:   Initializes diplay valu formated string.  
    	Param:  SPN - dictonary object contians SPN data 
    	Return: None
	'''
	def __updateDispVal(self, SPN, val):
		SPN["UI_Objects"]["dispValLbl"].config(text=val)
		return str(val) + ' ' + SPN["unit"]


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
	    Desc: Sets button appearance for start stop button in the start mode
	    Param:  startStopBtn tkinter button object
	    Return: None
	'''
	def __StartSim(self, startStopBtn):
		startStopBtn.config(text= "STOP")
		startStopBtn.config(background= 'red', activebackground= 'red')
		startStopBtn.config(command= lambda: self.__StopSim(startStopBtn))
		self.__StartSimMsg()


	'''
	    Name: StartSim  
	    Desc: Sets button appearance for start stop button in the stop mode
	    Param:  startStopBtn tkinter button object
	    Return: None
	'''
	def __StopSim(self, startStopBtn):
		startStopBtn.config(text= "START")
		startStopBtn.config(background= 'green', activebackground= 'green')
		startStopBtn.config(command= lambda: self.__StartSim(startStopBtn))
		self.__StopSimMsg()


	'''
	    Name: 	StartSim  
	    Desc:   Passes a message down to start the sender
	    Param:  None
	    Return: None
	'''
	def __StartSimMsg(self):
		message = dict([("status", "start"), ("logging", self.isLogging), ("loggingFileName",self.logPath)])
		pub.sendMessage('ReceiverConfig', payload=message)
	

	'''
	    Name: 	StopSim
	    Desc:   Passes a message down to stop the sender 
	    Param:  None
	    Return: None
	'''
	def __StopSimMsg(self):
		message = dict([("status", "stop"), ("logging", False), ("loggingFileName","")])
		pub.sendMessage('ReceiverConfig', payload=message)


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
		filterSet = ["id","Label","simVisible","sa"]
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
	def __SPNDictComposer(self, SPN,):
		filterSet = ["Label","simVisible","id","dataLngth","resolution","offset","startBit", "unit"]
		filteredDict = {}
		
		for k,v in SPN.items():
			if k in filterSet:
				filteredDict[k] = v
		
		return {"SPN": filteredDict}


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
		#pprint(message)
		pub.sendMessage('InitRead', payload=message)


	'''
	    Name: 	UpdateValue
	    Desc:   Passes a message down to initialize a specific SPN    
	    Param:  PGUDict - dictonary object contianing all PGU data
	    Return: None
	'''
	def __UpdateValue(self, payload=None):
		PGN = payload["PGN"]["id"]
		SPNDict = self.PGUDict[str(PGN)]["SPNDict"]
		for SPN in payload['SPNArry']:
			newVal = '{:f}'.format(decimal.Decimal(SPN["currentVal"]).normalize())
			SPNDict[str(SPN['id'])]["UI_Objects"]["dispValLbl"].config(text=str(newVal))