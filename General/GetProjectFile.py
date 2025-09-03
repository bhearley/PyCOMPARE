#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# GetProjectFile.py
#
# PURPOSE: Load existing project information or define a new project.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateNewProject(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Get the filepath for a new project.
    #
    #--------------------------------------------------------------------------

    # Import Modules
    from tkinter import filedialog

    # Preallocate file path
    file_path = ''

    # Ask where to save the new file
    while '.cmprj' not in file_path:
        file_path = filedialog.asksaveasfilename(
            title="Create a new project file",
            filetypes=(("Compare Project Files", "*.cmprj"),)
        )

        if file_path == '':
            self.proj_file = None
            return
        
        elif '.cmprj' not in file_path:
            if '.' in file_path:
                file_path = file_path[:file_path.index('.')] + '.cmprj'
            else:
                file_path = file_path + '.cmprj'

    # Set the project file path
    self.proj_file = file_path

    return
 
def LoadProject(self):
    #--------------------------------------------------------------------------
    #
    #   PURPOSE: Load an existing project file.
    #
    #--------------------------------------------------------------------------

    # Import Modules
    from tkinter import filedialog
    from tkinter import messagebox
    import os
    import pickle

    # Preallocate file path
    file_path = ''

    # Ask for the file name
    while '.cmprj' not in file_path:
        file_path = filedialog.askopenfilename(
            title="Open a file project",
            filetypes=(("Compare Project Files", "*.cmprj"),)
        )

        if file_path == '':
            self.proj_file = None
            return
        
        elif '.cmprj' not in file_path:
            messagebox.showinfo("Wrong Filetype", "Compare Project File not selected. Please select a valid file or press 'Cancel' and select 'New Project File'.")

    # Set the project file path
    self.proj_file = file_path

    # Initialize the data structure
    try:
        # Read the File
        with open(file_path, "rb") as file:
            self.Compare = pickle.load(file)

        # Get the log file
        if os.path.exists(os.path.join(os.getcwd(),"Logs",os.path.basename(self.proj_file).split('.')[0] + ".log")):
            self.log_file = os.path.join(os.getcwd(),"Logs",os.path.basename(self.proj_file).split('.')[0] + ".log")
        
    except:
        # Return empty data structure
        self.Compare = {}

    # Re-Initialize the Path Dependencies
    model_library = os.path.join(self.home,'Model','AvailableModels.json')
    import_template = os.path.join(self.home,'Templates','ImportTemplate.xlsx')
    export_template = os.path.join(self.home,'Templates','ExportTemplate.xlsx')
    compare_path = os.path.join(self.home,'compnasardamage.exe')
    self.Compare['Paths'] = {'Model Library':model_library,
                                'Import Template':import_template,
                                'Export Template':export_template,
                                'Compare Executable':compare_path,}

    return