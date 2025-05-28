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
    self.btn_db = tk.Button(window, text = "Database", command = self.data_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_db.place(anchor = 'w', relx = self.startx+self.delx*0, rely = starty)
    self.att_list.append('self.btn_db')

    # Create the Characerization Tab
    self.btn_db = tk.Button(window, text = "Characterization", command = self.char_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_db.place(anchor = 'w', relx = self.startx+self.delx*1, rely = starty)
    self.att_list.append('self.btn_db')

    # Create the Optimize Model Tab
    self.btn_mod = tk.Button(window, text = "Optimize Model", command = self.model_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_mod.place(anchor = 'w', relx = self.startx+self.delx*2, rely = starty)
    self.att_list.append('self.btn_mod')

    # Create the Analyze Model Tab
    self.btn_anly = tk.Button(window, text = "Analyze Model", command = self.analyze_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_anly.place(anchor = 'w', relx = self.startx+self.delx*3, rely = starty)
    self.att_list.append('self.btn_anly')

    # Create the Visualization Tab
    self.btn_anly = tk.Button(window, text = "Visualization", command = self.viz_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_anly.place(anchor = 'w', relx = self.startx+self.delx*4, rely = starty)
    self.att_list.append('self.btn_anly')

    # Create the Export Tab
    self.btn_anly = tk.Button(window, text = "Export", command = self.export_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_anly.place(anchor = 'w', relx = self.startx+self.delx*5, rely = starty)
    self.att_list.append('self.btn_anly')

    # Create the Settings Tab
    self.btn_anly = tk.Button(window, text = "Settings", command = self.settings_tab, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn_anly.place(anchor = 'w', relx = self.startx+self.delx*6, rely = starty)
    self.att_list.append('self.btn_anly')

    # Create the Save Button
    self.btn_save = tk.Button(window, text = "Save", command = self.save, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 10)
    self.btn_save.place(anchor = 'w', relx = self.startx, rely = 0.965)
    self.att_list.append('self.btn_save')