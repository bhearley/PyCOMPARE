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
                            width = 400,
                            height = 400,
                            bg="white"
                            )
    self.frame1.place(
                    anchor = 'c', 
                    relx = 0.5, 
                    rely = 0.5
                    )
    self.att_list.append('self.frame1')

    # Create the Database Tab
    self.btn_imp = ttk.Button(
                            window, 
                            text = "Import Test Data", 
                            command = self.import_data,
                            style = 'Modern1.TButton',
                            width = 18
                            )
    self.btn_imp.place(
                    anchor = 'c', 
                    relx = 0.5, 
                    rely = 0.4
                    )
    self.att_list.append('self.btn_imp')

    # Create the Characerization Tab
    self.btn_exp = ttk.Button(
                            window, 
                            text = "Export Model Data", 
                            command = self.export_data, 
                            style = 'Modern1.TButton',
                            width = 18
                            )
    self.btn_exp.place(
                    anchor = 'c', 
                    relx = 0.5, 
                    rely = 0.6
                    )
    self.att_list.append('self.btn_exp')