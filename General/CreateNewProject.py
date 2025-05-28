#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# CreateNewProject.py
#
# PURPOSE: Create a new project file.
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def CreateNewProject(self):
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