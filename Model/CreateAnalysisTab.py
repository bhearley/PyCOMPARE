#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateAnalysisTab.py
#
# PURPOSE: Create the Analyze Model tab. The Analyze Model tab allows users to define a model manually and evaluate.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def CreateAnalysisTab(self,window):
    # Import Modules
    import copy
    import json
    from openpyxl import load_workbook
    import tkinter as tk
    from tkinter import messagebox
    from tkinter import simpledialog
    from tkinter import ttk 
    from tkinter import scrolledtext 
    import tksheet

    # Import Functions
    from General.DeleteWidgets import DeleteTab
    from Model.UpdateModelData import UpdateModelData

    # Initialize Model
    if 'Analysis' not in self.Compare.keys():
        self.Compare['Analysis'] = {}
        
    if 'Model ID' not in self.Compare.keys() == False:
        self.Compare['Model ID'] = None

    # Get available model information
    model_info = load_workbook(self.Compare['Paths']['Model Library'], data_only=True)

    # Delete all tab attributes
    if hasattr(self,"tab_att_list"):
        if hasattr(self,'clicked') == False:
            UpdateModelData(None, self, 3, 'Analysis')
        else:
            if self.clicked == 1:
                self.clicked = 0
            else:
                UpdateModelData(None, self, 3, 'Analysis')
        DeleteTab(self)

    if hasattr(self, 'canvas'):
        self.toolbar.destroy()
        self.canvas.get_tk_widget().destroy()
        del self.canvas

    # Preallocate the att list
    self.att_list = []
    self.loc_att_list = []
    self.tab_att_list = []
    self.clicked = 0

    # Preallocate Saved Models
    if 'Model Library' not in self.Compare.keys():
        self.Compare['Model Library'] = {}

    # Define Available Models
    self.Models = model_info.sheetnames

    def change_model(value):
        #----------------------------------------------------------------------
        #
        #   PURPOSE: Recreate page based on model choice.
        #
        #----------------------------------------------------------------------

        # Clear the model information if the model type changed
        try:
            if value != self.Compare['Analysis']['Model Name']:
                # Prompt user to save model
                self.save_model(None)

                # Clear model information
                self.Compare['Analysis'] = {}
        except:
            pass
        
        # Delete local attributes
        DeleteTab(self)

        # Clear sheets
        if hasattr(self,'sheet1_anly'):
            self.sheet1_anly.destroy()
            del self.sheet1
        if hasattr(self,'sheet2_anly'):
            self.sheet2_anly.destroy()
            del self.sheet2_anly

        # Read the model info
        ws = model_info[value]
        self.Compare['Analysis']['Model Name'] = value
        self.Compare['Analysis']['Model Info'] = {}
        for i in range(1,ws.max_row+1):
            self.Compare['Analysis']['Model Info'][ws.cell(row=i,column=1).value] = []
            j = 2
            if "Units" not in ws.cell(row=i,column=1).value:
                while ws.cell(row=i,column=j).value != None:
                    self.Compare['Analysis']['Model Info'][ws.cell(row=i,column=1).value].append(ws.cell(row=i,column=j).value)
                    j= j+1
            else:
                for j in range(2,len(self.Compare['Analysis']['Model Info'][ws.cell(row=i-1,column=1).value])+2):
                    self.Compare['Analysis']['Model Info'][ws.cell(row=i,column=1).value].append(ws.cell(row=i,column=j).value)
            
        # Get available reversible models
        self.RevModels = self.Compare['Analysis']['Model Info']['Reversible Models']
        
        if len(self.RevModels) > 0:
            # Create the label
            self.desc2 = ttk.Label(
                                window, 
                                text="Reversible Model:", 
                                anchor=tk.CENTER,       
                                style = 'Modern1.TLabel'                    
                                )
            self.desc2.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Label1'][0], 
                            rely = self.Placement['Analysis']['Label1'][1]
                            )
            self.tab_att_list.append('self.desc2')

            # Initialize the model
            rmod_opt = self.RevModels[0]

            # Check if previous data exists
            if 'Analysis' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'Reversible Model Name' in list(self.Compare['Analysis'].keys()):
                    if self.Compare['Analysis']['Reversible Model Name'] in self.RevModels:
                        rmod_opt = self.Compare['Analysis']['Reversible Model Name']

            # Create the reversible model drop down   
            self.optmenu2 = ttk.Combobox(
                                        window,
                                        values=self.RevModels,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu2.place(
                                anchor='n', 
                                relx = self.Placement['Analysis']['Combo1'][0], 
                                rely = self.Placement['Analysis']['Combo1'][1]
                                )
            self.optmenu2.set(rmod_opt)
            self.optmenu2.bind("<<ComboboxSelected>>",  lambda event:UpdateModelData(event, self, 1, 'Analysis'))
            self.tab_att_list.append('self.optmenu2')

            # Initialize Parameter List
            self.Params_VE = self.Compare['Analysis']['Model Info']['Reversible Deformation Parameters'] + self.Compare['Analysis']['Model Info']['Reversible Damage Parameters']
            self.Params_VE_Units = self.Compare['Analysis']['Model Info']['Reversible Deformation Parameter Units'] + self.Compare['Analysis']['Model Info']['Reversible Damage Parameter Units']

        # Get available irreversible models
        self.IrrevModels = self.Compare['Analysis']['Model Info']['Irreversible Models']

        if len(self.IrrevModels) > 0:
            # Create the label
            self.desc3 = ttk.Label(
                                window, 
                                text= "Irreversible Model:", 
                                anchor=tk.CENTER,       
                                style = "Modern1.TLabel"
                                )
            self.desc3.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Label2'][0], 
                            rely = self.Placement['Analysis']['Label2'][1]
                            )
            self.tab_att_list.append('self.desc3')

            # Initialize the irreversible model
            irmod_opt = self.IrrevModels[0]

            # Check if previous data exists
            if 'Analysis' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'Irreversible Model Name' in list(self.Compare['Analysis'].keys()):
                    if self.Compare['Analysis']['Irreversible Model Name'] in self.IrrevModels:
                        irmod_opt = self.Compare['Analysis']['Irreversible Model Name']

            # Create the irreversible model drop down
            self.optmenu3 = ttk.Combobox(
                                        window,
                                        values=self.IrrevModels,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu3.place(
                                anchor='n', 
                                relx = self.Placement['Analysis']['Combo2'][0], 
                                rely = self.Placement['Analysis']['Combo2'][1]
                                )
            self.optmenu3.set(irmod_opt)
            self.optmenu3.bind("<<ComboboxSelected>>",  lambda event:UpdateModelData(event, self, 2, 'Analysis'))
            self.tab_att_list.append('self.optmenu3')

            # Initialize Parameter List
            self.Params_VP = self.Compare['Analysis']['Model Info']['Irreversible Deformation Parameters'] + self.Compare['Analysis']['Model Info']['Irreversible Damage Parameters']
            self.Params_VP_Units = self.Compare['Analysis']['Model Info']['Irreversible Deformation Parameter Units'] + self.Compare['Analysis']['Model Info']['Irreversible Damage Parameter Units']

        def update_reversible_table(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Update the reversible model parameters table.
            #
            #------------------------------------------------------------------

            # Delete table if it exists
            if hasattr(self,"sheet_anly1"):
                if hasattr(self,"res_flag1") == True:
                    if self.res_flag1 == 0:
                        # Store data
                        self.sheet_anly1_data = self.sheet_anly1.data
                else:
                    # Store data
                    self.sheet_anly1_data = self.sheet_anly1.data

                # Delete sheet
                self.sheet_anly1.destroy()
                del self.sheet_anly1

            # Check if previous data exists
            if 'Analysis' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'VE_Param' in list(self.Compare['Analysis'].keys()):
                    if hasattr(self,"res_flag1") == True:
                        if self.res_flag1 == 0:
                            self.sheet_anly1_data = self.Compare['Analysis']['VE_Param']
                        else:
                            self.res_flag1 = 0
                    else:
                        self.sheet_anly1_data = self.Compare['Analysis']['VE_Param']

            if hasattr(self,"sheet_anly1_data") == False:
                self.sheet_anly1_data = []

            # Set the columns
            Cols = ['Parameter', 'Units', 'Value']

            # Create the table
            self.sheet_anly1 = tksheet.Sheet(
                                            window, 
                                            total_rows = len(self.Params_VE), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Analysis']['Sheet1'][2], 
                                            height = self.Placement['Analysis']['Sheet1'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Analysis']['Sheet1'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Analysis']['Sheet1'][4],"bold")
                                            )
            self.sheet_anly1.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Sheet1'][0], 
                            rely = self.Placement['Analysis']['Sheet1'][1]
                            )
            self.tab_att_list.append('self.sheet_anly1')
            self.sheet_anly1.change_theme("blue")
            self.sheet_anly1.set_index_width(0)

            def sort_cols(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Custom soring function.
                #
                #----------------------------------------------------------------------

                # Get the currently selected element
                currently_selected = self.sheet_anly1.get_currently_selected()
                
                # Get the list of values
                sort_list = []
                for i in range(self.sheet_anly1.visible_rows[1]):
                    sort_list.append(self.sheet_anly1.data[i][currently_selected.column])
                index_list = sorted(range(len(sort_list)), key=lambda k: sort_list[k])
                
                # Rewrite the table
                temp_data = copy.deepcopy(self.sheet_anly1.data)
                for i in range(self.sheet_anly1.visible_rows[1]):
                    for j in range(self.sheet_anly1.visible_columns[1]):
                        self.sheet_anly1.set_cell_data(i,j,temp_data[index_list[i]][j])
                self.sheet_anly1.redraw()

            # Enable Bindings
            self.sheet_anly1.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
            self.sheet_anly1.popup_menu_add_command('Sort', lambda : sort_cols(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet_anly1.extra_bindings([("cell_select", lambda event: self.cell_select_anly(event, 'sheet_anly1'))])

            # Set Column Widths
            self.sheet_anly1.column_width(column = 0, width = self.Placement['Analysis']['Sheet1'][5], redraw = True)
            self.sheet_anly1.column_width(column = 1, width = self.Placement['Analysis']['Sheet1'][6], redraw = True)
            self.sheet_anly1.column_width(column = 2, width = self.Placement['Analysis']['Sheet1'][7], redraw = True)
            self.sheet_anly1.table_align(align = 'c',redraw=True)

            # Set unit dictionary
            Units = {'Stress':['GPa','MPa','kPa','Pa','msi','ksi','psi'],
                    'Time':['s'],
                    'Time-1':['1/s']
                    }

            # Set Rows
            for i in range(len(self.Params_VE)):
                self.sheet_anly1.set_cell_data(i,0, self.Params_VE[i])
                if self.Params_VE_Units[i] != None:
                    for key in list(Units.keys()):
                        if self.Params_VE_Units[i] in Units[key]:
                            units_list = Units[key]
                else:
                    units_list = []
                def_val = self.Params_VE_Units[i]
                    
                self.sheet_anly1.create_dropdown(r=i, c = 1,values=units_list)
                if def_val != None:
                    self.sheet_anly1.set_cell_data(i,1, def_val)

            # Add Existing Data
            for i in range(len(self.sheet_anly1_data)):
                try:
                    # Find the corresponding index
                    rown = None
                    for j in range(len(self.sheet_anly1.data)):
                        if self.sheet_anly1.data[j][0] == self.sheet_anly1_data[i][0]:
                            rown = j

                    if rown != None:
                        for j in range(1,len(Cols)):
                            try:
                                self.sheet_anly1.set_cell_data(rown,j, self.sheet_anly1_data[i][j])
                            except:
                                pass
                except:
                    pass

            # Redraw the table
            self.sheet_anly1.redraw()

            # Update the Model Data
            UpdateModelData(None, self, 1, 'Analysis')

        def VE_param(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Get List of of ViscoElastic Mechanisms.
            #
            #------------------------------------------------------------------

            # Initialize Parameters
            self.Params_VE = []
            self.Params_VE_Units = []

            # Add non-mechanism dependent parameters
            for i in range(len(self.Compare['Analysis']['Model Info']['Reversible Deformation Parameters'])):
                param = self.Compare['Analysis']['Model Info']['Reversible Deformation Parameters'][i]
                unit = self.Compare['Analysis']['Model Info']['Reversible Deformation Parameter Units'][i]
                if '_[M]' not in param:
                    self.Params_VE.append(param)
                    self.Params_VE_Units.append(unit)
                else:
                    for i in range(int(value)):
                        param_mech = param.replace("_[M]",str(i+1))
                        self.Params_VE.append(param_mech)
                        self.Params_VE_Units.append(unit)

            # Update the reversible mechanisms table
            update_reversible_table(self)

        def update_irreversible_table(self):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Update the irreversible model parameters table.
            #
            #------------------------------------------------------------------

            # Delete table if it exists
            if hasattr(self,"sheet_anly2"):
                if hasattr(self,"res_flag2") == True:
                    if self.res_flag2 == 0:
                        # Store data
                        self.sheet_anly2_data = self.sheet_anly2.data
                else:
                    # Store data
                    self.sheet_anly2_data = self.sheet_anly2.data

                # Delete sheet
                self.sheet_anly2.destroy()
                del self.sheet_anly2
            
            # Check if previous data exists
            if 'Analysis' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'VP_Param' in list(self.Compare['Analysis'].keys()):
                    if hasattr(self,"res_flag2") == True:
                        if self.res_flag2 == 0:
                            self.sheet_anly2_data = self.Compare['Analysis']['VP_Param']
                        else:
                            self.res_flag2 = 0
                    else:
                        self.sheet_anly2_data = self.Compare['Analysis']['VP_Param']

            if hasattr(self,"sheet_anly2_data") == False:
                self.sheet_anly2_data = []

            # Set the columns
            Cols = ['Parameter', 'Units','Value']

            # Create the table
            self.sheet_anly2 = tksheet.Sheet(
                                            window, 
                                            total_rows = len(self.Params_VP), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            width = self.Placement['Analysis']['Sheet2'][2], 
                                            height = self.Placement['Analysis']['Sheet2'][3], 
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",self.Placement['Analysis']['Sheet2'][4],"normal"),
                                            header_font = ("Segoe UI",self.Placement['Analysis']['Sheet2'][4],"bold")
                                            )
            self.sheet_anly2.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Sheet2'][0], 
                            rely = self.Placement['Analysis']['Sheet2'][1]
                            )
            self.tab_att_list.append('self.sheet_anly2')
            self.sheet_anly2.change_theme("blue")
            self.sheet_anly2.set_index_width(0)

            def sort_cols(self):
                #----------------------------------------------------------------------
                #
                #   PURPOSE: Custom soring function.
                #
                #----------------------------------------------------------------------

                # Get currently selected element
                currently_selected = self.sheet_anly2.get_currently_selected()
                
                # Get the list of values
                sort_list = []
                for i in range(self.sheet_anly2.visible_rows[1]):
                    sort_list.append(self.sheet_anly2.data[i][currently_selected.column])
                index_list = sorted(range(len(sort_list)), key=lambda k: sort_list[k])
                
                # Rewrite the table
                temp_data = copy.deepcopy(self.sheet_anly2.data)
                for i in range(self.sheet_anly2.visible_rows[1]):
                    for j in range(self.sheet_anly2.visible_columns[1]):
                        self.sheet_anly2.set_cell_data(i,j,temp_data[index_list[i]][j])
                self.sheet_anly2.redraw()

            # Enable Bindings
            self.sheet_anly2.enable_bindings('single_select','cell_select', 'column_select', 'edit_cell',"arrowkeys", "right_click_popup_menu")
            self.sheet_anly2.popup_menu_add_command('Sort', lambda : sort_cols(self), table_menu = True, index_menu = True, header_menu = True)
            self.sheet_anly2.extra_bindings([("cell_select", lambda event: self.cell_select_anly(event, 'sheet_anly2'))])

            # Set Column Widths
            self.sheet_anly2.column_width(column = 0, width = self.Placement['Analysis']['Sheet2'][5], redraw = True)
            self.sheet_anly2.column_width(column = 1, width = self.Placement['Analysis']['Sheet2'][6], redraw = True)
            self.sheet_anly2.column_width(column = 2, width = self.Placement['Analysis']['Sheet2'][7], redraw = True)
            self.sheet_anly2.table_align(align = 'c',redraw=True)

            # Set unit dictionary
            Units = {'Stress':['GPa','MPa','kPa','Pa','msi','ksi','psi'],
                     'Stress-Time':['GPa-s','MPa-s','kPa-s','Pa-s','msi-s','ksi-s','psi-s'],
                    'Time':['s'],
                    'Time-1':['1/s']
                    }

            # Set Rows
            for i in range(len(self.Params_VP)):
                self.sheet_anly2.set_cell_data(i,0, self.Params_VP[i])
                if self.Params_VP_Units[i] != None:
                    for key in list(Units.keys()):
                        if self.Params_VP_Units[i] in Units[key]:
                            units_list = Units[key]
                else:
                    units_list = []
                def_val = self.Params_VP_Units[i]
                    
                self.sheet_anly2.create_dropdown(r=i, c = 1,values=units_list)
                if def_val != None:
                    self.sheet_anly2.set_cell_data(i,1, def_val)

            # Add Existing Data
            for i in range(len(self.sheet_anly2_data)):
                try:
                    # Find the corresponding index
                    rown = None
                    for j in range(len(self.sheet_anly2.data)):
                        if self.sheet_anly2.data[j][0] == self.sheet_anly2_data[i][0]:
                            rown = j

                    if rown != None:
                        for j in range(1,len(Cols)):
                            try:
                                self.sheet_anly2.set_cell_data(rown,j, self.sheet_anly2_data[i][j])
                            except:
                                pass
                except:
                    pass

            # Redraw the table
            self.sheet_anly2.redraw()

            # Update the Model Data
            UpdateModelData(None, self, 2, 'Analysis')

        # Get Number of ViscoPlastic Mechanisms
        def VP_param(value):
            #------------------------------------------------------------------
            #
            #   PURPOSE: Get List of of ViscoPlastic Mechanisms.
            #
            #------------------------------------------------------------------

            # Initialize Parameters
            self.Params_VP = []
            self.Params_VP_Units = []

            # Add non-mechanism dependent parameters
            for i in range(len(self.Compare['Analysis']['Model Info']['Irreversible Deformation Parameters'])):
                param = self.Compare['Analysis']['Model Info']['Irreversible Deformation Parameters'][i]
                unit = self.Compare['Analysis']['Model Info']['Irreversible Deformation Parameter Units'][i]
                if '_[N]' not in param:
                    self.Params_VP.append(param)
                    self.Params_VP_Units.append(unit)
                else:
                    for i in range(int(value)):
                        param_mech = param.replace("_[N]",str(i+1))
                        self.Params_VP.append(param_mech)
                        self.Params_VP_Units.append(unit)

            # Update the reversible mechanisms table
            update_irreversible_table(self)

        # Get number of viscoelastic parameters
        self.VEMech = self.Compare['Analysis']['Model Info']['Reversible Mechanisms']
        if len(self.VEMech) > 0:
            # Create the label
            self.desc4 = ttk.Label(
                                window, 
                                text="Viscoelastic Mechanisms (M):", 
                                anchor=tk.CENTER,       
                                style = "Modern1.TLabel"                   
                                )
            self.desc4.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Label3'][0], 
                            rely = self.Placement['Analysis']['Label3'][1]
                            )
            self.tab_att_list.append('self.desc4')

            # Initialize number of viscoelastic mechanisms
            ve_opt = self.VEMech[0]

            # Check if previous data exists
            if 'Analysis' in list(self.Compare.keys()):
                # Set the reversible model type
                if 'M' in list(self.Compare['Analysis'].keys()):
                    if int(self.Compare['Analysis']['M']) in self.VEMech:
                        ve_opt = int(self.Compare['Analysis']['M'])

            # Create the drop down
            self.optmenu4 = ttk.Combobox(
                                        window,
                                        values=self.VEMech,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu4.place(
                                anchor='n', 
                                relx = self.Placement['Analysis']['Combo3'][0], 
                                rely = self.Placement['Analysis']['Combo3'][1]
                                )
            self.optmenu4.set(ve_opt)
            self.optmenu4.bind("<<ComboboxSelected>>",  VE_param)
            self.tab_att_list.append('self.optmenu4')

            # Get list of viscoelastic parameters
            VE_param(ve_opt)

        # Get Number of Viscoplastic Mechanisms
        self.VPMech = self.Compare['Analysis']['Model Info']['Irreversible Mechanisms']
        if len(self.VPMech) > 0:
            # Create the label
            self.desc5 = ttk.Label(window, 
                            text="Viscoplastic Mechanisms (N):", 
                            anchor=tk.CENTER,       
                            style = "Modern1.TLabel"                  
                            )
            self.desc5.place(
                            anchor = 'n', 
                            relx = self.Placement['Analysis']['Label4'][0], 
                            rely = self.Placement['Analysis']['Label4'][1]
                            )
            self.tab_att_list.append('self.desc5')

            # Initialize Viscoplastic number of mechanisms
            vp_opt = self.VPMech[0]

            # Create the drop down menu
            self.optmenu5 = ttk.Combobox(
                                        window,
                                        values=self.VEMech,
                                        style="Modern.TCombobox",
                                        state="readonly"
                                        )
            self.optmenu5.place(
                                anchor='n', 
                                relx = self.Placement['Analysis']['Combo4'][0], 
                                rely = self.Placement['Analysis']['Combo4'][1]
                                )
            self.optmenu5.set(ve_opt)
            self.optmenu5.bind("<<ComboboxSelected>>",  VP_param)
            self.tab_att_list.append('self.optmenu5')

            # Get list of viscoplastic parameters
            VP_param(vp_opt)

        # Create the Load from Database button
        self.btn_load_db = ttk.Button(
                                    window, 
                                    text = "Load from Excel", 
                                    command = lambda:self.load_from_db('Analysis'), 
                                    style = "Modern3.TButton",
                                    width = self.Placement['Analysis']['Button1'][2]
                                    )
        self.btn_load_db.place(
                            anchor = 'w', 
                            relx = self.Placement['Analysis']['Button1'][0], 
                            rely = self.Placement['Analysis']['Button1'][1]
                            )
        self.tab_att_list.append('self.btn_load_db')

        # Create button to view/delete models
        self.btn_modlib = ttk.Button(
                                    window, 
                                    text = "Model Library", 
                                    command = lambda : self.Model_Library('Analysis'), 
                                    style = "Modern3.TButton",
                                    width = self.Placement['Analysis']['Button2'][2]
                                    )
        self.btn_modlib.place(
                            anchor = 'w', 
                            relx = self.Placement['Analysis']['Button2'][0], 
                            rely = self.Placement['Analysis']['Button2'][1]
                            )
        self.tab_att_list.append('self.btn_modlib')

        # Create the Optimize button
        self.btn_anly = ttk.Button(
                                window, 
                                text = "Analyze", 
                                command = self.analyze, 
                                style = "Modern3.TButton",
                                width = self.Placement['Analysis']['Button3'][2]
                                )
        self.btn_anly.place(
                            anchor = 'w', 
                            relx = self.Placement['Analysis']['Button3'][0], 
                            rely = self.Placement['Analysis']['Button3'][1]
                            )
        self.tab_att_list.append('self.btn_anly')

        def save_model_local():
            #------------------------------------------------------------------
            #
            #   PURPOSE: Save models to the project library.
            #
            #------------------------------------------------------------------

            # Set the model type
            self.Compare['Analysis']['Compare Type'] = 'Analysis'

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
            json_string = json.dumps(self.Compare['Analysis'])
            binary_data = json_string.encode('utf-8')
            self.Compare['Model Library'][user_input] = binary_data

            # Set the model name
            self.Compare['Model ID'] = user_input

        # Create button to save a model
        self.btn_savemod = ttk.Button(
                                    window, 
                                    text = "Save Model", 
                                    command = save_model_local, 
                                    style = "Modern3.TButton",
                                    width = self.Placement['Analysis']['Button4'][2]
                                    )
        self.btn_savemod.place(
                            anchor = 'w', 
                            relx = self.Placement['Analysis']['Button4'][0], 
                            rely = self.Placement['Analysis']['Button4'][1]
                            )
        self.tab_att_list.append('self.btn_savemod')

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
                root = tk.Tk() 
                root.geometry("600x400")
                root.title("Enter Model Notes") 
                
                # Create the label
                ttk.Label(
                        root, 
                        text="Enter Model Notes:", 
                        style = "Modern1.TLabel"
                        ).place(anchor='n', relx = 0.5, rely = 0.1) 
                
                # Create the note area
                text_area = scrolledtext.ScrolledText(
                                                    root, 
                                                    wrap=tk.WORD, 
                                                    width=40, 
                                                    height=8, 
                                                    font=("Segoe UI", 14)) 
                text_area.place(anchor='c', relx = 0.5, rely = 0.5)

                # Display any existing notes
                if 'Note' in list(self.Compare['Analysis'].keys()):
                    text_area.insert("end", self.Compare['Analysis']['Note']) 
                
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
                        self.Compare['Analysis']['Note'] = text_area.get("1.0",'end-1c')
                    except:
                        pass

                    # Reset the window
                    self.note_click = 0
                    root.destroy()

                # Add the exit protocol to the root
                root.protocol("WM_DELETE_WINDOW", lambda:on_closing_root(self))


        # Create button to add a note
        self.btn_addnote = ttk.Button(
                                    window, 
                                    text = "Model Notes", 
                                    command = add_note, 
                                    style = "Modern3.TButton",
                                    width = self.Placement['Analysis']['Button5'][2]
                                    )
        self.btn_addnote.place(
                            anchor = 'w', 
                            relx = self.Placement['Analysis']['Button5'][0], 
                            rely = self.Placement['Analysis']['Button5'][1]
                            )
        self.tab_att_list.append('self.btn_addnote')

        # Update Model Data
        UpdateModelData(None, self, 3, 'Analysis')

        # Update Tables
        if len(self.Compare['Analysis']['Model Info']['Reversible Models']) > 0:
                update_reversible_table(self)
        if len(self.Compare['Analysis']['Model Info']['Irreversible Models']) > 0:
            update_irreversible_table(self)

    # Create the label for Model Type
    self.desc1 = ttk.Label(
                        window, 
                        text="Select the Model:", 
                        anchor=tk.CENTER,       
                        style = "Modern1.TLabel"                   
                        )
    self.desc1.place(
                    anchor = 'n', 
                    relx = self.Placement['Analysis']['Label6'][0], 
                    rely = self.Placement['Analysis']['Label6'][1]
                    )
    self.loc_att_list.append('self.desc1')

    # Initialize the model option
    mod_opt = self.Models[0]

    # Check if previous value exists
    if 'Analysis' in list(self.Compare.keys()):
        # Set the model name
        if 'Model Name' in list(self.Compare['Analysis'].keys()):
            if self.Compare['Analysis']['Model Name'] in self.Models:
                mod_opt = self.Compare['Analysis']['Model Name']

     # Create Option Menu for Model Type
    self.optmenu1 = ttk.Combobox(
                                window,
                                values=self.Models,
                                style="Modern.TCombobox",
                                state="readonly"
                                )
    self.optmenu1.place(
                        anchor='n', 
                        relx = self.Placement['Analysis']['Combo5'][0], 
                        rely = self.Placement['Analysis']['Combo5'][1]
                        )
    self.optmenu1.set(mod_opt)
    self.optmenu1.bind("<<ComboboxSelected>>",  change_model)
    change_model(mod_opt)
    self.loc_att_list.append('self.optmenu1')