#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# BuildGeneralPage.py
#
# PURPOSE: Build the general page with the different tab selections
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def BuildGeneralPage(self,window):
    # Import Modules
    import os
    from tkinter import ttk

    # Import Functions
    from Data.CreateDataTab import CreateDataTab

    # Try to create the log directory
    try:
        os.mkdir(os.path.join(os.getcwd(),"Logs"))
    except:
        pass

    # Set the log file name
    try:
        self.log_file = os.path.join(os.getcwd(),"Logs",os.path.basename(self.proj_file).split('.')[0] + ".log")
    except:
        self.log_file = os.path.join(os.getcwd(),"Logs","temp.log")

    # Create the file if it doesn't exist
    if os.path.exists(self.log_file) == False:
        self.log = ['-- LOG FILE STARTED --']

        with open(self.log_file, "w", encoding="utf-8") as f:
            for line in self.log:
                f.write(line + "\n")
        f.close()

    # Reset Log
    self.log = []

    # Create a frame for the notebook
    if hasattr(self, 'frame_tab') == True:
        def clear_frame(frame):
            for widget in frame.winfo_children():

                # If the widget is a Notebook, also destroy its tabs
                if isinstance(widget, ttk.Notebook):
                    for tab_id in widget.tabs():
                        tab = widget.nametowidget(tab_id)
                        clear_frame(tab)  # recursively clear widgets inside the tab
                widget.destroy()
                del widget
        clear_frame(self.frame_tab)

    self.frame_tab = ttk.Frame(window, style = "Custom1.TFrame")
    self.frame_tab.place( 
                    anchor='n',
                    relx = self.Placement['General']['FrameTab'][0], 
                    rely = self.Placement['General']['FrameTab'][1],
                    relwidth = self.Placement['General']['FrameTab'][2],
                    relheight = self.Placement['General']['FrameTab'][3]   
                    )


    # Create a Notebook widget (the tab container)
    self.nb_tab = ttk.Notebook(self.frame_tab, style="CustomNotebook.TNotebook")
    self.nb_tab.place(  
                    relx = self.Placement['General']['NBTab'][0], 
                    rely = self.Placement['General']['NBTab'][1],
                    relwidth = self.Placement['General']['NBTab'][2],
                    relheight = self.Placement['General']['NBTab'][3]   
                    )
    
    # Initialize Attributes Lists
    self.atts = {'Database':{'Local': [],
                            'Permanent':[]},
                'Characterization':{'Local': [],
                            'Permanent':[]},
                'Optimize':{'Local': [],
                            'Permanent':[]},
                'Analysis':{'Local': [],
                            'Permanent':[]},
                'Visualization':{'Local': [],
                            'Permanent':[]},
                'Export':{'Local': [],
                            'Permanent':[]},
                'Settings':{'Local': [],
                            'Permanent':[]},
                            }

    # --- Database Tab
    self.nb_tab_tab1 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab1, text="   Database   ")

    # --- Characterization Tab
    self.nb_tab_tab2 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab2, text="   Characterization   ")
    
    # --- Optimize Tab
    self.nb_tab_tab3 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab3, text="   Optimize Model   ")

    # --- Analyze Tab
    self.nb_tab_tab4 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab4, text="   Analyze Model   ")

    # --- Visualization Tab
    self.nb_tab_tab5 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab5, text="   Visualization   ")

    # --- Export Tab
    self.nb_tab_tab6 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab6, text="   Export   ")

    # --- Settings Tab
    self.nb_tab_tab7 = ttk.Frame(self.nb_tab, style = "Custom1.TFrame")
    self.nb_tab.add(self.nb_tab_tab7, text="   Settings   ")

    # Bind tab change function
    self.nb_tab.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    # Initialize with data tab
    self.db_init = 1
    self.char_init = 1
    self.opt_init = 1
    self.analy_init = 1
    self.viz_init = 1
    self.exp_init = 1
    self.set_init = 1
    CreateDataTab(self, window)