#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# TestSelection.py
#
# PURPOSE: Allow the user to search for tests in the database
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def TestSelection(self,window):
    # Import Modules
    import os
    import shutil
    import threading
    import tkinter as tk
    from tkinter import filedialog
    from tkinter import messagebox
    from tkinter import ttk
    import tkinter.font as tkfont
    import tksheet
    import webbrowser

    # Import Functions
    from Gateway.ExportData import ExportData
    from Gateway.Search import Search
    from Model.UnitConversion import UnitConversion

    # Function for selection options
    def sel_opts(event, self):
        # Get the selected widget and id
        widget = event.widget
        i = widget.id

        # Delete all Label and Entry widgets in the frame
        for j in range(4,7):
            if self.srch_vals[i][j] is not None:
                self.srch_vals[i][j].destroy()
                self.srch_vals[i][j] = None

        # Get the selection
        sel = self.srch_vals[i][3].get()

        # Build the rest of the frame
        single = ['equals', 'is less than', 'is greater than']
        double = ['is between']
        if sel in single:
            # Create an entry box with numerical float values only
            vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

            # Add the Entry Box Equals
            self.srch_vals[i][4] = ttk.Entry(
                                            self.srch_vals[i][1], 
                                            validate="key", 
                                            validatecommand=vcmd, 
                                            style="Custom.TEntry",
                                            justify='center',
                                            width = 10,
                                            font = tkfont.Font(family="Segoe UI", size=10)
                                            )
            self.srch_vals[i][4].grid(row = 0, column = 2, sticky = 'ew', padx = 5, pady = 5)
            self.att_list.append('self.srch_vals[i][4]')

        if sel in double:
            # Create an entry box with numerical float values only
            vcmd = (window.register(only_numbers_and_decimal), "%S", "%P")

            # Add the Entry Box Equals
            self.srch_vals[i][4] = ttk.Entry(
                                            self.srch_vals[i][1], 
                                            validate="key", 
                                            validatecommand=vcmd, 
                                            style="Custom.TEntry",
                                            justify='center',
                                            width = 10,
                                            font = tkfont.Font(family="Segoe UI", size=10)
                                            )
            self.srch_vals[i][4].grid(row = 0, column = 2, sticky = 'ew', padx = 5, pady = 5)
            self.att_list.append('self.srch_vals[i][4]')

            # Create label
            self.srch_vals[i][5] = ttk.Label(
                                            self.srch_vals[i][1], 
                                            text="and",
                                            style = 'Modern2.TLabel'
                                            )
            self.srch_vals[i][5].grid(row = 0, column = 3, sticky = 'ew', padx = 10, pady = 5)
            self.att_list.append('self.srch_vals[i][5]')

            # Add the Entry Box Equals
            self.srch_vals[i][6] = ttk.Entry(
                                            self.srch_vals[i][1], 
                                            validate="key", 
                                            validatecommand=vcmd, 
                                            style="Custom.TEntry",
                                            justify='center',
                                            width = 10,
                                            font = tkfont.Font(family="Segoe UI", size=10)
                                            )
            self.srch_vals[i][6].grid(row = 0, column = 4, sticky = 'ew', padx = 5, pady = 5)
            self.att_list.append('self.srch_vals[i][6]')

    # Function for Validation of Entry - only float values
    def only_numbers_and_decimal(char, current_value):

        # Check if the character is a digit or a decimal point
        if char.isdigit():
            return True
        elif char == '.' and current_value.count('.') == 1:
            return True
        return False

    # Function to view data sheet
    def view_datasheet():
        try:
            # Get the record
            record = self.records[self.res_sheet.get_currently_selected().row]

            # Get the url
            url = record.viewer_url

            # Open in browser
            webbrowser.open(url, new=2)
        except:
            pass
        
    # Function to show search results
    def search_for_records():
        # Delete the previous frame and table
        try:
            self.res_frame.destroy()
            self.res_sheet.destroy()
            self.btn_res_exp.destroy()
        except:
            pass

        # Function to conduct the search
        def Search_DB(callback):
            
            # Conduct search
            self.records = Search(self)

            # Notify when done
            callback()

        # Function to export records
        def export_records():
            
            # Function to write export files
            def write_export(callback):
                # Preallocate list of filenames
                self.fnames = []

                # Set the temp path
                temp_path = os.path.join(os.getcwd(),'Temp')
                # Get the sheet data
                data = self.res_sheet.data
                for i in range(len(data)):
                    if data[i][4] == True:
                        # Get the record
                        record = self.records[i]

                        # Create the temporary record
                        file, msg = ExportData(record, temp_path)
                        if file is not None:    
                            self.fnames.append(file)
                        else:
                            messagebox.showerror(message=msg)
            
                # Notify when done
                callback()
            
            # Function to display progress bar while saving
            def show_export_window():

                # Create the window
                loading = tk.Toplevel(window)
                loading.title("Exporting Data")
                loading.geometry("350x100")
                loading.resizable(False, False)
                loading.configure(bg='white')
                loading.grab_set()  

                # Function for progress bar Exit Protocol
                def on_closing_saving(self):

                    # Don't allow exit while saving
                    return
                
                # Create the window exit protocal
                loading.protocol("WM_DELETE_WINDOW", lambda:on_closing_saving(self))

                # Create the loading label
                ttk.Label(
                        loading, 
                        text="Writing Excel Files - Please Wait.", 
                        style = "Modern2.TLabel"
                        ).pack(pady=10)

                # Create the progress bar
                pb = ttk.Progressbar(
                                    loading, 
                                    mode='indeterminate',
                                    style = "Modern.Horizontal.TProgressbar"
                                    )
                pb.pack(fill='x', padx=20, pady=10)
                pb.start(10)

                # Function to close window when task is completed
                def on_task_done():

                    # Stop Progress bar
                    pb.stop()

                    # Destroy Window
                    loading.destroy()

                # Begin save on background thread
                threading.Thread(target=write_export, args=(on_task_done,), daemon=True).start()

                # Wait until loading window is closed
                window.wait_window(loading)

            # Start Search
            show_export_window()

            try:
                if len(self.fnames) > 0:
                    # Ask user where to save
                    save_dir = filedialog.askdirectory()
                    for file in self.fnames:
                        shutil.move(file, os.path.join(save_dir,os.path.basename(file)))

                    # Show message the file is saved
                    messagebox.showinfo(message = 'Files saved!')

            except:
                messagebox.showerror(message = 'Save Failed - Check that all files are closed and try again.')

        # Function to display progress bar while saving
        def show_loading_window():

            # Create the window
            loading = tk.Toplevel(window)
            loading.title("Searching Database")
            loading.geometry("350x100")
            loading.resizable(False, False)
            loading.configure(bg='white')
            loading.grab_set()  

            # Function for progress bar Exit Protocol
            def on_closing_saving(self):

                # Don't allow exit while saving
                return
            
            # Create the window exit protocal
            loading.protocol("WM_DELETE_WINDOW", lambda:on_closing_saving(self))

            # Create the loading label
            ttk.Label(
                    loading, 
                    text="Searching the Database - Please Wait.", 
                    style = "Modern2.TLabel"
                    ).pack(pady=10)

            # Create the progress bar
            pb = ttk.Progressbar(
                                loading, 
                                mode='indeterminate',
                                style = "Modern.Horizontal.TProgressbar"
                                )
            pb.pack(fill='x', padx=20, pady=10)
            pb.start(10)

            # Function to close window when task is completed
            def on_task_done():

                # Stop Progress bar
                pb.stop()

                # Destroy Window
                loading.destroy()

            # Begin save on background thread
            threading.Thread(target=Search_DB, args=(on_task_done,), daemon=True).start()

            # Wait until loading window is closed
            window.wait_window(loading)

        # Start Search
        show_loading_window()

        if len(self.records) > 0:
            # Create the frame
            self.res_frame = tk.Frame(
                            window, 
                            bd=1, 
                            bg="white"
                            )
            self.res_frame.place(
                            anchor = 'nw', 
                            relx = self.Placement['Gateway']['ResFrame'][0], 
                            rely = self.Placement['Gateway']['ResFrame'][1],
                            relwidth = self.Placement['Gateway']['ResFrame'][2],
                            relheight = self.Placement['Gateway']['ResFrame'][3],
                            )
            self.att_list.append('self.res_frame')

            # Create the sheet
            Cols = ['Name','Type','Direction','Temperature (°C)',' ']
            self.res_sheet = tksheet.Sheet(
                                            self.res_frame, 
                                            total_rows = len(self.records), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"bold"),
                                            #table_bg = 'red' # For checking formatting only
                                            )
            self.res_sheet.place(
                                anchor = 'n', 
                                relx = self.Placement['Gateway']['ResSheet'][0], 
                                rely = self.Placement['Gateway']['ResSheet'][1],
                                relwidth = self.Placement['Gateway']['ResSheet'][2],
                                relheight = self.Placement['Gateway']['ResSheet'][3],
                                )
            self.att_list.append('self.res_sheet')

            # -- Format the table
            self.res_sheet.change_theme("blue")
            self.res_sheet.table_align(align = 'c',redraw=True)
            self.res_frame.update_idletasks()
            total_width = self.res_sheet.winfo_width()
            self.res_sheet.column_width(column = 0, width = int(total_width*self.Placement['Gateway']['ResSheet'][4]), redraw = True)
            self.res_sheet.column_width(column = 1, width = int(total_width*self.Placement['Gateway']['ResSheet'][5]), redraw = True)
            self.res_sheet.column_width(column = 2, width = int(total_width*self.Placement['Gateway']['ResSheet'][6]), redraw = True)
            self.res_sheet.column_width(column = 3, width = int(total_width*self.Placement['Gateway']['ResSheet'][7]), redraw = True)
            self.res_sheet.column_width(column = 4, width = int(total_width*self.Placement['Gateway']['ResSheet'][8]), redraw = True)
            self.res_sheet.checkbox("E",checked=False)

            # -- Populate the data
            for i in range(len(self.records)):
                record = self.records[i]
                # -- Name
                self.res_sheet.set_cell_data(i,0,record.attributes['Specimen ID'].value)

                # -- Test Type
                self.res_sheet.set_cell_data(i,1,record.attributes['Test Type'].value)

                # -- Direction
                self.res_sheet.set_cell_data(i,2,record.attributes['Material Test Direction'].value)

                # -- Test Temperature
                temp = UnitConversion(record.attributes['Test Temperature'].unit, record.attributes['Test Temperature'].value, "°C")
                self.res_sheet.set_cell_data(i,3,round(temp))

                # -- Selection
                self.res_sheet.set_cell_data(i,4,True)

            # Enable Bindings
            self.res_sheet.enable_bindings('single_select','cell_select','row_select', "right_click_popup_menu")
            self.res_sheet.popup_menu_add_command('View Datasheet', view_datasheet, table_menu = True, index_menu = True, header_menu = True)

            # Create search button
            self.btn_res_exp = ttk.Button(
                                    window, 
                                    text = "Export", 
                                    command = export_records,
                                    style = 'Modern1.TButton',
                                    )
            self.btn_res_exp.place(
                            anchor = 'n', 
                            relx = self.Placement['Gateway']['ButtonResExp'][0], 
                            rely = self.Placement['Gateway']['ButtonResExp'][1],
                            relwidth = self.Placement['Gateway']['ButtonResExp'][2],
                            relheight = self.Placement['Gateway']['ButtonResExp'][3],
                            )
            self.att_list.append('self.btn_res_exp')
    
    # Create the search criteria frame
    self.srch_frame = tk.Frame(
                            window, 
                            bd=1, 
                            bg="white"
                            )
    self.srch_frame.place(
                    anchor = 'nw', 
                    relx = self.Placement['Gateway']['SearchFrame'][0], 
                    rely = self.Placement['Gateway']['SearchFrame'][1],
                    relwidth = self.Placement['Gateway']['SearchFrame'][2],
                    relheight = self.Placement['Gateway']['SearchFrame'][3],
                    )
    self.srch_frame.update_idletasks()
    frame_width = self.srch_frame.winfo_width()
    
    self.att_list.append('self.srch_frame')

    # Scrollable Frame in the left half
    self.srch_canvas = tk.Canvas(
                            self.srch_frame,
                            bg="white", 
                            highlightthickness=0
                            )
    self.att_list.append('self.srch_canvas')

    # Create search for material name
    # -- Create label
    self.label_mat = ttk.Label(
                            self.srch_frame,
                            text = 'Material Name:',
                            style='Modern3.TLabel'
                            )
    self.label_mat.grid(row = 0, column = 0, sticky="w", padx=10, pady=5)
    self.att_list.append('self.label_mat')

    # -- create the entry pox
    self.text_mat = tk.Text(
                self.srch_frame,
                width = int(85*frame_width/990),
                height=4,
                font=("Segoe UI", max([self.min_font, int(12*self.scale)])), 
                bg="white",
                fg="black",
                bd=1,                    
                relief="solid",
                wrap="word"
                )
    self.text_mat.grid(row = 0, column = 1, sticky="ew", padx=20, pady=5)
    self.att_list.append('self.text_mat')

    # Create search for Test Type
    # -- Create label
    self.label_type = ttk.Label(
                            self.srch_frame,
                            text = 'Test Type:',
                            style='Modern3.TLabel'
                            )
    self.label_type.grid(row = 1, column = 0, sticky="w", padx=10, pady=5)
    self.att_list.append('self.label_type')

    # -- Create the combobox
    opts = [''] + self.table.attributes['Test Type'].discrete_values
    self.combo_type = ttk.Combobox(
                                self.srch_frame,
                                values=opts,
                                style="Modern.TCombobox",
                                state="readonly",
                                )
    self.combo_type.grid(row = 1, column = 1, sticky="ew", padx=20, pady=5)
    self.att_list.append('self.combo_type')
    

    # Create search for Generic Test Type
    # -- Create label
    self.label_gtype = ttk.Label(
                            self.srch_frame,
                            text = 'Generic Test Type:',
                            style='Modern3.TLabel'
                            )
    self.label_gtype.grid(row = 2, column = 0, sticky="w", padx=10, pady=5)
    self.att_list.append('self.label_gtype')

    # -- Create the combobox
    opts = [''] + self.table.attributes['Variable Load Test Type'].discrete_values
    self.combo_gtype = ttk.Combobox(
                                self.srch_frame,
                                values=opts,
                                style="Modern.TCombobox",
                                state="readonly",
                                )
    self.combo_gtype.grid(row = 2, column = 1, sticky="ew", padx=20, pady=5)
    self.att_list.append('self.combo_gtype')

    # Preallocate self for changing widgets
    self.srch_vals = []

    Variables = {
                'Test Temperature:':['°F', '°C', 'K'],
                'Strain Rate:':['1/s','%/s'],
                'Stress Rate:':['psi/s', 'ksi/s', 'msi/s', 'Pa/s', 'kPa/s', 'MPa/s', 'GPa/s'],
                'Creep Stress:':['psi', 'ksi', 'msi', 'Pa', 'kPa', 'MPa', 'GPa'],
                'Relaxation Strain:':['%'],
                }
    
    for i in range(len(Variables.keys())):
        # Preallocate variables
        # -- [Label, Frame, Units, Drop Down Options, Entry1, "And", "Entry2"]
        self.srch_vals.append([None, None, None, None, None, None, None])

        # Get the key
        key = list(Variables.keys())[i]


        # -- Create label
        self.srch_vals[i][0] = ttk.Label(
                                self.srch_frame,
                                text = key,
                                style='Modern3.TLabel'
                                )
        self.srch_vals[i][0].grid(row = i+3, column = 0, sticky="w", padx=10, pady=5)
        self.att_list.append('self.srch_vals[i][0]')

        # -- Create the mini frame
        self.srch_vals[i][1] = ttk.Frame(self.srch_frame, style = 'White.TFrame')
        self.srch_vals[i][1].grid(row = i+3, column = 1, sticky="ew", padx=10, pady=5)
        self.att_list.append('self.srch_vals[i][1]')

        # -- Create units drop down
        opts = Variables[key]
        self.srch_vals[i][2] = ttk.Combobox(
                                    self.srch_vals[i][1],
                                    values=opts,
                                    style="Modern.TCombobox",
                                    state="readonly",
                                    width = 8,
                                    )
        self.srch_vals[i][2].grid(row = 0, column = 0, sticky="w", padx=5, pady=5)
        self.att_list.append('self.srch_vals[i][2]')

        # -- Create options drop down
        opts = ['equals', 'is between', 'is less than', 'is greater than']
        self.srch_vals[i][3] = ttk.Combobox(
                                    self.srch_vals[i][1],
                                    values=opts,
                                    style="Modern.TCombobox",
                                    state="readonly",
                                    )
        self.srch_vals[i][3].grid(row = 0, column = 1, sticky="ew", padx=5, pady=5)
        self.att_list.append('self.srch_vals[i][4]')
        self.srch_vals[i][3].bind("<<ComboboxSelected>>",  lambda event:sel_opts(event, self))
        self.srch_vals[i][3].id = i

    # Create search button
    self.btn_srch = ttk.Button(
                            window, 
                            text = "Search", 
                            command = search_for_records,
                            style = 'Modern1.TButton',
                            )
    self.btn_srch.place(
                    anchor = 'n',  
                    relx = self.Placement['Gateway']['ButtonSearch'][0], 
                    rely = self.Placement['Gateway']['ButtonSearch'][1],
                    relwidth = self.Placement['Gateway']['ButtonSearch'][2],
                    relheight = self.Placement['Gateway']['ButtonSearch'][3],
                    )
    self.att_list.append('self.btn_srch')

    # Create Back Button
    self.btn_back = ttk.Button(
                            window, 
                            text = "Back", 
                            command = self.back,
                            style = 'Modern2.TButton',
                            )
    self.btn_back.place(
                    anchor = 'nw',  
                    relx = self.Placement['Gateway']['ButtonBack'][0], 
                    rely = self.Placement['Gateway']['ButtonBack'][1],
                    relwidth = self.Placement['Gateway']['ButtonBack'][2],
                    relheight = self.Placement['Gateway']['ButtonBack'][3],
                    )
    self.att_list.append('self.btn_back')
