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
    if tag == 'Model':
        # Get the Model Name
        if hasattr(self,"optmenu1_opt"):
            if self.optmenu1_opt.winfo_exists():
                self.Compare['Model']['Model Name'] = self.optmenu1_opt.get()

        # Get the Reversible Model
        if hasattr(self,"optmenu2_opt"):
            if self.optmenu2_opt.winfo_exists():
                self.Compare['Model']['Reversible Model Name'] = self.optmenu2_opt.get() 

        # Get the Irreversible Model
        if hasattr(self,"optmenu3_opt"):
            if self.optmenu3_opt.winfo_exists():
                self.Compare['Model']['Irreversible Model Name'] = self.optmenu3_opt.get() 

        # Get the Viscoelastic Mechanisms
        if hasattr(self,"optmenu4_opt"):
            if self.optmenu4_opt.winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare['Model']['M'] = self.optmenu4_opt.get()

        # Get the Viscoelastic Parameters
        if hasattr(self,'sheet1_opt'):
            if self.sheet1_opt.winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare['Model']['VE_Param'] = self.sheet1_opt.data
                    
        # Get the Viscoplastic Mechanisms
        if hasattr(self,"optmenu5_opt"):
            if self.optmenu5_opt.winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare['Model']['N'] = self.optmenu5_opt.get() 

        # Get the Viscoplastic Parameters
        if hasattr(self,'sheet2_opt'):
            if self.sheet2_opt.winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare['Model']['VP_Param'] = self.sheet2_opt.data

    elif tag == 'Analysis':
        # Get the Model Name
        if hasattr(self,"optmenu1_analy"):
            if self.optmenu1_analy.winfo_exists():
                self.Compare['Analysis']['Model Name'] = self.optmenu1_analy.get()

        # Get the Reversible Model
        if hasattr(self,"optmenu2_analy"):
            if self.optmenu2_analy.winfo_exists():
                self.Compare['Analysis']['Reversible Model Name'] = self.optmenu2_analy.get() 

        # Get the Irreversible Model
        if hasattr(self,"optmenu3_analy"):
            if self.optmenu3_analy.winfo_exists():
                self.Compare['Analysis']['Irreversible Model Name'] = self.optmenu3_analy.get() 

        # Get the Viscoelastic Mechanisms
        if hasattr(self,"optmenu4_analy"):
            if self.optmenu4_analy.winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare['Analysis']['M'] = self.optmenu4_analy.get()

        # Get the Viscoelastic Parameters
        if hasattr(self,'sheet1_analy'):
            if self.sheet1_analy.winfo_exists():
                if opt == 1 or opt == 3:
                    self.Compare['Analysis']['VE_Param'] = self.sheet1_analy.data
                    
        # Get the Viscoplastic Mechanisms
        if hasattr(self,"optmenu5_analy"):
            if self.optmenu5_analy.winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare['Analysis']['N'] = self.optmenu5_analy.get() 

        # Get the Viscoplastic Parameters
        if hasattr(self,'sheet2_analy'):
            if self.sheet2_analy.winfo_exists():
                if opt == 2 or opt == 3:
                    self.Compare['Analysis']['VP_Param'] = self.sheet2_analy.data