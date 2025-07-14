#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateVisualizationTab.py
#
# PURPOSE: Create the Visualization tab. The Vizualization tab allows users to view predicitons on the characterization set
#          and analyze/visualize tests held out for verification.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateVisualizationTab(self,window):
    # Import Modules
    import threading
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteTab

    # Delete all tab attributes
    if hasattr(self,"tab_att_list"):
        #update_data(None)
        DeleteTab(self)

        if hasattr(self, 'canvas'):
            self.toolbar.destroy()
            self.canvas.get_tk_widget().destroy()
            del self.canvas

        if hasattr(self, 'canvas2'):
            self.toolbar2.destroy()
            self.canvas2.get_tk_widget().destroy()
            del self.canvas2

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []

        # Function to deselect sheet
    def deselect_sheet(event,self,tag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Deselect one tksheet when selecting another
        #
        #--------------------------------------------------------------------------
        if tag == 'sheet_char_viz':
            try:
                self.sheet_ver_viz.deselect("all", redraw=True)
            except:
                pass
        if tag == 'sheet_ver_viz':
            try:
                self.sheet_char_viz.deselect("all", redraw=True)
            except:
                pass

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
            if hasattr(self, 'optmenu3_viz'):
                self.optmenu3_viz.destroy()
            if hasattr(self, 'pred_label'):
                self.pred_label.destroy()
            if hasattr(self, 'raw_label'):
                self.raw_label.destroy()
            if hasattr(self, 'btn_plot'):
                self.btn_plot.destroy()
            if hasattr(self, 'canvas'):
                self.toolbar.destroy()
                self.canvas.get_tk_widget().destroy()
                del self.canvas
            if hasattr(self, 'canvas2'):
                self.toolbar2.destroy()
                self.canvas2.get_tk_widget().destroy()
                del self.canvas2
        
            # Get the selected row and name
            if tag == 'char':
                table_name = "self.sheet_char_viz"
            else:
                table_name = "self.sheet_ver_viz"
            currently_selected = eval(table_name).get_currently_selected()
            self.test_name = eval(table_name).data[currently_selected.row][1]
            self.test_type = eval(table_name).data[currently_selected.row][2]

            # Create a model prediction if it doesn't exist
            if self.test_name not in list(self.Compare['Prediction'].keys()):
                self.Compare['Prediction'][self.test_name] = None
            if self.Compare['Prediction'][self.test_name] is None:
                self.run_compare_anly([self.test_name])
                eval(table_name).set_cell_data(currently_selected.row, -1, round(self.Compare['Prediction'][self.test_name]['Error'],3))
                eval(table_name).redraw()

            # Remove Highlights from all tables and add the selected row
            for i in range(len(self.sheet_char_viz.data)):
                self.sheet_char_viz.highlight_rows(i,'white','black')
            for i in range(len(self.sheet_ver_viz.data)):
                self.sheet_ver_viz.highlight_rows(i,'white','black')
            eval(table_name).highlight_rows(currently_selected.row,'lightblue1','black')

            # -- Get list of options
            data = self.Compare['Data'][self.test_name]
            self.plot_opts = []
            # -- Stress vs Strain
            for keys in data['Stress'].keys():
                for keye in data['Strain'].keys():
                    self.plot_opts.append('Stress-' + str(keys) + ' vs Strain-' + str(keye))

            # -- Strain vs Time
            for keye in data['Strain'].keys():
                self.plot_opts.append('Strain-' + str(keye) + ' vs Time')

            # -- Stress vs Time
            for keys in data['Stress'].keys():
                self.plot_opts.append('Stress-' + str(keys) + ' vs Time')

            # Find first stress and first strain
            idx1 = 0
            idx2 = 1
            for i in range(len(self.plot_opts)):
                if 'Strain' in self.plot_opts[i] and 'Stress' in self.plot_opts[i] :
                    idx1 = i
                    break
            if data['Test Type'] == 'Relaxation':
                for i in range(len(self.plot_opts)):
                    if 'Stress' in self.plot_opts[i] and 'Time' in self.plot_opts[i] :
                        idx2 = i
                        break

            elif data['Test Type'] == 'Creep':
                for i in range(len(self.plot_opts)):
                    if 'Strain' in self.plot_opts[i] and 'Time' in self.plot_opts[i] :
                        idx2 = i
                        break

            else:
                if data['Control'][0] == 'Strain':
                    for i in range(len(self.plot_opts)):
                        if 'Stress' in self.plot_opts[i] and 'Time' in self.plot_opts[i] :
                            idx2 = i
                            break
                else:
                    for i in range(len(self.plot_opts)):
                        if 'Strain' in self.plot_opts[i] and 'Time' in self.plot_opts[i] :
                            idx2 = i
                            break

            # Create the X Option Menu
            self.optmenu1_viz = ttk.Combobox(
                                        window,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_viz.place(
                                anchor='n', 
                                relx = self.Placement['Visualization']['Combo1'][0], 
                                rely = self.Placement['Visualization']['Combo1'][1]
                                )
            self.optmenu1_viz.set(self.plot_opts[idx1])
            self.tab_att_list.append('self.optmenu1_viz')

            # Create the Y Option Menu
            self.optmenu2_viz = ttk.Combobox(
                                        window,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2_viz.place(
                                anchor='n', 
                                relx = self.Placement['Visualization']['Combo2'][0], 
                                rely = self.Placement['Visualization']['Combo2'][1]
                                )
            self.optmenu2_viz.set(self.plot_opts[idx2])
            self.tab_att_list.append('self.optmenu2_viz')


            # Create the plot button
            self.btn_plot = ttk.Button(
                                    window, 
                                    text = "Plot", 
                                    command = self.plotter_viz,
                                    style = "Modern2.TButton",
                                    width = self.Placement['Visualization']['Button1'][2]
                                    )
            self.btn_plot.place(
                                anchor = 'n', 
                                relx = self.Placement['Visualization']['Button1'][0], 
                                rely = self.Placement['Visualization']['Button1'][1]
                                )
            self.tab_att_list.append('self.btn_plot')

            # Call the plotting function
            self.plotter_viz()

        def eval_all(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Evaluate all tests in the verificaiton set
            #
            #------------------------------------------------------------------

            # Run Compare
            def run_cmd_anly_ver(callback, temp_dir):

                # Get All Tests
                test_names = []
                for i in range(len(self.sheet_ver_viz.data)):
                    test_names.append(self.sheet_ver_viz.data[i][1])

                for i in range(len(test_names)):
                    self.test_name = test_names[i]
                            
                    # Create a model prediction if it doesn't exist
                    if self.test_name not in list(self.Compare['Prediction'].keys()):
                        self.Compare['Prediction'][self.test_name] = None
                    if self.Compare['Prediction'][self.test_name] is None:
                        self.run_compare_anly([self.test_name])
                        self.sheet_ver_viz.set_cell_data(i, -1, round(self.Compare['Prediction'][self.test_name]['Error'],3))
                    
                # Notify when done
                callback()
            
            # Function to display progress bar while running
            def run_compare_start(self):

                # Create the window
                loading = tk.Toplevel(window)
                loading.title("Running Compare")
                loading.geometry("300x100")
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
                        text="Running COMPARE - Please Wait", 
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
                threading.Thread(target=run_cmd_anly_ver, args=(on_task_done,self), daemon=True).start()

                # Wait until loading window is closed
                window.wait_window(loading)

            run_compare_start(self)
        
        def select_all(self, tag):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Select or unselect all tests
            #
            #------------------------------------------------------------------
        
            # Get the selected row and name
            if tag == 'char':
                table_name = "self.sheet_char_viz"
            else:
                table_name = "self.sheet_ver_viz"

            # Check if any are false
            val = False
            for i in range(len(eval(table_name).data)):
                if eval(table_name).data[i][0] == False:
                    val = True
            for i in range(len(eval(table_name).data)):
                eval(table_name).data[i][0] = val
            eval(table_name).redraw()

        def select_all_type(self, tag):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Select or unselect all tests of the same type
            #
            #------------------------------------------------------------------
        
            # Get the selected row and name
            if tag == 'char':
                table_name = "self.sheet_char_viz"
            else:
                table_name = "self.sheet_ver_viz"
            currently_selected = eval(table_name).get_currently_selected()
            self.test_type = eval(table_name).data[currently_selected.row][2]

            # Select All of Same Type
            for i in range(len(eval(table_name).data)):
                if eval(table_name).data[i][2] == self.test_type:
                    eval(table_name).data[i][0] = True
            eval(table_name).redraw()

        def view_data_all(self):
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
            if hasattr(self, 'optmenu3_viz'):
                self.optmenu3_viz.destroy()
            if hasattr(self, 'pred_label'):
                self.pred_label.destroy()
            if hasattr(self, 'raw_label'):
                self.raw_label.destroy()
            if hasattr(self, 'btn_plot'):
                self.btn_plot.destroy()
            if hasattr(self, 'canvas'):
                self.toolbar.destroy()
                self.canvas.get_tk_widget().destroy()
                del self.canvas
            if hasattr(self, 'canvas2'):
                self.toolbar2.destroy()
                self.canvas2.get_tk_widget().destroy()
                del self.canvas2

            # Get List of all tests
            tests_all = []
            row_char = {}
            for i in range(len(self.sheet_char_viz.data)):
                if self.sheet_char_viz.data[i][0] == True:
                    tests_all.append(self.sheet_char_viz.data[i][1])
                    row_char[self.sheet_char_viz.data[i][1]] = i

            row_ver = {}
            for i in range(len(self.sheet_ver_viz.data)):
                if self.sheet_ver_viz.data[i][0] == True:
                    tests_all.append(self.sheet_ver_viz.data[i][1])
                    row_ver[self.sheet_ver_viz.data[i][1]] = i

            if len(tests_all) > 0:
                # Create a model prediction if it doesn't exist
                for test in tests_all:
                    self.test_name = test
                    if test not in list(self.Compare['Prediction'].keys()):
                        self.Compare['Prediction'][self.test_name] = None
                    if self.Compare['Prediction'][self.test_name] is None:
                        self.run_compare_anly([self.test_name])

                        if self.test_name in row_char.keys():
                            self.sheet_char_viz.set_cell_data(row_char[self.test_name], -1, round(self.Compare['Prediction'][self.test_name]['Error'],3))
                            self.sheet_char_viz.redraw()

                        if self.test_name in row_ver.keys():
                            self.sheet_ver_viz.set_cell_data(row_ver[self.test_name], -1, round(self.Compare['Prediction'][self.test_name]['Error'],3))
                            self.sheet_ver_viz.redraw()

                # Remove Highlights from all tables and add the selected row
                for i in range(len(self.sheet_char_viz.data)):
                    self.sheet_char_viz.highlight_rows(i,'white','black')
                for i in range(len(self.sheet_ver_viz.data)):
                    self.sheet_ver_viz.highlight_rows(i,'white','black')

                # -- Get list of options
                data = self.Compare['Data'][self.test_name]
                self.plot_opts_all = None

                # -- Get list of options
                for test in tests_all:

                    self.plot_opts = []

                    # -- Stress vs Strain
                    for keys in data['Stress'].keys():
                        for keye in data['Strain'].keys():
                            self.plot_opts.append('Stress-' + str(keys) + ' vs Strain-' + str(keye))

                    # -- Strain vs Time
                    for keye in data['Strain'].keys():
                        self.plot_opts.append('Strain-' + str(keye) + ' vs Time')

                    # -- Stress vs Time
                    for keys in data['Stress'].keys():
                        self.plot_opts.append('Stress-' + str(keys) + ' vs Time')

                        if self.plot_opts_all is None:
                            self.plot_opts_all = self.plot_opts
                        else:
                            self.plot_opts_all = list(set(self.plot_opts_all) & set(self.plot_opts))

                self.plot_opts = self.plot_opts_all

                # Find first stress and first strain
                idx1 = 0
                for i in range(len(self.plot_opts)):
                    if 'Strain' in self.plot_opts[i] and 'Stress' in self.plot_opts[i] :
                        var = self.plot_opts[i].split(' vs ')
                        dir1 = var[0].split('-')[1].strip()
                        dir2 = var[1].split('-')[1].strip()

                        if dir1 == dir2:
                            idx1 = i
                            break

                # Create the X Option Menu
                self.optmenu3_viz = ttk.Combobox(
                                            window,
                                            values=self.plot_opts,
                                            style="Modern.TCombobox",
                                            state="readonly"
                                            )
                self.optmenu3_viz.place(
                                    anchor='n', 
                                    relx = self.Placement['Visualization']['Combo3'][0], 
                                    rely = self.Placement['Visualization']['Combo3'][1]
                                    )
                self.optmenu3_viz.set(self.plot_opts[idx1])
                self.tab_att_list.append('self.optmenu3_viz')

                # Create the Experiment Label
                self.raw_label = ttk.Label(
                                    window, 
                                    text="Experiments", 
                                    style = "Modern1.TLabel"
                                    )
                self.raw_label.place(
                                    anchor = 'n', 
                                    relx = self.Placement['Visualization']['Label4'][0], 
                                    rely = self.Placement['Visualization']['Label4'][1]
                                    )
                self.tab_att_list.append('self.raw_label')
                
                # Create the Predictions Label
                self.pred_label = ttk.Label(
                                    window, 
                                    text="Predictions", 
                                    style = "Modern1.TLabel"
                                    )
                self.pred_label.place(
                                    anchor = 'n', 
                                    relx = self.Placement['Visualization']['Label5'][0], 
                                    rely = self.Placement['Visualization']['Label5'][1]
                                    )
                self.tab_att_list.append('self.pred_label')



                # Create the plot button
                self.btn_plot = ttk.Button(
                                        window, 
                                        text = "Plot", 
                                        command = self.plotter_viz_all,
                                        style = "Modern2.TButton",
                                        width = self.Placement['Visualization']['Button1'][2]
                                        )
                self.btn_plot.place(
                                    anchor = 'n', 
                                    relx = self.Placement['Visualization']['Button1'][0], 
                                    rely = self.Placement['Visualization']['Button1'][1]
                                    )
                self.tab_att_list.append('self.btn_plot')

                # Call the plotting function
                self.tests_all = tests_all
                self.plotter_viz_all()

        # Destroy existing widgets
        if hasattr(self,'sheet_char_viz'):
            self.sheet_char_viz.destroy()
        if hasattr(self,'char_label'):
            self.char_label.destroy()

        # Create the label
        self.char_label = ttk.Label(
                                    window, 
                                    text="Characterization Set:  Global Error = " + f"{self.Compare['Global Error']:.3e}", 
                                    style = "Modern1.TLabel"
                                    )
        self.char_label.place(
                            anchor = 'n', 
                            relx = self.Placement['Visualization']['Label2'][0], 
                            rely = self.Placement['Visualization']['Label2'][1]
                            )
        self.tab_att_list.append('self.char_label')
        self.loc_att_list.append('self.char_label')
        
        # Get the tests in the characterization set
        tests = list(self.Compare['Characterization'].keys())

        # Set the column names
        Cols = [' ', 'Name', 'Type', 'Weight','Error']

        # Create the sheet
        self.sheet_char_viz = tksheet.Sheet(
                                            window, 
                                            total_rows = len(tests), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Visualization']['Sheet1'][2], 
                                            height = self.Placement['Visualization']['Sheet1'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Visualization']['Sheet1'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Visualization']['Sheet1'][4],"bold")
                                            )
        self.sheet_char_viz.place(
                                anchor = 'n', 
                                relx = self.Placement['Visualization']['Sheet1'][0], 
                                rely = self.Placement['Visualization']['Sheet1'][1]
                                )

        # Format the sheet
        self.tab_att_list.append('self.sheet_char_viz')
        self.sheet_char_viz.change_theme("blue")
        self.sheet_char_viz.set_index_width(0)

        # Enable Bindings
        self.sheet_char_viz.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_char_viz.extra_bindings([("cell_select", lambda event: deselect_sheet(event, self, 'sheet_char_viz'))])
        self.sheet_char_viz.popup_menu_add_command('View Data', lambda : view_data(self,'char'), table_menu = True, index_menu = True, header_menu = True)  
        self.sheet_char_viz.popup_menu_add_command('Select All', lambda : select_all(self,'char'), table_menu = True, index_menu = True, header_menu = True) 
        self.sheet_char_viz.popup_menu_add_command('Select All of Same Type', lambda : select_all_type(self,'char'), table_menu = True, index_menu = True, header_menu = True) 
        self.sheet_char_viz.popup_menu_add_command('View Selected Data', lambda : view_data_all(self), table_menu = True, index_menu = True, header_menu = True)   
        
        # Set Column Widths
        self.sheet_char_viz.column_width(column = 0, width = self.Placement['Visualization']['Sheet1'][5], redraw = True)
        self.sheet_char_viz.column_width(column = 1, width = self.Placement['Visualization']['Sheet1'][6], redraw = True)
        self.sheet_char_viz.column_width(column = 2, width = self.Placement['Visualization']['Sheet1'][7], redraw = True)
        self.sheet_char_viz.column_width(column = 3, width = self.Placement['Visualization']['Sheet1'][8], redraw = True)
        self.sheet_char_viz.column_width(column = 4, width = self.Placement['Visualization']['Sheet1'][9], redraw = True)
        self.sheet_char_viz.checkbox("A",checked=False)
        self.sheet_char_viz.table_align(align = 'c',redraw=True)

        # Populate Data
        for i in range(len(tests)):
            self.sheet_char_viz.set_cell_data(i,1, tests[i])
            self.sheet_char_viz.set_cell_data(i,2, self.Compare['Data'][tests[i]]['Test Type'])
            self.sheet_char_viz.set_cell_data(i,3,self.Compare['Data'][tests[i]]['RelWeight'])
            self.sheet_char_viz.set_cell_data(i,4,round(self.Compare['Prediction'][tests[i]]['Error'],3))

        # Delete existing widgets
        if hasattr(self,'sheet_ver_viz'):
            self.sheet_ver_viz.destroy()
        if hasattr(self,'ver_label'):
            self.ver_label.destroy()

        # Create the label
        self.ver_label = ttk.Label(
                                window, 
                                text="Verification Set:", 
                                style = "Modern1.TLabel"
                                )
        self.ver_label.place(
                            anchor = 'n', 
                            relx = self.Placement['Visualization']['Label3'][0], 
                            rely = self.Placement['Visualization']['Label3'][1]
                            )
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
        Cols = [' ', 'Name', 'Type', 'Error']
        
        # Create the sheet
        self.sheet_ver_viz = tksheet.Sheet(
                                            window, 
                                            total_rows = len(tests_ver), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Visualization']['Sheet2'][2], 
                                            height = self.Placement['Visualization']['Sheet2'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Visualization']['Sheet2'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Visualization']['Sheet2'][4],"bold")
                                            )
        self.sheet_ver_viz.place(
                                anchor = 'n', 
                                relx = self.Placement['Visualization']['Sheet2'][0], 
                                rely = self.Placement['Visualization']['Sheet2'][1]
                                )
        self.tab_att_list.append('self.sheet_ver_viz')

        # Format the sheet
        self.sheet_ver_viz.change_theme("blue")
        self.sheet_ver_viz.set_index_width(0)

        # Enable Bindings
        self.sheet_ver_viz.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_ver_viz.extra_bindings([("cell_select", lambda event: deselect_sheet(event, self, 'sheet_ver_viz'))])
        self.sheet_ver_viz.popup_menu_add_command('Evaluate All', lambda : eval_all(self), table_menu = True, index_menu = True, header_menu = True)
        self.sheet_ver_viz.popup_menu_add_command('View Data', lambda : view_data(self,'ver'), table_menu = True, index_menu = True, header_menu = True)
        self.sheet_ver_viz.popup_menu_add_command('Select All', lambda : select_all(self,'ver'), table_menu = True, index_menu = True, header_menu = True)   
        self.sheet_ver_viz.popup_menu_add_command('Select All of Same Type', lambda : select_all_type(self,'ver'), table_menu = True, index_menu = True, header_menu = True)   
        self.sheet_ver_viz.popup_menu_add_command('View Selected Data', lambda : view_data_all(self), table_menu = True, index_menu = True, header_menu = True)   
        
        # Set Column Widths
        self.sheet_ver_viz.column_width(column = 0, width = self.Placement['Visualization']['Sheet2'][5], redraw = True)
        self.sheet_ver_viz.column_width(column = 1, width = self.Placement['Visualization']['Sheet2'][6], redraw = True)
        self.sheet_ver_viz.column_width(column = 2, width = self.Placement['Visualization']['Sheet2'][7], redraw = True)
        self.sheet_ver_viz.column_width(column = 3, width = self.Placement['Visualization']['Sheet2'][7], redraw = True)
        self.sheet_ver_viz.checkbox("A",checked=False)
        self.sheet_ver_viz.table_align(align = 'c',redraw=True)

        # Populate Data
        for i in range(len(tests_ver)):
            self.sheet_ver_viz.set_cell_data(i,1, tests_ver[i])
            self.sheet_ver_viz.set_cell_data(i,2, self.Compare['Data'][tests_ver[i]]['Test Type'])
            if tests_ver[i] in list(self.Compare['Prediction'].keys()):
                if self.Compare['Prediction'][tests_ver[i]] is not None:
                    self.sheet_ver_viz.set_cell_data(i,3,round(self.Compare['Prediction'][tests_ver[i]]['Error'],3))

    # Check that tests exist in the characterization set
    try:
        # Get Global Error
        glob_err = self.Compare['Global Error']

        # Check fo characterization data
        if 'Characterization' in list(self.Compare.keys()):
            if len(list(self.Compare['Characterization'].keys())) > 0:
                update_table()
            else:
                messagebox.showerror(message = 'No tests have been adde the the charicterization set.')
    
    # Check that model parameters have been set
    except:
        messagebox.showerror(message = 'Model parameters have not been set. Use the Optimize or Analyze tabs to set the model parameters and execute.')