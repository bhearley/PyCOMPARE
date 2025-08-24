#-----------------------------------------------------------------------------------------
#
#   GetStyles.py
#
#   PURPOSE: Set the self.btn_style1s for the GUI
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def GetStyles(self):
    # Import modules
    from tkinter import ttk

    # Initialize Syles
    self.style = ttk.Style()
    self.style.theme_use("alt") 
    self.style_man = {}

    self.min_font = 10
    min_pad = 2

    # Buttons
    # -- Blue Large Text
    self.style.configure(
                        "Modern1.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", max([self.min_font, int(18*self.scale)])),
                        borderwidth=2,
                        padding=max([self.min_font, int(5*self.scale)]),
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern1.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Red Small Text
    self.style.configure(
                        "Modern2.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", max([self.min_font, int(16*self.scale)])),
                        borderwidth=2,
                        padding=max([min_pad, int(5*self.scale)]),
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern2.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Red Large Text
    self.style.configure(
                        "Modern3.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", max([self.min_font, int(18*self.scale)])),
                        borderwidth=2,
                        padding=max([min_pad, int(4*self.scale)]),
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern3.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Red Mini Text
    self.style.configure(
                        "Modern4.TButton",
                        background='#0b3d91',
                        foreground="white",
                        font=("Segoe UI", max([self.min_font, int(12*self.scale)])),
                        borderwidth=2,
                        padding=2,
                        focuscolor='',
                        highlightthickness=0
                        )

    self.style.map(
                        "Modern4.TButton",
                        background=[("active", "#428bca")]
                )
    
    # -- Toolbar
    self.style.configure(
                        "Modern5.TButton",
                        background="#FFFFFF",
                        foreground="black",
                        font=("Segoe UI", max([8, int(10*self.scale)])),
                        borderwidth=2,
                        padding=2,
                        focuscolor='',
                        highlightthickness=0,
                        relief = 'flat'
                        )

    self.style.map(
                        "Modern5.TButton",
                        background=[
                                ("active", "#B4B4B4"),
                                ("pressed", "#FFFFFF")  
                        ],
                        relief=[
                                ("pressed", "flat"),    
                                ("!pressed", "flat")
                        ]
                )
    
    # Combo Box Style
    self.style.configure(
                        "Modern.TCombobox",
                        fieldbackground="white",   
                        background="white",        
                        foreground="black",        
                        bordercolor="#cccccc",
                        lightcolor="#dddddd",
                        darkcolor="#aaaaaa",
                        borderwidth=1,
                        relief="flat",
                        padding=2,
                        font=("Segoe UI", max([8, int(12*self.scale)]))
                        )
    self.style_man['Combo'] = ("Segoe UI", max([8, int(12*self.scale)]))
    self.style.map(
                        "Modern.TCombobox",
                        fieldbackground=[("readonly", "white"), ("active", "white")], 
                        foreground=[("readonly", "black"), ("active", "black")],  
                        background=[("readonly", "white"), ("active", "white")],  
                        selectbackground=[("active", "white"), ("readonly", "white")],  
                        selectforeground=[("active", "black"), ("readonly", "black")]  
                 )
    
    # Frame
    self.style.configure(
                        'White.TFrame',
                        background = 'white'
                        )
    
    # Frames
    self.style.configure(
        "Custom1.TFrame",
        background="#ffffff",
        relief="flat",
        borderwidth = 0
    )
    
    # Label
    # -- Label 1
    self.style.configure(
                        "Modern1.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", max([8, int(14*self.scale)])),
                        padding=0
                        )
    
    # -- Label 2
    self.style.configure(
                        "Modern2.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", max([8, int(10*self.scale)])),
                        padding=0
                        )
    
    # -- Label 2
    self.style.configure(
                        "Modern3.TLabel",
                        foreground="black",
                        background="white",
                        font=("Segoe UI", max([8, int(12*self.scale)])),
                        padding=0
                        )
    
    # Notebook
    # -- Configure the Notebook itself
    self.style.layout("TNotebook.Tab", [
            ('Notebook.tab', {
                'children': [
                    ('Notebook.padding', {
                        'side': 'top',
                        'children': [
                            ('Notebook.label', {'side': 'top', 'sticky': ''})
                        ]
                    })
                ],
                'sticky': 'nswe'
            })
        ])
    
    self.style.configure(
        "CustomNotebook.TNotebook",
        background="#d8e8f8",
        borderwidth = 0,
        relief = 'flat'
    )

    # -- Configure the tabs
    self.style.configure(
        "CustomNotebook.TNotebook.Tab",
        background="#d9e6ff",      # Tab background color
        foreground="#0b3d91",      # Tab text color
        font=("Segoe UI", max([self.min_font, int(16*self.scale)]), "bold"),
    )

    # Optional: change color on selected tab
    self.style.map(
        "CustomNotebook.TNotebook.Tab",
        background=[("selected", "#428bca")],
        foreground=[("selected", "#ffffff")]
    )
    
    # Progress Bar
    self.style.configure(
                        "Modern.Horizontal.TProgressbar",
                        thickness=20,             
                        troughcolor="#d3d3d3",    
                        background="#0b3d91",     
                        )
    
    # Scale Style
    self.style.configure(
                        "Modern.Horizontal.TScale",
                        troughcolor="#DD361C", 
                        background="white",
                        borderwidth=1,
                        relief='rasied'
                        )

    # Scrollbar Style
    self.style.configure(
                        "Vertical.TScrollbar",
                        background="#0b3d91",
                        troughcolor="#d9d9d9",
                        bordercolor="#cccccc",
                        arrowcolor="#d9d9d9"#"#0b3d91",
                        )