#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateSettingsTab.py
#
# PURPOSE: Create the Settings tab. The Settings tab allows users to define project settings and path locations
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateSettingsTab(self):

    if self.set_init == 1:

        # Import Modules
        from pathlib import Path
        import shutil
        import tkinter as tk
        from tkinter import filedialog
        from tkinter import ttk

        # Set the paths
        # -- Compare Executable
        def set_comp_path(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Set the compare path file.
            #
            #----------------------------------------------------------

            # Ask for the new file path
            file = filedialog.askopenfile(title = "Compare Executable", filetypes= [('Executable', '*.exe')], mode ='r',)
            
            # Set new path and reset window
            if file is not None:
                self.Compare['Paths']['Compare Executable'] = file.name
                self.comp_path.configure(text="Compare Executable Path: " + self.Compare['Paths']['Compare Executable'])

        # Create label
        self.comp_path = ttk.Label( 
                                self.nb_tab_tab7, 
                                text="Compare Executable Path: " + self.Compare['Paths']['Compare Executable'] ,
                                style = "Modern2.TLabel",
                                )
        self.comp_path.place(
                            anchor='nw', 
                            relx = self.Placement['Settings']['LabelComp'][0], 
                            rely = self.Placement['Settings']['LabelComp'][1]
                            )

        # Create button to edit path
        self.comp_path_btn = ttk.Button(
                                        self.nb_tab_tab7, 
                                        text = "Edit", 
                                        command = lambda:set_comp_path(self), 
                                        style = "Modern4.TButton",
                                        )
        self.comp_path_btn.place(
                                anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonComp'][0],
                                rely = self.Placement['Settings']['ButtonComp'][1], 
                                relwidth = self.Placement['Settings']['ButtonComp'][2], 
                                relheight = self.Placement['Settings']['ButtonComp'][3]
                                )

        # -- Model Library
        def set_mod_path(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Set the model library path file.
            #
            #----------------------------------------------------------

            # Ask for the new file path
            file = filedialog.askopenfile(title = "Available Models", filetypes= [('Excel', '*.json')], mode ='r',)
            
            # Set new path and reset window
            if file is not None:
                self.Compare['Paths']['Model Library'] = file.name
                self.mod_path.configure(text="Available Models: " + self.Compare['Paths']['Model Library'])


        # Create the label
        self.mod_path = ttk.Label(
                                self.nb_tab_tab7, 
                                text="Available Models: " + self.Compare['Paths']['Model Library'] , 
                                style = "Modern2.TLabel"
                                )
        self.mod_path.place(
                            anchor='nw', 
                            relx = self.Placement['Settings']['LabelMod'][0], 
                            rely = self.Placement['Settings']['LabelMod'][1]
                            )

        # Create Button to edit the path
        self.mod_path_btn = ttk.Button(
                                    self.nb_tab_tab7, 
                                    text = "Edit", 
                                    command = lambda:set_mod_path(self), 
                                    style = "Modern4.TButton",
                                    )
        self.mod_path_btn.place(
                                anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonMod'][0],
                                rely = self.Placement['Settings']['ButtonMod'][1], 
                                relwidth = self.Placement['Settings']['ButtonMod'][2], 
                                relheight = self.Placement['Settings']['ButtonMod'][3]
                                )
        
        # -- Excel Import Template
        def set_imp_path(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Set the excel import template file path file.
            #
            #----------------------------------------------------------

            # Ask for the new file path
            file = filedialog.askopenfile(title = "Import Template", filetypes= [('Excel', '*.xlsx')], mode ='r',)
            
            # Set new path and reset window
            if file is not None:
                self.Compare['Paths']['Import Template'] = file.name
                self.imp_path.configure(text="Excel Import Template: " + self.Compare['Paths']['Import Template'])


        def download_imp(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Download the import template file.
            #
            #----------------------------------------------------------

            # Ask where to save the file
            try:
                file = filedialog.asksaveasfile(title = "Import Template", filetypes=[('Excel', '*.xlsx')],
                                            initialdir = str(Path.home() / "Downloads"),
                                            initialfile="ImportTemplate.xlsx")
            except:
                file = filedialog.asksaveasfile(title = "Import Template", filetypes=[('Excel', '*.xlsx')],
                                                initialfile="ImportTemplate.xlsx")

            # Copy the file
            if file is not None:
                shutil.copy(self.Compare['Paths']['Import Template'], file.name)

        # Create the label
        self.imp_path = ttk.Label(
                                self.nb_tab_tab7, 
                                text="Excel Import Template: " + self.Compare['Paths']['Import Template'] , 
                                style = "Modern2.TLabel")
        self.imp_path.place( 
                            anchor='nw', 
                            relx = self.Placement['Settings']['LabelImp'][0], 
                            rely = self.Placement['Settings']['LabelImp'][1]
                            )

        # Create button to edit the path
        self.imp_path_btn = ttk.Button(
                                    self.nb_tab_tab7, 
                                    text = "Edit", 
                                    command = lambda:set_imp_path(self), 
                                    style = 'Modern4.TButton',
                                    )
        self.imp_path_btn.place(
                                anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonImp'][0],
                                rely = self.Placement['Settings']['ButtonImp'][1], 
                                relwidth = self.Placement['Settings']['ButtonImp'][2], 
                                relheight = self.Placement['Settings']['ButtonImp'][3]
                                )

        # Create button to download file
        self.imp_dwnld_btn = ttk.Button(
                                    self.nb_tab_tab7, 
                                    text = "Download", 
                                    command = lambda:download_imp(self), 
                                    style = 'Modern4.TButton',
                                    )
        self.imp_dwnld_btn.place(
                                anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonImpD'][0],
                                rely = self.Placement['Settings']['ButtonImpD'][1], 
                                relwidth = self.Placement['Settings']['ButtonImpD'][2], 
                                relheight = self.Placement['Settings']['ButtonImpD'][3]
                                )
        
        # -- Excel Export Template
        def set_exp_path(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Set the export template path file.
            #
            #----------------------------------------------------------

            # Ask for the new file path
            file = filedialog.askopenfile(title = "Export Template", filetypes= [('Excel', '*.xlsx')], mode ='r',)
            
            # Set new path and reset window
            if file is not None:
                self.Compare['Paths']['Export Template'] = file.name
                self.exp_path.configure(text="Excel Export Template: " + self.Compare['Paths']['Export Template'] )

        def download_exp(self):
            #----------------------------------------------------------
            #
            #   PURPOSE: Download the export template.
            #
            #----------------------------------------------------------

            # Ask for the new file path
            try:
                file = filedialog.asksaveasfile(title = "Export Template", filetypes=[('Excel', '*.xlsx')],
                                            initialdir = str(Path.home() / "Downloads"),
                                            initialfile="ExportTemplate.xlsx")
            except:
                file = filedialog.asksaveasfile(title = "Export Template", filetypes=[('Excel', '*.xlsx')],
                                                initialfile="ExportTemplate.xlsx")

            # Copy file
            if file is not None:
                shutil.copy(self.Compare['Paths']['Export Template'], file.name)

        # Create the label
        self.exp_path = ttk.Label(
                                self.nb_tab_tab7, 
                                text="Excel Export Template: " + self.Compare['Paths']['Export Template'] , 
                                style = 'Modern2.TLabel'
                                )
        self.exp_path.place(
                            anchor = 'nw',
                            relx = self.Placement['Settings']['LabelExp'][0], 
                            rely = self.Placement['Settings']['LabelExp'][1]
                            )

        # Create button to edit the path
        self.exp_path_btn = ttk.Button(
                                    self.nb_tab_tab7, 
                                    text = "Edit", 
                                    command = lambda:set_exp_path(self), 
                                    style = "Modern4.TButton",
                                    )
        self.exp_path_btn.place(anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonExp'][0],
                                rely = self.Placement['Settings']['ButtonExp'][1], 
                                relwidth = self.Placement['Settings']['ButtonExp'][2], 
                                relheight = self.Placement['Settings']['ButtonExp'][3])

        # Create button to download the file
        self.exp_dwnld_btn = ttk.Button(
                                    self.nb_tab_tab7, 
                                    text = "Download", 
                                    command = lambda:download_exp(self), 
                                    style = "Modern4.TButton",
                                    )
        self.exp_dwnld_btn.place(
                                anchor = 'nw', 
                                relx = self.Placement['Settings']['ButtonExpD'][0],
                                rely = self.Placement['Settings']['ButtonExpD'][1], 
                                relwidth = self.Placement['Settings']['ButtonExpD'][2], 
                                relheight = self.Placement['Settings']['ButtonExpD'][3]
                                )
        
        # Set Flag
        self.set_init = 0