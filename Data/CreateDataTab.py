#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateDataTab.py
#
# PURPOSE: Create the database tab. The Database tab allows users to upload test data to the database through
#          a configured database or through the excel import tool
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateDataTab(self,window,frmt):
    # Import Modules
    import pandas as pd
    import tkinter as tk
    from tkinter import messagebox
    from tkinter.filedialog import askopenfilenames
    from tkinter import ttk
    import tksheet
    
    # Import Functions
    from Data.FunctionalDataSampling import FunctionalDataSampling
    from Data.ReadExcelInput import ReadExcelInput
    from General.DeleteWidgets import DeleteTab

    # Unpack Formatting
    fontname = frmt[1]
    fsize_s = frmt[2]

    # Delete existing widgets
    if hasattr(self,"tab_att_list"):
        # Delete tab attributes
        DeleteTab(self)

        # Delete the canvas
        if hasattr(self, 'canvas'):
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            del self.canvas

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []

    # Initialize button press
    self.clicked = 0

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
        update_table()

    def update_table():
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
            if hasattr(self, 'optmenu1_plt'):
                self.optmenu1_plt.destroy()
            if hasattr(self, 'optmenu2_plt'):
                self.optmenu2_plt.destroy()
            if hasattr(self, 'btn_plot'):
                self.btn_plot.destroy()
            if hasattr(self, 'canvas'):
                self.toolbar.destroy()
                self.canvas.get_tk_widget().destroy()
                del self.canvas
            if hasattr(self, 'stage_label'):
                self.stage_label.destroy()
            if hasattr(self, 'plot_label'):
                self.plot_label.destroy()
            if hasattr(self, 'stage_table'):
                self.stage_table.destroy()
            
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
            self.optmenu1_plt = ttk.Combobox(
                                        window,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['Combo1'][0], 
                                    rely = self.Placement['Data']['Combo1'][1]
                                    )
            self.optmenu1_plt.set(self.plot_opts[idx1]) 
            self.tab_att_list.append('self.optmenu1_plt')

            # Create the vs Label
            self.plot_label = ttk.Label(
                                    window, 
                                    text="vs",
                                    style = 'Modern1.TLabel' 
                                    )
            self.plot_label.place(
                                anchor = 'n', 
                                relx = self.Placement['Data']['Label1'][0], 
                                rely = self.Placement['Data']['Label1'][1]
                                )
            self.tab_att_list.append('self.plot_label')

            # Create the Y drop down menu
            self.optmenu2_plt = ttk.Combobox(
                                        window,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2_plt.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['Combo2'][0], 
                                    rely = self.Placement['Data']['Combo2'][1]
                                    )
            self.optmenu2_plt.set(self.plot_opts[idx2])
            self.tab_att_list.append('self.optmenu2_plt')

            # Create the plot button
            self.btn_plot = ttk.Button(
                                window, 
                                text = "Plot", 
                                command = self.plotter, 
                                style = "Modern2.TButton",
                                width = self.Placement['Data']['Button1'][2], 
                                )
            self.btn_plot.place(
                                anchor = 'n', 
                                relx = self.Placement['Data']['Button1'][0], 
                                rely = self.Placement['Data']['Button1'][1]
                                )
            self.tab_att_list.append('self.btn_plot')

            # Create the stage table
            self.stage_label = ttk.Label(
                                        window, 
                                        text="Stage Table:", 
                                        style = "Modern1.TLabel"
                                        )
            self.stage_label.place(
                                anchor = 'nw', 
                                relx = self.Placement['Data']['Label2'][0], 
                                rely = self.Placement['Data']['Label2'][1]
                                )
            self.tab_att_list.append('self.stage_label')
            Cols = ['Type', 'Direction','Control','Load Rate','Target','End Time (s)']
            self.stage_table = tksheet.Sheet(
                                            window, 
                                            total_rows = len(self.Compare['Data'][self.test_name]['Stage Type']), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Data']['Sheet1'][2], 
                                            height = self.Placement['Data']['Sheet1'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Data']['Sheet1'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Data']['Sheet1'][4],"bold"),
                                            #table_bg = 'red' # For checking formatting only
                                            )
            self.stage_table.place(
                                anchor = 'nw', 
                                relx = self.Placement['Data']['Sheet1'][0], 
                                rely = self.Placement['Data']['Sheet1'][1]
                                )
            self.tab_att_list.append('self.stage_table')

            # Format the sheet
            self.stage_table.change_theme("blue")
            self.stage_table.set_index_width(0)
            self.stage_table.column_width(column = 0, width = self.Placement['Data']['Sheet1'][5], redraw = True)
            self.stage_table.column_width(column = 1, width = self.Placement['Data']['Sheet1'][6], redraw = True)
            self.stage_table.column_width(column = 2, width = self.Placement['Data']['Sheet1'][7], redraw = True)
            self.stage_table.column_width(column = 3, width = self.Placement['Data']['Sheet1'][8], redraw = True)
            self.stage_table.column_width(column = 4, width = self.Placement['Data']['Sheet1'][9], redraw = True)
            self.stage_table.column_width(column = 5, width = self.Placement['Data']['Sheet1'][10], redraw = True)
            self.stage_table.table_align(align = 'c',redraw=True)

            # Enable Bindings
            self.stage_table.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys")

            # Set stage table cell values
            for i in range(len(self.Compare['Data'][self.test_name]['Stage Type'])):
                self.stage_table.set_cell_data(i,0,self.Compare['Data'][self.test_name]['Stage Type'][i])
                self.stage_table.set_cell_data(i,1,self.Compare['Data'][self.test_name]['Loading Direction'][i])
                self.stage_table.set_cell_data(i,2,self.Compare['Data'][self.test_name]['Control'][i])
                self.stage_table.set_cell_data(i,3,str(self.Compare['Data'][self.test_name]['Load Rate'][i][0]) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Load Rate'][i][1])
                self.stage_table.set_cell_data(i,4,str(round(self.Compare['Data'][self.test_name]['Target'][i][0],2)) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Target'][i][1])
                self.stage_table.set_cell_data(i,5,self.Compare['Data'][self.test_name]['Time'][self.Compare['Data'][self.test_name]['Stage Index'][i]])
            self.stage_table.redraw()

            # Call the plotting function
            self.plotter()

        def view_all_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view all test data on the same plot.
            #
            #----------------------------------------------------------------------

            # Delete existing widgets
            if hasattr(self, 'optmenu1_plt'):
                self.optmenu1_plt.destroy()
            if hasattr(self, 'optmenu2_plt'):
                self.optmenu2_plt.destroy()
            if hasattr(self, 'btn_plot'):
                self.btn_plot.destroy()
            if hasattr(self, 'stage_table'):
                self.stage_table.destroy()
            if hasattr(self, 'stage_label'):
                self.stage_label.destroy()
            if hasattr(self, 'plot_label'):
                self.plot_label.destroy()
            if hasattr(self, 'canvas'):
                self.toolbar.destroy()
                self.canvas.get_tk_widget().destroy()
                del self.canvas
            
            # Get list of options
            self.plot_opts = ['Tensile', 'Creep', 'Relaxation','Generic','All']

            # Create the plot option menu
            self.optmenu1_plt = ttk.Combobox(
                                        window,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt.place(
                                    anchor='n', 
                                    relx = self.Placement['Data']['Combo3'][0], 
                                    rely = self.Placement['Data']['Combo3'][1]
                                    )
            self.optmenu1_plt.set(self.plot_opts[0])
            self.optmenu1_plt.bind("<<ComboboxSelected>>",  lambda event:self.plotter_all(event, 'sheet_db'))

            # Call the plotting function
            self.plotter_all(self.plot_opts[0], 'sheet_db')

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

                # Delete exissting widgets
                if hasattr(self,"canvas"):
                    self.toolbar.destroy()
                    self.canvas.get_tk_widget().destroy()
                    del self.canvas
                atts = ['self.optmenu1_plt', 'self.btn_loc3', 'self.btn_loc4', 'self.btn_loc5']
                for widget in atts:
                    try:
                        eval(widget).destroy()
                    except:
                        pass

                # Update the table                 
                update_table()

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

        # Destroy test table if it exists
        if hasattr(self,'sheet_db'):
            self.sheet_db.destroy()

        # Create the test table
        tests = list(self.Compare['Data'].keys())
        Cols = [' ','Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)']
        self.sheet_db = tksheet.Sheet(
                                    window, 
                                    total_rows = len(tests), 
                                    total_columns = len(Cols), 
                                    headers = Cols,
                                    width = self.Placement['Data']['Sheet2'][2], 
                                    height = self.Placement['Data']['Sheet2'][3], 
                                    show_x_scrollbar = False, 
                                    show_y_scrollbar = True,
                                    font = ("Segoe UI",self.Placement['Data']['Sheet2'][4],"normal"),
                                    header_font = ("Segoe UI",self.Placement['Data']['Sheet2'][4],"bold"),
                                    #table_bg = 'blue' # For checking formatting only
                                    )
        self.sheet_db.place(
                            anchor = 'nw', 
                            relx = self.Placement['Data']['Sheet2'][0], 
                            rely = self.Placement['Data']['Sheet2'][1]
                            )
        self.tab_att_list.append('self.sheet_db')

        # Format the sheet
        self.sheet_db.change_theme("blue")
        self.sheet_db.set_index_width(0)
        self.sheet_db.column_width(column = 0, width = self.Placement['Data']['Sheet2'][5], redraw = True)
        self.sheet_db.column_width(column = 1, width = self.Placement['Data']['Sheet2'][6], redraw = True)
        self.sheet_db.column_width(column = 2, width = self.Placement['Data']['Sheet2'][7], redraw = True)
        self.sheet_db.column_width(column = 3, width = self.Placement['Data']['Sheet2'][8], redraw = True)
        self.sheet_db.column_width(column = 4, width = self.Placement['Data']['Sheet2'][9], redraw = True)
        self.sheet_db.column_width(column = 5, width = self.Placement['Data']['Sheet2'][10], redraw = True)
        self.sheet_db.column_width(column = 6, width = self.Placement['Data']['Sheet2'][11], redraw = True)
        self.sheet_db.column_width(column = 7, width = self.Placement['Data']['Sheet2'][12], redraw = True)
        self.sheet_db.checkbox("A",checked=False)
        self.sheet_db.table_align(align = 'c',redraw=True)

        # Enanble bindings
        self.sheet_db.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_db.popup_menu_add_command('Select/Unselect All', lambda : select_all(self), table_menu = True, index_menu = True, header_menu = True)
        self.sheet_db.popup_menu_add_command('View Data', lambda : view_data(self), table_menu = True, index_menu = True, header_menu = True)
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
            self.sheet_db.set_cell_data(i,6,str(self.Compare['Data'][tests[i]]['Load Rate'][0][0]) + ' ' + self.Compare['Data'][tests[i]]['Load Rate'][0][1] )
            self.sheet_db.set_cell_data(i,7,self.Compare['Data'][tests[i]]['Angle'])

        # Check if test is in the characterization set
        if 'Characterization' in list(self.Compare.keys()):
            char_tests = self.Compare['Characterization'].keys()
            for i in range(len(tests)):
                if tests[i] in char_tests:
                    self.sheet_db.set_cell_data(i,0, True)

    # Create the upload from excel button
    self.btn_loc2 = ttk.Button(
                            window, 
                            text = "Upload from Excel", 
                            command = upload_from_excel,
                            style = "Modern3.TButton" ,
                            width = self.Placement['Data']['Button2'][2]
                            )
    self.btn_loc2.place(
                        anchor = 'w', 
                        relx = self.Placement['Data']['Button2'][0], 
                        rely = self.Placement['Data']['Button2'][1]
                        )
    self.loc_att_list.append('self.btn_loc2')

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
        else:
            # Show error message that no tests were added
            messagebox.showerror(message = 'No tests have been added to the database.')
                     
    # Create button to add data to characterization set
    self.btn_add_to_char = ttk.Button(
                                    window, 
                                    text = "Add To Characterization", 
                                    command = add_selected,
                                    style = 'Modern3.TButton', 
                                    width = self.Placement['Data']['Button3'][2]
                                    )
    self.btn_add_to_char.place(
                            anchor = 'w', 
                            relx = self.Placement['Data']['Button3'][0], 
                            rely = self.Placement['Data']['Button3'][1]
                            )
    self.loc_att_list.append('self.btn_add_to_char')

    # Load data
    if 'Data' in list(self.Compare.keys()):
        update_table()