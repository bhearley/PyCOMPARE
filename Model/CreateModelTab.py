#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateModelTab.py
#
# PURPOSE: Create the Optimize Model tab. The Optimize Model tab allows users to define a model to fit and run COMPARE
#          to determine the optimal parameter values
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateModelTab(self,window):
    # Import Modules
    import copy
    import json
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import simpledialog
    from tkinter import ttk 
    from tkinter import scrolledtext 
    import tksheet
    
    # Import Functions
    from Model.UpdateModelData import UpdateModelData

    # Initialize Model
    if 'Model' not in self.Compare.keys():
        self.Compare['Model'] = {}
        self.Compare['Model']['Status'] = 0

    if 'Model ID' not in self.Compare.keys() == False:
        self.Compare['Model ID'] = None

    # Get available model information
    if hasattr(self,"model_info_all") == False:
        with open(self.Compare['Paths']['Model Library'], 'r', encoding='utf8') as f:
            self.model_info_all = json.load(f)

    self.optimize = 0
    self.clicked = 0

    # Preallocate Saved Models
    if 'Model Library' not in self.Compare.keys():
        self.Compare['Model Library'] = {}

    # Define Available Models
    self.Models = list(self.model_info_all.keys())

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
            if widget != self.sheet1_opt.MT:
                self.sheet1_opt.deselect("all")
        except:
            pass

        try:
            if widget != self.sheet2_opt.MT:
                self.sheet2_opt.deselect("all")
        except:
            pass

    # Bind the deselect function to the window
    window.bind_all("<Button-1>", on_click, add="+")

    def change_model(value):
        #----------------------------------------------------------------------
        #
        #   PURPOSE: Recreate page based on model choice.
        #
        #----------------------------------------------------------------------

        def update_reversible_table(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Update the reversible model parameters table.
            #
            #------------------------------------------------------------------

            # Delete table if it exists
            if hasattr(self,"sheet1_opt"):
                if hasattr(self,"res_flag1") == True:
                    if self.res_flag1 == 0:
                        # Store data
                        self.sheet1_opt_data = self.sheet1_opt.data
                else:
                    # Store data
                    self.sheet1_opt_data = self.sheet1_opt.data

                # Delete sheet
                self.sheet1_opt.destroy()
                del self.sheet1_opt

            # Check if previous data exists
            if 'Model' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'VE_Param' in list(self.Compare['Model'].keys()):
                    if hasattr(self,"res_flag1") == True:
                        if self.res_flag1 == 0:
                            self.sheet1_opt_data = self.Compare['Model']['VE_Param']
                        else:
                            self.res_flag1 = 0
                    else:
                        self.sheet1_opt_data = self.Compare['Model']['VE_Param']

            if hasattr(self,"sheet1_opt_data") == False:
                self.sheet1_opt_data = []

            # Set the columns
            Cols = ['Parameter', 'Units','Lower Bound','Initial Guess','Upper Bound','Active/Passive', 'COMPARE']

            # Create the table
            self.sheet1_opt = tksheet.Sheet(
                                        self.nb_tab_tab3, 
                                        total_rows = len(self.Params_VE), 
                                        total_columns = len(Cols), 
                                        headers = Cols,
                                        show_x_scrollbar = False, 
                                        show_y_scrollbar = True,
                                        font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                        header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                        )
            self.sheet1_opt.place(
                            anchor = 'n', 
                            relx = self.Placement['Optimization']['Sheet1'][0], 
                            rely = self.Placement['Optimization']['Sheet1'][1],
                            relwidth = self.Placement['Optimization']['Sheet1'][2], 
                            relheight = self.Placement['Optimization']['Sheet1'][3], 
                            )
            if 'self.sheet1_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.sheet1_opt') 

            # Format Sheet
            self.sheet1_opt.change_theme("blue")
            self.sheet1_opt.set_index_width(0)

            # Set Bindings
            def sort_cols(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Custom soring function.
                #
                #----------------------------------------------------------------------

                # Get the currently selected element
                currently_selected = self.sheet1_opt.get_currently_selected()
                
                # Get the list of values
                sort_list = []
                for i in range(self.sheet1_opt.visible_rows[1]):
                    sort_list.append(self.sheet1_opt.data[i][currently_selected.column])
                index_list = sorted(range(len(sort_list)), key=lambda k: sort_list[k])
                
                # Rewrite the table
                temp_data = copy.deepcopy(self.sheet1_opt.data)
                for i in range(self.sheet1_opt.visible_rows[1]):
                    for j in range(self.sheet1_opt.visible_columns[1]):
                        self.sheet1_opt.set_cell_data(i,j,temp_data[index_list[i]][j])
                self.sheet1_opt.redraw()

            def all_active(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Set all parameters to active.
                #
                #----------------------------------------------------------------------

                # Set all rows to Active
                for i in range(len(self.sheet1_opt.data)):
                    self.sheet1_opt.set_cell_data(i,5, 'Active')

            def all_passive(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Set all parameters to passive.
                #
                #----------------------------------------------------------------------

                # Set all rows to Passive
                for i in range(len(self.sheet1_opt.data)):
                    self.sheet1_opt.set_cell_data(i,5, 'Passive')

            def genbounds(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Automatically generate bounds.
                #
                #----------------------------------------------------------------------

                # Get the bounds slider value
                value = float(self.slider1_opt.get())
                if value == 0:
                    value = 5

                # Generate bounds
                for i in range(len(self.sheet1_opt.data)):
                    try:
                        val = float(self.sheet1_opt.data[i][3])
                        lb = val-val*float(value)/100
                        self.sheet1_opt.set_cell_data(i,2, '{:0.4e}'.format(lb))
                        ub = val+val*float(value)/100
                        self.sheet1_opt.set_cell_data(i,4, '{:0.4e}'.format(ub))
                        self.sheet1_opt.redraw() 

                        # -- Check lower bound
                        self.sheet1_opt.highlight((i,2),fg = 'black', bg = 'white')
                        try:
                            if float(self.sheet1_opt.data[i][2]) > float(self.sheet1_opt.data[i][3]):
                                self.sheet1_opt.highlight((i,2),fg = 'red', bg = 'white')
                        except:
                            pass

                        # -- Check upper bound
                        self.sheet1_opt.highlight((i,4),fg = 'black', bg = 'white')
                        try:
                            if float(self.sheet1_opt.data[i][4]) < float(self.sheet1_opt.data[i][3]):
                                self.sheet1_opt.highlight((i,4),fg = 'red', bg = 'white')
                        except:
                            pass
                    except:
                        pass

            
            self.sheet1_opt.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
            self.sheet1_opt.popup_menu_add_command('Sort', lambda : sort_cols(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet1_opt.popup_menu_add_command('Change All to Active', lambda : all_active(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet1_opt.popup_menu_add_command('Change All to Passive', lambda : all_passive(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet1_opt.popup_menu_add_command('Auto-Generate Bounds', lambda : genbounds(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet1_opt.extra_bindings([("cell_select", lambda event: self.cell_select_opt(event, 'sheet1_opt'))])
            
            # Set Column Widths
            window.update_idletasks()
            total_width = self.sheet1_opt.winfo_width()
            self.sheet1_opt.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['Sheet1'][4]), redraw = True)
            self.sheet1_opt.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['Sheet1'][5]), redraw = True)
            self.sheet1_opt.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['Sheet1'][6]), redraw = True)
            self.sheet1_opt.column_width(column = 3, width = int(total_width*self.Placement['Optimization']['Sheet1'][7]), redraw = True)
            self.sheet1_opt.column_width(column = 4, width = int(total_width*self.Placement['Optimization']['Sheet1'][8]), redraw = True)
            self.sheet1_opt.column_width(column = 5, width = int(total_width*self.Placement['Optimization']['Sheet1'][9]), redraw = True)
            self.sheet1_opt.column_width(column = 6, width = int(total_width*self.Placement['Optimization']['Sheet1'][10]), redraw = True)
            self.sheet1_opt.table_align(align = 'c',redraw=True)

            # Set Cell Color
            for i in range(len(self.Params_VE)):
                if self.Params_VE_Status[i] == 'A':
                    self.sheet1_opt.highlight_cells(i, 2, bg='white', fg = 'black', redraw=False)
                    self.sheet1_opt.highlight_cells(i, 4, bg='white', fg = 'black', redraw=False)
                    self.sheet1_opt.highlight_cells(i, 5, bg='white', fg = 'black', redraw=False)
                else:
                    self.sheet1_opt.highlight_cells(i, 2, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                    self.sheet1_opt.highlight_cells(i, 4, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                    self.sheet1_opt.highlight_cells(i, 5, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)

            # Set unit dictionary
            Units = {'Stress':['GPa','MPa','kPa','Pa','msi','ksi','psi'],
                    'Time':['s'],
                    'Time-1':['1/s']
                    }

            # Set Rows
            for i in range(len(self.Params_VE)):
                try:
                    self.sheet1_opt.set_cell_data(i,0, '{:0.4e}'.format(self.Params_VE[i]))
                except:
                    self.sheet1_opt.set_cell_data(i,0, self.Params_VE[i])

                if self.Params_VE_Status[i] == 'A':
                    self.sheet1_opt.create_dropdown(r=i, c = 5,values=['Active','Passive'])
                else:
                    self.sheet1_opt.create_dropdown(r=i, c = 5,values=['Passive'])
                if self.Params_VE_Units[i] != None:
                    for key in list(Units.keys()):
                        if self.Params_VE_Units[i] in Units[key]:
                            units_list = Units[key]
                else:
                    units_list = []
                def_val = self.Params_VE_Units[i]
                    
                self.sheet1_opt.create_dropdown(r=i, c = 1,values=units_list)
                if def_val != None:
                    self.sheet1_opt.set_cell_data(i,1, def_val)

            # Set Optimization Flag
            try:
                if self.sheet1_opt_data[0][6] != '' and self.sheet1_opt_data[0][6] != None:
                    self.optimize = 1
                    self.Compare['Model']['Status'] = 1
            except:
                pass

            # Add Existing Data
            for i in range(len(self.sheet1_opt_data)):
                try:
                    # Find the corresponding index
                    rown = None
                    for j in range(len(self.sheet1_opt.data)):
                        if self.sheet1_opt.data[j][0] == self.sheet1_opt_data[i][0]:
                            rown = j

                    if rown != None:
                        for j in range(1,len(Cols)):
                            try:
                                try:
                                    self.sheet1_opt.set_cell_data(rown,j, '{:0.4e}'.format(self.sheet1_opt_data[i][j]))
                                except:
                                    self.sheet1_opt.set_cell_data(rown,j, self.sheet1_opt_data[i][j])
                                if j == 6:
                                    if self.optimize == 1:
                                        try:
                                            if float(self.sheet1_opt_data[i][6]) > 1.01*float(self.sheet1_opt_data[i][2]) and float(self.sheet1_opt_data[i][6]) < 0.99*float(self.sheet1_opt_data[i][4]):
                                                self.sheet1_opt.highlight((rown,6),fg = 'green', bg = 'white')
                                            else:
                                                self.sheet1_opt.highlight((rown,6),fg = 'red', bg = 'white')
                                        except:
                                            pass
                                    else:
                                        self.sheet1_opt.set_cell_data(rown,j, '')
                            except:
                                pass
                except:
                    pass

            # Format the table
            self.format_cell(None, 'self.sheet1_opt')

            # Redraw the table
            self.sheet1_opt.redraw()

            # Update the Model Data
            UpdateModelData(None, self, 1, 'Model')

        def VE_param(values):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Get List of of ViscoElastic Mechanisms.
            #
            #------------------------------------------------------------------

            # Get Value
            try:
                value = self.optmenu4_opt.get()
            except:
                value = 1

            # Initialize Parameters
            self.Params_VE = []
            self.Params_VE_Units = []
            self.Params_VE_Status = []

            # Add non-mechanism dependent parameters
            for i in range(len(self.model_info_all[self.mod_opt]['Reversible Models'][self.rmod_opt]['Parameters'])):
                param = self.model_info_all[self.mod_opt]['Reversible Models'][self.rmod_opt]['Parameters'][i]
                unit = self.model_info_all[self.mod_opt]['Reversible Models'][self.rmod_opt]['Units'][i]
                status = self.model_info_all[self.mod_opt]['Reversible Models'][self.rmod_opt]['Active'][i]
                if '_[M]' not in param:
                    self.Params_VE.append(param)
                    self.Params_VE_Units.append(unit)
                    self.Params_VE_Status.append(status)
                else:
                    for i in range(int(value)):
                        param_mech = param.replace("_[M]",str(i+1))
                        self.Params_VE.append(param_mech)
                        self.Params_VE_Units.append(unit)
                        self.Params_VE_Status.append(status)

            # Update the reversible mechanisms table
            update_reversible_table(self)

        def change_rev_model(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Recreate the number of viscoelastic mechanisms
            #
            #------------------------------------------------------------------

            # Destory old widgets
            if hasattr(self, "optmenu4_opt"):
                if self.optmenu4_opt.winfo_exists():
                    self.desc4_opt.destroy()
                    self.optmenu4_opt.destroy()

            # Store Value
            self.rmod_opt = self.optmenu2_opt.get()

            # Update the model
            UpdateModelData(value, self, 1, 'Model')

            # Get number of viscoelastic parameters
            ve_opt = None
            self.VEMech =  list(self.model_info_all[self.mod_opt]['Reversible Models'][self.rmod_opt ]['Mechanisms'])
            if len(self.VEMech) > 0:
                # Create the label
                self.desc4_opt = ttk.Label(
                                    self.nb_tab_tab3, 
                                    text="Viscoelastic Mechanisms (M):", 
                                    anchor=tk.NW,       
                                    style = "Modern1.TLabel"                   
                                    )
                self.desc4_opt.place(
                                anchor = 'n', 
                                relx = self.Placement['Optimization']['LabelVE'][0], 
                                rely = self.Placement['Optimization']['LabelVE'][1]
                                )
                if 'self.desc4_opt' not in self.atts['Optimize']['Local']:
                    self.atts['Optimize']['Local'].append('self.desc4_opt') 

                # Initialize number of viscoelastic mechanisms
                ve_opt = self.VEMech[0]

                # Check if previous data exists
                if 'Model' in list(self.Compare.keys()):
                    # Set the reversible model type
                    if 'M' in list(self.Compare['Model'].keys()):
                        if int(self.Compare['Model']['M']) in self.VEMech:
                            ve_opt = int(self.Compare['Model']['M'])

                # Create the drop down
                self.optmenu4_opt = ttk.Combobox(
                                            self.nb_tab_tab3,
                                            values=self.VEMech,
                                            style="Modern.TCombobox",
                                            state="readonly"
                                            )
                self.optmenu4_opt.configure(font = self.style_man['Combo'])
                self.optmenu4_opt.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
                self.optmenu4_opt.place(
                                    anchor='n', 
                                    relx = self.Placement['Optimization']['ComboVE'][0], 
                                    rely = self.Placement['Optimization']['ComboVE'][1], 
                                    relwidth = self.Placement['Optimization']['ComboVE'][2], 
                                    relheight = self.Placement['Optimization']['ComboVE'][3]
                                    )
                self.optmenu4_opt.set(ve_opt)
                self.optmenu4_opt.bind("<<ComboboxSelected>>",  VE_param)
                if 'self.optmenu4_opt' not in self.atts['Optimize']['Local']:
                    self.atts['Optimize']['Local'].append('self.optmenu4_opt')

            # Get list of viscoelastic parameters
            VE_param(ve_opt)

        def update_irreversible_table(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Update the irreversible model parameters table.
            #
            #------------------------------------------------------------------
                        
            # Delete table if it exists
            if hasattr(self,"sheet2_opt"):
                if hasattr(self,"res_flag2") == True:
                    if self.res_flag2 == 0:
                        # Store data
                        self.sheet2_opt_data = self.sheet2_opt.data
                else:
                    # Store data
                    self.sheet2_opt_data = self.sheet2_opt.data

                # Delete sheet
                self.sheet2_opt.destroy()
                del self.sheet2_opt
                
            # Check if previous data exists
            if 'Model' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'VP_Param' in list(self.Compare['Model'].keys()):
                    if hasattr(self,"res_flag2") == True:
                        if self.res_flag2 == 0:
                            self.sheet2_opt_data = self.Compare['Model']['VP_Param']
                        else:
                            self.res_flag2 = 0
                    else:
                        self.sheet2_opt_data = self.Compare['Model']['VP_Param']

            if hasattr(self,"sheet2_opt_data") == False:
                self.sheet2_opt_data = []

            # Set the columns
            Cols = ['Parameter', 'Units','Lower Bound','Initial Guess','Upper Bound','Active/Passive','COMPARE']

            # Create the table
            self.sheet2_opt = tksheet.Sheet(
                                        self.nb_tab_tab3, 
                                        total_rows = len(self.Params_VP), 
                                        total_columns = len(Cols), 
                                        headers = Cols,
                                        show_x_scrollbar = False, 
                                        show_y_scrollbar = True,
                                        font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                        header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                        )
            self.sheet2_opt.place(
                            anchor = 'n', 
                            relx = self.Placement['Optimization']['Sheet2'][0], 
                            rely = self.Placement['Optimization']['Sheet2'][1],
                            relwidth = self.Placement['Optimization']['Sheet2'][2], 
                            relheight = self.Placement['Optimization']['Sheet2'][3], 
                            )
            if 'self.sheet2_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.sheet2_opt') 

            # Format the sheet
            self.sheet2_opt.change_theme("blue")
            self.sheet2_opt.set_index_width(0)

            # Set Bindings
            def sort_cols(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Custom soring function.
                #
                #----------------------------------------------------------------------

                # Get currently selected element
                currently_selected = self.sheet2_opt.get_currently_selected()
                
                # Get the list of values
                sort_list = []
                for i in range(self.sheet2_opt.visible_rows[1]):
                    sort_list.append(self.sheet2_opt.data[i][currently_selected.column])
                index_list = sorted(range(len(sort_list)), key=lambda k: sort_list[k])
                
                # Rewrite the table
                temp_data = copy.deepcopy(self.sheet2_opt.data)
                for i in range(self.sheet2_opt.visible_rows[1]):
                    for j in range(self.sheet2_opt.visible_columns[1]):
                        self.sheet2_opt.set_cell_data(i,j,temp_data[index_list[i]][j])
                self.sheet2_opt.redraw()
        
            def all_active(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Set all parameters to active.
                #
                #----------------------------------------------------------------------

                # Set all parameters to Active
                for i in range(len(self.sheet2_opt.data)):
                    self.sheet2_opt.set_cell_data(i,5, 'Active')

            def all_passive(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Set all parameters to passive.
                #
                #----------------------------------------------------------------------

                # Set all parameters to Passive
                for i in range(len(self.sheet2_opt.data)):
                    self.sheet2_opt.set_cell_data(i,5, 'Passive')
                
            # Auto generate bounds
            def genbounds(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Automatically generate bounds.
                #
                #----------------------------------------------------------------------

                # Get the bounds slider value
                value = float(self.slider1_opt.get())
                if value == 0:
                    value = 5

                for i in range(len(self.sheet2_opt.data)):
                    try:
                        val = float(self.sheet2_opt.data[i][3])
                        lb = val-val*float(value)/100
                        self.sheet2_opt.set_cell_data(i,2, '{:0.4e}'.format(lb))
                        ub = val+val*float(value)/100
                        self.sheet2_opt.set_cell_data(i,4, '{:0.4e}'.format(ub))
                        self.sheet2_opt.redraw() 

                        # -- Check lower bound
                        self.sheet2_opt.highlight((i,2),fg = 'black', bg = 'white')
                        try:
                            if float(self.sheet2_opt.data[i][2]) > float(self.sheet2_opt.data[i][3]):
                                self.sheet2_opt.highlight((i,2),fg = 'red', bg = 'white')
                        except:
                            pass

                        # -- Check upper bound
                        self.sheet2_opt.highlight((i,4),fg = 'black', bg = 'white')
                        try:
                            if float(self.sheet2_opt.data[i][4]) < float(self.sheet2_opt.data[i][3]):
                                self.sheet2_opt.highlight((i,4),fg = 'red', bg = 'white')
                        except:
                            pass
                    except:
                        pass

            self.sheet2_opt.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
            self.sheet2_opt.popup_menu_add_command('Sort', lambda : sort_cols(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet2_opt.popup_menu_add_command('Change All to Active', lambda : all_active(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet2_opt.popup_menu_add_command('Change All to Passive', lambda : all_passive(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet2_opt.popup_menu_add_command('Auto-Generate Bounds', lambda : genbounds(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet2_opt.extra_bindings([("cell_select", lambda event: self.cell_select_opt(event, 'sheet2_opt'))])

            # Set Cell Color
            for i in range(len(self.Params_VP)):
                if self.Params_VP_Status[i] == 'A':
                    self.sheet2_opt.highlight_cells(i, 2, bg='white', fg = 'black', redraw=False)
                    self.sheet2_opt.highlight_cells(i, 4, bg='white', fg = 'black', redraw=False)
                    self.sheet2_opt.highlight_cells(i, 5, bg='white', fg = 'black', redraw=False)
                else:
                    self.sheet2_opt.highlight_cells(i, 2, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                    self.sheet2_opt.highlight_cells(i, 4, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                    self.sheet2_opt.highlight_cells(i, 5, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)

            # Set Column Widths
            window.update_idletasks()
            total_width = self.sheet1_opt.winfo_width()
            self.sheet2_opt.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['Sheet2'][4]), redraw = True)
            self.sheet2_opt.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['Sheet2'][5]), redraw = True)
            self.sheet2_opt.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['Sheet2'][6]), redraw = True)
            self.sheet2_opt.column_width(column = 3, width = int(total_width*self.Placement['Optimization']['Sheet2'][7]), redraw = True)
            self.sheet2_opt.column_width(column = 4, width = int(total_width*self.Placement['Optimization']['Sheet2'][8]), redraw = True)
            self.sheet2_opt.column_width(column = 5, width = int(total_width*self.Placement['Optimization']['Sheet2'][9]), redraw = True)
            self.sheet2_opt.column_width(column = 6, width = int(total_width*self.Placement['Optimization']['Sheet2'][10]), redraw = True)
            self.sheet2_opt.table_align(align = 'c',redraw=True)

            # Set unit dictionary
            Units = {'Stress':['GPa','MPa','kPa','Pa','msi','ksi','psi'],
                     'Stress-Time':['GPa-s','MPa-s','kPa-s','Pa-s','msi-s','ksi-s','psi-s'],
                    'Time':['s'],
                    'Time-1':['1/s'],
                    }

            # Set Rows
            for i in range(len(self.Params_VP)):
                try:
                    self.sheet2_opt.set_cell_data(i,0, '{:0.4e}'.format(self.Params_VP[i]))
                except:
                    self.sheet2_opt.set_cell_data(i,0, self.Params_VP[i])
                if self.Params_VP_Status[i] == 'A':
                    self.sheet2_opt.create_dropdown(r=i, c = 5,values=['Active','Passive'])
                else:
                    self.sheet2_opt.create_dropdown(r=i, c = 5,values=['Passive'])
                if self.Params_VP_Units[i] != None:
                    for key in list(Units.keys()):
                        if self.Params_VP_Units[i] in Units[key]:
                            units_list = Units[key]
                else:
                    units_list = []
                def_val = self.Params_VP_Units[i]
                    
                self.sheet2_opt.create_dropdown(r=i, c = 1,values=units_list)
                if def_val != None:
                    self.sheet2_opt.set_cell_data(i,1, def_val)

            # Set Optimization Flag
            try:
                if self.sheet2_opt_data[0][6] != '' and self.sheet2_opt_data[0][6] != None:
                    self.optimize = 1
                    self.Compare['Model']['Status'] = 1
            except:
                pass

            # Add Existing Data
            for i in range(len(self.sheet2_opt_data)):
                try:
                    # Find the corresponding index
                    rown = None
                    for j in range(len(self.sheet2_opt.data)):
                        if self.sheet2_opt.data[j][0] == self.sheet2_opt_data[i][0]:
                            rown = j

                    if rown != None:
                        for j in range(1,len(Cols)):
                            try:
                                try:
                                    self.sheet2_opt.set_cell_data(rown,j, '{:0.4e}'.format(self.sheet2_opt_data[i][j]))
                                except:
                                    self.sheet2_opt.set_cell_data(rown,j, self.sheet2_opt_data[i][j])
                                if j == 6:
                                    if self.optimize == 1:
                                        try:
                                            if float(self.sheet2_opt_data[i][6]) > 1.01*float(self.sheet2_opt_data[i][2]) and float(self.sheet2_opt_data[i][6]) < 0.99*float(self.sheet2_opt_data[i][4]):
                                                self.sheet2_opt.highlight((rown,6),fg = 'green', bg = 'white')
                                            else:
                                                self.sheet2_opt.highlight((rown,6),fg = 'red', bg = 'white')
                                        except:
                                            pass
                                    else:
                                        self.sheet2_opt.set_cell_data(rown,j, '')
                            except:
                                pass
                except:
                    pass

            # Format the table
            self.format_cell(None, 'self.sheet2_opt')

            #Redraw the table
            self.sheet2_opt.redraw()

            # Update the Model Data
            UpdateModelData(None, self, 2, 'Model')

        def VP_param(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Get List of of ViscoPlastic Mechanisms.
            #
            #------------------------------------------------------------------

            # Get Value
            try:
                value = self.optmenu5_opt.get()
            except:
                value = 1


            # Initialize Parameters
            self.Params_VP = []
            self.Params_VP_Units = []
            self.Params_VP_Status = []

            # Add non-mechanism dependent parameters
            for i in range(len(self.model_info_all[self.mod_opt]['Irreversible Models'][self.irrmod_opt]['Parameters'])):
                param = self.model_info_all[self.mod_opt]['Irreversible Models'][self.irrmod_opt]['Parameters'][i]
                unit = self.model_info_all[self.mod_opt]['Irreversible Models'][self.irrmod_opt]['Units'][i]
                status = self.model_info_all[self.mod_opt]['Irreversible Models'][self.irrmod_opt]['Active'][i]
                if '_[N]' not in param:
                    self.Params_VP.append(param)
                    self.Params_VP_Units.append(unit)
                    self.Params_VP_Status.append(status)
                else:
                    for j in range(int(value)):
                        param_mech = param.replace("_[N]",str(j+1))
                        self.Params_VP.append(param_mech)
                        self.Params_VP_Units.append(unit)
                        self.Params_VP_Status.append(status)

            # Update the irreversible mechanisms table
            update_irreversible_table(self)

        def change_irrev_model(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Recreate the number of viscoelastic mechanisms
            #
            #------------------------------------------------------------------

            # Destory old widgets
            if hasattr(self, "optmenu5_opt"):
                if self.optmenu5_opt.winfo_exists():
                    self.desc5_opt.destroy()
                    self.optmenu5_opt.destroy()

            # Store Value
            self.irrmod_opt = self.optmenu3_opt.get()

            # Update the model
            UpdateModelData(value, self, 2, 'Model')

            # Get number of viscoelastic parameters
            vp_opt = None
            self.VPMech =  list(self.model_info_all[self.mod_opt]['Irreversible Models'][self.irrmod_opt ]['Mechanisms'])

            if len(self.VPMech) > 0:
                # Create the label
                self.desc5_opt = ttk.Label(self.nb_tab_tab3, 
                                text="Viscoplastic Mechanisms (N):", 
                                anchor=tk.CENTER,       
                                style = "Modern1.TLabel"                  
                                )
                self.desc5_opt.place(
                                anchor = 'n', 
                                relx = self.Placement['Optimization']['LabelVP'][0], 
                                rely = self.Placement['Optimization']['LabelVP'][1]
                                )
                if 'self.desc5_opt' not in self.atts['Optimize']['Local']:
                    self.atts['Optimize']['Local'].append('self.desc5_opt')

                # Initialize Viscoplastic number of mechanisms
                vp_opt = self.VPMech[0]

                # Check if previous data exists
                if 'Model' in list(self.Compare.keys()):
                    # Set the reversible model type
                    if 'N' in list(self.Compare['Model'].keys()):
                        if int(self.Compare['Model']['N']) in self.VPMech:
                            vp_opt = int(self.Compare['Model']['N'])

                # Create the drop down menu
                self.optmenu5_opt = ttk.Combobox(
                                            self.nb_tab_tab3,
                                            values=self.VEMech,
                                            style="Modern.TCombobox",
                                            state="readonly"
                                            )
                self.optmenu5_opt.configure(font = self.style_man['Combo'])
                self.optmenu5_opt.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
                self.optmenu5_opt.place(
                                    anchor='n', 
                                    relx = self.Placement['Optimization']['ComboVP'][0], 
                                    rely = self.Placement['Optimization']['ComboVP'][1], 
                                    relwidth = self.Placement['Optimization']['ComboVP'][2], 
                                    relheight = self.Placement['Optimization']['ComboVP'][3]
                                    )
                self.optmenu5_opt.set(vp_opt)
                self.optmenu5_opt.bind("<<ComboboxSelected>>",  VP_param)
                if 'self.optmenu5_opt' not in self.atts['Optimize']['Local']:
                    self.atts['Optimize']['Local'].append('self.optmenu5_opt')

            # Get list of viscoplastic parameters
            VP_param(vp_opt)

        # Get the model
        self.mod_opt = self.optmenu1_opt.get()

        # Clear the model information if the model type changed
        try:
            if value != self.Compare['Model']['Model Name']:
                # Prompt user to save model
                self.save_model(None)

                # Clear model information
                self.Compare['Model'] = {}
                self.Compare['Model']['Status'] = 0
        except:
            pass
        
        # Delete local attributes
        for att in self.atts['Optimize']['Local']:
            try:
                eval(f"{att}").destroy()
            except:
                pass

        # Read the model info
        self.Compare['Model']['Model Name'] = self.mod_opt
        self.Compare['Model']['Model Info'] = {'Core': self.model_info_all[self.mod_opt]['Model Info']['Core'],
                                               'Model': self.model_info_all[self.mod_opt]['Model Info']['Model'],
                                               }
            
        # Get available reversible models
        self.RevModels = list(self.model_info_all[self.mod_opt]['Reversible Models'].keys())
        self.Compare['Model']['Model Info']['Reversible Models'] = self.RevModels
        
        if len(self.RevModels) > 0:
            # Create the label
            self.desc2_opt = ttk.Label(
                                self.nb_tab_tab3, 
                                text="Reversible Model:", 
                                anchor=tk.NW,       
                                style = 'Modern1.TLabel'                    
                                )
            self.desc2_opt.place(
                            anchor = 'n', 
                            relx = self.Placement['Optimization']['LabelRev'][0], 
                            rely = self.Placement['Optimization']['LabelRev'][1],
                            )
            
            if 'self.desc2_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.desc2_opt')    

            # Initialize the model
            rmod_opt = self.RevModels[0]

            # Check if previous data exists
            if 'Model' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'Reversible Model Name' in list(self.Compare['Model'].keys()):
                    if self.Compare['Model']['Reversible Model Name'] in self.RevModels:
                        rmod_opt = self.Compare['Model']['Reversible Model Name']

            # Create the reversible model drop down   
            self.optmenu2_opt = ttk.Combobox(
                                        self.nb_tab_tab3,
                                        values=self.RevModels,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2_opt.configure(font = self.style_man['Combo'])
            self.optmenu2_opt.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu2_opt.place(
                                anchor='n', 
                                relx = self.Placement['Optimization']['ComboRev'][0], 
                                rely = self.Placement['Optimization']['ComboRev'][1],
                                relwidth = self.Placement['Optimization']['ComboRev'][2], 
                                relheight = self.Placement['Optimization']['ComboRev'][3]
                                )
            self.optmenu2_opt.set(rmod_opt)
            self.optmenu2_opt.bind("<<ComboboxSelected>>",  lambda event:change_rev_model(event))
            if 'self.optmenu2_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.optmenu2_opt') 

            # Call the reversible model function
            change_rev_model(rmod_opt)

        # Get available irreversible models
        self.IrrevModels =  list(self.model_info_all[self.mod_opt]['Irreversible Models'].keys())
        self.Compare['Model']['Model Info']['Irreversible Models'] = self.IrrevModels

        if len(self.IrrevModels) > 0:
            # Create the label
            self.desc3_opt = ttk.Label(
                                self.nb_tab_tab3, 
                                text= "Irreversible Model:", 
                                anchor=tk.NW,       
                                style = "Modern1.TLabel"
                                )
            self.desc3_opt.place(
                            anchor = 'n', 
                            relx = self.Placement['Optimization']['LabelIrrev'][0], 
                            rely = self.Placement['Optimization']['LabelIrrev'][1]
                            )
            if 'self.desc3_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.desc3_opt') 

            # Initialize the irreversible model
            irmod_opt = self.IrrevModels[0]

            # Check if previous data exists
            if 'Model' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'Irreversible Model Name' in list(self.Compare['Model'].keys()):
                    if self.Compare['Model']['Irreversible Model Name'] in self.IrrevModels:
                        irmod_opt = self.Compare['Model']['Irreversible Model Name']

            # Create the irreversible model drop down
            self.optmenu3_opt = ttk.Combobox(
                                        self.nb_tab_tab3,
                                        values=self.IrrevModels,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu3_opt.configure(font = self.style_man['Combo'])
            self.optmenu3_opt.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
            self.optmenu3_opt.place(
                                anchor='n', 
                                relx = self.Placement['Optimization']['ComboIrrev'][0], 
                                rely = self.Placement['Optimization']['ComboIrrev'][1],
                                relwidth = self.Placement['Optimization']['ComboIrrev'][2], 
                                relheight = self.Placement['Optimization']['ComboIrrev'][3]
                                )
            self.optmenu3_opt.set(irmod_opt)
            self.optmenu3_opt.bind("<<ComboboxSelected>>",  lambda event:change_irrev_model(event))
            if 'self.optmenu3_opt' not in self.atts['Optimize']['Local']:
                self.atts['Optimize']['Local'].append('self.optmenu3_opt') 

            # Call the irreversible model function
            change_irrev_model(irmod_opt)

        
        # Create the bounds slider
        def update_value(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Format the slider value and save to memory.
            #
            #------------------------------------------------------------------

            formatted_value = f"Bounds: ± {str(int(float(value)))}%" 
            self.desc6_opt.config(text=formatted_value)

            self.slider_val = value

        # Create the label
        self.desc6_opt = ttk.Label(self.nb_tab_tab3, 
                        text="Bounds: ± 5%", 
                        anchor=tk.CENTER,       
                        style = 'Modern1.TLabel'                  
                        )
        self.desc6_opt.place(
                        anchor = 'n', 
                        relx = self.Placement['Optimization']['LabelBnd'][0], 
                        rely = self.Placement['Optimization']['LabelBnd'][1]
                        )
        if 'self.desc6_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.desc6_opt')

        # Create the slider
        self.slider1_opt = ttk.Scale(
                                self.nb_tab_tab3, 
                                from_=5, 
                                to=50, 
                                orient='horizontal',  
                                style="Modern.Horizontal.TScale", 
                                command = update_value, 
                                )
        self.slider1_opt.place(
                        anchor = 'n', 
                        relx = self.Placement['Optimization']['Slider1'][0], 
                        rely = self.Placement['Optimization']['Slider1'][1],
                        relwidth= self.Placement['Optimization']['Slider1'][2],
                        )
        if 'self.slider1_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.slider1_opt')

        if hasattr(self,"slider_val"):
            self.slider1_opt.set(self.slider_val)

        # Create the Load from Excel button
        self.btn_load_opt = ttk.Button(
                                    self.nb_tab_tab3, 
                                    text = "Load from Excel", 
                                    command = lambda:self.load_from_db('Optimize'), 
                                    style = "Modern3.TButton",
                                    )
        self.btn_load_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonLoad'][0], 
                            rely = self.Placement['Optimization']['ButtonLoad'][1], 
                            relwidth = self.Placement['Optimization']['ButtonLoad'][2], 
                            relheight = self.Placement['Optimization']['ButtonLoad'][3]
                            )
        if 'self.btn_load_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_load_opt')

        # Create button to view/delete models
        self.btn_modlib_opt = ttk.Button(
                                    self.nb_tab_tab3, 
                                    text = "Model Library", 
                                    command = lambda : self.Model_Library('Optimize'), 
                                    style = "Modern3.TButton",
                                    )
        self.btn_modlib_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonModLib'][0], 
                            rely = self.Placement['Optimization']['ButtonModLib'][1], 
                            relwidth = self.Placement['Optimization']['ButtonModLib'][2], 
                            relheight = self.Placement['Optimization']['ButtonModLib'][3]
                            )
        if 'self.btn_modlib_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_modlib_opt')

        # Create the Optimize button
        self.btn_opt = ttk.Button(
                                self.nb_tab_tab3, 
                                text = "Optimize", 
                                command = self.optimizer, 
                                style = "Modern3.TButton",
                                )
        self.btn_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonOpt'][0], 
                            rely = self.Placement['Optimization']['ButtonOpt'][1], 
                            relwidth = self.Placement['Optimization']['ButtonOpt'][2], 
                            relheight = self.Placement['Optimization']['ButtonOpt'][3]
                            )
        if 'self.btn_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_opt')

        # Create Replace Values
        def reset_guess(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Reset the initial guess with the last compare run
            #
            #------------------------------------------------------------------

            # # Check that values exist
            # flag = 0
            # # -- Check Viscoelastic
            # for i in range(len(self.sheet1_opt.data)):
            #     try:
            #         val = float(self.sheet1_opt.data[i][-1])
            #     except:
            #         flag = 1

            # # -- Check Viscoplastic
            # for i in range(len(self.sheet2_opt.data)):
            #     try:
            #         val = float(self.sheet2_opt.data[i][-1])
            #     except:
            #         flag = 1

            # if flag == 1:
            #     messagebox.showerror(message ='No COMPARE result found.')
            #     return
            
            # Get list of bound percentages
            # -- Viscoelastic
            ve_bnds = []
            for i in range(len(self.sheet1_opt.data)):
                try:
                    lp = (float(self.sheet1_opt.data[i][2]) - float(self.sheet1_opt.data[i][3]))/(-float(self.sheet1_opt.data[i][3]))
                    up = (float(self.sheet1_opt.data[i][4]) - float(self.sheet1_opt.data[i][3]))/(float(self.sheet1_opt.data[i][3]))
                except:
                    lp = ''
                    up = ''
                ve_bnds.append([lp, up])

            # -- Viscoplastic
            vp_bnds = []
            for i in range(len(self.sheet2_opt.data)):
                try:
                    lp = (float(self.sheet2_opt.data[i][2]) - float(self.sheet2_opt.data[i][3]))/(-float(self.sheet2_opt.data[i][3]))
                    up = (float(self.sheet2_opt.data[i][4]) - float(self.sheet2_opt.data[i][3]))/(float(self.sheet2_opt.data[i][3]))
                except:
                    lp = ''
                    up = ''
                vp_bnds.append([lp, up])

            # Reset Values
            # -- Viscoelastic
            for i in range(len(self.sheet1_opt.data)):
                try:
                    self.sheet1_opt.data[i][3] = '{:0.4e}'.format(float(self.sheet1_opt.data[i][-1]))
                except:
                    pass

                try:
                    self.sheet1_opt.data[i][2] = '{:0.4e}'.format(float(self.sheet1_opt.data[i][-1]) - float(self.sheet1_opt.data[i][-1])*ve_bnds[i][0])
                    self.sheet1_opt.data[i][4] = '{:0.4e}'.format(float(self.sheet1_opt.data[i][-1]) + float(self.sheet1_opt.data[i][-1])*ve_bnds[i][1])
                except:
                    pass
                self.sheet1_opt.data[i][-1] = ''

            # -- Viscoplastic
            for i in range(len(self.sheet2_opt.data)):
                try:
                    self.sheet2_opt.data[i][3] = '{:0.4e}'.format(float(self.sheet2_opt.data[i][-1]))
                except:
                    pass

                try:
                    self.sheet2_opt.data[i][2] = '{:0.4e}'.format(float(self.sheet2_opt.data[i][-1]) - float(self.sheet2_opt.data[i][-1])*vp_bnds[i][0])
                    self.sheet2_opt.data[i][4] = '{:0.4e}'.format(float(self.sheet2_opt.data[i][-1]) + float(self.sheet2_opt.data[i][-1])*vp_bnds[i][1])
                except:
                    pass
                self.sheet2_opt.data[i][-1] = ''

            # Redraw sheets
            self.sheet1_opt.redraw() 
            self.sheet2_opt.redraw() 

        self.btn_reset_opt = ttk.Button(
                                self.nb_tab_tab3, 
                                text = "Reset Guess", 
                                command = lambda: reset_guess(self), 
                                style = "Modern3.TButton",
                                )
        self.btn_reset_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonRes'][0], 
                            rely = self.Placement['Optimization']['ButtonRes'][1], 
                            relwidth = self.Placement['Optimization']['ButtonRes'][2], 
                            relheight = self.Placement['Optimization']['ButtonRes'][3]
                            )
        if 'self.btn_reset_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_reset_opt')

        def save_model_local():
            #------------------------------------------------------------------
            #
            #   PURPOSE: Save models to the project library.
            #
            #------------------------------------------------------------------

            # Save notes if they exist
            nflag = 0
            if 'Note' in self.Compare['Model'].keys():
                note =  self.Compare['Model']['Note']
                nflag = 1

            # Update Model Data
            UpdateModelData(None, self, 3, 'Model')

            # Set the model type
            self.Compare['Model']['Compare Type'] = 'Optimize'

            # Add the note back
            if nflag == 1:
                self.Compare['Model']['Note'] = note

            # Get the save name
            save_flag = 0
            while save_flag == 0:
                user_input = simpledialog.askstring("Save Model", "Enter the model name:")

                if user_input in list(self.Compare['Model Library'].keys()):
                    askyn = messagebox.askyesno(title = 'Save Model', message = 'Do you want to overwrite ' + user_input + ' ?')
                    if askyn == True:
                        save_flag = 1
                else:
                    save_flag = 1
            
            # Save to binary in the model library
            json_string = json.dumps(self.Compare['Model'])
            binary_data = json_string.encode('utf-8')
            self.Compare['Model Library'][user_input] = binary_data

            # Set the model name
            self.Compare['Model ID']= user_input

        # Create button to save a model
        self.btn_savemod_opt = ttk.Button(
                                    self.nb_tab_tab3, 
                                    text = "Save Model", 
                                    command = save_model_local, 
                                    style = "Modern3.TButton",
                                    )
        self.btn_savemod_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonSaveMod'][0], 
                            rely = self.Placement['Optimization']['ButtonSaveMod'][1], 
                            relwidth = self.Placement['Optimization']['ButtonSaveMod'][2], 
                            relheight = self.Placement['Optimization']['ButtonSaveMod'][3]
                            )
        if 'self.btn_savemod_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_savemod_opt')

        def add_note():
            #------------------------------------------------------------------
            #
            #   PURPOSE: Add a note to the model.
            #
            #------------------------------------------------------------------

            # Set the flag for the window
            if hasattr(self,'note_click') == False:
                self.note_click = 0

            # Open the window if it does not exist
            if self.note_click == 0:
                self.note_click = 1

                # Create the window
                root = tk.Toplevel(window)
                root.geometry(f"{int(600*self.scale)}x{int(400*self.scale)}")
                root.title("Enter Model Notes") 
                root.configure(bg='white')
                root.grab_set()
                
                # Create the label
                ttk.Label(
                        root, 
                        text="Enter Model Notes:", 
                        style = "Modern1.TLabel"
                        ).place(anchor='n', 
                                relx = self.Placement['Optimization']['NotesLabel'][0], 
                                rely = self.Placement['Optimization']['NotesLabel'][1],
                                ) 
                
                # Create the note area
                text_area = scrolledtext.ScrolledText(
                                                    root, 
                                                    wrap=tk.WORD, 
                                                    width=int(40*self.scale), 
                                                    height=int(8*self.scale), 
                                                    font=("Segoe UI", max([self.min_font, int(14*self.scale)]))) 
                text_area.place(anchor='c', 
                                relx = self.Placement['Optimization']['NotesArea'][0], 
                                rely = self.Placement['Optimization']['NotesArea'][1],  
                                relwidth = self.Placement['Optimization']['NotesArea'][2], 
                                relheight = self.Placement['Optimization']['NotesArea'][3], 
                                )

                # Display any existing notes
                if 'Note' in list(self.Compare['Model'].keys()):
                    text_area.insert("end", self.Compare['Model']['Note']) 
                
                # placing cursor in text area 
                text_area.focus()

                def on_closing_root(self):
                    #--------------------------------------------------------------
                    #
                    #   PURPOSE: Create exit protocol for the note window.
                    #
                    #--------------------------------------------------------------
                    
                    # Save the note
                    try:
                        self.Compare['Model']['Note'] = text_area.get("1.0",'end-1c')
                    except:
                        pass

                    # Reset the window
                    self.note_click = 0
                    root.destroy()

                # Add the exit protocol to the root
                root.protocol("WM_DELETE_WINDOW", lambda:on_closing_root(self))

        # Create button to add a note
        self.btn_addnote_opt = ttk.Button(
                                    self.nb_tab_tab3, 
                                    text = "Model Notes", 
                                    command = add_note, 
                                    style = "Modern3.TButton",
                                    )
        self.btn_addnote_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonNote'][0], 
                            rely = self.Placement['Optimization']['ButtonNote'][1], 
                            relwidth = self.Placement['Optimization']['ButtonNote'][2], 
                            relheight = self.Placement['Optimization']['ButtonNote'][3]
                            )
        if 'self.btn_addnote_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_addnote_opt')

        # Function to view model history
        def view_history(self):
            #--------------------------------------------------------------
            #
            #   PURPOSE: View run history for this project.
            #
            #--------------------------------------------------------------

            def view_hist_data(self):
                #--------------------------------------------------------------
                #
                #   PURPOSE: Get parameters and test error for chosen run.
                #
                #--------------------------------------------------------------

                # Delete the old tables if they exist
                try:
                    self.hist_param_sheet.destroy()
                    self.hist_test_sheet.destroy()
                except:
                    pass

                # Get currently selected row
                currently_selected = self.run_hist_sheet.get_currently_selected()

                # Highlight Row
                for i in range(len(self.run_hist_sheet.data)):
                    self.run_hist_sheet.highlight_rows(i,'white','black')
                self.run_hist_sheet.highlight_rows(currently_selected.row,'lightblue1','black')

                # Get parameters
                params = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Parameters']
                param_keys = list(params.keys())

                # Create Parameter sheet
                Cols = ['Parameter', 'Value', 'Unit']
                self.hist_param_sheet = tksheet.Sheet(
                                                root, 
                                                total_rows = len(param_keys), 
                                                total_columns = len(Cols), 
                                                headers = Cols, 
                                                show_x_scrollbar = False, 
                                                show_y_scrollbar = True,
                                                font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"normal"),
                                                header_font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"bold"))
                self.hist_param_sheet.place(
                                    anchor = 'ne', 
                                    relx = self.Placement['Optimization']['HistSheetPar'][0], 
                                    rely = self.Placement['Optimization']['HistSheetPar'][1],
                                    relwidth = self.Placement['Optimization']['HistSheetPar'][2], 
                                    relheight = self.Placement['Optimization']['HistSheetPar'][3],
                                    )

                # Format the sheet
                self.hist_param_sheet.change_theme("blue")
                root.update_idletasks()
                total_width = self.hist_param_sheet.winfo_width()
                self.hist_param_sheet.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['HistSheetPar'][4]), redraw = True)
                self.hist_param_sheet.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['HistSheetPar'][5]), redraw = True)
                self.hist_param_sheet.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['HistSheetPar'][6]), redraw = True)
                self.hist_param_sheet.table_align(align = 'c',redraw=True)
                self.hist_param_sheet.set_index_width(0)

                # Fill existing values values
                for i, key in enumerate(param_keys):
                    self.hist_param_sheet.set_cell_data(i,0,key)
                    self.hist_param_sheet.set_cell_data(i,1,'{:0.4e}'.format(params[key][0]))
                    self.hist_param_sheet.set_cell_data(i,2,params[key][1]) 
                self.hist_param_sheet.redraw()

                # Get parameters
                tests = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Test Error']
                test_keys = list(tests.keys())

                # Create Parameter sheet
                Cols = ['Name', 'Type', 'Weight', 'Error']
                self.hist_test_sheet = tksheet.Sheet(
                                                root, 
                                                total_rows = len(test_keys), 
                                                total_columns = len(Cols), 
                                                headers = Cols,
                                                show_x_scrollbar = False, 
                                                show_y_scrollbar = True,
                                                font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"normal"),
                                                header_font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"bold"),
                                                )
                self.hist_test_sheet.place(
                                    anchor = 'ne', 
                                    relx = self.Placement['Optimization']['HistSheetTest'][0], 
                                    rely = self.Placement['Optimization']['HistSheetTest'][1], 
                                    relwidth = self.Placement['Optimization']['HistSheetTest'][2], 
                                    relheight = self.Placement['Optimization']['HistSheetTest'][3], 
                                    )
                
                # Format the sheet
                self.hist_test_sheet.change_theme("blue")
                root.update_idletasks()
                total_width = self.hist_test_sheet.winfo_width()
                self.hist_test_sheet.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['HistSheetTest'][4]), redraw = True)
                self.hist_test_sheet.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['HistSheetTest'][5]), redraw = True)
                self.hist_test_sheet.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['HistSheetTest'][6]), redraw = True)
                self.hist_test_sheet.column_width(column = 3, width = int(total_width*self.Placement['Optimization']['HistSheetTest'][7]), redraw = True)
                self.hist_test_sheet.table_align(align = 'c',redraw=True)
                self.hist_test_sheet.set_index_width(0)

                # Fill existing values values
                for i, key in enumerate(test_keys):
                    self.hist_test_sheet.set_cell_data(i,0,key)
                    self.hist_test_sheet.set_cell_data(i,1,tests[key][0])
                    self.hist_test_sheet.set_cell_data(i,2,tests[key][1]) 
                    self.hist_test_sheet.set_cell_data(i,3,tests[key][2]) 
                self.hist_test_sheet.redraw()

                # Deselect
                self.run_hist_sheet.deselect("all", redraw=True)

            # Get the log file
            with open(self.log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            lines = [line.strip() for line in lines]

            # Get indices of each test run
            test_start = []
            for i, line in enumerate(lines):
                if "-- NEW RUN --" in line:
                    test_start.append(i)
            test_start.append(len(lines))

            self.run_history = {}
            for i in range(len(test_start)-1):
                # Initialize Data
                self.run_history['Run #' + str(i+1)] = {}

                # Get Optimization Results
                self.run_history['Run #' + str(i+1)]['Parameters'] = {}
                self.run_history['Run #' + str(i+1)]['Global Error'] = None
                self.run_history['Run #' + str(i+1)]['Test Error'] = {}
                for j in range(test_start[i], test_start[i+1]):
                    keys = ['Model Name', 'Reversible Model Name','Irreversible Model Name','Viscoelastic Mechanisms','Viscoplastic Mechanisms']
                    for key in keys:
                        if ':' in lines[j] and key == lines[j].split(':')[0].strip():
                            self.run_history['Run #' + str(i+1)][key.split(':')[0]] = lines[j].split(':')[1].strip()

                    if "OPTIMIZATION RESULTS:" in lines[j]:
                        ct = 2
                        while lines[j+ct] != '':
                            line = lines[j+ct]
                            line = line.split(' ')
                            cline = [x for x in line if x != '']
                            try:
                                self.run_history['Run #' + str(i+1)]['Parameters'][cline[0]] = [float(cline[2]), cline[1]]
                            except:
                                self.run_history['Run #' + str(i+1)]['Parameters'][cline[0]] = [float(cline[1]), '']
                            ct = ct + 1
                            if j+ct == test_start[i+1]:
                                break

                    if "ERROR:" in lines[j]:
                        self.run_history['Run #' + str(i+1)]['Global Error'] = float(lines[j+1].split('=')[1])
                        ct = 5
                        while lines[j+ct] != '':
                            line = lines[j+ct]
                            line = line.split(' ')
                            cline = [x for x in line if x != '']
                            self.run_history['Run #' + str(i+1)]['Test Error'][cline[0]] = [cline[1], float(cline[2]), float(cline[3])]

                            ct = ct + 1
                            if j+ct == test_start[i+1]:
                                break


            def load_hist_data(self):
                #--------------------------------------------------------------
                #
                #   PURPOSE: Load a previous run back into PYCOMPARE
                #
                #--------------------------------------------------------------

                # Get currently selected row
                currently_selected = self.run_hist_sheet.get_currently_selected()

                # Get the model type
                mod_type = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Model Name']

                try:
                    self.optmenu1_opt.set(mod_type)
                    change_model(mod_type)
                except:
                    messagebox.showerror(message = 'Unable to load model.')

                # Get the reversible model
                try:
                    if 'Reversible Model Name' in self.run_history[self.run_hist_sheet.data[currently_selected.row][0]].keys():
                        rev_model = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Reversible Model Name']
                        if rev_model in self.optmenu2_opt['values']:
                            self.optmenu2_opt.set(rev_model)
                            change_rev_model(rev_model)
                except:
                    pass

                # Get the reversible mechanisms
                try:
                    if 'Viscoelastic Mechanisms' in self.run_history[self.run_hist_sheet.data[currently_selected.row][0]].keys():
                        rev_mech = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Viscoelastic Mechanisms']
                        if rev_mech in self.optmenu4_opt['values']:
                            self.optmenu4_opt.set(rev_mech)
                            VE_param(rev_mech)
                except:
                    pass

                # Get the irreversible model
                try:
                    if 'Irreversible Model Name' in self.run_history[self.run_hist_sheet.data[currently_selected.row][0]].keys():
                        irrev_model = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Irreversible Model Name']
                        if irrev_model in self.optmenu3_opt['values']:
                            self.optmenu3_opt.set(irrev_model)
                            change_irrev_model(irrev_model)
                except:
                    pass

                # Get the irreversible mechanisms
                try:
                    if 'Viscoplastic Mechanisms' in self.run_history[self.run_hist_sheet.data[currently_selected.row][0]].keys():
                        irrev_mech = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Viscoplastic Mechanisms']
                        if irrev_mech in self.optmenu5_opt['values']:
                            self.optmenu5_opt.set(irrev_mech)
                            VP_param(irrev_mech)
                except:
                    pass

                # Get parameters
                params = self.run_history[self.run_hist_sheet.data[currently_selected.row][0]]['Parameters']
                param_keys = list(params.keys())

                # Write Parameters
                for key in param_keys:
                    for i in range(len(self.sheet1_opt.data)):
                        if key == self.sheet1_opt.data[i][0]:
                            self.sheet1_opt.set_cell_data(i,1,params[key][1])
                            self.sheet1_opt.set_cell_data(i,2,'')
                            self.sheet1_opt.set_cell_data(i,3,'{:0.4e}'.format(params[key][0]))
                            self.sheet1_opt.set_cell_data(i,4,'')
                            self.sheet1_opt.set_cell_data(i,5,'Active')
                            self.sheet1_opt.set_cell_data(i,6,'')

                    for i in range(len(self.sheet2_opt.data)):
                        if key == self.sheet2_opt.data[i][0]:
                            self.sheet2_opt.set_cell_data(i,1,params[key][1])
                            self.sheet2_opt.set_cell_data(i,2,'')
                            self.sheet2_opt.set_cell_data(i,3,'{:0.4e}'.format(params[key][0]))
                            self.sheet2_opt.set_cell_data(i,4,'')
                            self.sheet2_opt.set_cell_data(i,5,'Active')
                            self.sheet2_opt.set_cell_data(i,6,'')
            
                # Recreate the Optimize Page
                self.opt_init = 1
                self.viz_init = 0
                root.destroy()
                CreateModelTab(self,window)


            # Create the run history window
            root = tk.Toplevel(window)
            root.title("Run History")
            root.geometry(f"{int(900*self.scale)}x{int(600*self.scale)}")
            root.resizable(False, False)
            root.configure(bg='white')
            root.grab_set()

            # Create the label
            ttk.Label(
                        root, 
                        text="Run History", 
                        anchor=tk.CENTER,       
                        style = "Modern1.TLabel"                   
                        ).place(
                                anchor='n', 
                                relx = self.Placement['Optimization']['HistLabel'][0], 
                                rely = self.Placement['Optimization']['HistLabel'][1]
                                )
            
            # Create the sheet
            Cols = ['Run', 'No. of Tests', 'Global Error']
            self.run_hist_sheet = tksheet.Sheet(
                                            root, 
                                            total_rows = len(self.run_history.keys()), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"bold"),
            )
            self.run_hist_sheet.place(
                                anchor = 'nw', 
                                relx = self.Placement['Optimization']['HistSheetRun'][0], 
                                rely = self.Placement['Optimization']['HistSheetRun'][1],
                                relwidth = self.Placement['Optimization']['HistSheetRun'][2], 
                                relheight = self.Placement['Optimization']['HistSheetRun'][3], 
                                )
            
            

            # Format the sheet
            self.run_hist_sheet.change_theme("blue")
            root.update_idletasks()
            total_width = self.run_hist_sheet.winfo_width()
            self.run_hist_sheet.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['HistSheetRun'][4]), redraw = True)
            self.run_hist_sheet.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['HistSheetRun'][5]), redraw = True)
            self.run_hist_sheet.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['HistSheetRun'][6]), redraw = True)
            self.run_hist_sheet.table_align(align = 'c',redraw=True)
            self.run_hist_sheet.set_index_width(0)

            # Enable Bindings
            self.run_hist_sheet.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys","rc_popup_menu")
            self.run_hist_sheet.popup_menu_add_command('View Data', lambda : view_hist_data(self), table_menu = True, index_menu = True, header_menu = True)
            self.run_hist_sheet.popup_menu_add_command('Load Model', lambda : load_hist_data(self), table_menu = True, index_menu = True, header_menu = True)

            
            # Fill existing values values
            key_list = list(self.run_history.keys())
            key_list.reverse()
            for i, key in enumerate(key_list):
                j = list(self.run_history.keys()).index(key)
                self.run_hist_sheet.set_cell_data(i,0,list(self.run_history.keys())[j])
                self.run_hist_sheet.set_cell_data(i,1,len(self.run_history[list(self.run_history.keys())[j]]['Test Error'].keys()))
                self.run_hist_sheet.set_cell_data(i,2,self.run_history[list(self.run_history.keys())[j]]['Global Error']) 
            self.run_hist_sheet.redraw()


        # Create button to view model history
        self.btn_view_hist_opt = ttk.Button(
                                    self.nb_tab_tab3, 
                                    text = "Run History", 
                                    command = lambda : view_history(self), 
                                    style = "Modern3.TButton",
                                    )
        self.btn_view_hist_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['ButtonView'][0], 
                            rely = self.Placement['Optimization']['ButtonView'][1], 
                            relwidth = self.Placement['Optimization']['ButtonView'][2], 
                            relheight = self.Placement['Optimization']['ButtonView'][3]
                            )
        if 'self.btn_view_hist_opt' not in self.atts['Optimize']['Local']:
            self.atts['Optimize']['Local'].append('self.btn_view_hist_opt')

        # Write Global Error
        if hasattr(self,'globalerr_opt'):
            self.globalerr_opt.destroy()

        if 'Global Error' in self.Compare.keys() and self.viz_init > 0:
            try:
                self.globalerr_opt = ttk.Label(
                                    self.nb_tab_tab3, 
                                    text=f"Global Error: {'{:0.4e}'.format(self.Compare['Global Error'])}", 
                                    anchor=tk.NW,       
                                    style = 'Modern1.TLabel'                    
                                    )
            except:
                self.globalerr_opt = ttk.Label(
                                    self.nb_tab_tab3, 
                                    text=f"Global Error:", 
                                    anchor=tk.NW,       
                                    style = 'Modern1.TLabel'                    
                                    )
            self.globalerr_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['LabelGlobalErr'][0], 
                            rely = self.Placement['Optimization']['LabelGlobalErr'][1],
                            )

        # Update Model Data
        UpdateModelData(None, self, 3, 'Model')

        # Update Tables
        if len(self.Compare['Model']['Model Info']['Reversible Models']) > 0:
            update_reversible_table(self)
        if len(self.Compare['Model']['Model Info']['Irreversible Models']) > 0:
            update_irreversible_table(self)

    # Initialize the tab
    if self.opt_init == 1:

        # Create the label
        self.desc1_opt = ttk.Label(
                            self.nb_tab_tab3, 
                            text="Select the Model:", 
                            anchor=tk.NW,       
                            style = "Modern1.TLabel"                   
                            )
        self.desc1_opt.place(
                        anchor = 'nw', 
                        relx = self.Placement['Optimization']['LabelSelModel'][0], 
                        rely = self.Placement['Optimization']['LabelSelModel'][1], 
                        relwidth = self.Placement['Optimization']['LabelSelModel'][2], 
                        relheight = self.Placement['Optimization']['LabelSelModel'][3]
                        )
        
        self.atts['Optimize']['Permanent'].append('self.desc1_opt')

        # Initialize the model option
        mod_opt = self.Models[0]

        # Check if previous value exists
        if 'Model' in list(self.Compare.keys()):
            # Set the model name
            if 'Model Name' in list(self.Compare['Model'].keys()):
                if self.Compare['Model']['Model Name'] in self.Models:
                    mod_opt = self.Compare['Model']['Model Name']

        # Create Option Menu for Model Type
        self.optmenu1_opt = ttk.Combobox(
                                    self.nb_tab_tab3,
                                    values=self.Models,
                                    style="Modern.TCombobox",
                                    state="readonly"
                                    )
        self.optmenu1_opt.configure(font = self.style_man['Combo'])
        self.optmenu1_opt.option_add('*TCombobox*Listbox.font', self.style_man['Combo'])
        self.optmenu1_opt.place(
                            anchor='nw', 
                            relx = self.Placement['Optimization']['ComboSelModel'][0], 
                            rely = self.Placement['Optimization']['ComboSelModel'][1], 
                            relwidth = self.Placement['Optimization']['ComboSelModel'][2], 
                            relheight = self.Placement['Optimization']['ComboSelModel'][3]
                            )
        self.optmenu1_opt.set(mod_opt)
        self.optmenu1_opt.bind("<<ComboboxSelected>>",  change_model)
        change_model(mod_opt)
        self.atts['Optimize']['Permanent'].append('self.optmenu1_opt')

        # Set Initialization Flag
        self.opt_init = 0