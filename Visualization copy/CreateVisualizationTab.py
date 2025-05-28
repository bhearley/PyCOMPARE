#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateVisualizationTab.py
#
# PURPOSE: Create the Visualization tab. The Vizualization tab allows users to view predicitons on the characterization set
#          and analyze/visualize tests held out for verification.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateVisualizationTab(self,window,frmt):
    # Import Modules

    import tkinter as tk
    from tkinter import messagebox
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteTab

    #Unpack Formatting
    fontname = frmt[1]
    fsize_s = frmt[2]

    # Delete all tab attributes
    if hasattr(self,"tab_att_list"):
        #update_data(None)
        DeleteTab(self)

        if hasattr(self, 'canvas'):
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            del self.canvas

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []

    def update_table():
        #----------------------------------------------------------------------
        #
        #   PURPOSE: Create the characterization and verification tables.
        #
        #----------------------------------------------------------------------

        def view_data(self, tag):
            #------------------------------------------------------------------
            #
            #   PURPOSE: View characterization data.
            #
            #------------------------------------------------------------------

            # Delete the option menu
            if hasattr(self, 'optmenu1_viz'):
                self.optmenu1_viz.destroy()
            if hasattr(self, 'optmenu2_viz'):
                self.optmenu2_viz.destroy()
            if hasattr(self, 'btn_plot'):
                self.btn_plot.destroy()
            if hasattr(self, 'canvas'):
                self.toolbar.destroy()
                self.canvas.get_tk_widget().destroy()
                del self.canvas
        
            # Get the selected row and name
            if tag == 'char':
                table_name = "self.sheet_char_viz"
            else:
                table_name = "self.sheet_ver_viz"
            currently_selected = eval(table_name).get_currently_selected()
            self.test_name = eval(table_name).data[currently_selected.row][0]
            self.test_type = eval(table_name).data[currently_selected.row][1]

            # Create a model prediction if it doesn't exist
            if self.test_name not in list(self.Compare['Prediction'].keys()):
                self.Compare['Prediction'][self.test_name] = None
            if self.Compare['Prediction'][self.test_name] is None:
                self.run_compare_anly([self.test_name])
                eval(table_name).set_cell_data(currently_selected.row, -1, self.Compare['Prediction'][self.test_name]['Error'])
                eval(table_name).redraw()

            # Remove Highlights from all tables and add the selected row
            for i in range(len(self.sheet_char_viz.data)):
                self.sheet_char_viz.highlight_rows(i,'white','black')
            for i in range(len(self.sheet_ver_viz.data)):
                self.sheet_ver_viz.highlight_rows(i,'white','black')
            eval(table_name).highlight_rows(currently_selected.row,'lightblue1','black')

            # -- Get list of options
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

            # Create the X Option Menu
            self.opt1_viz = tk.StringVar(window)
            self.opt1_viz.set(self.plot_opts[idx1]) 
            self.optmenu1_viz = tk.OptionMenu(window, self.opt1_viz, *self.plot_opts) 
            self.optmenu1_viz.place(anchor = 'e', relx = 0.73, rely = 0.275)
            self.optmenu1_viz.configure(font = fsize_s)
            self.tab_att_list.append('self.optmenu1_viz')
            if 'self.optmenu1_viz' not in self.tab_att_list:
                    self.tab_att_list.append('self.optmenu1_viz')

            # Create the vs Label
            self.plot_label = tk.Label(window, text="vs", 
                                        font=(fontname, fsize_s), background='white')
            self.plot_label.place(anchor = 'e', relx = 0.765, rely = 0.275)
            self.tab_att_list.append('self.plot_label')

            # Create the Y Option Menu
            self.opt2_viz = tk.StringVar(window)
            self.opt2_viz.set(self.plot_opts[idx2]) 
            self.optmenu2_viz = tk.OptionMenu(window, self.opt2_viz, *self.plot_opts) 
            self.optmenu2_viz.place(anchor = 'e', relx = 0.87, rely = 0.275)
            self.optmenu2_viz.configure(font = fsize_s)
            self.tab_att_list.append('self.optmenu2_viz')
            if 'self.optmenu1_viz' not in self.tab_att_list:
                    self.tab_att_list.append('self.optmenu2_viz')

            # Create the plot button
            self.btn_plot = tk.Button(window, text = "Plot", command = self.plotter_viz, 
                                font = (fontname, fsize_s), bg = '#fc3d21', fg='white',
                                width = 6, height = 1)
            self.btn_plot.place(anchor = 'e', relx = 0.95, rely = 0.275)
            self.tab_att_list.append('self.btn_plot')

            # Call the plotting function
            self.plotter_viz()

        # Destroy existing widgets
        if hasattr(self,'sheet_char_viz'):
            self.sheet_char_viz.destroy()
        if hasattr(self,'char_label'):
            self.char_label.destroy()

        # Create the label
        self.char_label = tk.Label(window, text="Characterization Set:", 
                                        font=(fontname, fsize_s), background='white')
        self.char_label.place(anchor = 'w', relx = self.startx, rely = 0.22)
        self.tab_att_list.append('self.char_label')
        self.loc_att_list.append('self.char_label')
        
        # Get the tests in the characterization set
        tests = list(self.Compare['Characterization'].keys())

        # Set the column names
        Cols = ['Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)','Weight','Error']

        # Create the sheet
        self.sheet_char_viz = tksheet.Sheet(window, total_rows = len(tests), total_columns = len(Cols), 
                        headers = Cols,
                        width = 800, height = 270, show_x_scrollbar = False, show_y_scrollbar = True,
                        font = (fontname,12,"normal"),
                        header_font = (fontname,12,"bold"))
        self.sheet_char_viz.place(anchor = 'n', relx = 0.274, rely = 0.245)

        # Format the sheet
        self.tab_att_list.append('self.sheet_char_viz')
        self.sheet_char_viz.change_theme("blue")
        self.sheet_char_viz.set_index_width(0)

        # Enable Bindings
        self.sheet_char_viz.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_char_viz.popup_menu_add_command('View Data', lambda : view_data(self,'char'), table_menu = True, index_menu = True, header_menu = True)   
        
        # Set Column Widths
        self.sheet_char_viz.column_width(column = 0, width = 90, redraw = True)
        self.sheet_char_viz.column_width(column = 1, width = 80, redraw = True)
        self.sheet_char_viz.column_width(column = 2, width = 90, redraw = True)
        self.sheet_char_viz.column_width(column = 3, width = 90, redraw = True)
        self.sheet_char_viz.column_width(column = 4, width = 90, redraw = True)
        self.sheet_char_viz.column_width(column = 5, width = 100, redraw = True)
        self.sheet_char_viz.column_width(column = 6, width = 90, redraw = True)
        self.sheet_char_viz.column_width(column = 7, width = 70, redraw = True)
        self.sheet_char_viz.column_width(column = 8, width = 70, redraw = True)
        self.sheet_char_viz.table_align(align = 'c',redraw=True)

        # Populate Data
        for i in range(len(tests)):
            self.sheet_char_viz.set_cell_data(i,0, tests[i])
            self.sheet_char_viz.set_cell_data(i,1, self.Compare['Data'][tests[i]]['Test Type'])
            self.sheet_char_viz.set_cell_data(i,2, self.Compare['Data'][tests[i]]['Temperature'][0])
            ldir = ''
            ldir_list = []
            for j in range(len(self.Compare['Data'][tests[i]]['Loading Direction'])):
                if self.Compare['Data'][tests[i]]['Loading Direction'][j] not in ldir_list:
                    ldir_list.append(self.Compare['Data'][tests[i]]['Loading Direction'][j])
            for j in range(len(ldir_list)):
                ldir = ldir + str(ldir_list[j]) + ', '
            self.sheet_char_viz.set_cell_data(i,3, ldir[:len(ldir)-2])
            self.sheet_char_viz.set_cell_data(i,4,self.Compare['Data'][tests[i]]['Control'][0])
            self.sheet_char_viz.set_cell_data(i,5,str(self.Compare['Data'][tests[i]]['Load Rate'][0][0]) + ' ' + self.Compare['Data'][tests[i]]['Load Rate'][0][1] )
            self.sheet_char_viz.set_cell_data(i,6,self.Compare['Data'][tests[i]]['Angle'])
            self.sheet_char_viz.set_cell_data(i,7,self.Compare['Data'][tests[i]]['RelWeight'])
            self.sheet_char_viz.set_cell_data(i,8,round(self.Compare['Prediction'][tests[i]]['Error'],3))

        # Delete existing widgets
        if hasattr(self,'sheet_ver_viz'):
            self.sheet_ver_viz.destroy()
        if hasattr(self,'ver_label'):
            self.ver_label.destroy()

        # Create the label
        self.ver_label = tk.Label(window, text="Verification Set:", 
                                        font=(fontname, fsize_s), background='white')
        self.ver_label.place(anchor = 'w', relx = self.startx, rely = 0.605)
        self.tab_att_list.append('self.ver_label')
        self.loc_att_list.append('self.ver_label')

        # Get list of verification tests
        tests_all = list(self.Compare['Data'].keys())
        tests_ver = []
        for test in tests_all:
            if test not in list(self.Compare['Characterization'].keys()):
                if self.Compare['Data'][test]['Temperature'][0] == self.Compare['Data'][list(self.Compare['Characterization'].keys())[0]]['Temperature'][0]:
                    tests_ver.append(test)

        # Set the column names
        Cols = ['Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)','Error']
        
        # Create the sheet
        self.sheet_ver_viz = tksheet.Sheet(window, total_rows = len(tests_ver), total_columns = len(Cols), 
                        headers = Cols,
                        width = 730, height = 240, show_x_scrollbar = False, show_y_scrollbar = True,
                        font = (fontname,12,"normal"),
                        header_font = (fontname,12,"bold"))
        self.sheet_ver_viz.place(anchor = 'n', relx = 0.25, rely = 0.63)
        self.tab_att_list.append('self.sheet_ver_viz')

        # Format the sheet
        self.sheet_ver_viz.change_theme("blue")
        self.sheet_ver_viz.set_index_width(0)

        # Enable Bindings
        self.sheet_ver_viz.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_ver_viz.popup_menu_add_command('View Data', lambda : view_data(self,'ver'), table_menu = True, index_menu = True, header_menu = True)   
        
        # Set Column Widths
        self.sheet_ver_viz.column_width(column = 0, width = 90, redraw = True)
        self.sheet_ver_viz.column_width(column = 1, width = 80, redraw = True)
        self.sheet_ver_viz.column_width(column = 2, width = 90, redraw = True)
        self.sheet_ver_viz.column_width(column = 3, width = 90, redraw = True)
        self.sheet_ver_viz.column_width(column = 4, width = 90, redraw = True)
        self.sheet_ver_viz.column_width(column = 5, width = 100, redraw = True)
        self.sheet_ver_viz.column_width(column = 6, width = 90, redraw = True)
        self.sheet_ver_viz.column_width(column = 7, width = 70, redraw = True)
        self.sheet_ver_viz.table_align(align = 'c',redraw=True)

        # Populate Data
        for i in range(len(tests_ver)):
            self.sheet_ver_viz.set_cell_data(i,0, tests_ver[i])
            self.sheet_ver_viz.set_cell_data(i,1, self.Compare['Data'][tests_ver[i]]['Test Type'])
            self.sheet_ver_viz.set_cell_data(i,2, self.Compare['Data'][tests_ver[i]]['Temperature'][0])
            ldir = ''
            ldir_list = []
            for j in range(len(self.Compare['Data'][tests_ver[i]]['Loading Direction'])):
                if self.Compare['Data'][tests_ver[i]]['Loading Direction'][j] not in ldir_list:
                    ldir_list.append(self.Compare['Data'][tests_ver[i]]['Loading Direction'][j])
            for j in range(len(ldir_list)):
                ldir = ldir + str(ldir_list[j]) + ', '
            self.sheet_ver_viz.set_cell_data(i,3, ldir[:len(ldir)-2])
            self.sheet_ver_viz.set_cell_data(i,4,self.Compare['Data'][tests_ver[i]]['Control'][0])
            self.sheet_ver_viz.set_cell_data(i,5,str(self.Compare['Data'][tests_ver[i]]['Load Rate'][0][0]) + ' ' + self.Compare['Data'][tests_ver[i]]['Load Rate'][0][1] )
            self.sheet_ver_viz.set_cell_data(i,6,self.Compare['Data'][tests_ver[i]]['Angle'])
            if tests_ver[i] in list(self.Compare['Prediction'].keys()):
                if self.Compare['Prediction'][tests_ver[i]] is not None:
                    self.sheet_ver_viz.set_cell_data(i,7,round(self.Compare['Prediction'][tests_ver[i]]['Error'],3))

    # Check that tests exist in the characterization set
    try:
        if 'Characterization' in list(self.Compare.keys()):
            if len(list(self.Compare['Characterization'].keys())) > 0:
                update_table()
            else:
                messagebox.showerror(message = 'No tests have been adde the the charicterization set.')
    
    # Check that model parameters have been set
    except:
        messagebox.showerror(message = 'Model parameters have not been set. Use the Optimize or Analyze tabs to set the model parameters and execute.')