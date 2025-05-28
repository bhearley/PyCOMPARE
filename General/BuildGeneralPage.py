#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# BuildGeneralPage.py
#
# PURPOSE: Build the general page with the different tab selections
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def BuildGeneralPage(self,window,frmt):
    # Import Modules
    import tkinter as tk
    from tkinter import ttk

    # Unpack Formatting
    fontname = frmt[1]
    fsize_s = frmt[2]

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []

    # Set formating variables
    self.startx = 0.0125
    self.delx = 0.140
    starty = 0.13

    # Create the Database Tab
    self.btn_db = ttk.Button(
                            window, 
                            text = "Database", 
                            command = self.data_tab,
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button1'][2]
                            )
    self.btn_db.place(
                    anchor = 'w', 
                    relx = self.Placement['General']['Button1'][0], 
                    rely = self.Placement['General']['Button1'][1]
                    )
    self.att_list.append('self.btn_db')

    # Create the Characerization Tab
    self.btn_ch = ttk.Button(
                            window, 
                            text = "Characterization", 
                            command = self.char_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button2'][2]
                            )
    self.btn_ch.place(
                    anchor = 'w', 
                    relx = self.Placement['General']['Button2'][0], 
                    rely = self.Placement['General']['Button2'][1]
                    )
    self.att_list.append('self.btn_ch')

    # Create the Optimize Model Tab
    self.btn_mod = ttk.Button(
                            window, 
                            text = "Optimize Model", 
                            command = self.model_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button3'][2]
                            )
    self.btn_mod.place(
                    anchor = 'w', 
                    relx = self.Placement['General']['Button3'][0], 
                    rely = self.Placement['General']['Button3'][1]
                    )
    self.att_list.append('self.btn_mod')

    # Create the Analyze Model Tab
    self.btn_anly = ttk.Button(
                            window, 
                            text = "Analyze Model", 
                            command = self.analyze_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button4'][2]
                            )
    self.btn_anly.place(
                        anchor = 'w', 
                        relx = self.Placement['General']['Button4'][0], 
                        rely = self.Placement['General']['Button4'][1]
                        )
    self.att_list.append('self.btn_anly')

    # Create the Visualization Tab
    self.btn_viz = ttk.Button(
                            window, 
                            text = "Visualization", 
                            command = self.viz_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button5'][2]
                            )
    self.btn_viz.place(
                        anchor = 'w', 
                        relx = self.Placement['General']['Button5'][0], 
                        rely = self.Placement['General']['Button5'][1]
                        )
    self.att_list.append('self.btn_viz')

    # Create the Export Tab
    self.btn_exp = ttk.Button(
                            window, 
                            text = "Export", 
                            command = self.export_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button6'][2]
                            )
    self.btn_exp.place(
                    anchor = 'w', 
                    relx = self.Placement['General']['Button6'][0], 
                    rely = self.Placement['General']['Button6'][1]
                    )
    self.att_list.append('self.btn_exp')

    # Create the Settings Tab
    self.btn_set = ttk.Button(
                            window, 
                            text = "Settings", 
                            command = self.settings_tab, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button7'][2]
                            )
    self.btn_set.place(
                        anchor = 'w', 
                        relx = self.Placement['General']['Button7'][0], 
                        rely = self.Placement['General']['Button7'][1]
                        )
    self.att_list.append('self.btn_set')

    # Create the Save Button
    self.btn_save = ttk.Button(
                            window, 
                            text = "Save", 
                            command = self.save, 
                            style = 'Modern1.TButton',
                            width = self.Placement['General']['Button8'][2]
                            )
    self.btn_save.place(
                        anchor = 'w', 
                        relx = self.Placement['General']['Button8'][0], 
                        rely = self.Placement['General']['Button8'][1]
                        )
    self.att_list.append('self.btn_save')