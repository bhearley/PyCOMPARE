#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateSettingsTab.py
#
# PURPOSE: Allow user to edit project settings
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateSettingsTab(self,window,frmt):
    # Import Modules
    import json
    import tkinter as tk
    from tkinter.filedialog import askopenfile
    from tkinter import messagebox
    import pickle

    # Import Functions
    from General.DeleteWidgets import DeleteTab

    # Unpack Formatting
    fontname = frmt[1]
    fsize_s = frmt[2]

    # Delete existing widgets
    if hasattr(self,"tab_att_list"):
        DeleteTab(self)

        if hasattr(self, 'canvas'):
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            del self.canvas

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []
    
    # Define Local Formating
    starty = 0.20

    # Set Paths Button
    def set_paths(self):
        # Set flag to check for open setings tab
        if hasattr(self,"settings_window") == False:
            self.settings_window = 0
        if self.settings_window == 0:
            self.settings_window = 1

            # Create the window
            root = tk.Tk()
            root.config(width=900, height=700)
            root.title("Path Dependencies")

            # Reset Window
            def reset_window():
                atts =  ["self.comp_path", "self.mod_path", "self.imp_path", "self.exp_path",
                         "self.comp_path_btn", "self.mod_path_btn", "self.imp_path_btn", "self.exp_path_btn"]
                
                for att in atts:
                    try:
                        eval(atts).destroy()

                    except:
                        pass


                # Set the paths
                # -- Compare Executable
                def set_comp_path(self):
                    file = askopenfile(title = "Compare Executable", filetypes= [('Executable', '*.exe')], mode ='r',)
                    if file is not None:
                        self.compare_path = file.name
                        self.comp_path.configure(text='')
                        reset_window()

                self.comp_path = tk.Label(root, text="Compare Executable Path: " + self.compare_path , 
                                            font=(fontname, 10))
                self.comp_path.place(anchor='w', relx = 0.025, rely = 0.1)
                self.comp_path_btn = tk.Button(root, text = "Edit", command = lambda:set_comp_path(self), 
                                            font = (fontname, 10), bg = '#fc3d21', fg='white',
                                            width = 10)
                self.comp_path_btn.place(anchor = 'w', relx = 0.025, rely = 0.15)

                
                # -- Model Library
                def set_mod_path(self):
                    file = askopenfile(title = "Available Models", filetypes= [('Excel', '*.xlsx')], mode ='r',)
                    if file is not None:
                        self.model_library = file.name
                        self.mod_path.configure(text='')
                        reset_window()
                self.mod_path = tk.Label(root, text="Available Models: " + self.model_library , 
                                            font=(fontname, 10))
                self.mod_path.place(anchor='w', relx = 0.025, rely = 0.2)
                self.mod_path_btn = tk.Button(root, text = "Edit", command = lambda:set_mod_path(self), 
                                            font = (fontname, 10), bg = '#fc3d21', fg='white',
                                            width = 10)
                self.mod_path_btn.place(anchor = 'w', relx = 0.025, rely = 0.25)
                
                # -- Excel Import Template
                def set_imp_path(self):
                    file = askopenfile(title = "Import Template", filetypes= [('Excel', '*.xlsx')], mode ='r',)
                    if file is not None:
                        self.import_template = file.name
                        self.imp_path.configure(text='')
                        reset_window()
                self.imp_path = tk.Label(root, text="Excel Import Template: " + self.import_template , 
                                            font=(fontname, 10))
                self.imp_path.place(anchor='w', relx = 0.025, rely = 0.3)
                self.imp_path_btn = tk.Button(root, text = "Edit", command = lambda:set_imp_path(self), 
                                            font = (fontname, 10), bg = '#fc3d21', fg='white',
                                            width = 10)
                self.imp_path_btn.place(anchor = 'w', relx = 0.025, rely = 0.35)
                
                # -- Excel Export Template
                def set_exp_path(self):
                    file = askopenfile(title = "Export Template", filetypes= [('Excel', '*.xlsx')], mode ='r',)
                    if file is not None:
                        self.export_template = file.name
                        self.exp_path.configure(text='')
                        reset_window()
                self.exp_path = tk.Label(root, text="Excel Export Template: " + self.export_template , 
                                            font=(fontname, 10))
                self.exp_path.place(anchor='w', relx = 0.025, rely = 0.4)
                self.exp_path_btn = tk.Button(root, text = "Edit", command = lambda:set_exp_path(self), 
                                            font = (fontname, 10), bg = '#fc3d21', fg='white',
                                            width = 10)
                self.exp_path_btn.place(anchor = 'w', relx = 0.025, rely = 0.45)
            

            # Create the window
            reset_window()

            # Create Exit Protocol
            def on_closing_root(self):
                # Reset the window
                self.settings_window = 0
                root.destroy()

            # Add the exit protocol to the root
            root.protocol("WM_DELETE_WINDOW", lambda:on_closing_root(self))

    self.btn_paths = tk.Button(window, text = "Path Dependencies", command = lambda:set_paths(self), 
                                font = (fontname, fsize_s), bg = '#fc3d21', fg='white',
                                width = 18)
    self.btn_paths.place(anchor = 'w', relx = self.startx + self.delx*0, rely = 0.2)
    self.tab_att_list.append('self.btn_paths')