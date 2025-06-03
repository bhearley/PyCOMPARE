#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# PyCOMPARE.py
#   Brandon Hearley - LMS
#   brandon.l.hearley@nasa.gov
#   4/15/2025
#
# PURPOSE: Run the PyCOMPARE GUI
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Import Modules
from GRCMI import Connect
import copy
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.ticker import ScalarFormatter
import numpy as np
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Border, Side
import os
import pandas as pd
from pathlib import Path
import pickle
from PIL import ImageTk, Image
from scipy.interpolate import CubicSpline
import shutil
import tkinter as tk
from tkinter import filedialog 
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import scrolledtext
from tkinter import ttk 
import tksheet

# Import Functions
from Gateway.BuildStartPage import *
from Gateway.TestSelection import *
from General.DeleteWidgets import *
from GUI.GetStyles import *



# Set Directories
home = os.getcwd()

# Define Images
title_img = os.path.join(home,'GUI','TitleHeader.png') # Set the title image path
logo_img = os.path.join(home,'GUI','NasaLogo.png')     # Set the logo image path

#Create the GUI
class PY_COMPARE:
    #Initialize
    def __init__(self):
        #--------------------------------------------------------------------------
        #
        #   PURPOSE: Initialize the GUI.
        #
        #--------------------------------------------------------------------------

        # Set global variales
        global window, frmt

        #Create Background Window
        window = tk.Tk()
        window.title("PyCOMPARE")
        window.geometry("1500x875")
        window.resizable(False, False)
        window.configure(bg='white')

        # Get Styles
        GetStyles(self)

        #Add the Title
        img = Image.open(title_img)
        scale = 0.9
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_hdr = ImageTk.PhotoImage(img)
        self.panel_hdr = tk.Label(window, image = self.img_hdr, bg = 'white')
        self.panel_hdr.place(
                            anchor = 'n', 
                            relx = 0.5, 
                            rely = 0.005
                            )

        #Add the NASA Logo
        img = Image.open(logo_img)
        scale = 0.8
        img = img.resize((int(img.width*scale), int(img.height*scale)))
        self.img_nasa = ImageTk.PhotoImage(img)
        self.panel_nasa = tk.Label(window, image = self.img_nasa, bg = 'white')
        self.panel_nasa.place(
                            anchor = 'e', 
                            relx = 0.999, 
                            rely = 0.045
                            )

        # Connect to the database
        try:
            server_name = "https://granta.ndc.nasa.gov"
            db_key = "NasaGRC_MD_45_09-2-05"
            table_name = "Test Data: Thermomechanical"
            self.mi, self.db, self.table = Connect(server_name, db_key, table_name)
            BuildStartPage(self, window)
        except:
            messagebox.showerror(message = "Unable to connect to the Granta MI Database!")
        
        window.mainloop()

    # Function to import data
    def import_data(self):
        # Delete the home page
        DeletePages(self)

        # Load the tes selection page
        TestSelection(self, window)

    # Function to export data
    def export_data(self):
        # Delete the home page
        DeletePages(self)


# Run the GUI
PY_COMPARE()