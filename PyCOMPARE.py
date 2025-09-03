#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#   PyCOMPARE.py
#   Brandon Hearley - LMS
#   brandon.l.hearley@nasa.gov
#   8/25/2025
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import Modules
import copy
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from matplotlib.ticker import ScalarFormatter
import numpy as np
import os
import pandas as pd
import pickle
from PIL import ImageTk, Image
from scipy.interpolate import CubicSpline
import shutil
import threading
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import ttk 
import tksheet
import webbrowser

# Import Functions
from Data.CreateCharacterizationTab import *
from Data.CreateDataTab import *
from General.BuildGeneralPage import *
from General.CreateExportTab import *
from General.CreateSettingsTab import *
from General.GetProjectFile import *
from GUI.Placements import *
from GUI.GetStyles import *
from Model.CreateAnalysisTab import*
from Model.CreateModelTab import *
from Model.GVIPS.WriteDSG_GVIPS_ISO_ANLY import *
from Model.GVIPS.WriteDSG_GVIPS_TISO_ANLY import *
from Model.GVIPS.WriteDSG_GVIPS_ISO_OPT import *
from Model.GVIPS.WriteDSG_GVIPS_TISO_OPT import *
from Model.GVIPS.WriteNLP import *
from Model.GVIPS.WriteSIM_ISO import *
from Model.GVIPS.WriteSIM_TISO import *
from Model.ReadModel import *
from Model.UnitConversion import *
from Model.UpdateModelData import *
from Visualization.CreateVisualizationTab import *

#Create the GUI
class PY_COMPARE:

    #------------------------------------------------------------------------------
    #
    #   GENERAL FUNCTIONS
    #   Initialize the GUI, enable saving and loading of projects
    #
    #------------------------------------------------------------------------------

    def __init__(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Initialize the GUI.
        #
        #--------------------------------------------------------------------------

        # Set global variales
        global window

        # Create Background Window
        window = tk.Tk()
        window.title("PCOMPARE")
        window.configure(bg='white')

        # Get Placement Information
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        Placements(self, screen_width, screen_height)

        # Set Window Size
        window.geometry(f'{self.screen_w}x{self.screen_h}')

        # Load the style
        GetStyles(self)

        # Set home directory
        self.home = os.getcwd()

        # Initialize the data structure
        self.Compare = {}

        # Initialize the Path Dependencies
        model_library = os.path.join(self.home,'Model','AvailableModels.json')
        import_template = os.path.join(self.home,'Templates','ImportTemplate.xlsx')
        export_template = os.path.join(self.home,'Templates','ExportTemplate.xlsx')
        compare_path = os.path.join(self.home,'compnasardamage.exe')
        self.Compare['Paths'] = {'Model Library':model_library,
                                    'Import Template':import_template,
                                    'Export Template':export_template,
                                    'Compare Executable':compare_path,}

        # Create Main Toolbar
        self.toolbar = ttk.Frame(
                                window, 
                                padding=2, 
                                style = 'White.TFrame'
                                )
        self.toolbar.place(
                            anchor = 'nw', 
                            relx = self.Placement['HomePage']['Toolbar'][0], 
                            rely = self.Placement['HomePage']['Toolbar'][1],
                            relwidth = self.Placement['HomePage']['Toolbar'][2],
                            relheight = self.Placement['HomePage']['Toolbar'][3],
                            )

        # Function to show the menu
        def show_menu(event, menu):
            #--------------------------------------------------------------------------
            #
            #   PURPOSE: Show the menu
            #
            #--------------------------------------------------------------------------
            menu.post(event.x_root, event.y_root)

        # Create the file menu
        self.file_menu = tk.Menu(window, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_project)
        self.file_menu.add_command(label="Open", command=self.load_project)
        self.file_menu.add_command(label="Save", command=self.save)
        self.file_menu.add_command(label="Save As", command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=lambda:on_closing(self))

        # Create the file menu button
        self.file_btn = ttk.Button(self.toolbar, text="File", style = "Modern4.TButton")
        self.file_btn.pack(side="left", padx=2, pady = 0)
        self.file_btn.bind("<Button-1>", lambda e: show_menu(e, self.file_menu))

        # Create the help menu
        self.help_menu = tk.Menu(window, tearoff=0)
        self.help_menu.add_command(label="About", command=self.help)

        # Create the help menu button
        self.help_btn = ttk.Button(self.toolbar, text="Help", style = "Modern4.TButton")
        self.help_btn.pack(side="left", padx=2, pady = 0)
        self.help_btn.bind("<Button-1>", lambda e: show_menu(e, self.help_menu))

        # Create the Title
        img = Image.open(os.path.join(self.home,'GUI','TitleHeader.png'))
        scale = self.Placement['HomePage']['Title'][4]*self.scale
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_hdr = ImageTk.PhotoImage(img)
        self.panel_hdr = tk.Label(window, image = self.img_hdr, bg = 'white')
        self.panel_hdr.place(
                            anchor = 'n', 
                            relx = self.Placement['HomePage']['Title'][0], 
                            rely = self.Placement['HomePage']['Title'][1],
                            relwidth = self.Placement['HomePage']['Title'][2],
                            relheight = self.Placement['HomePage']['Title'][3],
                            )

        # Create the NASA Logo
        img = Image.open(os.path.join(self.home,'GUI','NasaLogo.png'))
        scale = self.Placement['HomePage']['Logo'][4]*self.scale
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_nasa = ImageTk.PhotoImage(img)
        self.panel_nasa = tk.Label(window, image = self.img_nasa, bg = 'white')
        self.panel_nasa.place(
                            anchor = 'e', 
                            relx = self.Placement['HomePage']['Logo'][0], 
                            rely = self.Placement['HomePage']['Logo'][1],
                            relwidth = self.Placement['HomePage']['Logo'][2],
                            relheight = self.Placement['HomePage']['Logo'][3],
                            )
        
        try:
            window.iconbitmap(os.path.join(self.home,'GUI','NasaLogo.ico'))
        except:
            img = Image.open(os.path.join(self.home,'GUI','Nasa-Logo-Large.jpg'))
            img.save(os.path.join(self.home,'GUI','NasaLogo.ico'), sizes=[(16,16), (32,32), (48,48), (64,64), (128, 128), (256, 256)])
            window.iconbitmap(os.path.join(self.home,'GUI','NasaLogo.ico'))

        
        # Build the general page
        BuildGeneralPage(self, window)

        # Ask for save when closing
        def on_closing(self):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Set exit protocol for the main prgoram.
            #
            #----------------------------------------------------------------------

            # Prompt user to save
            if messagebox.askyesno(title = "Quit", message = "Do you want to save before exiting?"):

                # Check if project file does not exist
                if hasattr(self,'proj_file') == False or self.proj_file is None:

                    # Create project file
                    CreateNewProject(self)
                
                # Update the model info
                UpdateModelData(None, self, 3, 'Model')

                # Write data to project file
                with open(self.proj_file, 'wb') as file:
                    pickle.dump(self.Compare, file)

                # Display save message to user
                messagebox.showinfo(title = 'Save', message = 'Project Saved!')

            # Destory the window
            window.destroy()

        # Create Window Exit Protocol
        window.protocol("WM_DELETE_WINDOW", lambda:on_closing(self))

        #Main Loop
        window.mainloop()

    def new_project(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Initialize a new project and load the general page.
        #
        #--------------------------------------------------------------------------

        # Check save
        if hasattr(self,'proj_file') and self.proj_file is not None:

            # Prompt user to save
            if messagebox.askyesno(title = "Quit", message = "Do you want to save the project first?"):

                # Update the model info
                UpdateModelData(None, self, 3, 'Model')

                # Write data to project file
                with open(self.proj_file, 'wb') as file:
                    pickle.dump(self.Compare, file)

                # Display save message to user
                messagebox.showinfo(title = 'Save', message = 'Project Saved!')

        # Create new project file
        CreateNewProject(self)

        # Build the General Page
        BuildGeneralPage(self, window)

    def load_project(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load an existing proejct file and the general page.
        #
        #--------------------------------------------------------------------------
        
        # Save previous
        prev_file = None
        try:
            prev_file = self.proj_file
        except:
            pass
        
        # Load existing project file
        LoadProject(self)

        # Initialize the data structure and build the home page
        if self.proj_file != None:

            # Build the General Page
            BuildGeneralPage(self, window)

        else:
            self.proj_file = prev_file

    def save(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the project file.
        #
        #--------------------------------------------------------------------------

        try:
            # Get the file name
            file = self.proj_file

            # Get the log file
            self.log_file = os.path.join(os.getcwd(),"Logs",os.path.basename(self.proj_file).split('.')[0] + ".log")
            if os.path.exists(os.path.join(os.getcwd(),"Logs","temp.log")) == True and os.path.exists(self.log_file) == False:
                os.rename(os.path.join(os.getcwd(),"Logs","temp.log"), self.log_file)

        except:
            # Create new project file
            CreateNewProject(self)

        # Check that file exists
        if self.proj_file is not None:
            # Update the model info
            UpdateModelData(None, self, 3, 'Model')

            # Write data to file
            with open(self.proj_file, 'wb') as file:
                pickle.dump(self.Compare, file)

            # Show save message to user
            messagebox.showinfo(title = 'Save', message = 'Project Saved!')

    def save_as(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the project file.
        #
        #--------------------------------------------------------------------------

        try:
            # Get the file name
            file = self.proj_file

            # Get the log file
            self.log_file = os.path.join(os.getcwd(),"Logs",os.path.basename(self.proj_file).split('.')[0] + ".log")
            if os.path.exists(os.path.join(os.getcwd(),"Logs","temp.log")) == True and os.path.exists(self.log_file) == False:
                os.rename(os.path.join(os.getcwd(),"Logs","temp.log"), self.log_file)

        except:

            # Create new project file
            file = None

        # Create new project file
        CreateNewProject(self)

        # Check that file exists
        if self.proj_file is not None:
            # Update the model info
            UpdateModelData(None, self, 3, 'Model')

            # Write data to file
            with open(self.proj_file, 'wb') as file:
                pickle.dump(self.Compare, file)

            # Show save message to user
            messagebox.showinfo(title = 'Save', message = 'Project Saved!')

        # Set the project file
        else:
            self.proj_file = file

    def help(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load the help page in a web browser
        #
        #--------------------------------------------------------------------------

        # Set path to HTM file
        file_path = os.path.join(os.getcwd(),'Documentation','PyCOMPARE_UserManual.htm')

        # Open in default browser
        webbrowser.open(f"file://{file_path}")

    def on_tab_changed(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load each tab to the notebook
        #
        #--------------------------------------------------------------------------

        # Get the notebook and selected tab
        notebook = event.widget  
        tab_id = notebook.select()   
        tab_index = notebook.index(tab_id)  

        # Load the corresponding page
        if tab_index == 0:
            CreateDataTab(self, window)
        elif tab_index == 1:
            CreateCharacterizationTab(self, window)
        elif tab_index == 2:
            CreateModelTab(self, window)
        elif tab_index == 3:
            CreateAnalysisTab(self,window)
        elif tab_index == 4:
            CreateVisualizationTab(self,window)
        elif tab_index == 5:
            CreateExportTab(self,window)
        elif tab_index == 6:
            CreateSettingsTab(self)

    #------------------------------------------------------------------------------
    #
    #   DATABASE FUNCTIONS
    #   Functions for the Database Tab
    #
    #------------------------------------------------------------------------------    

    def plotter_db(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create plots of individual test response curves on the 
        #            database tab
        #
        #--------------------------------------------------------------------------

        #  Delete the canvas and drop down if it exists
        if hasattr(self, 'canvas_db'):
            self.toolbar_db.destroy()
            self.canvas_db.get_tk_widget().destroy()
            del self.canvas_db

        # Create the plot
        self.fig_db = Figure(
                            figsize=(self.Placement['Data']['Figure1'][4],self.Placement['Data']['Figure1'][5]), 
                            dpi = self.Placement['Data']['Figure1'][6], 
                            constrained_layout = True
                            )
        self.plot1 = self.fig_db.add_subplot(111)

        # Get the arrays
        x_val = self.optmenu1_plt_db.get()
        y_val = self.optmenu2_plt_db.get()

        # X Value
        if 'Time' in x_val:
            x = self.Compare['Data'][self.test_name]['Time']
            xu = 'Time [s]'
        else:
            x_val = x_val.split('-')
            x = self.Compare['Data'][self.test_name][x_val[0]][int(x_val[1])]
            if x_val[0] == 'Strain':
                xu = 'Strain'
            else:
                xu = 'Stress [MPa]'

         # Y Value
        if 'Time' in y_val:
            y = self.Compare['Data'][self.test_name]['Time']
            ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            yu = 'Time [s]'
        else:
            y_val = y_val.split('-')
            y = self.Compare['Data'][self.test_name][y_val[0]][int(y_val[1])]
            if y_val[0] == 'Strain':
                yu = 'Strain'
            else:
                yu = 'Stress [MPa]'

        # Plot the data
        for i in range(len(self.Compare['Data'][self.test_name]['Stage Index'])):
            if i == 0:
                start_idx = 0
            else:
                start_idx = int(self.Compare['Data'][self.test_name]['Stage Index'][i-1])
            self.plot1.plot(x[start_idx:int(self.Compare['Data'][self.test_name]['Stage Index'][i])+1],
                            y[start_idx:int(self.Compare['Data'][self.test_name]['Stage Index'][i])+1],
                            label=self.Compare['Data'][self.test_name]['Stage Type'][i])
            
        # Set Plot Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot1.set_xlabel(xlab)
        self.plot1.set_ylabel(ylab)
        self.plot1.xaxis.set_major_formatter(xlab_frmt)
        self.plot1.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot1.legend()

        # Create the Tkinter canvas
        self.canvas_db = FigureCanvasTkAgg(self.fig_db, master = self.nb_tab_tab1)

        # Create the Matplotlib toolbar
        self.toolbar_db = NavigationToolbar2Tk(self.canvas_db, self.nb_tab_tab1)

        # Format Toolbar
        self.toolbar_db.config(bg='white')
        self.toolbar_db._message_label.config(background='white')
        self.toolbar_db.place(
                        anchor = 'n', 
                        relx = self.Placement['Data']['Toolbar1'][0], 
                        rely = self.Placement['Data']['Toolbar1'][1],
                        relwidth = self.Placement['Data']['Toolbar1'][2], 
                        relheight = self.Placement['Data']['Toolbar1'][3]
                        )

        # Add the figure to the GUI
        self.canvas_db.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Data']['Figure1'][0], 
                                        rely = self.Placement['Data']['Figure1'][1],
                                        relwidth = self.Placement['Data']['Figure1'][2], 
                                        relheight = self.Placement['Data']['Figure1'][3]
                                        )
        
        # Update window
        self.nb_tab_tab1.update_idletasks()
        self.canvas_db.draw()
        self.toolbar_db.update()
        
        if 'self.canvas_db' not in self.atts['Database']['Local']:
            self.atts['Database']['Local'].append('self.canvas_db')
            self.atts['Database']['Local'].append('self.toolbar_db')

    def plotter_all_db(self, val):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Plot all curves on the same plot on the database tab.
        #
        #--------------------------------------------------------------------------

        # Get the value
        value = self.optmenu1_plt_db.get()

        #  Delete the canvas and drop down if it exists
        if hasattr(self, 'canvas_db'):
            self.toolbar_db.destroy()
            self.canvas_db.get_tk_widget().destroy()
            del self.canvas_db

        # Reset any formatting on the test sheet
        for i in range(len(self.sheet_db.data)):
            self.sheet_db.highlight_rows(i,'white','black')

        # Create the plot
        self.fig_db = Figure(
                            figsize=(self.Placement['Data']['Figure1'][4],self.Placement['Data']['Figure1'][5]), 
                            dpi = self.Placement['Data']['Figure1'][6], 
                            constrained_layout = True
                            )
        self.plot1 = self.fig_db.add_subplot(111)

        # Initialize the display curves
        disp_tests = []
        disp_load = []
        disp_type = []

        # Get display curves for the database tab
        if self.sheet_db.winfo_exists():
            for i in range(len(self.sheet_db.data)):
                if self.sheet_db.data[i][0] == True:
                    if value in [self.sheet_db.data[i][2], 'All']:
                        disp_tests.append(self.sheet_db.data[i][1])
                        disp_load.append(int(self.sheet_db.data[i][4]))
                        disp_type.append(self.sheet_db.data[i][2])

        # Loop through all tests selected
        for test in disp_tests:
            if disp_type[disp_tests.index(test)] == 'Tensile':
                end_idx = self.Compare['Data'][test]['Stage Index'][0]
            if disp_type[disp_tests.index(test)] == 'Creep':
                end_idx = self.Compare['Data'][test]['Stage Index'][1]
            if disp_type[disp_tests.index(test)] == 'Relaxation':
                end_idx = self.Compare['Data'][test]['Stage Index'][1]
            if disp_type[disp_tests.index(test)] == 'Generic':
                end_idx = self.Compare['Data'][test]['Stage Index'][-1]
            
            # Plot the data
            if value == 'Tensile' or value == 'Generic' or value == 'All':
                self.plot1.plot(self.Compare['Data'][test]['Strain'][disp_load[disp_tests.index(test)]][:end_idx],
                                self.Compare['Data'][test]['Stress'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Strain'
                ylab = 'Stress [MPa]'
            elif value == 'Creep':
                self.plot1.plot(self.Compare['Data'][test]['Time'][:end_idx],
                                self.Compare['Data'][test]['Strain'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Time [s]'
                ylab = 'Strain'
            elif value == 'Relaxation':
                self.plot1.plot(self.Compare['Data'][test]['Time'][:end_idx],
                                self.Compare['Data'][test]['Stress'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Time [s]'
                ylab = 'Stress [MPa]'

        if len(disp_tests) > 0:

            # Format the plot
            xlab_frmt = ScalarFormatter() 
            ylab_frmt = ScalarFormatter()
            self.plot1.set_xlabel(xlab)
            self.plot1.set_ylabel(ylab)
            self.plot1.xaxis.set_major_formatter(xlab_frmt)
            self.plot1.yaxis.set_major_formatter(ylab_frmt)
            if "Strain" in xlab or "Time" in xlab:
                self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
            if "Strain" in ylab or "Time" in ylab:
                self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
            self.plot1.legend()

            # Create the Tkinter canvas
            self.canvas_db = FigureCanvasTkAgg(self.fig_db, master = self.nb_tab_tab1)
            
            # Create the Matplotlib toolbar
            self.toolbar_db = NavigationToolbar2Tk(self.canvas_db, self.nb_tab_tab1)
            
            # Format Toolbar
            self.toolbar_db.config(bg='white')
            self.toolbar_db._message_label.config(background='white')
            self.toolbar_db.place(
                            anchor = 'n', 
                            relx = self.Placement['Data']['Toolbar1'][0], 
                            rely = self.Placement['Data']['Toolbar1'][1],
                            relwidth = self.Placement['Data']['Toolbar1'][2], 
                            relheight = self.Placement['Data']['Toolbar1'][3]
                            )

            # Add the figure to the GUI
            self.canvas_db.get_tk_widget().place(
                                            anchor = 'n', 
                                            relx = self.Placement['Data']['Figure1'][0], 
                                            rely = self.Placement['Data']['Figure1'][1],
                                            relwidth = self.Placement['Data']['Figure1'][2], 
                                            relheight = self.Placement['Data']['Figure1'][3]
                                            )
            # Update window
            self.nb_tab_tab1.update_idletasks()
            self.canvas_db.draw()
            self.toolbar_db.update()

            #
            if 'self.canvas_db' not in self.atts['Database']['Local']:
                self.atts['Database']['Local'].append("self.canvas_db")
                self.atts['Database']['Local'].append("self.toolbar_db")

    #------------------------------------------------------------------------------
    #
    #   CHARACTERIZATION FUNCTIONS
    #   Functions for the Characterization Tab
    #
    #------------------------------------------------------------------------------
    
    def cell_select_char(self, response):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create Custom Column Disablement for Characterization Test Set
        #
        #--------------------------------------------------------------------------

        # Define locked columns (all but weight)
        locked_cols = [0,1,2,3,4,5,6]

        # Enable/Disable user ability to edit cells
        if response.selected.column != None:
            if response.selected.column in locked_cols:
                self.sheet_char.disable_bindings(("edit_cell"))
            else:
                self.sheet_char.enable_bindings(("edit_cell"))
                self.sheet_char.extra_bindings([("edit_cell", self.save_weight)])
            self.sheet_char.redraw()

    def save_weight(self, response):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save the test weights
        #
        #--------------------------------------------------------------------------
        
        # Get Characterization Table Data
        data = self.sheet_char.data

        # Get all weights
        weights = []
        for i in range(len(data)):
            try:
                weights.append(float(data[i][7]))
            except: 
                weights.append(0)

        # Write relative weights
        for i in range(len(data)):
            test_name = data[i][0]
            self.Compare['Characterization'][test_name]['RelWeight'] = weights[i]

    def cell_select_stage(self, response):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create Custom Column Disablement for Stage Table 
        #            (Data Reduction Window) 
        #
        #--------------------------------------------------------------------------

        # Get locked columns
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        if response.selected.column != None:
            if response.selected.column in locked_cols:
                self.stage_pts_sheet.disable_bindings(("edit_cell"))
            else:
                self.stage_pts_sheet.enable_bindings(("edit_cell"))
                self.stage_pts_sheet.extra_bindings([("edit_cell", self.edit_stage_pts)])
            self.stage_pts_sheet.redraw()

    def edit_stage_pts(self, response):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Edit the Stage Table (Characterization Tab) with the new 
        #            reduced number of data points 
        #
        #--------------------------------------------------------------------------

        # Get the selected row and column
        c = response.selected.column
        r = response.selected.row

        # Set the number of division points
        try:
            int(self.stage_pts_sheet.data[r][c])
        except:
            self.stage_pts_sheet.set_cell_data(r,c,10)
            self.stage_pts_sheet.redraw()

    def plotter_char(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create plots of individual test response curves in the
        #            characterization
        #
        #--------------------------------------------------------------------------

        #  Delete the canvas and drop down if it exists
        if hasattr(self, 'canvas_char'):
            self.toolbar_char.destroy()
            self.canvas_char.get_tk_widget().destroy()
            del self.canvas_char

        # Create the plot
        self.fig_char = Figure(
                            figsize=(self.Placement['Characterization']['Figure1'][4],self.Placement['Characterization']['Figure1'][5]), 
                            dpi = self.Placement['Characterization']['Figure1'][6], 
                            constrained_layout = True
                            )
        self.plot1 = self.fig_char.add_subplot(111)

        # Get the arrays
        x_val = self.optmenu1_plt_char.get()
        y_val = self.optmenu2_plt_char.get()

        # X Value
        if 'Time' in x_val:
            x = self.Compare['Data'][self.test_name]['Time']
            xs = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            xu = 'Time [s]'
        else:
            x_val = x_val.split('-')
            x = self.Compare['Data'][self.test_name][x_val[0]][int(x_val[1])]
            xs = self.Compare['Data'][self.test_name]['Reduced Data'][x_val[0]][int(x_val[1])]
            if x_val[0] == 'Strain':
                xu = 'Strain'
            else:
                xu = 'Stress [MPa]'

         # Y Value
        if 'Time' in y_val:
            y = self.Compare['Data'][self.test_name]['Time']
            ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            yu = 'Time [s]'
        else:
            y_val = y_val.split('-')
            y = self.Compare['Data'][self.test_name][y_val[0]][int(y_val[1])]
            ys = self.Compare['Data'][self.test_name]['Reduced Data'][y_val[0]][int(y_val[1])]
            if y_val[0] == 'Strain':
                yu = 'Strain'
            else:
                yu = 'Stress [MPa]'

        # Plot the data
        for i in range(len(self.Compare['Data'][self.test_name]['Stage Index'])):
            if i == 0:
                start_idx = 0
            else:
                start_idx = int(self.Compare['Data'][self.test_name]['Stage Index'][i-1])
            self.plot1.plot(x[start_idx:int(self.Compare['Data'][self.test_name]['Stage Index'][i])+1],
                            y[start_idx:int(self.Compare['Data'][self.test_name]['Stage Index'][i])+1],
                            label=self.Compare['Data'][self.test_name]['Stage Type'][i])

        # Plot Reduced Data Points on the Characterization Tab
        if xs is not None:
            self.xdata = x
            self.ydata = y
            self.xsdata = xs
            self.ysdata = ys
            self.plot1.plot(xs,ys,'ro',label='Sample Points')

            # Function to add a point
            def AddPoint():
                #----------------------------------------------------------
                #
                #   PURPOSE: Bind button click to adding a reduced data 
                #            point.
                #
                #----------------------------------------------------------

                # Bind the button click
                if self.clicked == 0:
                    self.clicked = 1
                    self.plot1.figure.canvas.mpl_connect('button_press_event', self.add_point)

                # Reset the vizualization flag
                self.viz_init = 0

            # Create Add Point Button
            if hasattr(self, 'btn_add_pt'):
                self.btn_add_pt.destroy()

            self.btn_add_pt = ttk.Button(
                                    self.nb_tab_tab2, 
                                    text = "Add", 
                                    command = AddPoint, 
                                    style = 'Modern3.TButton',
                                    )
            self.btn_add_pt.place(
                                anchor = 'n', 
                                relx = self.Placement['Characterization']['ButtonAdd'][0], 
                                rely = self.Placement['Characterization']['ButtonAdd'][1],
                                relwidth = self.Placement['Characterization']['ButtonAdd'][2], 
                                relheight = self.Placement['Characterization']['ButtonAdd'][3]
                                )
            if 'self.btn_add_pt' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.btn_add_pt')

            # Function to delete a point
            def DelPoint():
                #----------------------------------------------------------
                #
                #   PURPOSE: Bind button click to deleting a reduced data 
                #            point.
                #
                #----------------------------------------------------------

                # Bind the button click
                if self.clicked == 0:
                    self.clicked = 1
                    self.plot1.figure.canvas.mpl_connect('button_press_event', self.del_point)

                # Reset the vizualization flag
                self.viz_init = 0

            # Create Delete Point Button
            if hasattr(self, 'btn_del_pt'):
                self.btn_del_pt.destroy()
            self.btn_del_pt = ttk.Button(
                                    self.nb_tab_tab2, 
                                    text = "Delete", 
                                    command = DelPoint, 
                                    style = "Modern3.TButton",
                                    )
            self.btn_del_pt.place(
                                anchor = 'n', 
                                relx = self.Placement['Characterization']['ButtonDel'][0], 
                                rely = self.Placement['Characterization']['ButtonDel'][1],
                                relwidth = self.Placement['Characterization']['ButtonDel'][2], 
                                relheight = self.Placement['Characterization']['ButtonDel'][3]
                                )
            if 'self.btn_del_pt' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append('self.btn_del_pt')

        # Set Plot Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot1.set_xlabel(xlab)
        self.plot1.set_ylabel(ylab)
        self.plot1.xaxis.set_major_formatter(xlab_frmt)
        self.plot1.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot1.legend()

        # Create the Tkinter canvas
        self.canvas_char = FigureCanvasTkAgg(self.fig_char, master = self.nb_tab_tab2)

        # Create the Matplotlib toolbar
        self.toolbar_char = NavigationToolbar2Tk(self.canvas_char, self.nb_tab_tab2)

        # Format Toolbar
        self.toolbar_char.config(bg='white')
        self.toolbar_char._message_label.config(background='white')
        self.toolbar_char.place(
                        anchor = 'n', 
                        relx = self.Placement['Characterization']['Toolbar1'][0], 
                        rely = self.Placement['Characterization']['Toolbar1'][1],
                        relwidth = self.Placement['Characterization']['Toolbar1'][2], 
                        relheight = self.Placement['Characterization']['Toolbar1'][3]
                        )

        # Add the figure to the GUI
        self.canvas_char.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Characterization']['Figure1'][0], 
                                        rely = self.Placement['Characterization']['Figure1'][1],
                                        relwidth = self.Placement['Characterization']['Figure1'][2], 
                                        relheight = self.Placement['Characterization']['Figure1'][3]
                                        )
        
        # Update window
        self.nb_tab_tab2.update_idletasks()
        self.canvas_char.draw()
        self.toolbar_char.update()

        if "self.canvas_char" not in self.atts['Characterization']['Local']:
            self.atts['Characterization']['Local'].append('self.canvas_char')
            self.atts['Characterization']['Local'].append('self.toolbar_char')

        # Enable Data Reduction on the Characterization Table      
        def ReduceData():
            #--------------------------------------------------------------
            #
            #   PURPOSE: Reduce data based on stage type
            #
            #--------------------------------------------------------------
        
            # Get the selected row and name
            row = None
            for i in range(len(self.sheet_char.data)):
                if self.sheet_char.get_row_options(None)[i]['highlight'].bg == 'lightblue1':
                    row = i
            try:
                # Get the test information
                self.test_name = self.sheet_char.data[row][0]
                self.test_type = self.sheet_char.data[row][1]
                self.load_dir = int(self.sheet_char.data[row][3])
                rows = self.Compare['Data'][self.test_name]['Stage Type']
            except:
                messagebox.showinfo(message="No test selected.")

            # Create the Segmentation Control Panel
            root = tk.Toplevel(window)
            root.geometry(f"{int(400*self.scale)}x{int(600*self.scale)}")
            root.configure(bg='white')
            root.title("Segmentation Control")
            root.resizable(False, False)
            root.grab_set()

            # Create a sheet with number of stages
            Cols = ['Stage', 'Points']
            self.stage_pts_sheet = tksheet.Sheet(
                                                root, 
                                                total_rows = len(rows), 
                                                total_columns = len(Cols), 
                                                headers = Cols,
                                                show_x_scrollbar = False, 
                                                show_y_scrollbar = True,
                                                font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"normal"),
                                                header_font = ("Segoe UI", max([self.min_font, int(12*self.scale)]),"bold"),
                                                )
            self.stage_pts_sheet.place(
                                    anchor = 'c', 
                                    relx = self.Placement['Characterization']['SheetRed'][0], 
                                    rely = self.Placement['Characterization']['SheetRed'][1],
                                    relwidth = self.Placement['Characterization']['SheetRed'][2], 
                                    relheight = self.Placement['Characterization']['SheetRed'][3], 
                                    )

            # Format the sheet
            self.stage_pts_sheet.change_theme("blue")
            self.stage_pts_sheet.set_index_width(0)

            # Set column widths
            window.update_idletasks()
            total_width = self.stage_pts_sheet.winfo_width()
            self.stage_pts_sheet.column_width(column = 0, width = int(total_width*self.Placement['Characterization']['SheetRed'][4]), redraw = True)
            self.stage_pts_sheet.column_width(column = 1, width = int(total_width*self.Placement['Characterization']['SheetRed'][5]), redraw = True)
            self.stage_pts_sheet.table_align(align = 'c',redraw=True)

            # Enable Bindings
            self.stage_pts_sheet.enable_bindings('single_select','cell_select', 'column_select',"arrowkeys")
            self.stage_pts_sheet.extra_bindings([("cell_select", self.cell_select_stage)]) 
            
            # Fill existing values values
            for i in range(len(rows)):
                self.stage_pts_sheet.set_cell_data(i,0,self.Compare['Data'][self.test_name]['Stage Type'][i])
                self.stage_pts_sheet.set_cell_data(i,1,self.Compare['Data'][self.test_name]['Stage Divisions'][i]) 
            
            # Update the sheet
            self.stage_pts_sheet.redraw()

            # Reduce Data Points
            def GetReducedPts():
                #------------------------------------------------------
                #
                #   PURPOSE: Get reduced data points from the button
                #            press
                #------------------------------------------------------

                # Get the number of divisions for each stage
                for i in range(len(self.stage_pts_sheet.data)):
                    divp = int(self.stage_pts_sheet.data[i][1])
                    if divp < 0:
                        divp = 0
                    self.Compare['Data'][self.test_name]['Stage Divisions'][i] = divp

                # Reduce the data
                self.reduce_data(self.test_name, self.load_dir)

                # Destory the window
                root.destroy()

                # Update the data points
                for i in range(len(self.Compare['Data'][self.test_name]['Stage Divisions'])):
                    self.stage_table_char.set_cell_data(i, 6, self.Compare['Data'][self.test_name]['Stage Divisions'][i])
                self.stage_table_char.redraw()

                # Recall the plotting function
                self.plotter_char()

                # Reset the vizualization flag
                self.viz_init = 0
                    
            # Create button to get the reduced data points
            self.btn_get_red = ttk.Button(
                                        root, 
                                        text = "Get Data Points", 
                                        command = GetReducedPts,
                                        style = 'Modern2.TButton', 
                                        )
            self.btn_get_red.place(
                                anchor = 'c', 
                                relx = self.Placement['Characterization']['ButtonGetRed'][0], 
                                rely = self.Placement['Characterization']['ButtonGetRed'][1],
                                relwidth = self.Placement['Characterization']['ButtonGetRed'][2], 
                                relheight = self.Placement['Characterization']['ButtonGetRed'][3]
                                )

        # Create button to reduce data
        if hasattr(self, 'btn_red'):
            self.btn_red.destroy()

        self.btn_red = ttk.Button(
                                self.nb_tab_tab2, 
                                text = "Reduce Data", 
                                command = ReduceData,
                                style = 'Modern2.TButton', 
                                )
        self.btn_red.place(
                            anchor = 'n', 
                            relx = self.Placement['Characterization']['ButtonRed'][0], 
                            rely = self.Placement['Characterization']['ButtonRed'][1], 
                            relwidth = self.Placement['Characterization']['ButtonRed'][2], 
                            relheight = self.Placement['Characterization']['ButtonRed'][3]
                            )
        
        if 'self.btn_red' not in self.atts['Characterization']['Local']:
            self.atts['Characterization']['Local'].append('self.btn_red')

    def plotter_all_char(self, val):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Plot all curves on the same plot.
        #
        #--------------------------------------------------------------------------

        # Get the value
        value = self.optmenu1_plt_char.get()

        #  Delete the canvas and drop down if it exists
        if hasattr(self, 'canvas_char'):
            self.toolbar_char.destroy()
            self.canvas_char.get_tk_widget().destroy()
            del self.canvas_char

        # Delete local attributes
        atts = ['self.btn_add_pt', 'self.btn_del_pt', 'self.btn_red']
        for widget in atts:
            try:
                eval(widget).destroy()
            except:
                pass

        # Reset any formatting on the test sheet
        for i in range(len(self.sheet_char.data)):
            self.sheet_char.highlight_rows(i,'white','black')

        # Create the plot
        self.fig_char = Figure(
                                figsize=(self.Placement['Characterization']['Figure1'][4],self.Placement['Characterization']['Figure1'][5]), 
                                dpi = self.Placement['Characterization']['Figure1'][6], 
                                constrained_layout = True)
        self.plot1 = self.fig_char.add_subplot(111)

        # Initialize the display curves
        disp_tests = []
        disp_load = []
        disp_type = []

        # Get display curves for the characterization tab
        for i in range(len(self.sheet_char.data)):
            if value in [self.sheet_char.data[i][1], 'All']:
                disp_tests.append(self.sheet_char.data[i][0])
                disp_load.append(int(self.sheet_char.data[i][3]))
                disp_type.append(self.sheet_char.data[i][1])

        # Loop through all tests selected
        for test in disp_tests:
            if disp_type[disp_tests.index(test)] == 'Tensile':
                end_idx = self.Compare['Data'][test]['Stage Index'][0]
            if disp_type[disp_tests.index(test)] == 'Creep':
                end_idx = self.Compare['Data'][test]['Stage Index'][1]
            if disp_type[disp_tests.index(test)] == 'Relaxation':
                end_idx = self.Compare['Data'][test]['Stage Index'][1]
            if disp_type[disp_tests.index(test)] == 'Generic':
                end_idx = self.Compare['Data'][test]['Stage Index'][-1]
            
            # Plot the data
            if value == 'Tensile' or value == 'Generic' or value == 'All':
                self.plot1.plot(self.Compare['Data'][test]['Strain'][disp_load[disp_tests.index(test)]][:end_idx],
                                self.Compare['Data'][test]['Stress'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Strain'
                ylab = 'Stress [MPa]'
            elif value == 'Creep':
                self.plot1.plot(self.Compare['Data'][test]['Time'][:end_idx],
                                self.Compare['Data'][test]['Strain'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Time [s]'
                ylab = 'Strain'
            elif value == 'Relaxation':
                self.plot1.plot(self.Compare['Data'][test]['Time'][:end_idx],
                                self.Compare['Data'][test]['Stress'][disp_load[disp_tests.index(test)]][:end_idx],
                                label=test)
                xlab = 'Time [s]'
                ylab = 'Stress [MPa]'

        if len(disp_tests) > 0:

            # Format the plot
            xlab_frmt = ScalarFormatter() 
            ylab_frmt = ScalarFormatter()
            self.plot1.set_xlabel(xlab)
            self.plot1.set_ylabel(ylab)
            self.plot1.xaxis.set_major_formatter(xlab_frmt)
            self.plot1.yaxis.set_major_formatter(ylab_frmt)
            if "Strain" in xlab or "Time" in xlab:
                self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
            if "Strain" in ylab or "Time" in ylab:
                self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
            self.plot1.legend()

            # Create the Tkinter canvas
            self.canvas_char = FigureCanvasTkAgg(self.fig_char, master = self.nb_tab_tab2)

            # Create the Matplotlib toolbar
            self.toolbar_char = NavigationToolbar2Tk(self.canvas_char, self.nb_tab_tab2)

            # Format Toolbar
            self.toolbar_char.config(bg='white')
            self.toolbar_char._message_label.config(background='white')
            self.toolbar_char.place(
                            anchor = 'n', 
                            relx = self.Placement['Characterization']['Toolbar1'][0], 
                            rely = self.Placement['Characterization']['Toolbar1'][1],
                            relwidth = self.Placement['Characterization']['Toolbar1'][2], 
                            relheight = self.Placement['Characterization']['Toolbar1'][3]
                            )

            # Add the figure to the GUI
            self.canvas_char.get_tk_widget().place(
                                            anchor = 'n', 
                                            relx = self.Placement['Characterization']['Figure1'][0], 
                                            rely = self.Placement['Characterization']['Figure1'][1],
                                            relwidth = self.Placement['Characterization']['Figure1'][2], 
                                            relheight = self.Placement['Characterization']['Figure1'][3]
                                            )
            
            # Update window
            self.nb_tab_tab2.update_idletasks()
            self.canvas_char.draw()
            self.toolbar_char.update()

            if 'self.canvas_char' not in self.atts['Characterization']['Local']:
                self.atts['Characterization']['Local'].append("self.canvas_char")
                self.atts['Characterization']['Local'].append("self.toolbar_char")
    
    def reduce_data(self, test, load_dir):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create the reduced data arrays
        #
        #--------------------------------------------------------------------------

        # Reset the Reduced Arrays
        self.Compare['Data'][test]['Reduced Data']['Time'] = []
        dir_keys = list(self.Compare['Data'][test]['Strain'].keys())
        for key in dir_keys:
            self.Compare['Data'][test]['Reduced Data']['Strain'][key] = []
        dir_keys = list(self.Compare['Data'][test]['Stress'].keys())
        for key in dir_keys:
            self.Compare['Data'][test]['Reduced Data']['Stress'][key] = []

        # Loop through the stages to fit points
        for i in range(len(self.Compare['Data'][test]['Stage Type'])):
            # Get Index information
            if i == 0:
                sindex = 0
            else:
                sindex = self.Compare['Data'][test]['Stage Index'][i-1]
            eindex = self.Compare['Data'][test]['Stage Index'][i]

            # Prealloacte data
            data = []

            # Get the reduced Time
            data.append(self.Compare['Data'][test]['Time'][sindex:eindex])
            dir_keys = list(self.Compare['Data'][test]['Strain'].keys())
            for key in dir_keys:
                data.append(self.Compare['Data'][test]['Strain'][key][sindex:eindex])
            dir_keys = list(self.Compare['Data'][test]['Stress'].keys())
            for key in dir_keys:
                data.append(self.Compare['Data'][test]['Stress'][key][sindex:eindex])

            # Get the X and Y Data for the Stage (Response Curves)
            # - Tensile -> Stress vs Strain
            if self.Compare['Data'][test]['Stage Type'][i] == 'Tensile':
                x = self.Compare['Data'][test]['Strain'][load_dir][sindex:eindex]
                y = self.Compare['Data'][test]['Stress'][load_dir][sindex:eindex]
                time_flag = 0

            # - Creep -> Strain vs Time
            if self.Compare['Data'][test]['Stage Type'][i] == 'Creep':
                x = self.Compare['Data'][test]['Time'][sindex:eindex]
                y = self.Compare['Data'][test]['Strain'][load_dir][sindex:eindex]
                time_flag = 1

            # - Relaxation -> Stress vs Time
            if self.Compare['Data'][test]['Stage Type'][i] == 'Relaxation':
                x = self.Compare['Data'][test]['Time'][sindex:eindex]
                y = self.Compare['Data'][test]['Strain'][load_dir][sindex:eindex]
                time_flag = 1

            # Reduce and Smooth Data with Cubic Spline
            xall = x
            yall = y
            x = [xall[0]]
            y = [yall[0]]
            ct = 1
            while ct < len(xall) -1:
                if self.Compare['Data'][test]['Load Rate'][i][0] >= 0 or time_flag == 1:
                    if xall[ct] > x[-1]:
                        x.append(xall[ct])
                        y.append(yall[ct])
                    rev_flag = 0
                else: 
                    if xall[ct] < x[-1]:
                        x.append(xall[ct])
                        y.append(yall[ct])
                    rev_flag = 1
                ct = ct + 1
            x = np.array(x)
            y = np.array(y)

            # Reverse unloading for increasing X
            if rev_flag == 1:
                x = x[::-1]
                y = y[::-1]

            # Fit cubic spline
            x_cs = np.linspace(x.min(), x.max(), 10000)
            y_cs = CubicSpline(x, y, bc_type='not-a-knot')
            y_cs = y_cs(x_cs)

            # Flip unloading x and y back
            if rev_flag == 1:
                x = x[::-1]
                y = y[::-1]

            # Normalize
            x_cs_n = (x_cs - min(x_cs))/(max(x_cs)-min(x_cs))
            y_cs_n = (y_cs - min(y_cs))/(max(y_cs)-min(y_cs))

            # Initialize total curve length and set number of points
            LT = 0
            divp = self.Compare['Data'][test]['Stage Divisions'][i]

            # Get the reduced data points
            if divp > 0:
                # Get the total curve length
                for j in range(1,len(x_cs_n)):
                    LT = LT + ((x_cs_n[j]-x_cs_n[j-1])**2+(y_cs_n[j]-y_cs_n[j-1])**2)**(0.5)

                # Get the curve length of each segment
                Lbar = LT/divp

                # Initialize X and Y
                x_pts = [x_cs_n[0]]
                y_pts = [y_cs_n[0]]

                # Iterate next point until the curve length is met
                idx = 0
                k = idx+1
                for j in range(divp):
                    flag = 0
                    Li = 0
                    while flag == 0:
                        Li = Li + ((x_cs_n[k]-x_cs_n[k-1])**(2)+(y_cs_n[k]-y_cs_n[k-1])**(2))**(0.5)

                        if Li > Lbar:
                            idx = k
                            vec = [x_cs_n[k]-x_cs_n[k-1],y_cs_n[k]-y_cs_n[k-1]]
                            vec = vec/((vec[0])**2+(vec[1])**2)**(0.5)
                            vec = vec*(Lbar-LiPrev)
                            x_pts.append(x_cs_n[k-1]+vec[0])
                            y_pts.append(y_cs_n[k-1]+vec[1])
                            flag = 1

                        if k == len(y_cs_n)-1:
                            x_pts.append(x_cs_n[k-1]+vec[0])
                            y_pts.append(y_cs_n[k-1]+vec[1])
                            flag = 1

                        k = k+1
                        LiPrev = Li

                # Unnormalize
                x_pts = np.array(x_pts)*(max(x_cs)-min(x_cs)) + min(x_cs)
                y_pts = np.array(y_pts)*(max(y_cs)-min(y_cs)) + min(y_cs)

                # Inerpolate data points
                data_interp = []
                for i in range(len(data)):
                    new_vec = np.interp(x_pts, xall, data[i])
                    data_interp.append(new_vec)

                # Store Interpolated Points
                # -- Time
                for j in range(len(data_interp[0])):
                    self.Compare['Data'][test]['Reduced Data']['Time'].append(data_interp[0][j])
                ct = 1
                # -- Strain
                dir_keys = list(self.Compare['Data'][test]['Strain'].keys())
                for key in dir_keys:
                    for j in range(len(data_interp[ct])):
                        self.Compare['Data'][test]['Reduced Data']['Strain'][key].append(data_interp[ct][j])
                    ct= ct+1
                # -- Stress
                dir_keys = list(self.Compare['Data'][test]['Stress'].keys())
                for key in dir_keys:
                    for j in range(len(data_interp[ct])):
                        self.Compare['Data'][test]['Reduced Data']['Stress'][key].append(data_interp[ct][j])
                    ct= ct+1

    def add_point(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Add a data reduction point
        #
        #--------------------------------------------------------------------------

        # Check Clicked
        if self.clicked == 1:

            # Update Clicked for adding a point
            self.clicked = 2

            # Get the selected point
            self.x = event.xdata
            self.y = event.ydata

            # Plot the closest point
            mind = 10e3
            mindidx = -1

            # Normalize data
            x_min = min(self.xdata)
            x_max = max(self.xdata)
            x_range = x_max - x_min if x_max != x_min else 1  # avoid division by zero

            y_min = min(self.ydata)
            y_max = max(self.ydata)
            y_range = y_max - y_min if y_max != y_min else 1  # avoid division by zero

            # normalize x and y 
            xdata_n = [(x - x_min) / x_range for x in self.xdata]
            ydata_n = [(y - y_min) / y_range for y in self.ydata]  # you used x_min/x_max for y too

            xpt_n = (self.x - x_min) / x_range
            ypt_n = (self.y - y_min) / y_range

            mindidx = None
            mind = float("inf")

            for i, (xn, yn) in enumerate(zip(xdata_n, ydata_n)):
                d = ((xpt_n - xn)**2 + (ypt_n - yn)**2)**0.5
                if d < mind:
                    mind = d
                    mindidx = i

            # Store the data
            self.idx = mindidx
            self.xc = self.xdata[mindidx]
            self.yc= self.ydata[mindidx]

            # Update the canvas
            self.plot1.plot(self.xc, self.yc,'go')
            self.canvas_char.draw()

            # Bind the Right and Left Arrow Keys
            self.canvas_char.get_tk_widget().bind("<Right>", self.move_right)
            self.canvas_char.get_tk_widget().bind("<Left>", self.move_left)

            # Bind 'Return'
            self.canvas_char.get_tk_widget().bind("<Return>", self.update_pts)

            # Set Bindings
            self.canvas_char.get_tk_widget().focus_set()
        
    def del_point(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Delete a data reduction point
        #
        #--------------------------------------------------------------------------

        # Check Clicked
        if self.clicked == 1:

            # Update the clicked for deleting a point
            self.clicked = 3

            # Get the selected point
            self.x = event.xdata
            self.y= event.ydata

            # Normalize data
            mind = 10e3
            mindidx = -1
            xdata_n = [(x - min(self.xsdata)) / (max(self.xsdata) - min(self.xsdata)) for x in self.xsdata]
            ydata_n = [(x - min(self.xsdata)) / (max(self.xsdata) - min(self.xsdata)) for x in self.ysdata]
            xpt_n = (self.x - min(self.xsdata)) / (max(self.xsdata) - min(self.xsdata)) 
            ypt_n = (self.y - min(self.xsdata)) / (max(self.xsdata) - min(self.xsdata)) 
            for i in range(len(xdata_n)):
                d = ((xpt_n-xdata_n[i])**2+(ypt_n-ydata_n[i])**2)**(1/2)
                if d < mind:
                    mind = d
                    mindidx = i

            # Store the data
            self.idx = mindidx
            self.xc = self.xsdata[mindidx]
            self.yc= self.ysdata[mindidx]

            # Update the canvas
            self.plot1.plot(self.xc, self.yc,'go')
            self.canvas_char.draw()

            # Bind the Right and Left Arrow Keys
            self.canvas_char.get_tk_widget().bind("<Right>", self.move_right)
            self.canvas_char.get_tk_widget().bind("<Left>", self.move_left)

            # Bind 'Return'
            self.canvas_char.get_tk_widget().bind("<Return>", self.update_pts)

            # Set Bidnings
            self.canvas_char.get_tk_widget().focus_set()

    def move_left(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Move Data Reduction Point Left
        #
        #--------------------------------------------------------------------------

        # Remove the Previous Point
        self.plot1.lines[len(self.plot1.lines)-1].remove()
        self.canvas_char.draw()

        # Update the index
        # -- For adding a point
        if self.clicked == 2:
            self.idx  = self.idx - 1
            if self.idx < 0:
                self.idx = 0
            self.xc = self.xdata[self.idx]
            self.yc= self.ydata[self.idx]

        # -- For deleting a point
        if self.clicked == 3:
            self.idx  = self.idx - 1
            if self.idx < 0:
                self.idx = 0
            self.xc = self.xsdata[self.idx]
            self.yc= self.ysdata[self.idx]

        # Replot the data
        self.plot1.plot(self.xc, self.yc,'go')
        self.canvas_char.draw()

    def move_right(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Move Data Reduction Point Right
        #
        #--------------------------------------------------------------------------
        
        # Remove the Previous Point
        self.plot1.lines[len(self.plot1.lines)-1].remove()
        self.canvas_char.draw()

        # Update the index
        self.idx  = self.idx + 1
            
        # -- For Adding a point
        if self.clicked == 2:
            if self.idx > len(self.xdata)-1:
                self.idx = len(self.xdata)-1
            self.xc = self.xdata[self.idx]
            self.yc= self.ydata[self.idx]

        # -- For deleting a point
        if self.clicked == 3:
            if self.idx > len(self.xsdata)-1:
                self.idx = len(self.xsdata)-1
            self.xc = self.xsdata[self.idx]
            self.yc= self.ysdata[self.idx]

        # Replot the data
        self.plot1.plot(self.xc, self.yc,'go')
        self.canvas_char.draw()

    def update_pts(self, event):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Update the current data reduction point
        #
        #--------------------------------------------------------------------------

        # Adding a point
        if self.clicked == 2:

            # Get the current index
            idx = self.idx

            # Update Time
            new_time = []
            time = self.Compare['Data'][self.test_name]['Time'][idx]
            idx_insert = None
            i = 0
            while time > self.Compare['Data'][self.test_name]['Reduced Data']['Time'][i]:
                new_time.append(self.Compare['Data'][self.test_name]['Reduced Data']['Time'][i])
                i = i+1

                if i == len(self.Compare['Data'][self.test_name]['Reduced Data']['Time']):
                    break
            idx_insert = i
            new_time.append(time)
            i = i+1
            for i in range(len(self.Compare['Data'][self.test_name]['Reduced Data']['Time'])):
                if time < self.Compare['Data'][self.test_name]['Reduced Data']['Time'][i]:
                    new_time.append(self.Compare['Data'][self.test_name]['Reduced Data']['Time'][i])
            self.Compare['Data'][self.test_name]['Reduced Data']['Time'] = new_time

            # Update Strain
            keys = list(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'].keys())
            for key in keys:
                strain = self.Compare['Data'][self.test_name]['Strain'][key][idx]
                new_strain = []
                for i in range(idx_insert):
                    new_strain.append(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key][i])
                new_strain.append(strain)
                for i in range(idx_insert,len(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key])):
                    new_strain.append(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key][i])
                self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key] = new_strain

            # Update Stress
            keys = list(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'].keys())
            for key in keys:
                stress = self.Compare['Data'][self.test_name]['Stress'][key][idx]
                new_stress = []
                for i in range(idx_insert):
                    new_stress.append(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key][i])
                new_stress.append(stress)
                for i in range(idx_insert,len(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key])):
                    new_stress.append(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key][i])
                self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key] = new_stress

            # Find the stage that was changed
            stage_idx = [0] + self.Compare['Data'][self.test_name]['Stage Index']
            for i in range(len(self.Compare['Data'][self.test_name]['Stage Index'])):
                if  idx > stage_idx[i] and idx < stage_idx[i+1]:
                    self.Compare['Data'][self.test_name]['Stage Divisions'][i] = self.Compare['Data'][self.test_name]['Stage Divisions'][i]+1

            # Update the stage table
            for i in range(len(self.Compare['Data'][self.test_name]['Stage Divisions'])):
                self.stage_table_char.set_cell_data(i, 6, self.Compare['Data'][self.test_name]['Stage Divisions'][i])
            self.stage_table_char.redraw()

        # Deleting a point
        if self.clicked == 3:
            # Confirm delete
            askyn = messagebox.askyesno(title = 'Delete point', message = 'Do you want to delete this point?')
            if askyn == True:
                # Delete the Time Point
                self.Compare['Data'][self.test_name]['Reduced Data']['Time'] = np.delete(self.Compare['Data'][self.test_name]['Reduced Data']['Time'],[self.idx])
                
                # Delete the Strain Point
                keys = list(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'].keys())
                for key in keys:
                    self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key] = np.delete(self.Compare['Data'][self.test_name]['Reduced Data']['Strain'][key],[self.idx])
                
                # Delete the Stress Point
                keys = list(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'].keys())
                for key in keys:
                    self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key] = np.delete(self.Compare['Data'][self.test_name]['Reduced Data']['Stress'][key],[self.idx])
        
                # Find the stage that was changed
                stage_idx = [0] + self.Compare['Data'][self.test_name]['Stage Index']
                for i in range(len(self.Compare['Data'][self.test_name]['Stage Index'])):
                    if  self.Compare['Data'][self.test_name]['Time'][self.idx] > self.Compare['Data'][self.test_name]['Time'][stage_idx[i]] and self.Compare['Data'][self.test_name]['Time'][self.idx] < self.Compare['Data'][self.test_name]['Time'][stage_idx[i+1]]:
                        self.Compare['Data'][self.test_name]['Stage Divisions'][i] = self.Compare['Data'][self.test_name]['Stage Divisions'][i]-1

                # Update the stage table
                for i in range(len(self.Compare['Data'][self.test_name]['Stage Divisions'])):
                    self.stage_table_char.set_cell_data(i, 6, self.Compare['Data'][self.test_name]['Stage Divisions'][i])
                self.stage_table_char.redraw()

        # Reset the clicked variable
        self.clicked = 0

        # Replot data
        self.plotter_char()

    #------------------------------------------------------------------------------
    #
    #   OPTIMIZATION/ANALYSIS FUNCTIONS
    #   Functions for the Optimization and Analysis Tabs
    #
    #------------------------------------------------------------------------------

    def cell_select_opt(self, response, tag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create Custom Column Disablement for Model-Optimization 
        #            Parameters.
        #
        #--------------------------------------------------------------------------

        # Define the table
        table_name = "self." + tag

        # Define locked columns (parameter name and COMPARE value)
        locked_cols = [0,6]

        # -- Check for inactive cells
        locked_cells = []
        for i in range(len(eval(table_name).data)):
            if eval(table_name).data[i][5] == 'Passive':
                locked_cells.append([i, 2])
                locked_cells.append([i, 4])

        # Enable/Disable user ability to edit cells
        if response.selected.column != None:
            if response.selected.column in locked_cols:
                eval(table_name).disable_bindings(("edit_cell"))
                eval(table_name).disable_bindings(("end_edit_cell"))
            elif [response.selected.row, response.selected.column] in locked_cells:
                eval(table_name).disable_bindings(("edit_cell"))
                eval(table_name).disable_bindings(("end_edit_cell"))
            else:
                self.sheet_data = eval(table_name).data
                self.sheet_tag = tag
                eval(table_name).enable_bindings(("edit_cell"))
                eval(table_name).enable_bindings(("end_edit_cell"))
                eval(table_name).extra_bindings([("edit_cell", self.save_model),
                                                 ("end_edit_cell", lambda  event: self.format_cell(event, table_name))])

                # Loop through rows
                for i in range(len(eval(table_name).data)):

                    # -- Check lower bound
                    if [i,2] not in locked_cells:
                        eval(table_name).highlight((i,2),fg = 'black', bg = 'white')
                        try:
                            if float(eval(table_name).data[i][2]) > float(eval(table_name).data[i][3]):
                                eval(table_name).highlight((i,2),fg = 'red', bg = 'white')
                        except:
                            pass

                    # -- Check upper bound
                    if [i,4] not in locked_cells:
                        eval(table_name).highlight((i,4),fg = 'black', bg = 'white')
                        try:
                            if float(eval(table_name).data[i][4]) < float(eval(table_name).data[i][3]):
                                eval(table_name).highlight((i,4),fg = 'red', bg = 'white')
                        except:
                            pass

            # Redraw the table
            eval(table_name).redraw()

    def save_model(self, response):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Save an optimized model before editing parameters.
        #
        #--------------------------------------------------------------------------

        # Determine if optimized parameters were found
        if self.optimize == 1:

            # Ask user if they want to save
            askyn = messagebox.askyesno(title = 'Save Model', message = 'Editing the model tables will remove any optimized parameters. Do you want to save the model?')
            if askyn == True:
                # Reset the model status
                self.Compare['Model']['Status'] = 0

                # Get the model name
                save_flag = 0
                while save_flag == 0:
                    user_input = simpledialog.askstring("Save Model", "Enter the model name:")

                    if user_input in list(self.Compare['Model Library'].keys()):
                        askyn = messagebox.askyesno(title = 'Save Model', message = 'Do you want to overwrite ' + user_input + ' ?')
                        if askyn == True:
                            save_flag = 1
                    else:
                        save_flag = 1

                # Get the model type
                if len(self.Compare['Model']['VE_Params'][0]) > 3:
                    self.Compare['Model']['Compare Type'] = 'Optimize'
                else:
                    self.Compare['Model']['Compare Type'] = 'Analysis'
                
                # Write model data to binary in the mode library
                json_string = json.dumps(self.Compare['Model'])
                binary_data = json_string.encode('utf-8')
                self.Compare['Model Library'][user_input] = binary_data

            # Reset flags
            self.optimize = 0
            self.viz_init = 0

            # Destroy the global error label
            try:
                self.globalerr_opt.destroy()
            except:
                pass

        # Reset Parameter Values in the selected row
        # -- Viscoelastic Parameters
        if hasattr(self,'sheet1_opt'):
            try:
                # Get Current Row
                currently_selected = self.sheet1_opt.get_currently_selected()
                
                # Reset Optimized Value
                self.sheet1_opt.set_cell_data(currently_selected.row,self.sheet1_opt.visible_columns[1]-1,'')

                # Perform Data Validation/Formatting
                try:
                    self.sheet1_opt.set_cell_data(currently_selected.row, currently_selected.column, '{:0.4e}'.format(float(self.sheet1_opt.data[currently_selected.row][currently_selected.column])))
                except:
                    if currently_selected.column not in [0, 1, 5, 6]:
                        self.sheet1_opt.set_cell_data(currently_selected.row, currently_selected.column, '')
            except:
                pass

        # -- Viscoplastic Parameters
        if hasattr(self,'sheet2_opt'):
            try:
                # Get Current Row
                currently_selected = self.sheet2_opt.get_currently_selected()
                
                # Reset Optimized Value
                self.sheet2_opt.set_cell_data(currently_selected.row,self.sheet2_opt.visible_columns[1]-1,'')

                # Perform Data Validation/Formatting
                try:
                    self.sheet2_opt.set_cell_data(currently_selected.row, currently_selected.column, '{:0.4e}'.format(float(self.sheet2_opt.data[currently_selected.row][currently_selected.column])))
                except:
                    if currently_selected.column not in [0, 1, 5, 6]:
                        self.sheet2_opt.set_cell_data(currently_selected.row, currently_selected.column, '')
            except:
                pass
    
    def format_cell(self, response, table_name):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Disable passive parameters
        #
        #--------------------------------------------------------------------------

        # Loop through rows
        for i in range(len(eval(table_name).data)):
            if eval(table_name).data[i][5] == 'Active':
                eval(table_name).highlight_cells(i, 2, bg='white', fg = 'black', redraw=False)
                eval(table_name).highlight_cells(i, 4, bg='white', fg = 'black', redraw=False)
                eval(table_name).highlight_cells(i, 5, bg='white', fg = 'black', redraw=False)

                # Check val
                for j in range(2,5):
                    try:
                        eval(table_name).set_cell_data(i, j, '{:0.4e}'.format(float(eval(table_name).data[i][j])))
                    except:
                        eval(table_name).set_cell_data(i, j, '')
            else:
                eval(table_name).highlight_cells(i, 2, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                eval(table_name).highlight_cells(i, 4, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)
                eval(table_name).highlight_cells(i, 5, bg='#e0e0e0', fg = '#a0a0a0', redraw=False)

                # Check val
                for j in range(2,5):
                    try:
                        eval(table_name).set_cell_data(i, j, '{:0.4e}'.format(float(eval(table_name).data[i][j])))
                    except:
                        eval(table_name).set_cell_data(i, j, '')

        # Redraw table
        eval(table_name).redraw()
   
    def cell_select_anly(self, response, tag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Create Custom Column Disablement for Model-Analysis 
        #            Parameters.
        #
        #--------------------------------------------------------------------------

        # Try Deselecting from other table
        if tag == 'sheet1_analy':
            try:
                self.sheet2_analy.deselect("all", redraw=True)
            except:
                pass
        if tag == 'sheet2_analy':
            try:
                self.sheet1_analy.deselect("all", redraw=True)
            except:
                pass
        
        # Define the table
        table_name = "self." + tag

        # Define locked columns (parameter name)
        locked_cols = [0]

        # Enable/Disable user ability to edit cells
        def format_analy(event, self, table_name):
            #----------------------------------------------------------------------
            #
            #   PURPOSE: Format the analysis table
            #
            #----------------------------------------------------------------------

            try:
                eval(table_name).set_cell_data(event.row, event.column, '{:0.4e}'.format(float(eval(table_name).data[event.row][event.column])))
            except:
                pass

        # Set Bindings
        if response.selected.column != None:
            if response.selected.column in locked_cols:
                eval(table_name).disable_bindings(("edit_cell"))
            else:
                eval(table_name).enable_bindings(("edit_cell"))
                eval(table_name).extra_bindings([("edit_cell", lambda event: format_analy(event, self, table_name))])

            # Redrfaw table
            eval(table_name).redraw()

    def load_from_db(self, tag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Load a model from the excel template
        #
        #--------------------------------------------------------------------------

        # Get the Excel File
        file = filedialog.askopenfile(title = "Model Import", filetypes= [('Excel', '*.xlsx')], mode ='r',)

        # Get Data
        model, flag, msg = ReadModel(file.name, self)

        # Set NaN units as empty
        if 'VE_Param' in model.keys():
            for i in range(len(model['VE_Param'])):
                if pd.isna(model['VE_Param'][i][1]) == True:
                    model['VE_Param'][i][1] = ""
        if 'VP_Param' in model.keys():
            for i in range(len(model['VP_Param'])):
                if pd.isna(model['VP_Param'][i][1]) == True:
                    model['VP_Param'][i][1] = ""

        # Update the model and corresponding page
        if flag == 0:
            if tag == "Optimize":
                # Save the Model
                self.Compare['Model'] = copy.deepcopy(model)

                # Reformat the Parameters with empty bounds
                self.Compare['Model']['VE_Param'] = []
                for i in range(len(model['VE_Param'])):
                    self.Compare['Model']['VE_Param'].append([model['VE_Param'][i][0],
                                                            model['VE_Param'][i][1],
                                                            '',
                                                            model['VE_Param'][i][2],
                                                            '',
                                                            'Active',
                                                            ''
                                                            ])                                        
                    self.Compare['Model']['VP_Param'] = []
                    for i in range(len(model['VP_Param'])):
                        self.Compare['Model']['VP_Param'].append([model['VP_Param'][i][0],
                                                                model['VP_Param'][i][1],
                                                                '',
                                                                model['VP_Param'][i][2],
                                                                '',
                                                                'Active',
                                                                ''
                                                                ])

                # Set the Sheet Data
                formatc_data = self.Compare['Model']['VE_Param']
                self.sheet2_opt_data = self.Compare['Model']['VP_Param']
                self.res_flag1 = 1
                self.res_flag2 = 1
                
                # Recreate the Optimize Page
                CreateModelTab(self,window)

            else:
                # Save the Model
                self.Compare['Analysis'] = copy.deepcopy(model)

                # Set the Sheet Data
                self.sheet1_analy_data = self.Compare['Analysis']['VE_Param']
                self.sheet2_analy_data = self.Compare['Analysis']['VP_Param']
                self.res_flag1 = 1
                self.res_flag2 = 1

                # Recreate teh Analysis Page
                CreateAnalysisTab(self,window)
        else:
            messagebox.showerror(message=msg)

    def Model_Library(self, tag):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: View/Edit Model Libary.
        #
        #--------------------------------------------------------------------------

        # Get Existing Models
        self.models = list(self.Compare['Model Library'].keys())

        if len(self.models) > 0:

            # Create a window to view the model libary
            root = tk.Toplevel(window)
            root.geometry(f"{int(900*self.scale)}x{int(700*self.scale)}")
            root.title("Model Libary")
            root.configure(bg = 'white')
            root.resizable(False, False)
            root.grab_set()

            def create_sheet():
                #--------------------------------------------------------------
                #
                #   PURPOSE: Create the Material Library Sheet.
                #
                #--------------------------------------------------------------

                # Set column names
                Cols = ['Name', 'Type', 'Reversible Model','Irreversible Model','Method']

                # Create the table
                self.sheet_lib = tksheet.Sheet(
                                            root, 
                                            total_rows = len(self.models), 
                                            total_columns = len(Cols), 
                                            headers = Cols,
                                            show_x_scrollbar = False, 
                                            show_y_scrollbar = True,
                                            font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"normal"),
                                            header_font = ("Segoe UI",max([self.min_font, int(12*self.scale)]),"bold")
                                            )
                self.sheet_lib.place(
                                    anchor = 'n', 
                                    relx = self.Placement['Optimization']['ModLibSheet'][0], 
                                    rely = self.Placement['Optimization']['ModLibSheet'][1],
                                    relwidth = self.Placement['Optimization']['ModLibSheet'][2],
                                    relheight = self.Placement['Optimization']['ModLibSheet'][3],
                                    )
                self.sheet_lib.change_theme("blue")
                self.sheet_lib.set_index_width(0)
        
                def rename_model(self):
                    #----------------------------------------------------------
                    #
                    #   PURPOSE: Rename a model.
                    #
                    #----------------------------------------------------------

                    # Get the previous name
                    currently_selected = self.sheet_lib.get_currently_selected()
                    prev_name = self.sheet_lib.data[currently_selected.row][0]

                    # Get the model name
                    save_flag = 0
                    while save_flag == 0:
                        user_input = simpledialog.askstring("Save Model", "Enter the model name:")

                        if user_input in list(self.Compare['Model Library'].keys()):
                            askyn = messagebox.askyesno(title = 'Save Model', message = 'Do you want to overwrite ' + user_input + ' ?')
                            if askyn == True:
                                save_flag = 1
                        else:
                            save_flag = 1

                    if user_input != '' and user_input is not None:

                        if user_input != prev_name:

                            # Save the new data
                            self.Compare['Model Library'][user_input] = self.Compare['Model Library'][prev_name] 

                            # Delete the old data
                            del self.Compare['Model Library'][prev_name] 

                            # Reset the model list
                            self.models = list(self.Compare['Model Library'].keys())

                            # Recreate the sheet
                            self.sheet_lib.destroy()
                            del self.sheet_lib
                            create_sheet()
                
                def delete_model(self):
                    #----------------------------------------------------------
                    #
                    #   PURPOSE: Delete a model from the library.
                    #
                    #----------------------------------------------------------

                    # Confirm delete
                    askyn = messagebox.askyesno(title = 'Delete Model', message = 'Do you want to delete this model?')
                    if askyn == True:
                        # Get the previous name
                        currently_selected = self.sheet_lib.get_currently_selected()
                        prev_name = self.sheet_lib.data[currently_selected.row][0]

                        # Delete the data
                        del self.Compare['Model Library'][prev_name] 

                        # Reset the model list
                        self.models = list(self.Compare['Model Library'].keys())

                        # Recreate the sheet
                        self.sheet_lib.destroy()
                        del self.sheet_lib
                        create_sheet()

                def load_model(self):
                    #----------------------------------------------------------
                    #
                    #   PURPOSE: Load a model from the library into the page.
                    #
                    #----------------------------------------------------------

                    # Get the previous name
                    currently_selected = self.sheet_lib.get_currently_selected()
                    name = self.sheet_lib.data[currently_selected.row][0]

                    # Set the model name
                    self.Compare['Model ID'] = name

                    # Close the window
                    root.destroy()

                    # Get the data
                    json_string = self.Compare['Model Library'][name].decode('utf-8')
                    data = json.loads(json_string)

                    # Populate the Optimization Page
                    if tag == 'Optimize':
                        if data['Compare Type'] == 'Optimize':
                            self.Compare['Model'] = data   
                        else:
                            self.Compare['Model'] = dict(data) 
                            # Reformat Parameters
                            if 'VE_Param' in list(data.keys()):
                                self.Compare['Model']['VE_Param'] = []
                                for i in range(len(data['VE_Param'])):
                                    self.Compare['Model']['VE_Param'].append([data['VE_Param'][i][0],
                                                                            data['VE_Param'][i][1],
                                                                            '',
                                                                            data['VE_Param'][i][2],
                                                                            '',
                                                                            'Active',
                                                                            ''
                                                                            ])                                      
                            if 'VP_Param' in list(data.keys()):
                                self.Compare['Model']['VP_Param'] = []
                                for i in range(len(data['VP_Param'])):
                                    self.Compare['Model']['VP_Param'].append([data['VP_Param'][i][0],
                                                                            data['VP_Param'][i][1],
                                                                            '',
                                                                            data['VP_Param'][i][2],
                                                                            '',
                                                                            'Active',
                                                                            ''
                                                                            ])
                        
                        # Recreate the Optimize Page
                        self.opt_init = 1
                        self.viz_init = 0
                        CreateModelTab(self,window)

                    # Populate the Analysis Page
                    else:
                        if data['Compare Type'] == 'Analysis':
                            self.Compare['Analysis'] = data   
                        else:
                            self.Compare['Analysis'] = dict(data) 
                            # Reformat Parameters
                            if 'VE_Param' in list(data.keys()):
                                self.Compare['Analysis']['VE_Param'] = []
                                for i in range(len(data['VE_Param'])):
                                    self.Compare['Analysis']['VE_Param'].append([data['VE_Param'][i][0],
                                                                            data['VE_Param'][i][1],
                                                                            data['VE_Param'][i][6],
                                                                            ])                                       
                            if 'VP_Param' in list(data.keys()):
                                self.Compare['Analysis']['VP_Param'] = []
                                for i in range(len(data['VP_Param'])):
                                    self.Compare['Analysis']['VP_Param'].append([data['VP_Param'][i][0],
                                                                            data['VP_Param'][i][1],
                                                                            data['VP_Param'][i][6],
                                                                            ])

                        # Recreate Analysis Page
                        self.analy_init = 1
                        self.viz_init = 0
                        CreateAnalysisTab(self,window)

                def view_notes(self):
                    #----------------------------------------------------------
                    #
                    #   PURPOSE: View any model notes.
                    #
                    #----------------------------------------------------------

                    # Set the structure name
                    currently_selected = self.sheet_lib.get_currently_selected()
                    name = self.sheet_lib.data[currently_selected.row][0]
                    json_string = self.Compare['Model Library'][name].decode('utf-8')
                    data = json.loads(json_string)

                    # Get the note if it exists
                    if 'Note' in data.keys():
                        
                        # Get the note
                        note = data['Note']

                    else:
                        note = ''

                    # Create the window to display the note
                    root_v = tk.Toplevel(root)
                    root_v.geometry(f"{int(800*self.scale)}x{int(600*self.scale)}")
                    root_v.title("Model Notes") 
                    root_v.configure(bg='white')

                    # Prevent win_root interaction
                    root_v.grab_set()
                    
                    # When root_v closes, control returns to win_root
                    def on_close():
                        root_v.destroy()
                        root.grab_set()  # reapply grab to parent
                    root_v.protocol("WM_DELETE_WINDOW", on_close)
                    
                    # Create the label
                    ttk.Label(
                            root_v, 
                            text=f"Model Notes: {name}", 
                            font=('Segoe UI', max([self.min_font, int(12*self.scale)])),
                            style= "Modern1.TLabel",
                            ).place(
                                    anchor='n', 
                                    relx = self.Placement['Optimization']['ModLibNotesLabel'][0], 
                                    rely = self.Placement['Optimization']['ModLibNotesLabel'][1]
                                    ) 
                    
                    # Create the note
                    text_area = scrolledtext.ScrolledText(
                                                        root_v, 
                                                        wrap=tk.WORD, 
                                                        width=int(40*self.scale), 
                                                        height=int(8*self.scale), 
                                                        font=("Segoe UI", max([self.min_font, int(12*self.scale)]))
                                                        ) 
                    
                    text_area.place(
                                    anchor='n', 
                                    relx = self.Placement['Optimization']['ModLibNotesArea'][0], 
                                    rely = self.Placement['Optimization']['ModLibNotesArea'][1],
                                    relwidth = self.Placement['Optimization']['ModLibNotesArea'][2],
                                    relheight = self.Placement['Optimization']['ModLibNotesArea'][3]
                                    )
                    text_area.insert(tk.END, note) 
                    text_area.config(state="disabled")

                # Enable Bindings
                self.sheet_lib.enable_bindings('single_select','cell_select', 'column_select', "arrowkeys", "right_click_popup_menu")
                self.sheet_lib.popup_menu_add_command('Rename Model', lambda : rename_model(self), table_menu = True, index_menu = True, header_menu = True)
                self.sheet_lib.popup_menu_add_command('Delete Model', lambda : delete_model(self), table_menu = True, index_menu = True, header_menu = True)
                self.sheet_lib.popup_menu_add_command('Load Model', lambda : load_model(self), table_menu = True, index_menu = True, header_menu = True)
                self.sheet_lib.popup_menu_add_command('View Notes', lambda : view_notes(self), table_menu = True, index_menu = True, header_menu = True)

                # Set Column Widths
                root.update_idletasks()
                total_width = self.sheet_lib.winfo_width()
                self.sheet_lib.column_width(column = 0, width = int(total_width*self.Placement['Optimization']['ModLibSheet'][4]), redraw = True)
                self.sheet_lib.column_width(column = 1, width = int(total_width*self.Placement['Optimization']['ModLibSheet'][5]), redraw = True)
                self.sheet_lib.column_width(column = 2, width = int(total_width*self.Placement['Optimization']['ModLibSheet'][6]), redraw = True)
                self.sheet_lib.column_width(column = 3, width = int(total_width*self.Placement['Optimization']['ModLibSheet'][7]), redraw = True)
                self.sheet_lib.column_width(column = 4, width = int(total_width*self.Placement['Optimization']['ModLibSheet'][8]), redraw = True)
                self.sheet_lib.table_align(align = 'c',redraw=True)

                # Populate the sheet
                for i in range(len(self.models)):
                    json_string = self.Compare['Model Library'][self.models[i]].decode('utf-8')
                    data = json.loads(json_string)
                    self.sheet_lib.set_cell_data(i,0,self.models[i])
                    keys = ['Model Name', 'Reversible Model Name', 'Irreversible Model Name', 'Compare Type']
                    for j in range(len(keys)):
                        if keys[j] in list(data.keys()):
                            self.sheet_lib.set_cell_data(i,j+1,data[keys[j]])

            # Create the material library sheet
            create_sheet()

        else:
            messagebox.showinfo(message = 'There are no models in the library.')

    def optimizer(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Check all conditions before running optimization.
        #
        #--------------------------------------------------------------------------

        # -------------------------------------------------------------------------
        #   COMPARE
        # -------------------------------------------------------------------------
        # Run Compare
        def run_cmd_opt(callback, self):

            # Update the model
            UpdateModelData(None, self, 3, 'Model')

            # Set error checking flag
            self.flag = 0

            # Check all elastic inital guesses and bounds are populated
            if hasattr(self,'sheet1_opt'):
                for i in range(len(self.sheet1_opt.data)):
                    try:
                        # Check Value
                        float(self.sheet1_opt.data[i][3])

                        # Check Bounds
                        if self.sheet1_opt.data[i][5] == 'Active':
                            float(self.sheet1_opt.data[i][2])
                            float(self.sheet1_opt.data[i][4])
                    except:
                        self.flag = 1
                        self.msg = 'Invalid values for the elastic parameter initial guess and/or bounds.'
                        callback()

            # Check all elastic bounds are valid
            if hasattr(self,'sheet1_opt'):
                if self.flag == 0:
                    for i in range(len(self.sheet1_opt.data)):
                        # Check Bounds
                        if self.sheet1_opt.data[i][5] == 'Active':
                            if float(self.sheet1_opt.data[i][2]) > float(self.sheet1_opt.data[i][3]):
                                self.flag = 1
                                self.msg = 'Invalid values for elastic parameter bounds.'
                                callback()

                            if float(self.sheet1_opt.data[i][4]) < float(self.sheet1_opt.data[i][3]):
                                self.flag = 1
                                self.msg = 'Invalid values for elastic parameter bounds.'
                                callback()

            # Check all plastic inital guesses and bounds are populated
            if hasattr(self,'sheet2_opt'):
                for i in range(len(self.sheet2_opt.data)):
                    try:
                        # Check Value
                        float(self.sheet2_opt.data[i][3])

                        # Check Bounds
                        if self.sheet2_opt.data[i][5] == 'Active':
                            float(self.sheet2_opt.data[i][2])
                            float(self.sheet2_opt.data[i][4])
                    except:
                        self.flag = 1
                        self.msg = 'Invalid values for the plastic parameter initial guess and/or bounds.'
                        callback()

            # Check all elastic bounds are valid
            if hasattr(self,'sheet2_opt'):
                if self.flag == 0:
                    for i in range(len(self.sheet2_opt.data)):
                        if self.sheet2_opt.data[i][5] == 'Active':
                            if float(self.sheet2_opt.data[i][2]) > float(self.sheet2_opt.data[i][3]):
                                self.flag = 1
                                self.msg = 'Invalid values for plastic parameter bounds.'
                                callback()

                            if float(self.sheet2_opt.data[i][4]) < float(self.sheet2_opt.data[i][3]):
                                self.flag = 1
                                self.msg = 'Invalid values for plastic parameter bounds.'
                                callback()

            # Set the parameters
            self.Compare['Model']['Reversible Model Name'] = self.optmenu2_opt.get()
            self.Compare['Model']['Irreversible Model Name'] = self.optmenu3_opt.get()
            try:
                self.Compare['Model']['M'] = self.optmenu4_opt.get()
            except:
                self.Compare['Model']['M'] = 0
            try:
                self.Compare['Model']['N'] = self.optmenu5_opt.get()
            except:
                self.Compare['Model']['N'] = 0
            self.Compare['Model']['VE_Param'] = self.sheet1_opt.data
            self.Compare['Model']['VP_Param'] = self.sheet2_opt.data

            # Run Optimization
            if self.flag == 0:
                self.run_compare_opt()
                
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

                try:
                    # Stop Progress bar
                    pb.stop()

                    # Destroy Window
                    loading.destroy()
                except:
                    pass

            # Begin save on background thread
            threading.Thread(target=run_cmd_opt, args=(on_task_done, self), daemon=True).start()

            # Wait until loading window is closed
            self.loading = loading
            window.wait_window(loading)

        # Choose Model
        if self.Compare['Model']['Model Info']['Core'] == 'COMPARE':
            run_compare_start(self)

        if self.flag == 0:
            messagebox.showinfo(message=self.msg)
        else:
            messagebox.showerror(message=self.msg)
                               
    def run_compare_opt(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Run COMPARE Optimization.
        #
        #--------------------------------------------------------------------------

        try:
            # Create and clear the Temp Directory
            temp_dir = os.path.join(os.getcwd(),'Temp')
            try:
                os.mkdir(temp_dir)
            except:
                pass
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

            # Copy the executable
            shutil.copy(self.Compare['Paths']['Compare Executable'], temp_dir)

        except:
            self.msg = 'Unable to clear TEMP directory - clear manually.'
            self.flag = 1
            return

        try:
            # Set the model number
            mod =  mod = self.model_info_all[self.Compare['Model']['Model Name']]['Model Info']['Model']

            # Determine Model Type
            if self.Compare['Model']['Model Name'] == 'GVIPS ISO':

                # Write the DGS file
                Param, Param_U, Param_N = WriteDSG_GVIPS_ISO_OPT(self, temp_dir)

            if self.Compare['Model']['Model Name'] == 'GVIPS TISO':

                # Write the DGS file
                Param, Param_U, Param_N, P_Elas = WriteDSG_GVIPS_TISO_OPT(self, temp_dir)

        except:
            self.msg = 'Error writing DSG file.'
            self.flag = 1
            return

        try:
            # Write the Simulation files
            ct = 1
            sim_tests = list(self.Compare['Characterization'].keys())
            for sim_test in sim_tests:

                # Determine Model Type
                if self.Compare['Model']['Model Name'] == 'GVIPS ISO':
                    WriteSIM_ISO(self, self.Compare['Characterization'][sim_test], temp_dir, ct, mod, Param)

                if self.Compare['Model']['Model Name'] == 'GVIPS TISO':
                    WriteSIM_TISO(self, self.Compare['Characterization'][sim_test], temp_dir, ct, mod, Param, P_Elas)

                # Update counter
                ct = ct + 1

        except:
            self.msg = 'Error Writing SIM files.'
            self.flag = 1
            return

        try:
            # Write the NLP files
            WriteNLP(temp_dir, 'Opt')

        except:
            self.msg = 'Error Writing NLP file.'
            self.flag = 1
            return

        try:
            command = 'cmd /k "cd ' + temp_dir + ' & compnasardamage & exit"'
            os.system(command)

        except:
            self.msg = 'Error running COMPARE.'
            self.flag = 1
            return

        try:
            # Read Values
            Vals=  []
            with open(os.path.join(temp_dir,"final.val"), "r") as file:
                for line in file:
                    # Process each line here
                    line_all = line.strip()
                    val = line_all.split(' ')[-1]
                    Vals.append(val)
            
            #Update the Viscoelastic parameters
            if hasattr(self,'sheet1_opt'):
                VE = self.sheet1_opt.data
                for i in range(len(VE)):
                    try:
                        val = float(Vals[Param_N[Param.index(VE[i][0])]-1])
                        try:
                            val = UnitConversion(Param_U[Param.index(VE[i][0])], val, VE[i][1])
                        except:
                            pass
                        self.sheet1_opt.set_cell_data(i,6,'{:0.4e}'.format(val), redraw = False)

                        if VE[i][5] == 'Active':
                            if val >= 0.99*float(VE[i][4]) or val <= 1.01*float(VE[i][2]):
                                clr = 'red'
                            else:
                                clr = 'green'
                        else:
                            clr = 'green'
                        self.sheet1_opt.highlight((i,6),fg= clr, bg = 'white', redraw = False)
                    except:
                        pass

            #Update the Viscoplastic parameters
            if hasattr(self,'sheet2_opt'):
                VP = self.sheet2_opt.data
                for i in range(len(VP)):
                    try:
                        val = float(Vals[Param_N[Param.index(VP[i][0])]-1])
                        try:
                            val = UnitConversion(Param_U[Param.index(VP[i][0])], val, VP[i][1])
                        except:
                            pass
                        self.sheet2_opt.set_cell_data(i,6,'{:0.4e}'.format(val), redraw = False)

                        if VP[i][5] == 'Active':
                            if val >= 0.99*float(VP[i][4]) or val <= 1.01*float(VP[i][2]):
                                clr = 'red'
                            else:
                                clr = 'green'
                        else:
                            clr = 'green'
                        self.sheet2_opt.highlight((i,6),fg= clr, bg = 'white', redraw = False)
                    except:
                        pass

            # Redraw the sheet
            window.after_idle(lambda: (self.sheet1_opt.redraw(), self.sheet2_opt.redraw()))

            # Check that a name exists
            if 'Model ID' not in self.Compare.keys():
                self.Compare['Model ID'] = None 
            if self.Compare['Model ID'] == None:
                # Set the type
                self.Compare['Model']['Compare Type'] = 'Optimize' 

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

                    # Write model data to binary in the mode library
                    json_string = json.dumps(self.Compare['Model'])
                    binary_data = json_string.encode('utf-8')
                    self.Compare['Model Library'][user_input] = binary_data

                # Set the model name
                self.Compare['Model ID'] = user_input

            # Set model status to 1
            self.Compare['Model']['Status'] = 1

            # Get Test Error
            out_file = os.path.join(temp_dir,"comp.out")
            line_out = []
            line_ct = 1
            line_exp = []
            with open(out_file, "r") as file:
                for line in file:
                    line = line.strip()
                    line_out.append(line)
                    if "Experiment number:" in line:
                        line_exp.append(line_ct+4)
                    line_ct = line_ct + 1

            # Get the Global Error
            with open(out_file, "r") as file:
                for line in file:
                    line = line.strip()
                    line_out.append(line)
                    if "FINAL CONVERGENCE ANALYSIS" in line:
                        self.Compare['Global Error'] = float(line_out[line_out.index(line)+2].split('=')[1].replace('D','E'))

        
            # Evaluate all tests in the characterization set
            tests = list(self.Compare['Characterization'].keys())
            self.Compare['Prediction'] = dict.fromkeys(self.Compare['Data'])
            ct = 1
            for test in tests:
                # Preallocate the predictions for a test
                self.Compare['Prediction'][test] = dict.fromkeys(self.Compare['Data'][test])
                self.Compare['Prediction'][test]['Strain'] = dict.fromkeys(self.Compare['Data'][test]['Strain'])
                self.Compare['Prediction'][test]['Stress'] = dict.fromkeys(self.Compare['Data'][test]['Stress'])

                # Read the plot file
                data_plot = {'Time':[],
                            'Strain-11':[],
                            'Stress-11':[],
                            'Strain-22':[],
                            'Stress-22':[],
                            'Strain-12':[],
                            'Stress-12':[],}
                
                with open(os.path.join(temp_dir,"u" + str(ct) + ".plot"), "r") as file:
                    for line in file:
                        # Process each line here
                        line_all = line.strip()
                        line_all = line_all.split()
                        i = 0
                        for key in data_plot.keys():
                            data_plot[key].append(float(line_all[i]))
                            i=i+1

                # Populate Time
                self.Compare['Prediction'][test]['Time'] = data_plot['Time']

                # Populate Strain
                keys = list(self.Compare['Prediction'][test]['Strain'].keys())
                for key in keys:
                    self.Compare['Prediction'][test]['Strain'][key] = data_plot['Strain-' + str(key)]
                    
                # Populate Stress
                keys = list(self.Compare['Prediction'][test]['Stress'].keys())
                for key in keys:
                    self.Compare['Prediction'][test]['Stress'][key] = data_plot['Stress-' + str(key)]

                # Calculate Error
                err = float(line_out[line_exp[ct-1]].split(' ')[-1])
                self.Compare['Prediction'][test]['Error'] = err

                # Update ct
                ct = ct + 1

            

            # Write Global Error
            if hasattr(self,'globalerr_opt'):
                self.globalerr_opt.destroy()
            self.globalerr_opt = ttk.Label(
                                self.nb_tab_tab3, 
                                text=f"Global Error: {'{:0.4e}'.format(self.Compare['Global Error'])}", 
                                anchor=tk.NW,       
                                style = 'Modern1.TLabel'                    
                                )
            self.globalerr_opt.place(
                            anchor = 'w', 
                            relx = self.Placement['Optimization']['LabelGlobalErr'][0], 
                            rely = self.Placement['Optimization']['LabelGlobalErr'][1],
                            )
            
            # Update Analsysis
            self.Compare['Analysis'] = copy.deepcopy(self.Compare['Model'])
            if "VE_Param" in self.Compare['Analysis'].keys():
                for i in range(len(self.Compare['Analysis']["VE_Param" ])):
                    self.Compare['Analysis']["VE_Param" ][i] = [self.Compare['Analysis']["VE_Param" ][i][0], self.Compare['Analysis']["VE_Param" ][i][1], self.Compare['Analysis']["VE_Param" ][i][6]]
            if "VP_Param" in self.Compare['Analysis'].keys():
                for i in range(len(self.Compare['Analysis']["VP_Param" ])):
                    self.Compare['Analysis']["VP_Param" ][i] = [self.Compare['Analysis']["VP_Param" ][i][0], self.Compare['Analysis']["VP_Param" ][i][1], self.Compare['Analysis']["VP_Param" ][i][6]]

        except:
            self.msg = 'Error reading output data from COMPARE.'
            self.flag = 1
            return
        
        try:
            # Write all data to log
            self.update_log()
            self.msg = 'Optimization Complete!'

        except:
            self.msg = 'Error writing log file.'
            self.flag = 1
            return

        if self.msg == 'Optimization Complete!':
            # Set Flags
            self.flag = 0
            self.viz_init = 2
        else:
            self.flag = 1
        return 
    
    def analyze(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Check all conditions before running analysis.
        #
        #--------------------------------------------------------------------------

        # Run Compare
        def run_cmd_anly(callback, self):

            # Update the model
            UpdateModelData(None, self, 3, 'Analysis')

            # Set error checking flag
            self.flag = 0

            # Check all elastic values are populated
            if hasattr(self,'sheet1_anly'):
                for i in range(len(self.sheet1_anly.data)):
                    try:
                        float(self.sheet1_anly.data[i][3])
                    except:
                        self.flag = 1
                        self.msg = 'Invalid values for the elastic parameters.'
                        callback()

            # Check all plastic values are populated
            if hasattr(self,'sheet2_anly'):
                for i in range(len(self.sheet2_anly.data)):
                    try:
                        float(self.sheet2_anly.data[i][3])
                    except:
                        self.flag = 1
                        self.msg = 'Invalid values for the plastic parameters.'
                        callback()

            if self.flag == 0:
                if len(list(self.Compare['Data'].keys())) > 0:
                    tests = list(self.Compare['Data'].keys())
                    self.run_compare_anly(tests)
                else:
                    messagebox.showeror(message='No tests have been added to the Database.')

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
            threading.Thread(target=run_cmd_anly, args=(on_task_done,self), daemon=True).start()

            # Wait until loading window is closed
            window.wait_window(loading)

        run_compare_start(self)

        if self.flag == 0:
            messagebox.showinfo(message=self.msg)
        else:
            messagebox.showerror(message=self.msg)

    def run_compare_anly(self, tests):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Run COMPARE Analysis.
        #
        #--------------------------------------------------------------------------

        try:
            # Check for analysis
            if 'Analysis' in self.Compare.keys():
                data = copy.deepcopy(self.Compare['Analysis'])
                if 'Analysis' not in self.Compare.keys():                    
                    self.Compare['Analysis'] = data

                # Reset Model Names and Number of Mechanisms
                self.Compare['Analysis']['Reversible Model Name'] = data['Reversible Model Name']
                self.Compare['Analysis']['Irreversible Model Name'] = data['Irreversible Model Name']
                try:
                    self.Compare['Analysis']['M'] = data['M']
                except:
                    self.Compare['Analysis']['M'] = 1
                try:
                    self.Compare['Analysis']['N'] = data['N']
                except:
                    self.Compare['Analysis']['N'] = 1
                
                # Reformat Parameters
                if 'VE_Param' in list(data.keys()):
                    self.Compare['Analysis']['VE_Param'] = []
                    for i in range(len(data['VE_Param'])):
                        self.Compare['Analysis']['VE_Param'].append([data['VE_Param'][i][0],
                                                                data['VE_Param'][i][1],
                                                                data['VE_Param'][i][2],
                                                                ])
                        
                if 'VP_Param' in list(data.keys()):
                    self.Compare['Analysis']['VP_Param'] = []
                    for i in range(len(data['VP_Param'])):
                        self.Compare['Analysis']['VP_Param'].append([data['VP_Param'][i][0],
                                                                data['VP_Param'][i][1],
                                                                data['VP_Param'][i][2],
                                                                ])
        except:
            self.msg='Unable to set Analysis model parameters. Ensure a model has been loaded.'
            self.flag = 1
            return
        
        try:
            # Create and clear the Temp Directory
            temp_dir = os.path.join(os.getcwd(),'Temp')
            try:
                os.mkdir(temp_dir)
            except:
                pass
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")

            # Copy the executable
            shutil.copy(self.Compare['Paths']['Compare Executable'], temp_dir)

        except:
            self.msg = 'Unable to clear TEMP directory - clear manually.'
            self.flag = 1
            return

        try:
            # Determine Model Type
            mod = self.model_info_all[self.Compare['Analysis']['Model Name']]['Model Info']['Model']

            if self.Compare['Analysis']['Model Name'] == 'GVIPS ISO':
    
                # Write the DGS file
                Param, Param_U, Param_N = WriteDSG_GVIPS_ISO_ANLY(self, temp_dir, tests)

            elif self.Compare['Analysis']['Model Name'] == 'GVIPS TISO':
    
                # Write the DGS file
                Param, Param_U, Param_N, P_Elas = WriteDSG_GVIPS_TISO_ANLY(self, temp_dir, tests)
        except:
            self.msg = 'Error writing DSG file.'
            self.flag = 1
            return

        try:
            # Write the Simulation files
            ct = 1
            sim_tests = tests
            for sim_test in sim_tests:

                # Determine Model Type
                if self.Compare['Analysis']['Model Name'] == 'GVIPS ISO':
                    WriteSIM_ISO(self, self.Compare['Data'][sim_test], temp_dir, ct, mod, Param)

                if self.Compare['Analysis']['Model Name'] == 'GVIPS TISO':
                    WriteSIM_TISO(self, self.Compare['Data'][sim_test], temp_dir, ct, mod, Param, P_Elas)

                ct = ct + 1

        except:
            self.msg = 'Error writing SIM files.'
            self.flag = 1
            return

        try:
            # Write the NLP files
            WriteNLP(temp_dir, 'Analy')
        except:
            self.msg = 'Error writing NLP file.'
            self.flag = 1
            return

        try:
            command = 'cmd /k "cd ' + temp_dir + ' & compnasardamage & exit"'
            os.system(command)
        except:
            self.msg = 'Error running COMPARE.'
            self.flag = 1
            return

        try:
            # Set model status to 1
            self.Compare['Model']['Status'] = 1

            # Get Test Error
            out_file = os.path.join(temp_dir,"comp.out")
            line_out = []
            line_ct = 1
            line_exp = []
            with open(out_file, "r") as file:
                    for line in file:
                        line = line.strip()
                        line_out.append(line)
                        if "Experiment number:" in line:
                            line_exp.append(line_ct+4)
                        line_ct = line_ct + 1

            # Global error not calculated in analysis mode
            self.Compare['Global Error'] = ''

            # Evaluate all tests in the characterization set
            if "Prediction" not in self.Compare.keys():
                self.Compare['Prediction'] = dict.fromkeys(self.Compare['Data'])
            ct = 1
            for test in tests:
                # Preallocate the predictions for a test
                self.Compare['Prediction'][test] = dict.fromkeys(self.Compare['Data'][test])
                self.Compare['Prediction'][test]['Strain'] = dict.fromkeys(self.Compare['Data'][test]['Strain'])
                self.Compare['Prediction'][test]['Stress'] = dict.fromkeys(self.Compare['Data'][test]['Stress'])

                # Read the plot file
                data_plot = {'Time':[],
                            'Strain-11':[],
                            'Stress-11':[],
                            'Strain-22':[],
                            'Stress-22':[],
                            'Strain-12':[],
                            'Stress-12':[],}
                
                with open(os.path.join(temp_dir,"u" + str(ct) + ".plot"), "r") as file:
                    for line in file:
                        # Process each line here
                        line_all = line.strip()
                        line_all = line_all.split()
                        i = 0
                        for key in data_plot.keys():
                            data_plot[key].append(float(line_all[i]))
                            i=i+1

                # Populate Time
                self.Compare['Prediction'][test]['Time'] = data_plot['Time']

                # Populate Strain
                keys = list(self.Compare['Prediction'][test]['Strain'].keys())
                for key in keys:
                    self.Compare['Prediction'][test]['Strain'][key] = data_plot['Strain-' + str(key)]
                    
                # Populate Stress
                keys = list(self.Compare['Prediction'][test]['Stress'].keys())
                for key in keys:
                    self.Compare['Prediction'][test]['Stress'][key] = data_plot['Stress-' + str(key)]

                # Calculate Error
                err = float(line_out[line_exp[ct-1]].split(' ')[-1])
                self.Compare['Prediction'][test]['Error'] = err
                ct = ct+1

            self.msg = 'Analysis Complete!'

        except:
            self.msg = 'Error reading output data from COMPARE.'
            self.flag = 1
            return

        if self.msg == 'Analysis Complete!':
            self.flag = 0
            self.viz_init = 2
        else:
            self.flag = 1

        return 
    
    def update_log(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Update the log after a successful run
        #
        #--------------------------------------------------------------------------

        # Add spaces
        self.log.append(' ')
        self.log.append(' ')
        self.log.append('-- NEW RUN --')

        # Write Tests
        self.log.append(' ')
        self.log.append('TESTS:')
        test_data = [['NAME', 'TYPE', 'TEMP (°C)', 'DIREC', 'CONTROL', 'ANGLE (°)', 'WEIGHT' ]]
        for test in self.Compare['Characterization'].keys():
            test_data.append([test, 
                              self.Compare['Characterization'][test]['Test Type'],
                              UnitConversion(self.Compare['Characterization'][test]['Temperature'][1], self.Compare['Characterization'][test]['Temperature'][0], '°C'),
                              str(self.Compare['Characterization'][test]['Loading Direction'][0]),
                              self.Compare['Characterization'][test]['Control'][0],
                              self.Compare['Characterization'][test]['Angle'],
                              self.Compare['Characterization'][test]['RelWeight'],
                              ])
        # Column formatters matching your types
        formatter_header = "{:<10} {:<10} {:<10} {:<10} {:<10} {:<10} {:<10}"
        formatter_data   = "{:<10} {:<10} {:<10.2f} {:<10} {:<10} {:<10.2f} {:<10.4f}"

        # Write to file
        for row in test_data:
            if row[0] == 'NAME':  # Header row
                line = formatter_header.format(*row)
            else:
                line = formatter_data.format(
                    row[0], row[1],
                    float(row[2]), row[3], row[4],
                    float(row[5]), float(row[6])
                )
            self.log.append(line)

        # Write Model Information
        self.log.append(' ')
        self.log.append('MODEL INFORMATION:')
        self.log.append('Model Name: ' + self.Compare['Model']['Model Name'])
        self.log.append('Reversible Model Name: ' + self.Compare['Model']['Reversible Model Name'])
        self.log.append('Irreversible Model Name: ' + self.Compare['Model']['Irreversible Model Name'])
        try:
            self.log.append('Viscoelastic Mechanisms: ' + self.Compare['Model']['M'])
        except:
            pass
        try:
            self.log.append('Viscoplastic Mechanisms: ' + self.Compare['Model']['N'])
        except:
            pass
        self.log.append(' ')

        # Parameter information
        param = [['PARAM','UNIT','LB','INIT','UB']]
        for i in range(len(self.Compare['Model']['VE_Param'])):
            param.append(self.Compare['Model']['VE_Param'][i])
        for i in range(len(self.Compare['Model']['VP_Param'])):
            param.append(self.Compare['Model']['VP_Param'][i])

        formatter_header = "{:<10} {:<10} {:<10} {:<10} {:<10}"
        formatter_data   = "{:<10} {:<10} {:<10.4e} {:<10.4e} {:<10.4e}"
        
        # Write to file
        for row in param:
            if row[0] == 'PARAM':  # Header row
                line = formatter_header.format(*row)
            else:
                try:
                    line = formatter_data.format(
                        row[0], row[1],
                        float(row[2]), float(row[3]), float(row[4]),
                    )
                except:
                    line = formatter_data.format(
                        row[0], row[1],
                        float(row[3]), float(row[3]), float(row[3]),
                    )
            self.log.append(line)

        # Optimization Results
        self.log.append(' ')
        self.log.append('OPTIMIZATION RESULTS:')

        param = [['PARAM','UNIT','VALUE']]
        for i in range(len(self.Compare['Model']['VE_Param'])):
            param.append(self.Compare['Model']['VE_Param'][i])
        for i in range(len(self.Compare['Model']['VP_Param'])):
            param.append(self.Compare['Model']['VP_Param'][i])

        formatter_header = "{:<10} {:<10} {:<10}"
        formatter_data   = "{:<10} {:<10} {:<10.4e}"

        # Write to file
        for row in param:
            if row[0] == 'PARAM':  # Header row
                line = formatter_header.format(*row)
            else:
                try:
                    line = formatter_data.format(
                        row[0], row[1],
                        float(row[6]),
                    )
                except:
                    line = formatter_data.format(
                        row[0], row[1],
                        float(row[3]),
                    )
            self.log.append(line)

        # Test and Global Error
        self.log.append(' ')
        self.log.append('ERROR:')
        self.log.append('Global Error = ' + str(self.Compare['Global Error']))
        self.log.append(' ')

        # Write Tests
        self.log.append('TESTS:')
        test_data = [['NAME', 'TYPE', 'WEIGHT', 'ERROR' ]]
        for test in self.Compare['Characterization'].keys():
            test_data.append([test, 
                              self.Compare['Characterization'][test]['Test Type'],
                              self.Compare['Characterization'][test]['RelWeight'],
                              self.Compare['Prediction'][test]['Error'],
                              ])
        # Column formatters matching your types
        formatter_header = "{:<10} {:<10} {:<10} {:<10}"
        formatter_data   = "{:<10} {:<10} {:<10.4f} {:<10.4f}"

        # Write to file
        for row in test_data:
            if row[0] == 'NAME':  # Header row
                line = formatter_header.format(*row)
            else:

                line = formatter_data.format(
                    row[0], row[1],
                    float(row[2]), float(row[3]), 
                )

            self.log.append(line)

        # Write Data
        with open(self.log_file, "a", encoding="utf-8") as f:
            for line in self.log:
                f.write(line + "\n")

        # Close the file and reset lof
        f.close()
        self.log = []
    
    #------------------------------------------------------------------------------
    #
    #   VISUALIZATION FUNCTIONS
    #   Functions for the Visualization Tab
    #
    #------------------------------------------------------------------------------

    def plotter_viz(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Plot Visualization curves.
        #
        #--------------------------------------------------------------------------

        #  Delete the canvases and drop downs if it exists
        try:
            self.toolbar_viz1.destroy()
            self.canvas_viz1.get_tk_widget().destroy()
            del self.canvas_viz1
        except:
            pass

        try:
            self.toolbar_viz2.destroy()
            self.canvas_viz2.get_tk_widget().destroy()
            del self.canvas_viz2
        except:
            pass

        # -- LEFT PLOT --
        # Create the plot
        self.fig_viz1 = Figure(figsize=(
                                        self.Placement['Visualization']['Figure1'][4],self.Placement['Visualization']['Figure1'][5]), 
                                        dpi = self.Placement['Visualization']['Figure1'][6], 
                                        constrained_layout = True)
        self.plot1 = self.fig_viz1.add_subplot(111)

        # Get the arrays
        val = self.optmenu1_viz.get().split(' vs ')
        y_val = val[0]
        x_val = val[1]

        # X Value
        xp = None
        if 'Time' in x_val:
            x = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            xs = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            if 'Prediction' in list(self.Compare.keys()):
                xp = self.Compare['Prediction'][self.test_name]['Time']
            xu = 'Time [s]'
        else:
            x_val = x_val.split('-')
            x = self.Compare['Data'][self.test_name][x_val[0]][int(x_val[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            xs = self.Compare['Data'][self.test_name]['Reduced Data'][x_val[0]][int(x_val[1])]
            if 'Prediction' in list(self.Compare.keys()):
                xp = self.Compare['Prediction'][self.test_name][x_val[0]][int(x_val[1])]
            if x_val[0] == 'Strain':
                xu = 'Strain'
            else:
                xu = 'Stress [MPa]'

         # Y Value
        yp = None
        if 'Time' in y_val:
            y = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            if 'Prediction' in list(self.Compare.keys()):
                yp = self.Compare['Prediction'][self.test_name]['Time']
            yu = 'Time [s]'
        else:
            y_val = y_val.split('-')
            y = self.Compare['Data'][self.test_name][y_val[0]][int(y_val[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            ys = self.Compare['Data'][self.test_name]['Reduced Data'][y_val[0]][int(y_val[1])]
            if 'Prediction' in list(self.Compare.keys()):
                yp = self.Compare['Prediction'][self.test_name][y_val[0]][int(y_val[1])]
            if y_val[0] == 'Strain':
                yu = 'Strain'
            else:
                yu = 'Stress [MPa]'

        # Plot the data
        self.plot1.plot(x,y,'k',label = 'Raw Data')
        if xs is not None:
            self.plot1.plot(xs,ys,'ko',label = 'Reduced Data')
        if xp is not None:
            self.plot1.plot(xp,yp, color = 'r', linestyle='--', marker='o', markerfacecolor='none',label ='Prediction')

        # Set Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot1.set_xlabel(xlab)
        self.plot1.set_ylabel(ylab)
        self.plot1.xaxis.set_major_formatter(xlab_frmt)
        self.plot1.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot1.legend()

        # Create the Tkinter canvas
        self.canvas_viz1 = FigureCanvasTkAgg(self.fig_viz1, master = self.nb_tab_tab5)


        # Create the Matplotlib toolbar
        self.toolbar_viz1 = NavigationToolbar2Tk(self.canvas_viz1, self.nb_tab_tab5)

        # Format Toolbar
        self.toolbar_viz1.config(bg='white')
        self.toolbar_viz1._message_label.config(background='white')
        self.toolbar_viz1.place(
                        anchor = 'n', 
                        relx = self.Placement['Visualization']['Toolbar1'][0], 
                        rely = self.Placement['Visualization']['Toolbar1'][1],
                        relwidth = self.Placement['Visualization']['Toolbar1'][2],
                        relheight = self.Placement['Visualization']['Toolbar1'][3]
                        )

        # Add the figure to the GUI
        self.canvas_viz1.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Visualization']['Figure1'][0], 
                                        rely = self.Placement['Visualization']['Figure1'][1], 
                                        relwidth = self.Placement['Visualization']['Figure1'][2], 
                                        relheight = self.Placement['Visualization']['Figure1'][3]
                                        )

        if 'self.toolbar_viz1' not in self.atts['Visualization']['Local']:
            self.atts['Visualization']['Local'].append("self.toolbar_viz1")
            self.atts['Visualization']['Local'].append("self.canvas_viz1")

        # -- RIGHT PLOT --
        # Create the plot
        self.fig_viz2 = Figure(figsize=(self.Placement['Visualization']['Figure2'][4],self.Placement['Visualization']['Figure2'][5]), 
                               dpi = self.Placement['Visualization']['Figure2'][6], 
                               constrained_layout = True)
        self.plot2 = self.fig_viz2.add_subplot(111)

        # Get the arrays
        val = self.optmenu2_viz.get().split(' vs ')
        y_val2 = val[0]
        x_val2 = val[1]

        # X Value
        xp = None
        if 'Time' in x_val2:
            x = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            xs = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            if 'Prediction' in list(self.Compare.keys()):
                xp = self.Compare['Prediction'][self.test_name]['Time']
            xu = 'Time [s]'
        else:
            x_val2 = x_val2.split('-')
            x = self.Compare['Data'][self.test_name][x_val2[0]][int(x_val2[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            xs = self.Compare['Data'][self.test_name]['Reduced Data'][x_val2[0]][int(x_val2[1])]
            if 'Prediction' in list(self.Compare.keys()):
                xp = self.Compare['Prediction'][self.test_name][x_val2[0]][int(x_val2[1])]
            if x_val2[0] == 'Strain':
                xu = 'Strain'
            else:
                xu = 'Stress [MPa]'

         # Y Value
        yp = None
        if 'Time' in y_val2:
            y = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
            if 'Prediction' in list(self.Compare.keys()):
                yp = self.Compare['Prediction'][self.test_name]['Time']
            yu = 'Time [s]'
        else:
            y_val2 = y_val2.split('-')
            y = self.Compare['Data'][self.test_name][y_val2[0]][int(y_val2[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
            ys = self.Compare['Data'][self.test_name]['Reduced Data'][y_val2[0]][int(y_val2[1])]
            if 'Prediction' in list(self.Compare.keys()):
                yp = self.Compare['Prediction'][self.test_name][y_val2[0]][int(y_val2[1])]
            if y_val2[0] == 'Strain':
                yu = 'Strain'
            else:
                yu = 'Stress [MPa]'

        # Plot the data
        self.plot2.plot(x,y,'k',label = 'Raw Data')
        if xs is not None:
            self.plot2.plot(xs,ys,'ko',label = 'Reduced Data')
        if xp is not None:
            self.plot2.plot(xp,yp, color = 'r', linestyle='--', marker='o', markerfacecolor='none',label ='Prediction')

        # Set Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot2.set_xlabel(xlab)
        self.plot2.set_ylabel(ylab)
        self.plot2.xaxis.set_major_formatter(xlab_frmt)
        self.plot2.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot2.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot2.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot2.legend()

        # Create the Tkinter canvas
        self.canvas_viz2 = FigureCanvasTkAgg(self.fig_viz2, master = self.nb_tab_tab5)

        # Create the Matplotlib toolbar
        self.toolbar_viz2 = NavigationToolbar2Tk(self.canvas_viz2, self.nb_tab_tab5)

        # Format Toolbar
        self.toolbar_viz2.config(bg='white')
        self.toolbar_viz2._message_label.config(background='white')
        self.toolbar_viz2.place(
                        anchor = 'n', 
                        relx = self.Placement['Visualization']['Toolbar2'][0], 
                        rely = self.Placement['Visualization']['Toolbar2'][1], 
                        relwidth = self.Placement['Visualization']['Toolbar2'][2], 
                        relheight = self.Placement['Visualization']['Toolbar2'][3]
                        )

        # Add the figure to the GUI
        self.canvas_viz2.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Visualization']['Figure2'][0], 
                                        rely = self.Placement['Visualization']['Figure2'][1], 
                                        relwidth = self.Placement['Visualization']['Figure2'][2], 
                                        relheight = self.Placement['Visualization']['Figure2'][3]
                                        )
        # Update window
        self.nb_tab_tab5.update_idletasks()
        self.canvas_viz1.draw()
        self.toolbar_viz1.update()
        self.canvas_viz2.draw()
        self.toolbar_viz2.update()

        if 'self.toolbar_viz2' not in self.atts['Visualization']['Local']:
            self.atts['Visualization']['Local'].append("self.toolbar_viz2")
            self.atts['Visualization']['Local'].append("self.canvas_viz2")

    def plotter_viz_all(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Plot Visualization curves.
        #
        #--------------------------------------------------------------------------

        #  Delete the canvases and drop downs if it exists
        try:
            self.toolbar_viz1.destroy()
            self.canvas_viz1.get_tk_widget().destroy()
            del self.canvas_viz1
        except:
            pass

        try:
            self.toolbar_viz2.destroy()
            self.canvas_viz2.get_tk_widget().destroy()
            del self.canvas_viz2
        except:
            pass

        # Generate colors
        colors = plt.cm.tab10.colors
        while len(colors) < len(self.tests_all):
            colors = colors + colors

        # -- LEFT PLOT --
        # Create the plot
        self.fig_viz1 = Figure(
                        figsize=(self.Placement['Visualization']['Figure1'][4],self.Placement['Visualization']['Figure1'][5]), 
                        dpi = self.Placement['Visualization']['Figure1'][6], 
                        constrained_layout = True)
        self.plot1 = self.fig_viz1.add_subplot(111)

        # Get the arrays
        val = self.optmenu3_viz.get().split(' vs ')
        y_val_all = val[0]
        x_val_all = val[1]

        for i, test in enumerate(self.tests_all):
            self.test_name = test
            # X Value
            xp = None
            if 'Time' in x_val_all:
                x = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                xs = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
                xu = 'Time [s]'
            else:
                x_val = x_val_all.split('-')
                x = self.Compare['Data'][self.test_name][x_val[0]][int(x_val[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                xs = self.Compare['Data'][self.test_name]['Reduced Data'][x_val[0]][int(x_val[1])]
                if x_val[0] == 'Strain':
                    xu = 'Strain'
                else:
                    xu = 'Stress [MPa]'

            # Y Value
            yp = None
            if 'Time' in y_val_all:
                y = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
                yu = 'Time [s]'
            else:
                y_val = y_val_all.split('-')
                y = self.Compare['Data'][self.test_name][y_val[0]][int(y_val[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                ys = self.Compare['Data'][self.test_name]['Reduced Data'][y_val[0]][int(y_val[1])]
                if y_val[0] == 'Strain':
                    yu = 'Strain'
                else:
                    yu = 'Stress [MPa]'

            # Plot the data
            self.plot1.plot(x,y,color = colors[i],label = test)
            if xs is not None:
                self.plot1.plot(xs,ys,color = colors[i], label = None)


        # Set Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot1.set_xlabel(xlab)
        self.plot1.set_ylabel(ylab)
        self.plot1.xaxis.set_major_formatter(xlab_frmt)
        self.plot1.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot1.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot1.legend()

        # Create the Tkinter canvas
        self.canvas_viz1 = FigureCanvasTkAgg(self.fig_viz1, master = self.nb_tab_tab5)

        # Create the Matplotlib toolbar
        self.toolbar_viz1 = NavigationToolbar2Tk(self.canvas_viz1, self.nb_tab_tab5)

        # Format Toolbar
        self.toolbar_viz1.config(bg='white')
        self.toolbar_viz1._message_label.config(background='white')
        self.toolbar_viz1.place(
                        anchor = 'n', 
                        relx = self.Placement['Visualization']['Toolbar1'][0], 
                        rely = self.Placement['Visualization']['Toolbar1'][1], 
                        relwidth = self.Placement['Visualization']['Toolbar1'][2], 
                        relheight = self.Placement['Visualization']['Toolbar1'][3]
                        )

        # Add the figure to the GUI
        self.canvas_viz1.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Visualization']['Figure1'][0], 
                                        rely = self.Placement['Visualization']['Figure1'][1], 
                                        relwidth = self.Placement['Visualization']['Figure1'][2], 
                                        relheight = self.Placement['Visualization']['Figure1'][3]
                                        )
        if 'self.toolbar_viz1' not in self.atts['Visualization']['Local']:
            self.atts['Visualization']['Local'].append("self.toolbar_viz1")
            self.atts['Visualization']['Local'].append("self.canvas_viz1")

        # -- RIGHT PLOT --
        # Create the plot
        self.fig_viz2 = Figure(
                            figsize=(self.Placement['Visualization']['Figure2'][4],self.Placement['Visualization']['Figure2'][5]), 
                            dpi = self.Placement['Visualization']['Figure2'][6], 
                            constrained_layout = True)
        self.plot2 = self.fig_viz2.add_subplot(111)

        # Get the arrays
        val = self.optmenu3_viz.get().split(' vs ')
        y_val_all2 = val[0]
        x_val_all2 = val[1]

        for i, test in enumerate(self.tests_all):
            self.test_name = test

            # X Value
            xp = None
            if 'Time' in x_val_all2:
                x = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                xs = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
                if 'Prediction' in list(self.Compare.keys()):
                    xp = self.Compare['Prediction'][self.test_name]['Time']
                xu = 'Time [s]'
            else:
                x_val2 = x_val_all2.split('-')
                x = self.Compare['Data'][self.test_name][x_val2[0]][int(x_val2[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                xs = self.Compare['Data'][self.test_name]['Reduced Data'][x_val2[0]][int(x_val2[1])]
                if 'Prediction' in list(self.Compare.keys()):
                    xp = self.Compare['Prediction'][self.test_name][x_val2[0]][int(x_val2[1])]
                if x_val2[0] == 'Strain':
                    xu = 'Strain'
                else:
                    xu = 'Stress [MPa]'

            # Y Value
            yp = None
            if 'Time' in y_val_all2:
                y = self.Compare['Data'][self.test_name]['Time'][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                ys = self.Compare['Data'][self.test_name]['Reduced Data']['Time']
                if 'Prediction' in list(self.Compare.keys()):
                    yp = self.Compare['Prediction'][self.test_name]['Time']
                yu = 'Time [s]'
            else:
                y_val2 = y_val_all2.split('-')
                y = self.Compare['Data'][self.test_name][y_val2[0]][int(y_val2[1])][:self.Compare['Data'][self.test_name]['Stage Index'][-1]]
                ys = self.Compare['Data'][self.test_name]['Reduced Data'][y_val2[0]][int(y_val2[1])]
                if 'Prediction' in list(self.Compare.keys()):
                    yp = self.Compare['Prediction'][self.test_name][y_val2[0]][int(y_val2[1])]
                if y_val2[0] == 'Strain':
                    yu = 'Strain'
                else:
                    yu = 'Stress [MPa]'

            # Plot the data
            if xp is not None:
                self.plot2.plot(xp,yp, color = colors[i], linestyle='--', markerfacecolor='none',label =self.test_name)

        # Set Formatting
        xlab = xu
        ylab = yu
        xlab_frmt = ScalarFormatter() 
        ylab_frmt = ScalarFormatter()

        # Format the plot
        self.plot2.set_xlabel(xlab)
        self.plot2.set_ylabel(ylab)
        self.plot2.xaxis.set_major_formatter(xlab_frmt)
        self.plot2.yaxis.set_major_formatter(ylab_frmt)
        if "Strain" in xlab or "Time" in xlab:
            self.plot2.ticklabel_format(style='sci',scilimits=(-6,-3),axis='x')
        if "Strain" in ylab or "Time" in ylab:
            self.plot2.ticklabel_format(style='sci',scilimits=(-6,-3),axis='y')
        self.plot2.legend()

        # Create the Tkinter canvas
        self.canvas_viz2 = FigureCanvasTkAgg(self.fig_viz2, master = self.nb_tab_tab5)

        # Create the Matplotlib toolbar
        self.toolbar_viz2 = NavigationToolbar2Tk(self.canvas_viz2, self.nb_tab_tab5)

        # Format Toolbar
        self.toolbar_viz2.config(bg='white')
        self.toolbar_viz2._message_label.config(background='white')
        self.toolbar_viz2.place(
                        anchor = 'n', 
                        relx = self.Placement['Visualization']['Toolbar2'][0], 
                        rely = self.Placement['Visualization']['Toolbar2'][1], 
                        relwidth = self.Placement['Visualization']['Toolbar2'][2], 
                        relheight = self.Placement['Visualization']['Toolbar2'][3]
                        )

        # Add the figure to the GUI
        self.canvas_viz2.get_tk_widget().place(
                                        anchor = 'n', 
                                        relx = self.Placement['Visualization']['Figure2'][0], 
                                        rely = self.Placement['Visualization']['Figure2'][1],
                                        relwidth = self.Placement['Visualization']['Figure2'][2],
                                        relheight = self.Placement['Visualization']['Figure2'][3]
                                        )
        
        # Update window
        self.nb_tab_tab5.update_idletasks()
        self.canvas_viz1.draw()
        self.toolbar_viz1.update()
        self.canvas_viz2.draw()
        self.toolbar_viz2.update()

        if 'self.toolbar_viz2' not in self.atts['Visualization']['Local']:
            self.atts['Visualization']['Local'].append("self.toolbar_viz2")
            self.atts['Visualization']['Local'].append("self.canvas_viz2")

# Run the GUI
PY_COMPARE()