#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# BuildHomePage.py
#
# PURPOSE: Build the home page to load a project a create a new project
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def BuildHomePage(self,window,frmt):
    # Import Modules
    import tkinter as tk

    # Unpack Formatting
    bg_color = frmt[0] 
    fontname = frmt[1]
    fsize_s = frmt[2]

    # Preallocate the att list
    self.att_list = []

    # Create a StringVar to associate with the label
    text_var = tk.StringVar()
    text_var.set("")

    # Create the label widget with all options
    self.desc1 = tk.Label(window, 
                     textvariable=text_var, 
                     anchor=tk.CENTER,       
                     bg=bg_color,                  
                     bd=3,  
                     width=30,            
                     height = 10,
                     font=(fontname, fsize_s),              
                     padx=25,               
                     pady=25,                
                     justify=tk.CENTER,    
                     relief=tk.RAISED,                
                     wraplength=800         
                    )
    self.desc1.place(anchor = 'center', relx = 0.5, rely = 0.5)
    self.att_list.append('self.desc1')

    #Create a button to create a new project
    self.btn1 = tk.Button(window, text = "New Project", command = self.new_project, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn1.place(anchor = 'center', relx = 0.5, rely = 0.4)
    self.att_list.append('self.btn1')

    #Create a button to load a project
    self.btn2 = tk.Button(window, text = "Load Project", command = self.load_project, 
                                font = (fontname, fsize_s), bg = '#0b3d91', fg='white',
                                width = 18)
    self.btn2.place(anchor = 'center', relx = 0.5, rely = 0.6)
    self.att_list.append('self.btn2')