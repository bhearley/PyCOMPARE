#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateCharacterizationTab.py
#
# PURPOSE: Create the characterization tab. The Characterization tab allows users to view the data that has been uploaded
#          for characterization and edit the reduce data
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateCharacterizationTab(self,window):
    # Import Modules
    import math
    from tkinter import messagebox
    from tkinter import ttk
    import tksheet

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []

    # Initialize button press
    self.clicked = 0

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
        widget = event.widget

        # If the click is *not* inside the sheet, deselect it
        try:
            if widget != self.sheet_char.MT:
                self.sheet_char.deselect("all")
        except:
            pass
            
        try:
            if widget != self.stage_table_char.MT:
                self.stage_table_char.deselect("all")
        except:
            pass

    window.bind_all("<Button-1>", on_click, add="+")


    def update_table(init_flag):
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
            for att in self.atts['Characterization']['Local']:
                if att == "self.sheet_char":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass
            
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
            self.optmenu1_plt_char = ttk.Combobox(
                                        self.nb_tab_tab2,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt_char.configure(font = self.style_man['Combo'])
            self.optmenu1_plt_char.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu1_plt_char.place(
                                    anchor='n', 
                                    relx = self.Placement['Characterization']['ComboX'][0], 
                                    rely = self.Placement['Characterization']['ComboX'][1],
                                    relwidth = self.Placement['Characterization']['ComboX'][2], 
                                    relheight = self.Placement['Characterization']['ComboX'][3]
                                    )
            self.optmenu1_plt_char.set(self.plot_opts[idx1]) 
            if "self.optmenu1_plt_char" not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.optmenu1_plt_char')

            # Create the vs Label
            self.plot_label_char = ttk.Label(
                                    self.nb_tab_tab2, 
                                    text="vs",
                                    style = 'Modern1.TLabel' 
                                    )
            self.plot_label_char.place(
                                anchor = 'n', 
                                relx = self.Placement['Characterization']['LabelVS'][0], 
                                rely = self.Placement['Characterization']['LabelVS'][1]
                                )
            if 'self.plot_label_char' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.plot_label_char')

            # Create the Y drop down menu
            self.optmenu2_plt_char = ttk.Combobox(
                                        self.nb_tab_tab2,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2_plt_char.configure(font = self.style_man['Combo'])
            self.optmenu2_plt_char.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu2_plt_char.place(
                                    anchor='n', 
                                    relx = self.Placement['Characterization']['ComboY'][0], 
                                    rely = self.Placement['Characterization']['ComboY'][1],
                                    relwidth = self.Placement['Characterization']['ComboY'][2], 
                                    relheight = self.Placement['Characterization']['ComboY'][3]
                                    )
            self.optmenu2_plt_char.set(self.plot_opts[idx2])
            if "self.optmenu2_plt_char" not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.optmenu2_plt_char')

            # Create the plot button
            self.btn_plot_char = ttk.Button(
                                self.nb_tab_tab2, 
                                text = "Plot", 
                                command = self.plotter_char, 
                                style = "Modern2.TButton",
                                )
            self.btn_plot_char.place(
                                anchor = 'n', 
                                relx = self.Placement['Characterization']['ButtonPlot'][0], 
                                rely = self.Placement['Characterization']['ButtonPlot'][1],
                                relwidth = self.Placement['Characterization']['ButtonPlot'][2], 
                                relheight = self.Placement['Characterization']['ButtonPlot'][3]
                                )
            if "self.btn_plot_char" not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.btn_plot_char')
            
            # Create the stage table label
            self.stage_label_char = ttk.Label(
                                        self.nb_tab_tab2, 
                                        text="Stage Table:", 
                                        style = "Modern1.TLabel"
                                        )
            self.stage_label_char.place(
                                anchor = 'nw', 
                                relx = self.Placement['Characterization']['LabelStage'][0], 
                                rely = self.Placement['Characterization']['LabelStage'][1]
                                )
            if "self.stage_label_char" not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.stage_label_char')

            # Create the stage table
            Cols = ['Type', 'Direction','Control','Load Rate','Target','End Time (s)']
            self.stage_table_char = tksheet.Sheet(
                                            self.nb_tab_tab2, 
                                            total_rows = len(self.Compare['Data'][self.test_name]['Stage Type']), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                            )
            self.stage_table_char.place(
                                anchor = 'nw', 
                                relx = self.Placement['Characterization']['SheetSTG'][0], 
                                rely = self.Placement['Characterization']['SheetSTG'][1],
                                relwidth = self.Placement['Characterization']['SheetSTG'][2], 
                                relheight = self.Placement['Characterization']['SheetSTG'][3],
                                )
            if "self.stage_table_char" not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.stage_table_char')

            # Format the sheet
            self.stage_table_char.change_theme("blue")
            self.stage_table_char.set_index_width(0)
            window.update_idletasks()
            total_width = self.stage_table_char.winfo_width()
            self.stage_table_char.column_width(column = 0, width = int(total_width*self.Placement['Characterization']['SheetSTG'][4]), redraw = True)
            self.stage_table_char.column_width(column = 1, width = int(total_width*self.Placement['Characterization']['SheetSTG'][5]), redraw = True)
            self.stage_table_char.column_width(column = 2, width = int(total_width*self.Placement['Characterization']['SheetSTG'][6]), redraw = True)
            self.stage_table_char.column_width(column = 3, width = int(total_width*self.Placement['Characterization']['SheetSTG'][7]), redraw = True)
            self.stage_table_char.column_width(column = 4, width = int(total_width*self.Placement['Characterization']['SheetSTG'][8]), redraw = True)
            self.stage_table_char.column_width(column = 5, width = int(total_width*self.Placement['Characterization']['SheetSTG'][9]), redraw = True)
            self.stage_table_char.table_align(align = 'c',redraw=True)

            # Enable Bindings
            self.stage_table_char.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys")
            
            # Set stage table cell values
            for i in range(len(self.Compare['Data'][self.test_name]['Stage Type'])):
                self.stage_table_char.set_cell_data(i,0,self.Compare['Data'][self.test_name]['Stage Type'][i])
                self.stage_table_char.set_cell_data(i,1,self.Compare['Data'][self.test_name]['Loading Direction'][i])
                self.stage_table_char.set_cell_data(i,2,self.Compare['Data'][self.test_name]['Control'][i])
                self.stage_table_char.set_cell_data(i,3,str(round_sig(self.Compare['Data'][self.test_name]['Load Rate'][i][0],2)) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Load Rate'][i][1])
                self.stage_table_char.set_cell_data(i,4,str(round_sig(self.Compare['Data'][self.test_name]['Target'][i][0],2)) 
                                               + ' ' + self.Compare['Data'][self.test_name]['Target'][i][1])
                self.stage_table_char.set_cell_data(i,5,self.Compare['Data'][self.test_name]['Time'][self.Compare['Data'][self.test_name]['Stage Divisions'][i]])
                if self.Compare['Data'][self.test_name]['Reduced Data']['Time'] is not None:
                    self.stage_table_char.set_cell_data(i,6,self.Compare['Data'][self.test_name]['Stage Divisions'][i])
                else:
                    self.stage_table_char.set_cell_data(i,6,len(self.Compare['Data'][self.test_name]['Time']))
            self.stage_table_char.redraw()

            # Call the plotting function
            self.plotter_char()

        def view_all_data(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Create the plots to view all characterization data on the
            #            same plot.
            #
            #----------------------------------------------------------------------

            # Delete existing widgets
            for att in self.atts['Characterization']['Local']:
                if att == "self.sheet_char":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass
            
            # Get list of options
            self.plot_opts = ['Tensile', 'Creep', 'Relaxation','Generic','All']

            # Create the plot option menu
            self.optmenu1_plt_char = ttk.Combobox(
                                        self.nb_tab_tab2,
                                        values=self.plot_opts,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu1_plt_char.configure(font = self.style_man['Combo'])
            self.optmenu1_plt_char.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu1_plt_char.place(
                                    anchor='n', 
                                    relx = self.Placement['Characterization']['ComboPlot'][0], 
                                    rely = self.Placement['Characterization']['ComboPlot'][1],
                                    relwidth = self.Placement['Characterization']['ComboPlot'][2], 
                                    relheight = self.Placement['Characterization']['ComboPlot'][3]
                                    )
            self.optmenu1_plt_char.set(self.plot_opts[0])
            self.optmenu1_plt_char.bind("<<ComboboxSelected>>",  lambda event:self.plotter_all_char(event))
            if 'self.optmenu1_plt_char' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append("self.optmenu1_plt_char")

            # Call the plotting function
            self.plotter_all_char(self.plot_opts[0])

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
                if hasattr(self,"canvas_char"):
                    self.toolbar_char.destroy()
                    self.canvas_char.get_tk_widget().destroy()
                    del self.canvas_char

                atts = ['self.optmenu1_plt_char', 'self.btn_loc3', 'self.btn_loc4', 'self.btn_loc5']
                for widget in atts:
                    try:
                        eval(widget).destroy()
                    except:
                        pass

                # Update flags
                self.db_init = 0
                self.char_init = 0
                self.viz_init = 0

                # Update the table
                update_table(self.char_init)


        # Create the test table label
        if hasattr(self,"char_label") == False:
            self.char_label = ttk.Label(
                                        self.nb_tab_tab2, 
                                        text="Characterization Set:",
                                        style = "Modern1.TLabel" 
                                        )
            self.char_label.place(
                                anchor = 'w', 
                                relx = self.Placement['Characterization']['LabelChar'][0], 
                                rely = self.Placement['Characterization']['LabelChar'][1]
                                )
            if 'self.char_label' not in self.atts['Characterization']['Permanent']:
                self.atts['Characterization']['Permanent'].append('self.char_label')

        if init_flag == 0:
            # Delete existing widgets
            for att in self.atts['Characterization']['Local']:
                if att == "self.sheet_char":
                    continue
                try:
                    eval(f"{att}").destroy()
                except:
                    pass

            try:
                self.canvas_char.get_tk_widget().destroy()
                del self.canvas_char
            except:
                pass

        if (init_flag == 1 and hasattr(self, 'sheet_char') == False) or init_flag == 0:

            # Create the test table
            tests = list(self.Compare['Characterization'].keys())
            Cols = ['Name', 'Type', 'Temp (°C)', 'Direction','Control','Load Rate','Angle (°)','Weight']
            self.sheet_char = tksheet.Sheet(
                                            self.nb_tab_tab2, 
                                            total_rows = len(tests), 
                                            total_columns = len(Cols), 
                                            headers = Cols,        
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                            )
            self.sheet_char.place(
                                anchor = 'nw', 
                                relx = self.Placement['Characterization']['SheetChar'][0], 
                                rely = self.Placement['Characterization']['SheetChar'][1],
                                relwidth = self.Placement['Characterization']['SheetChar'][2], 
                                relheight = self.Placement['Characterization']['SheetChar'][3], 
                                )
            if 'self.sheet_char' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.sheet_char')

            # Format the sheet
            self.sheet_char.change_theme("blue")
            self.sheet_char.set_index_width(0)
            window.update_idletasks()
            total_width = self.sheet_char.winfo_width()
            self.sheet_char.column_width(column = 0, width = int(total_width*self.Placement['Characterization']['SheetChar'][4]), redraw = True)
            self.sheet_char.column_width(column = 1, width = int(total_width*self.Placement['Characterization']['SheetChar'][5]), redraw = True)
            self.sheet_char.column_width(column = 2, width = int(total_width*self.Placement['Characterization']['SheetChar'][6]), redraw = True)
            self.sheet_char.column_width(column = 3, width = int(total_width*self.Placement['Characterization']['SheetChar'][7]), redraw = True)
            self.sheet_char.column_width(column = 4, width = int(total_width*self.Placement['Characterization']['SheetChar'][8]), redraw = True)
            self.sheet_char.column_width(column = 5, width = int(total_width*self.Placement['Characterization']['SheetChar'][9]), redraw = True)
            self.sheet_char.column_width(column = 6, width = int(total_width*self.Placement['Characterization']['SheetChar'][10]), redraw = True)
            self.sheet_char.column_width(column = 7, width = int(total_width*self.Placement['Characterization']['SheetChar'][11]), redraw = True)
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
                self.sheet_char.set_cell_data(i,5,str(round_sig(self.Compare['Data'][tests[i]]['Load Rate'][0][0],2)) + ' ' + self.Compare['Data'][tests[i]]['Load Rate'][0][1] )
                self.sheet_char.set_cell_data(i,6,self.Compare['Data'][tests[i]]['Angle'])
                self.sheet_char.set_cell_data(i,7,self.Compare['Data'][tests[i]]['RelWeight'])

        self.char_init = 1

    # Update the table if characterization data exists
    if 'Characterization' in list(self.Compare.keys()):
        if len(list(self.Compare['Characterization'].keys())) > 0:
            update_table(self.char_init)
        else:
            messagebox.showinfo(title= '', message = 'No tests have been added to the characterization set. Use the Database tab to add tests for characterization.')