#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# UpdateModelData.py
#
# PURPOSE: Update the model data from the Optimize Model or Analysis Page
#
# INPUTS: 
#   event   Placeholder for if an event triggers the function call 
#   self    GUI Data structure
#   opt     Option for what data to update
#               1 - Viscoelastic parameters only
#               2 - Viscoplastic parameters only
#               3 - All parameters
#   tag     Indicator if model data is from the Optimize or Analyze structure
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def UpdateModelData(event, self, opt, tag):

    # Check for existing data structure
    if tag not in list(self.Compare.keys()):
        self.Compare[tag] = {}

    # Get the model
    if hasattr(self,"opt1"):
        # Get the Model Name
        if hasattr(self,"optmenu1"):
            if self.optmenu1.winfo_exists():
                self.Compare[tag]['Model Name'] = self.optmenu1.get()

        # Get the Reversible Model
        if hasattr(self,"optmenu2"):
            if self.optmenu2.winfo_exists():
                self.Compare[tag]['Reversible Model Name'] = self.optmenu2.get() 

        # Get the Irreversible Model
        if hasattr(self,"optmenu3"):
            if self.optmenu3.winfo_exists():
                self.Compare[tag]['Irreversible Model Name'] = self.optmenu3.get() 

        # Get the Viscoelastic Mechanisms
        if hasattr(self,"optmenu4"):
            if self.optmenu4.winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare[tag]['M'] = self.optmenu4.get()

        # Set the model parameter sheet names
        if tag == 'Model':
            s1 = 'sheet1'
            s1val = 'self.sheet1'
            s2 = 'sheet2'
            s2val = 'self.sheet2'
        else:
            s1 = 'sheet_anly1'
            s1val = 'self.sheet_anly1'
            s2 = 'sheet_anly2'
            s2val = 'self.sheet_anly2'

        # Get the Viscoelastic Parameters
        if hasattr(self,s1):
            if eval(s1val).winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare[tag]['VE_Param'] = eval(s1val).data
                    
        # Get the Viscoplastic Mechanisms
        if hasattr(self,"optmenu5"):
            if self.optmenu5.winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare[tag]['N'] = self.optmenu5.get() 

        # Get the Viscoplastic Parameters
        if hasattr(self,s2):
            if eval(s2val).winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare[tag]['VP_Param'] = eval(s2val).data