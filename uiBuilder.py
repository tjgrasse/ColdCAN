import fileMgr as fM
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import dispFmat as dF 



class simulatorWindow:
	
	def __init__(self, parent, configDict):
		self.parent = parent
		self.PGUDict = fM.get_PGUDict(configDict)
		self.simDetails = fM.get_simDetails(configDict)
		self.mainFrame = None

	'''
    	Name:   initMainSimWindow
    	Desc:   initialize main window by bulind main composition frame and calling builder functions.  
    	Param:  Class variables: parent and PGUDict
    	Return: None
	'''
	def initMainSimWindow(self):
		self.parent.title("J1939 Simulator")

		self.mainFrame = ttk.Frame(self.parent, padding=(10,10))
		self.mainFrame.pack()

		titleFont = tkFont.Font(family="Helvetica",size=36,weight="bold")
		self.titleFrame = ttk.Frame(self.mainFrame, padding=(30,0))
		self.titleFrame.pack()
		
		ttk.Label(self.titleFrame, text='J1939 Simulator Sender', font = titleFont).pack(expand=1, fill=tk.X)
		
		self.SimTitle()
		self.BuildPGURows()
		self.BuildStopStart()
		
		#TODO FUTURE CONFIGURATION HERE


	'''
	    Name: 	SimTitle  
	    Desc: 	Add the user selected short description to th UI   
	    Param:  None
	    Return: None
	'''
	def SimTitle(self):
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
	def BuildPGURows(self):
		lblFrmFont = tkFont.Font(family="Helvetica",size=10)
		
		for PGNKey in self.PGUDict.keys():
			if self.PGUDict[PGNKey]["simVisible"] == True:
				PGUFrame = tk.LabelFrame(self.mainFrame, text= self.PGUDict[PGNKey]["Label"] + " - " + str(self.PGUDict[PGNKey]["PGN"]), font=lblFrmFont)
				PGUFrame.pack()
				self.BuildSPNs(self.PGUDict[PGNKey], PGUFrame)


	'''
    	Name:  	BuildSPNs 
    	Desc:  	Builds the individual SPN widgets, which are cunstructed from a human 
    			readable value and a set of buttons for changeing the value by calling 
    			a function to build the value and another to build the buttons. 
    	Param:  PGU dictonary, PGUFrame tkinter frame
    	Return: None
	'''
	def BuildSPNs(self, PGU, PGUFrame):
		lblFrmFont = tkFont.Font(family="Helvetica",size=10)
		
		for SPNkey in PGU["SPNDict"].keys():
			if PGU["SPNDict"][SPNkey]["simVisible"] == True:
				SPNFrame = tk.LabelFrame(PGUFrame, text=  PGU["SPNDict"][SPNkey]["Label"] + " - " + str(SPNkey), font=lblFrmFont)
				SPNFrame.pack(padx=5, pady=10, side=tk.LEFT, fill=tk.Y)
				self.BuildParamValue(PGU["SPNDict"][SPNkey], SPNFrame)
				self.BuildModButtons(PGU["SPNDict"][SPNkey], SPNFrame, PGU)


	'''
    	Name:  	BuildParamValue 
	    Desc:   Initializes and updates the display value and stores the widget object for future modification.  
    	Param:  SPN, SPNFrame, SPNvalue= None
    	Return: None
	'''
	#TODO this need to be broken into an initialization and an update function. 
	def BuildParamValue(self, SPN, SPNFrame, SPNvalue= None):
		valueFont = tkFont.Font(family="Helvetica",size=18,weight="bold")
		valueFrame = ttk.Frame(SPNFrame, padding=(20,5))
		valueFrame.pack()
		dispVal = self.dispValFmat(SPN, SPNvalue)
		SPN["UI_Objects"]["dispValLbl"] = ttk.Label(SPNFrame, text= dispVal, font= valueFont)
		SPN["UI_Objects"]["dispValLbl"].config(anchor="center")
		SPN["UI_Objects"]["dispValLbl"].pack()


	'''
    	Name:  	BuildParamValue 
	    Desc:   Initializes and updates the display value and stores the widget object for future modification.  
    	Param:  SPN, SPNFrame, SPNvalue= None
    	Return: None
	'''
	#TODO this need to be broken into an initialization and an update function. 
	def dispValFmat(self, SPN, val):
		if val != None:
			rawVal = val 
		else:
			rawVal = SPN["initialValue"]

		if "UI_Objects" in SPN.keys():
			SPN["UI_Objects"]["currentVal"] = rawVal			#TODO this is ugly, FIX
		else:	
			temp = {"UI_Objects": {"currentVal": rawVal}} 
			SPN.update(temp)
		
		offsetVal = rawVal + SPN["offset"]
		factoredVal = offsetVal * SPN["resolution"]

		return str(factoredVal) + ' ' + SPN["unit"]


	'''
    	Name: 	BuildModButtons  
    	Desc:   Creates the SPN modifier buttons in the SPN widget
    	Param:  PN, SPNFrame, PGU
    	Return: None
	'''	
	def BuildModButtons(self, SPN, SPNFrame, PGU):
		if SPN["simMutable"] == True:
			modFont = tkFont.Font(family="Helvetica",size=14,weight="bold")
			
			buttonFrame = ttk.Frame(SPNFrame, padding=(5,5))
			buttonFrame.pack()
		
			decButton= tk.Button(buttonFrame, text="-", command= lambda: self.DecButtonUpdate(SPN, buttonFrame, PGU), font= modFont)
			decButton.grid(row=1, column=1, sticky="ew")
			
			incButton= tk.Button(buttonFrame, text="+", command= lambda: self.IncButtonUpdate(SPN, buttonFrame, PGU), font= modFont)
			incButton.grid(row=1, column=2, sticky="ew")


	'''
	    Name: BuildStopStart  
	    Desc: Create the start and stop simulation buttons in the mainFrame of the UI   
	    Param:  None
	    Return: None
	'''
	def BuildStopStart(self):
		startstopFont = tkFont.Font(family="Helvetica",size=14,weight="bold")
		
		buttonFrame = ttk.Frame(self.mainFrame, padding=(5,5))
		buttonFrame.pack()
		
		startButton= tk.Button(buttonFrame, text="START", command= self.StartSim, font= buttonFrame)
		startButton.grid(row=1, column=1, sticky="ew")
		
		stopButton= tk.Button(buttonFrame, text="STOP", command= self.StopSim, font= buttonFrame)
		stopButton.grid(row=1, column=2, sticky="ew")


	'''
	    Name:   IncButtonUpdate
	    Desc:   Increments and updates the current value of the SPN 
	    Param:  SPN, buttonFrame, PGU
	    Return: None
	'''
	def IncButtonUpdate(self, SPN, buttonFrame, PGU):
		temp = SPN["UI_Objects"]["currentVal"] + 1
		if temp <= SPN["hiLimit"]:
			dispVal = self.dispValFmat(SPN, temp)
			SPN["UI_Objects"]["dispValLbl"].config(text=dispVal)
			SPN["UI_Objects"]["currentVal"] = temp


	'''
	    Name:   decButtonUpdate
	    Desc:   decrements and updates the current value of the SPN 
	    Param:  SPN, buttonFrame, PGU
	    Return: None
	'''
	def DecButtonUpdate(self, SPN, buttonFrame, PGU):
		temp = SPN["UI_Objects"]["currentVal"] - 1
		if temp >= SPN["loLimit"]:
			dispVal = self.dispValFmat(SPN, temp)
			SPN["UI_Objects"]["dispValLbl"].config(text=dispVal)
			SPN["UI_Objects"]["currentVal"] = temp


	'''
	    Name: 	StartSim  
	    Desc:   Passes a message down to start the sender
	    Param:  None
	    Return: None
	'''
	#TODO WEEK 4
	def StartSim():
		pass


	'''
	    Name: 	StopSim
	    Desc:   Passes a message down to stop the sender 
	    Param:  None
	    Return: 
	'''
	#TODO WEEK 4
	def StopSim():
		pass
