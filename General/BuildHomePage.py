#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# BuildHomePage.py
#
# PURPOSE: Build the home page to load a project a create a new project
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def BuildHomePage(self,window):
    # Import Modules
    import tkinter as tk
    from tkinter import ttk


    # Preallocate the att list
    self.att_list = []

    # Create the frame
    self.frame1 = tk.Frame(
                            window, 
                            bd=self.Placement['HomePage']['Frame1'][2], 
                            relief="ridge", 
                            width = self.Placement['HomePage']['Frame1'][3],
                            height = self.Placement['HomePage']['Frame1'][4],
                            bg="white"
                            )
    self.frame1.place(
                    anchor = 'c', 
                    relx = self.Placement['HomePage']['Frame1'][0], 
                    rely = self.Placement['HomePage']['Frame1'][1]
                    )
    self.att_list.append('self.frame1')


    #Create a button to create a new project
    self.btn1 = ttk.Button(
                        self.frame1, 
                        text = "New Project", 
                        command = self.new_project, 
                        style = "Modern1.TButton",
                        width = self.Placement['HomePage']['Button1'][2]
                        )
    self.btn1.place(
                    anchor = 'center', 
                    relx = self.Placement['HomePage']['Button1'][0], 
                    rely = self.Placement['HomePage']['Button1'][1]
                    )
    self.att_list.append('self.btn1')

    #Create a button to load a project
    self.btn2 = ttk.Button(
                        self.frame1, 
                        text = "Load Project", 
                        command = self.load_project, 
                        style = 'Modern1.TButton',
                        width = self.Placement['HomePage']['Button2'][2]
                        )
    self.btn2.place(
                    anchor = 'center', 
                    relx = self.Placement['HomePage']['Button2'][0], 
                    rely = self.Placement['HomePage']['Button2'][1]
                    )
    self.att_list.append('self.btn2')