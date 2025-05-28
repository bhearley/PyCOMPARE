#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateCharacterizationTab.py
#
# PURPOSE: Create the characterization tab. The Characterization tab allows users to view the data that has been uploaded
#          for characterization and edit the reduce data
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateCharacterizationTab(self,window,frmt):
    # Import Modules
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import ttk
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteTab

    #Unpack Formatting
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

    # Initialize button press
    self.clicked = 0

    def update_table():
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Update the characterization set table.
        #
        #--------------------------------------------------------------------------

        def view_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view characterization data.
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
                self.stage_label.destroy()
            if hasattr(self, 'stage_table'):
                self.stage_table.destroy()
            
            # Get the selected row and name
            currently_selected = self.sheet_char.get_currently_selected()
            self.test_name = self.sheet_char.data[currently_selected.row][0]
            self.test_type = self.sheet_char.data[currently_selected.row][1]

            # Remove Highlights from all rows and highlight the selected row
            for i in range(len(self.sheet_char.data)):
                self.sheet_char.highlight_rows(i,'white','black')
            self.sheet_char.highlight_rows(currently_selected.row,'lightblue1','black')

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
                                    relx = self.Placement['Characterization']['Combo1'][0], 
                                    rely = self.Placement['Characterization']['Combo1'][1]
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
                                relx = self.Placement['Characterization']['Label1'][0], 
                                rely = self.Placement['Characterization']['Label1'][1]
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
                                    relx = self.Placement['Characterization']['Combo2'][0], 
                                    rely = self.Placement['Characterization']['Combo2'][1]
                                    )
            self.optmenu2_plt.set(self.plot_opts[idx2])
            self.tab_att_list.append('self.optmenu2_plt')

            # Create the plot button
            self.btn_plot = ttk.Button(
                                window, 
                                text = "Plot", 
                                command = self.plotter, 
                                style = "Modern2.TButton",
                                width = self.Placement['Characterization']['Button1'][2], 
                                )
            self.btn_plot.place(
                                anchor = 'n', 
                                relx = self.Placement['Characterization']['Button1'][0], 
                                rely = self.Placement['Characterization']['Button1'][1]
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
                                relx = self.Placement['Characterization']['Label2'][0], 
                                rely = self.Placement['Characterization']['Label2'][1]
                                )
            self.tab_att_list.append('self.stage_label')
            Cols = ['Type', 'Direction','Control','Load Rate','Target','End Time (s)']
            self.stage_table = tksheet.Sheet(
                                            window, 
                                            total_rows = len(self.Compare['Data'][self.test_name]['Stage Type']), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Characterization']['Sheet1'][2], 
                                            height = self.Placement['Characterization']['Sheet1'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Characterization']['Sheet1'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Characterization']['Sheet1'][4],"bold"),
                                            #table_bg = 'red' # For checking formatting only
                                            )
            self.stage_table.place(
                                anchor = 'nw', 
                                relx = self.Placement['Characterization']['Sheet1'][0], 
                                rely = self.Placement['Characterization']['Sheet1'][1]
                                )
            self.tab_att_list.append('self.stage_table')

            # Format the sheet
            self.stage_table.change_theme("blue")
            self.stage_table.set_index_width(0)
            self.stage_table.column_width(column = 0, width = self.Placement['Characterization']['Sheet1'][5], redraw = True)
            self.stage_table.column_width(column = 1, width = self.Placement['Characterization']['Sheet1'][6], redraw = True)
            self.stage_table.column_width(column = 2, width = self.Placement['Characterization']['Sheet1'][7], redraw = True)
            self.stage_table.column_width(column = 3, width = self.Placement['Characterization']['Sheet1'][8], redraw = True)
            self.stage_table.column_width(column = 4, width = self.Placement['Characterization']['Sheet1'][9], redraw = True)
            self.stage_table.column_width(column = 5, width = self.Placement['Characterization']['Sheet1'][10], redraw = True)
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
                self.stage_table.set_cell_data(i,5,self.Compare['Data'][self.test_name]['Time'][self.Compare['Data'][self.test_name]['Stage Divisions'][i]])
                if self.Compare['Data'][self.test_name]['Reduced Data']['Time'] is not None:
                    self.stage_table.set_cell_data(i,6,self.Compare['Data'][self.test_name]['Stage Divisions'][i])
                else:
                    self.stage_table.set_cell_data(i,6,len(self.Compare['Data'][self.test_name]['Time']))
            self.stage_table.redraw()

            # Call the plotting function
            self.plotter()

        def view_all_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view all characterization data on the
            #            same plot.
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
                                    relx = self.Placement['Characterization']['Combo3'][0], 
                                    rely = self.Placement['Characterization']['Combo3'][1]
                                    )
            self.optmenu1_plt.set(self.plot_opts[0])
            self.optmenu1_plt.bind("<<ComboboxSelected>>",  lambda event:self.plotter_all(event, 'sheet_char'))
            self.tab_att_list.append("self.optmenu1_plt")

            # Call the plotting function
            self.plotter_all(self.plot_opts[0], 'sheet_char')

        def delete_test(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Delete a test from the characterization set.
            #
            #----------------------------------------------------------------------
            
            # Get the selected row and name
            currently_selected = self.sheet_char.get_currently_selected()
            self.test_name = self.sheet_char.data[currently_selected.row][0]

            # Ask user to confirm delete
            askyn = messagebox.askyesno(title = 'Delete test', message = 'Do you want to delete test ' + self.test_name  + ' from the characterization set?')
            if askyn == True:
                # Delete from characterization set
                del self.Compare['Characterization'][self.test_name]

                # Delete existin widgets
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

        # Destroy test table if it exists
        if hasattr(self,'sheet_char'):
            self.sheet_char.destroy()

        # Create the test table
        self.char_label = ttk.Label(
                                    window, 
                                    text="Characterization Set:",
                                    style = "Modern1.TLabel" 
                                    )
        self.char_label.place(
                            anchor = 'w', 
                            relx = self.Placement['Characterization']['Label3'][0], 
                            rely = self.Placement['Characterization']['Label3'][1]
                            )
        self.loc_att_list.append('self.char_label')
        self.tab_att_list.append('self.char_label')

        tests = list(self.Compare['Characterization'].keys())
        Cols = ['Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)','Weight']
        self.sheet_char = tksheet.Sheet(
                                        window, 
                                        total_rows = len(tests), 
                                        total_columns = len(Cols), 
                                        headers = Cols,
                                        width = self.Placement['Characterization']['Sheet2'][2], 
                                        height = self.Placement['Characterization']['Sheet2'][3], 
                                        show_x_scrollbar = False, 
                                        show_y_scrollbar = True,
                                        font = ('Segoe UI',self.Placement['Characterization']['Sheet2'][4],"normal"),
                                        header_font = ('Segoe UI',self.Placement['Characterization']['Sheet2'][4],"bold"),
                                        #table_bg = 'blue' # For formatting purposes only
                                        )
        self.sheet_char.place(
                            anchor = 'nw', 
                            relx = self.Placement['Characterization']['Sheet2'][0], 
                            rely = self.Placement['Characterization']['Sheet2'][1]
                            )
        self.tab_att_list.append('self.sheet_char')

        # Format the sheet
        self.sheet_char.change_theme("blue")
        self.sheet_char.set_index_width(0)
        self.sheet_char.column_width(column = 0, width = self.Placement['Characterization']['Sheet2'][5], redraw = True)
        self.sheet_char.column_width(column = 1, width = self.Placement['Characterization']['Sheet2'][6], redraw = True)
        self.sheet_char.column_width(column = 2, width = self.Placement['Characterization']['Sheet2'][7], redraw = True)
        self.sheet_char.column_width(column = 3, width = self.Placement['Characterization']['Sheet2'][8], redraw = True)
        self.sheet_char.column_width(column = 4, width = self.Placement['Characterization']['Sheet2'][9], redraw = True)
        self.sheet_char.column_width(column = 5, width = self.Placement['Characterization']['Sheet2'][10], redraw = True)
        self.sheet_char.column_width(column = 6, width = self.Placement['Characterization']['Sheet2'][11], redraw = True)
        self.sheet_char.column_width(column = 7, width = self.Placement['Characterization']['Sheet2'][12], redraw = True)
        self.sheet_char.table_align(align = 'c',redraw=True)
        self.sheet_char.extra_bindings([("cell_select", self.cell_select_char)])

        # Enable bindings
        self.sheet_char.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys", "right_click_popup_menu")
        self.sheet_char.popup_menu_add_command('View Data', lambda : view_data(self), table_menu = True, index_menu = True, header_menu = True)
        self.sheet_char.popup_menu_add_command('View All Data', lambda : view_all_data(self), table_menu = True, index_menu = True, header_menu = True)
        self.sheet_char.popup_menu_add_command('Delete From Set', lambda : delete_test(self), table_menu = True, index_menu = True, header_menu = True)   
        
        # Populate test cell data
        for i in range(len(tests)):
            self.sheet_char.set_cell_data(i,0, tests[i])
            self.sheet_char.set_cell_data(i,1, self.Compare['Data'][tests[i]]['Test Type'])
            self.sheet_char.set_cell_data(i,2, self.Compare['Data'][tests[i]]['Temperature'][0])
            ldir = ''
            ldir_list = []
            for j in range(len(self.Compare['Data'][tests[i]]['Loading Direction'])):
                if self.Compare['Data'][tests[i]]['Loading Direction'][j] not in ldir_list:
                    ldir_list.append(self.Compare['Data'][tests[i]]['Loading Direction'][j])
            for j in range(len(ldir_list)):
                ldir = ldir + str(ldir_list[j]) + ', '
            self.sheet_char.set_cell_data(i,3, ldir[:len(ldir)-2])
            self.sheet_char.set_cell_data(i,4,self.Compare['Data'][tests[i]]['Control'][0])
            self.sheet_char.set_cell_data(i,5,str(self.Compare['Data'][tests[i]]['Load Rate'][0][0]) + ' ' + self.Compare['Data'][tests[i]]['Load Rate'][0][1] )
            self.sheet_char.set_cell_data(i,6,self.Compare['Data'][tests[i]]['Angle'])
            self.sheet_char.set_cell_data(i,7,self.Compare['Data'][tests[i]]['RelWeight'])

    # Update the table if characterization data exists
    if 'Characterization' in list(self.Compare.keys()):
        if len(list(self.Compare['Characterization'].keys())) > 0:
            update_table()
        else:
            messagebox.showinfo(title= '', message = 'No tests have been added to the characterization set. Use the Database tab to add tests for characterization.')