#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# BuildStartPage.py
#
# PURPOSE: Build the Gateway start page to load a project a create a new project
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def BuildStartPage(self,window):
    # Import Modules
    import tkinter as tk
    from tkinter import ttk

    # Preallocate the att list
    self.att_list = []

    # Create the frame
    self.frame1 = tk.Frame(
                            window, 
                            bd=3, 
                            relief="ridge", 
                            bg="white"
                            )
    self.frame1.place(
                    anchor = 'c', 
                    relx = self.Placement['Gateway']['MainFrame'][0], 
                    rely = self.Placement['Gateway']['MainFrame'][1],
                    relwidth = self.Placement['Gateway']['MainFrame'][2], 
                    relheight = self.Placement['Gateway']['MainFrame'][3], 
                    )
    self.att_list.append('self.frame1')

    # Create the Database Tab
    self.btn_imp = ttk.Button(
                            self.frame1, 
                            text = "Import Test Data", 
                            command = self.import_data,
                            style = 'Modern1.TButton',
                            )
    self.btn_imp.place(
                    anchor = 'c', 
                    relx = self.Placement['Gateway']['ButtonImp'][0], 
                    rely = self.Placement['Gateway']['ButtonImp'][1],
                    relwidth = self.Placement['Gateway']['ButtonImp'][2], 
                    relheight = self.Placement['Gateway']['ButtonImp'][3], 
                    )
    self.att_list.append('self.btn_imp')

    # Create the Characerization Tab
    self.btn_exp = ttk.Button(
                            self.frame1, 
                            text = "Export Model Data", 
                            command = self.export_data, 
                            style = 'Modern1.TButton',
                            )
    self.btn_exp.place(
                    anchor = 'c', 
                    relx = self.Placement['Gateway']['ButtonExp'][0], 
                    rely = self.Placement['Gateway']['ButtonExp'][1],
                    relwidth = self.Placement['Gateway']['ButtonExp'][2], 
                    relheight = self.Placement['Gateway']['ButtonExp'][3], 
                    )
    self.att_list.append('self.btn_exp')