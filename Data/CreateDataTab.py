#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateDataTab.py
#
# PURPOSE: Create the database tab. The Database tab allows users to upload test data to the database through
#          a configured database or through the excel import tool
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateDataTab(self, window):
    # Import Modules
    import math
    import pandas as pd
    from tkinter import messagebox
    from tkinter.filedialog import askopenfilenames
    from tkinter import ttk
    import tksheet
    
    # Import Functions
    from Data.FunctionalDataSampling import FunctionalDataSampling
    from Data.ReadExcelInput import ReadExcelInput

    # Sig Fig Rounding
    def round_sig(x, sig=3):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Format number with defined significant figures
        #
        #--------------------------------------------------------------------------

        if x == 0:
            return 0
        return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)
    
    # Deselect Function
    def on_click(event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Deselect from sheets not currently pressed in
        #
        #--------------------------------------------------------------------------

        widget = event.widget

        # If the click is *not* inside the sheet, deselect it
        try:
            if widget != self.sheet_db.MT:
                self.sheet_db.deselect("all")
        except:
            pass

        try:
            if widget != self.stage_table_db.MT:
                self.stage_table_db.deselect("all")
        except:
            pass

    # Bind the deselect function to the window
    window.bind_all("<Button-1>", on_click, add="+")

    # Upload from excel function
    def upload_from_excel():
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Upload test data from excel.
        #
        #--------------------------------------------------------------------------

        # Ask to open excel files
        image_formats= [("Excel", "*.xlsx")]
        file_path_list = askopenfilenames(filetypes=image_formats, title='Select Excel Files')

        # Create the Data Structure if it doesn't exist
        if "Data" not in list(self.Compare.keys()):
            self.Compare['Data'] = {}

        # Read all selected files
        for file in file_path_list:
            # Read Excel to data frame
            df = pd.read_excel(file)

            # Run error chekcing
            data, flag, msg = ReadExcelInput(df)

            # Display error message to the user and continue
            if flag == 1:
                messagebox.showinfo(message=msg)
                continue

            # Populate Data into self
            self.Compare['Data'][data['name']] = {
                'Test Type':data['test_type'],
                'Temperature':[data['temp'],'°C'],
                'Loading Direction':data['load_dir'],
                'Control_All':data['control_all'],
                'Control':data['control'],
                'Target':data['target'],
                'Load Rate':data['load_rate'],
                'Angle':data['angle'],
                }

            # Separate the test into stages
            index = FunctionalDataSampling(data)

            # Populate Functional Data and Stage Information into self
            self.Compare['Data'][data['name']]['Time'] = data['Time']
            self.Compare['Data'][data['name']]['Strain'] = data['Strain']
            self.Compare['Data'][data['name']]['Stress'] = data['Stress']
            self.Compare['Data'][data['name']]['Stage Index'] = index
            self.Compare['Data'][data['name']]['Stage Type'] = data['stage_type']
            self.Compare['Data'][data['name']]['Stage Divisions'] = []
            for i in range(len(data['stage_type'])):
                self.Compare['Data'][data['name']]['Stage Divisions'].append(10)
            self.Compare['Data'][data['name']]['Reduced Data'] = {
                                                                  'Time':[],
                                                                  'Strain':dict.fromkeys(data['Strain']),
                                                                  'Stress':dict.fromkeys(data['Stress'])
                                                                  }
            
            # Initalize Data Reduction
            self.reduce_data(data['name'], data['load_dir'][0])
            
        # Update the table
        self.db_init = 0
        update_table(self.db_init)
        
    def update_table(init_flag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Update the database table.
        #
        #--------------------------------------------------------------------------

        def view_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view test data.
            #
            #----------------------------------------------------------------------

            # Delete existing widgets
            for att in self.atts['Database']['Local']:
                if att == "self.sheet_db":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass
            try:
                self.canvas_db.get_tk_widget().destroy()
                del self.canvas_db
            except:
                pass

            # Get the selected row and name
            currently_selected = self.sheet_db.get_currently_selected()
            self.test_name = self.sheet_db.data[currently_selected.row][1]
            self.test_type = self.sheet_db.data[currently_selected.row][2]

            # Remove Highlights from all rows and highlight the selected row
            for i in range(len(self.sheet_db.data)):
                self.sheet_db.highlight_rows(i,'white','black')
            self.sheet_db.highlight_rows(currently_selected.row,'lightblue1','black')
            
            # Get list of response curve options
            self.plot_opts = ['Time']
            data = self.Compare['Data'][self.test_name]
            data_keys = ['Strain','Stress']
            for key in data_keys:
                dir_keys = list(data[key].keys())
                for dir_key in dir_keys:
                    self.plot_opts.append(key + '-' + str(dir_key))

            # Find first stress and first strain
            idx1 = 0
            idx2 = 1
            for i in range(len(self.plot_opts)):
                if 'Strain' in self.plot_opts[i]:
                    idx1 = i
                    break
            for i in range(len(self.plot_opts)):
                if 'Stress' in self.plot_opts[i]:
                    idx2 = i
                    break

            # Create the X drop down menu
            self.optmenu1_plt_db = ttk.Combobox(
                                        self.nb_tab_tab1,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt_db.configure(font = self.style_man['Combo'])
            self.optmenu1_plt_db.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu1_plt_db.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['ComboX'][0], 
                                    rely = self.Placement['Data']['ComboX'][1],
                                    relwidth = self.Placement['Data']['ComboX'][2], 
                                    relheight = self.Placement['Data']['ComboX'][3]
                                    )
            self.optmenu1_plt_db.set(self.plot_opts[idx1]) 
            if "self.optmenu1_plt_db" not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.optmenu1_plt_db')

            # Create the vs Label
            self.plot_label_db = ttk.Label(
                                    self.nb_tab_tab1, 
                                    text="vs",
                                    style = 'Modern1.TLabel' 
                                    )
            self.plot_label_db.place(
                                anchor = 'n', 
                                relx = self.Placement['Data']['LabelVS'][0], 
                                rely = self.Placement['Data']['LabelVS'][1]
                                )
            if 'self.plot_label_db' not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.plot_label_db')

            # Create the Y drop down menu
            self.optmenu2_plt_db = ttk.Combobox(
                                        self.nb_tab_tab1,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2_plt_db.configure(font = self.style_man['Combo'])
            self.optmenu2_plt_db.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu2_plt_db.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['ComboY'][0], 
                                    rely = self.Placement['Data']['ComboY'][1],
                                    relwidth = self.Placement['Data']['ComboY'][2], 
                                    relheight = self.Placement['Data']['ComboY'][3]
                                    )
            self.optmenu2_plt_db.set(self.plot_opts[idx2])
            if "self.optmenu2_plt_db" not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.optmenu2_plt_db')

            # Create the plot button
            self.btn_plot_db = ttk.Button(
                                self.nb_tab_tab1, 
                                text = "Plot", 
                                command = self.plotter_db, 
                                style = "Modern2.TButton",
                                )
            self.btn_plot_db.place(
                                anchor = 'n', 
                                relx = self.Placement['Data']['ButtonPlot'][0], 
                                rely = self.Placement['Data']['ButtonPlot'][1],
                                relwidth = self.Placement['Data']['ButtonPlot'][2], 
                                relheight = self.Placement['Data']['ButtonPlot'][3]
                                )
            if "self.btn_plot_db" not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.btn_plot_db')
            

            # Create the stage table label
            self.stage_label_db = ttk.Label(
                                        self.nb_tab_tab1, 
                                        text="Stage Table:", 
                                        style = "Modern1.TLabel"
                                        )
            self.stage_label_db.place(
                                anchor = 'nw', 
                                relx = self.Placement['Data']['LabelStage'][0], 
                                rely = self.Placement['Data']['LabelStage'][1]
                                )
            if "self.stage_label_db" not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.stage_label_db')

            # Create the stage table
            Cols = ['Type', 'Direction','Control','Load Rate','Target','End Time (s)']
            self.stage_table_db = tksheet.Sheet(
                                            self.nb_tab_tab1, 
                                            total_rows = len(self.Compare['Data'][self.test_name]['Stage Type']), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                            )
            self.stage_table_db.place(
                                anchor = 'nw', 
                                relx = self.Placement['Data']['SheetSTG'][0], 
                                rely = self.Placement['Data']['SheetSTG'][1],
                                relwidth = self.Placement['Data']['SheetSTG'][2], 
                                relheight = self.Placement['Data']['SheetSTG'][3]
                                )
            if "self.stage_table_db" not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.stage_table_db')

            # Format the sheet
            self.stage_table_db.change_theme("blue")
            self.stage_table_db.set_index_width(0)
            window.update_idletasks()
            total_width = self.stage_table_db.winfo_width()
            self.stage_table_db.column_width(column = 0, width = int(total_width*self.Placement['Data']['SheetSTG'][4]), redraw = True)
            self.stage_table_db.column_width(column = 1, width = int(total_width*self.Placement['Data']['SheetSTG'][5]), redraw = True)
            self.stage_table_db.column_width(column = 2, width = int(total_width*self.Placement['Data']['SheetSTG'][6]), redraw = True)
            self.stage_table_db.column_width(column = 3, width = int(total_width*self.Placement['Data']['SheetSTG'][7]), redraw = True)
            self.stage_table_db.column_width(column = 4, width = int(total_width*self.Placement['Data']['SheetSTG'][8]), redraw = True)
            self.stage_table_db.column_width(column = 5, width = int(total_width*self.Placement['Data']['SheetSTG'][9]), redraw = True)
            self.stage_table_db.table_align(align = 'c',redraw=True)

            # Enable Bindings
            self.stage_table_db.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys")

            # Set stage table cell values
            for i in range(len(self.Compare['Data'][self.test_name]['Stage Type'])):
                self.stage_table_db.set_cell_data(i,0,self.Compare['Data'][self.test_name]['Stage Type'][i])
                self.stage_table_db.set_cell_data(i,1,self.Compare['Data'][self.test_name]['Loading Direction'][i])
                self.stage_table_db.set_cell_data(i,2,self.Compare['Data'][self.test_name]['Control'][i])
                self.stage_table_db.set_cell_data(i,3,str(round_sig(self.Compare['Data'][self.test_name]['Load Rate'][i][0],2)) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Load Rate'][i][1])
                self.stage_table_db.set_cell_data(i,4,str(round_sig(self.Compare['Data'][self.test_name]['Target'][i][0],2)) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Target'][i][1])
                self.stage_table_db.set_cell_data(i,5,self.Compare['Data'][self.test_name]['Time'][self.Compare['Data'][self.test_name]['Stage Index'][i]])
            self.stage_table_db.redraw()

            # Call the plotting function
            self.plotter_db()

        def view_all_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view all test data on the same plot.
            #
            #----------------------------------------------------------------------

            # Delete existing widgets
            for att in self.atts['Database']['Local']:
                if att == "self.sheet_db":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass

            try:
                self.canvas_db.get_tk_widget().destroy()
                del self.canvas_db
            except:
                pass
            
            # Get list of options
            self.plot_opts = ['Tensile', 'Creep', 'Relaxation','Generic','All']

            # Create the plot option menu
            self.optmenu1_plt_db = ttk.Combobox(
                                        self.nb_tab_tab1,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt_db.configure(font = self.style_man['Combo'])
            self.optmenu1_plt_db.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu1_plt_db.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['ComboPlot'][0], 
                                    rely = self.Placement['Data']['ComboPlot'][1],
                                    relwidth = self.Placement['Data']['ComboPlot'][2], 
                                    relheight = self.Placement['Data']['ComboPlot'][3]
                                    )
            self.optmenu1_plt_db.set(self.plot_opts[0])
            self.optmenu1_plt_db.bind("<<ComboboxSelected>>",  lambda event:self.plotter_all_db(event))
            if 'self.optmenu1_plt_db' not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append("self.optmenu1_plt_db")

            # Call the plotting function
            self.plotter_all_db(self.plot_opts[0])

        def delete_test(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Delete a test from the database.
            #
            #----------------------------------------------------------------------
            
            # Get the selected row and name
            currently_selected = self.sheet_db.get_currently_selected()
            self.test_name = self.sheet_db.data[currently_selected.row][1]

            # Ask user to confirm delete
            askyn = messagebox.askyesno(title = 'Delete test', message = 'Do you want to delete test ' + self.test_name  + ' from the database?')
            if askyn == True:
                # Clear all data for that test
                try:
                    del self.Compare['Data'][self.test_name]
                except:
                    pass
                try:
                    del self.Compare['Characterization'][self.test_name]
                except:
                    pass
                try:
                    del self.Compare['Prediction'][self.test_name]
                except:
                    pass

                # Delete existing widgets
                if hasattr(self,"canvas_db"):
                    self.toolbar_db.destroy()
                    self.canvas_db.get_tk_widget().destroy()
                    del self.canvas_db
                atts = ['self.optmenu1_plt_db']
                for widget in atts:
                    try:
                        eval(widget).destroy()
                    except:
                        pass

                # Update the flags                 
                self.db_init = 0
                self.char_init = 0
                self.viz_init = 0

                # Update table
                update_table(self.db_init)

        def select_all(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Select/Unselect all tests to add to characterization.
            #
            #----------------------------------------------------------------------
            if len(self.sheet_db.data) > 0:
                val = self.sheet_db.data[0][0]
                if val == True:
                    new_val = False
                else:
                    new_val = True
                for i in range(len(self.sheet_db.data)):
                    self.sheet_db.set_cell_data(i,0, new_val)

        # Delete widgets if data has changed
        if init_flag == 0:
            # Delete existing widgets
            for att in self.atts['Database']['Local']:
                if att == "self.sheet_db":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass

            try:
                self.canvas_db.get_tk_widget().destroy()
                del self.canvas_db
            except:
                pass

        # Check if the database sheet exists
        exist_flag = 0
        if hasattr(self, 'sheet_db'):
            if self.sheet_db.winfo_exists():
                exist_flag = 1

        # Create the database sheet
        if (init_flag == 1 and exist_flag == 0) or init_flag == 0:
            # Create the test table
            tests = list(self.Compare['Data'].keys())
            Cols = [' ','Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)']
            self.sheet_db = tksheet.Sheet(
                                        self.nb_tab_tab1, 
                                        total_rows = len(tests), 
                                        total_columns = len(Cols), 
                                        headers = Cols,
                                        show_x_scrollbar = False, 
                                        show_y_scrollbar = True,
                                        font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                        header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                        )
            self.sheet_db.place(
                                anchor = 'nw', 
                                relx = self.Placement['Data']['SheetDB'][0], 
                                rely = self.Placement['Data']['SheetDB'][1],
                                relwidth = self.Placement['Data']['SheetDB'][2], 
                                relheight = self.Placement['Data']['SheetDB'][3], 
                                )
            if 'self.sheet_db' not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append('self.sheet_db')

            # Format the sheet
            self.sheet_db.change_theme("blue")
            self.sheet_db.set_index_width(0)
            window.update_idletasks()
            total_width = self.sheet_db.winfo_width()
            if int(total_width*self.Placement['Data']['SheetDB'][4]) < 21:
                origA = self.Placement['Data']['SheetDB'][4]
                origB = self.Placement['Data']['SheetDB'][5]
                self.Placement['Data']['SheetDB'][4] = 21/total_width
                self.Placement['Data']['SheetDB'][5] = origA + origB - self.Placement['Data']['SheetDB'][4]
            self.sheet_db.column_width(column = 0, width = int(total_width*self.Placement['Data']['SheetDB'][4]), redraw = True)
            self.sheet_db.column_width(column = 1, width = int(total_width*self.Placement['Data']['SheetDB'][5]), redraw = True)
            self.sheet_db.column_width(column = 2, width = int(total_width*self.Placement['Data']['SheetDB'][6]), redraw = True)
            self.sheet_db.column_width(column = 3, width = int(total_width*self.Placement['Data']['SheetDB'][7]), redraw = True)
            self.sheet_db.column_width(column = 4, width = int(total_width*self.Placement['Data']['SheetDB'][8]), redraw = True)
            self.sheet_db.column_width(column = 5, width = int(total_width*self.Placement['Data']['SheetDB'][9]), redraw = True)
            self.sheet_db.column_width(column = 6, width = int(total_width*self.Placement['Data']['SheetDB'][10]), redraw = True)
            self.sheet_db.column_width(column = 7, width = int(total_width*self.Placement['Data']['SheetDB'][11]), redraw = True)
            self.sheet_db.checkbox("A",checked=False)
            self.sheet_db.table_align(align = 'c',redraw=True)

            # Enanble bindings
            self.sheet_db.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
            self.sheet_db.popup_menu_add_command('Select/Unselect All', lambda : select_all(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet_db.popup_menu_add_command('View Data', lambda : view_data(self), table_menu = True, index_menu = True, header_menu = True)
            #self.sheet_db.popup_menu_add_command('View Data', lambda : view_data(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet_db.popup_menu_add_command('View All Selected Data', lambda : view_all_data(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet_db.popup_menu_add_command('Delete Test', lambda : delete_test(self), table_menu = True, index_menu = True, header_menu = True)

            # Populate test cell data
            for i in range(len(tests)):
                self.sheet_db.set_cell_data(i,1, tests[i])
                self.sheet_db.set_cell_data(i,2, self.Compare['Data'][tests[i]]['Test Type'])
                self.sheet_db.set_cell_data(i,3, self.Compare['Data'][tests[i]]['Temperature'][0])
                ldir = ''
                ldir_list = []
                for j in range(len(self.Compare['Data'][tests[i]]['Loading Direction'])):
                    if self.Compare['Data'][tests[i]]['Loading Direction'][j] not in ldir_list:
                        ldir_list.append(self.Compare['Data'][tests[i]]['Loading Direction'][j])
                for j in range(len(ldir_list)):
                    ldir = ldir + str(ldir_list[j]) + ', '
                self.sheet_db.set_cell_data(i,4, ldir[:len(ldir)-2])
                self.sheet_db.set_cell_data(i,5,self.Compare['Data'][tests[i]]['Control'][0])
                self.sheet_db.set_cell_data(i,6,str(round_sig(self.Compare['Data'][tests[i]]['Load Rate'][0][0],2)) + ' ' + self.Compare['Data'][tests[i]]['Load Rate'][0][1] )
                self.sheet_db.set_cell_data(i,7,self.Compare['Data'][tests[i]]['Angle'])

            # Check if test is in the characterization set
            if 'Characterization' in list(self.Compare.keys()):
                char_tests = self.Compare['Characterization'].keys()
                for i in range(len(tests)):
                    if tests[i] in char_tests:
                        self.sheet_db.set_cell_data(i,0, True)

        # Set the initialization flag
        self.db_init = 1

    def add_selected():
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Add selected tests to the Characterization set.
        #
        #--------------------------------------------------------------------------

        # Check that the database sheet exists
        if hasattr(self, "sheet_db"):
            # Check for single temeprature
            flag = 0
            temp = []
            for i in range(len(self.sheet_db.data)):
                if self.sheet_db.data[i][0] == True:
                    if self.sheet_db.data[i][3] not in temp:
                        temp.append(self.sheet_db.data[i][3])

            # Show error message
            if len(temp) > 1:
                messagebox.showinfo(message = 'Multiple temperatures given. Select tests all at the same temperature.')
            else:
                # Get existing characterization data
                if 'Characterization' not in list(self.Compare.keys()):
                    self.Compare['Characterization'] = {}

                # Check for matching temperature
                if len(list(self.Compare['Characterization'].keys())) > 0:
                    temp_exist = self.Compare['Characterization'][list(self.Compare['Characterization'].keys())[0]]['Temperature'][0]
                    
                    # Show error message
                    if temp[0] != temp_exist:
                        messagebox.showinfo(message = 'There are already tests conducted at ' + str(temp_exist) + '°C in the characterization set. Only add tests at that temperature.')
                        flag = 1

                # Add to characterization set
                if flag == 0:
                    tests = list(self.Compare['Characterization'].keys())
                    ct = 0
                    for i in range(len(self.sheet_db.data)):
                        if self.sheet_db.data[i][0] == True:
                            test_name = self.sheet_db.data[i][1]
                            if test_name not in tests:
                                self.Compare['Characterization'][test_name] = self.Compare['Data'][test_name]
                                self.Compare['Characterization'][test_name]['RelWeight'] = 1
                                ct = ct + 1

                    # Show number of tests added to the user
                    messagebox.showinfo(message = 'Added ' + str(ct) + ' tests to the characterization set.')

                    self.char_init = 0
                    self.viz_init = 0
        else:
            # Show error message that no tests were added
            messagebox.showerror(message = 'No tests have been added to the database.')
                     
    # Create the upload from excel button
    self.btn_up_exc = ttk.Button(
                            self.nb_tab_tab1, 
                            text = "Upload from Excel", 
                            command = upload_from_excel,
                            style = "Modern1.TButton" ,
                            )
    self.btn_up_exc.place(
                        anchor = 'w', 
                        relx = self.Placement['Data']['ButtonExc'][0], 
                        rely = self.Placement['Data']['ButtonExc'][1],
                        relwidth = self.Placement['Data']['ButtonExc'][2], 
                        relheight = self.Placement['Data']['ButtonExc'][3]
                        )
    self.atts['Database']['Permanent'].append('self.btn_up_exc')
    
    # Create button to add data to characterization set
    self.btn_add_to_char = ttk.Button(
                                    self.nb_tab_tab1, 
                                    text = "Add To Characterization", 
                                    command = add_selected,
                                    style = 'Modern1.TButton', 
                                    )
    self.btn_add_to_char.place(
                            anchor = 'w', 
                            relx = self.Placement['Data']['ButtonAdd'][0], 
                            rely = self.Placement['Data']['ButtonAdd'][1],
                            relwidth = self.Placement['Data']['ButtonAdd'][2], 
                            relheight = self.Placement['Data']['ButtonAdd'][3]
                            )
    self.atts['Database']['Permanent'].append('self.btn_add_to_char')

    # Load data
    if 'Data' in list(self.Compare.keys()):
        update_table(self.db_init)