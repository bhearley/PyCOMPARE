#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
#   PyCOMPARE_Gateway.py
#   Brandon Hearley - LMS
#   brandon.l.hearley@nasa.gov
#   8/25/2025
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def PyCOMPARE_Gateway():
    # Import Modules
    import os
    from PIL import ImageTk, Image
    from powermi import Connect
    import tkinter as tk
    from tkinter import messagebox

    # Import Functions
    from Gateway.BuildStartPage import BuildStartPage
    from Gateway.TestSelection import TestSelection
    from Gateway.WriteToGranta import WriteToGranta
    from GUI.GetStyles import GetStyles
    from GUI.Placements import Placements

    #Create the GUI
    class PY_COMPARE_Gateway:

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
            window.title("PCOMPARE Gateway")
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
            for att in self.att_list:
                try:
                    eval(att).destroy()
                except:
                    pass
            self.att_list = []
            window.update()

            # Load the test selection page
            TestSelection(self, window)

        # Function to export data
        def export_data(self):
            # Delete the home page
            for att in self.att_list:
                try:
                    eval(att).destroy()
                except:
                    pass
            self.att_list = []
            window.update()

            WriteToGranta(self, window)

        # Function to go back to home page
        def back(self):
            # Delete the home page
            for att in self.att_list:
                try:
                    eval(att).destroy()
                except:
                    pass
            self.att_list = []
            window.update()

            # Load the home page
            BuildStartPage(self, window)

    # Run the GUI   
    PY_COMPARE_Gateway()

# Run the Function
PyCOMPARE_Gateway()