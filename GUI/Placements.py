#-----------------------------------------------------------------------------------------
#
#   Placements.py
#
#   PURPOSE: Get the coordinates and size of each widget based on screen size
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def Placements(self, screen_width, screen_height):
    # Initialize Placement
    Placement = {
                'HomePage':{},
                'General':{},
                'Data':{},
                'Characterization':{},
                'Optimization':{},
                'Analysis':{},
                'Visualization':{},
                'Export':{},
                'Settings':{},
                'Gateway':{},
                }
    
    # Set Window Sizes
    sizes = [[1500, 850],
             [2200, 1300]]
    
    size = -1
    for i in range(len(sizes)):
        if screen_width > sizes[i][0] and screen_height > sizes[i][1]:
            size = i
    self.screen_w = sizes[size][0]
    self.screen_h = sizes[size][1]

    # Set Scale
    self.scale = ((self.screen_w / sizes[-1][0]) * (self.screen_h / sizes[-1][1])) ** 0.5

    # -- Home Page
    Placement['HomePage']['Toolbar'] = [0.0, 0.0, 0.3, 0.035]
    Placement['HomePage']['Title'] = [0.5, 0.005, 0.3, 0.07, 0.9]
    Placement['HomePage']['Logo'] = [0.999, 0.03, 0.06, 0.06, 0.8]
    Placement['General']['FrameTab'] = [0.5, 0.075, 0.99, 0.915]
    Placement['General']['NBTab'] = [0, 0, 1.0, 1.0]


    # -- General Page
    startx = 0.0
    delx = 0.105

    # -- Data
    Placement['Data']['ComboX'] = [0.67, 0.05, 0.075, 0.03]
    Placement['Data']['LabelVS'] = [0.735, 0.05]
    Placement['Data']['ComboY'] = [0.8, 0.05, 0.075, 0.03]
    Placement['Data']['ButtonPlot'] = [0.9, 0.0425, 0.05, 0.04]
    Placement['Data']['LabelStage'] = [0, 0.51]
    Placement['Data']['SheetSTG'] = [0, 0.55, 0.425, 0.4, 0.158, 0.173, 0.128, 0.188, 0.188, .128]
    Placement['Data']['ComboPlot'] = [0.765, 0.05, 0.075, 0.03]
    Placement['Data']['SheetDB'] = [0, 0.1, 0.425, 0.4, 0.035, 0.173, 0.11, 0.128, 0.128, 0.128, 0.142, 0.128]
    Placement['Data']['ButtonExc'] = [0.0, 0.05, 0.12, 0.05]
    Placement['Data']['ButtonAdd'] = [0.125, 0.05, 0.135, 0.05]
    Placement['Data']['Figure1'] = [0.75, 0.1275, 0.5, 0.7, 5, 3.6, 125]
    Placement['Data']['Toolbar1'] = [0.815, 0.825, 0.2, 0.05]

    # -- Characterization
    Placement['Characterization']['ComboX'] = [0.67, 0.05, 0.075, 0.03]
    Placement['Characterization']['LabelVS'] = [0.735, 0.05]
    Placement['Characterization']['ComboY'] = [0.8, 0.05, 0.075, 0.03]
    Placement['Characterization']['ButtonPlot'] = [0.9, 0.0425, 0.05, 0.04]
    Placement['Characterization']['LabelStage'] = [0, 0.59]
    Placement['Characterization']['SheetSTG'] = [0, 0.63, 0.4, 0.3, 0.16, 0.175, 0.13, 0.19, 0.19, .15]
    Placement['Characterization']['ComboPlot'] = [0.765, 0.05, 0.075, 0.03]
    Placement['Characterization']['LabelChar'] = [0, 0.05]
    Placement['Characterization']['SheetChar'] = [0, 0.075, 0.4, 0.3, 0.15, 0.11, 0.12, 0.12, 0.12, 0.14, 0.12, 0.11]
    Placement['Characterization']['ButtonRed'] = [0.765, 0.9, 0.08, 0.04]
    Placement['Characterization']['SheetRed'] = [0.5, 0.4, 0.8, 0.7, 0.48, 0.48]
    Placement['Characterization']['ButtonGetRed'] = [0.5, 0.9, 0.8, 0.1]
    Placement['Characterization']['ButtonAdd'] = [0.74, 0.96, 0.04, 0.04]
    Placement['Characterization']['ButtonDel'] = [0.79, 0.96, 0.04, 0.04]
    Placement['Characterization']['Figure1'] = [0.75, 0.1275, 0.5, 0.7, 5, 3.6, 125]
    Placement['Characterization']['Toolbar1'] = [0.815, 0.825, 0.2, 0.05]

    # -- Optimization
    Placement['Optimization']['LabelSelModel'] = [0, 0.05, 0.1, 0.035]
    Placement['Optimization']['ComboSelModel'] = [0.1, 0.0475, 0.125, 0.035]
    Placement['Optimization']['LabelRev'] = [0.29, 0.05]
    Placement['Optimization']['ComboRev'] = [0.4, 0.0475, 0.125, 0.035]
    Placement['Optimization']['LabelIrrev'] = [0.58, 0.05]
    Placement['Optimization']['ComboIrrev'] = [0.69, 0.0475, 0.125, 0.035]
    Placement['Optimization']['Sheet1'] = [0.245, 0.2, 0.47, 0.7, 0.1275, 0.1, 0.1525, 0.1525, 0.1525, 0.155, 0.135]
    Placement['Optimization']['Sheet2'] = [0.745, 0.2, 0.47, 0.7, 0.1275, 0.1, 0.1525, 0.1525, 0.1525, 0.155, 0.135]
    Placement['Optimization']['LabelVE'] = [0.29, 0.11]
    Placement['Optimization']['ComboVE'] = [0.41, 0.105, 0.1, 0.035]
    Placement['Optimization']['LabelVP'] = [0.58, 0.11]
    Placement['Optimization']['ComboVP'] = [0.70, 0.105, 0.1, 0.035]
    Placement['Optimization']['LabelBnd'] = [0.87, 0.05]
    Placement['Optimization']['Slider1'] = [0.87, 0.11, 0.1]
    Placement['Optimization']['ButtonLoad'] = [startx + delx*0, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonModLib'] = [startx + delx*1, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonOpt'] = [startx + delx*2, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonRes'] = [startx + delx*3, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonSaveMod'] = [startx + delx*4, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonView'] = [startx + delx*5, 0.98, 0.1, 0.05]
    Placement['Optimization']['ButtonNote'] = [0.1, 0.12, 0.1, 0.05]
    Placement['Optimization']['NotesLabel'] = [0.5, 0.1]
    Placement['Optimization']['NotesArea'] = [0.5, 0.5, 0.8, 0.6]
    Placement['Optimization']['HistLabel'] = [0.5, 0.02]
    Placement['Optimization']['HistSheetRun'] = [0.025, 0.1, 0.45, 0.85, 0.33, 0.3, 0.3, 0.02]
    Placement['Optimization']['ScrollHistSheetRun'] = [0.6, 0.1, 0.02, 0.85]
    Placement['Optimization']['HistSheetPar'] = [0.9675, 0.1, 0.4525, 0.4, 0.315, 0.3, 0.315]
    Placement['Optimization']['HistSheetTest'] = [0.9675, 0.55, 0.4525, 0.4, 0.28, 0.27, 0.22, 0.17]
    Placement['Optimization']['ModLibSheet'] = [0.5, 0.05, 0.95, 0.95, 0.2, .125, 0.25, 0.25, 0.125]
    Placement['Optimization']['ModLibNotesLabel'] = [0.5, 0.075]
    Placement['Optimization']['ModLibNotesArea'] = [0.5, 0.15, 0.8, 0.8]
    Placement['Optimization']['LabelGlobalErr'] = [startx + delx*7, 0.98]
    
    # -- Analysis
    Placement['Analysis']['LabelSelModel'] = [0, 0.05, 0.1, 0.035]
    Placement['Analysis']['ComboSelModel'] = [0.1, 0.0475, 0.125, 0.035]
    Placement['Analysis']['LabelRev'] = [0.29, 0.05]
    Placement['Analysis']['ComboRev'] = [0.4, 0.0475, 0.125, 0.035]
    Placement['Analysis']['LabelIrrev'] = [0.58, 0.05]
    Placement['Analysis']['ComboIrrev'] = [0.69, 0.0475, 0.125, 0.035]
    Placement['Analysis']['Sheet1'] = [0.31, 0.2, 0.3, 0.7, 0.3, 0.3, 0.33]
    Placement['Analysis']['Sheet2'] = [0.675, 0.2, 0.3, 0.7, 0.3, 0.3, 0.33]
    Placement['Analysis']['LabelVE'] = [0.29, 0.11]
    Placement['Analysis']['ComboVE'] = [0.41, 0.105, 0.1, 0.035]
    Placement['Analysis']['LabelVP'] = [0.58, 0.11]
    Placement['Analysis']['ComboVP'] = [0.70, 0.105, 0.1, 0.035]
    Placement['Analysis']['ButtonLoad'] = [startx + delx*0, 0.98, 0.1, 0.04]
    Placement['Analysis']['ButtonModLib'] = [startx + delx*1, 0.98, 0.1, 0.04]
    Placement['Analysis']['ButtonAnaly'] = [startx + delx*2, 0.98, 0.1, 0.04]
    Placement['Analysis']['ButtonSaveMod'] = [startx + delx*3, 0.98, 0.1, 0.04]
    Placement['Analysis']['ButtonView'] = [startx + delx*4, 0.98, 0.1, 0.04]
    Placement['Analysis']['ButtonNote'] = [0.1, 0.12, 0.075, 0.04]
    Placement['Analysis']['NotesLabel'] = [0.5, 0.1]
    Placement['Analysis']['NotesArea'] = [0.5, 0.5, 0.8, 0.6]
    Placement['Analysis']['HistLabel'] = [0.5, 0.02]
    Placement['Analysis']['HistSheetRun'] = [0.025, 0.1, 0.45, 0.85, 0.33, 0.3, 0.3, 0.02]
    Placement['Analysis']['ScrollHistSheetRun'] = [0.6, 0.1, 0.02, 0.85]
    Placement['Analysis']['HistSheetPar'] = [0.9675, 0.1, 0.4525, 0.4, 0.315, 0.3, 0.315]
    Placement['Analysis']['HistSheetTest'] = [0.9675, 0.55, 0.4525, 0.4, 0.28, 0.27, 0.22, 0.17]
    Placement['Analysis']['ModLibSheet'] = [0.5, 0.05, 0.95, 0.95, 0.2, .125, 0.25, 0.25, 0.125]
    Placement['Analysis']['ModLibNotesLabel'] = [0.5, 0.075]
    Placement['Analysis']['ModLibNotesArea'] = [0.5, 0.15, 0.8, 0.8]

    # -- Visualization
    Placement['Visualization']['ComboX'] = [0.4975, 0.15, 0.1, 0.03]
    Placement['Visualization']['ComboY'] = [0.835, 0.15, 0.1, 0.03]
    Placement['Visualization']['ButtonPlot'] = [0.665, 0.05, 0.05, 0.04]
    Placement['Visualization']['ComboPlot'] = [0.665, 0.15, 0.1, 0.03]
    Placement['Visualization']['LabelRaw'] = [0.4975, 0.2]
    Placement['Visualization']['LabelPred'] = [0.835, 0.2]
    Placement['Visualization']['LabelChar'] = [0, 0.05]
    Placement['Visualization']['SheetChar'] = [0, 0.085, 0.3, 0.415, 0.05, 0.325, 0.22, 0.185, 0.18]
    Placement['Visualization']['LabelVer'] = [0.0, 0.5]
    Placement['Visualization']['SheetVer'] = [0.0, 0.535, 0.3, 0.415, 0.05, 0.4, 0.27, 0.24]
    Placement['Visualization']['Figure1'] = [0.475, 0.224, 0.3, 0.6, 4.25, 4, 125]
    Placement['Visualization']['Toolbar1'] = [0.507, 0.825, 0.268, 0.05]
    Placement['Visualization']['Figure2'] = [0.8125, 0.224, 0.3, 0.6, 4.25, 4, 125]
    Placement['Visualization']['Toolbar2'] = [0.8445, 0.825, 0.268, 0.05]

    # -- Export
    Placement['Export']['LabelOpts'] = [0.025, 0.01]
    Placement['Export']['Check1'] = [0.025, 0.045]
    Placement['Export']['Check2'] = [0.025, 0.08]
    Placement['Export']['Check3'] = [0.025, 0.115]
    Placement['Export']['Check4'] = [0.025, 0.15]
    Placement['Export']['Check5'] = [0.025, 0.185]
    Placement['Export']['ButtonExp'] = [0.025, 0.25, 0.06, 0.0325]

    # -- Settings
    Placement['Settings']['LabelComp'] = [0.025, 0.1]
    Placement['Settings']['ButtonComp'] = [0.025, 0.125, 0.06, 0.0325]
    Placement['Settings']['LabelMod'] = [0.025, 0.2]
    Placement['Settings']['ButtonMod'] = [0.025, 0.225, 0.06, 0.0325]
    Placement['Settings']['LabelImp'] = [0.025, 0.3]
    Placement['Settings']['ButtonImp'] = [0.025, 0.325, 0.06, 0.0325]
    Placement['Settings']['ButtonImpD'] = [0.1, 0.325, 0.06, 0.0325]
    Placement['Settings']['LabelExp'] = [0.025, 0.4]
    Placement['Settings']['ButtonExp'] = [0.025, 0.425, 0.06, 0.0325]
    Placement['Settings']['ButtonExpD'] = [0.1, 0.425, 0.06, 0.0325]

    # -- Gateway
    Placement['Gateway']['MainFrame'] = [0.5, 0.5, 0.25, 0.35]
    Placement['Gateway']['ButtonImp'] = [0.5, 0.35, 0.65, 0.15]
    Placement['Gateway']['ButtonExp'] = [0.5, 0.65, 0.65, 0.15]
    Placement['Gateway']['SearchFrame'] = [0.005, 0.125, 0.45, 0.7]
    Placement['Gateway']['SearchCanvas'] = [0.5, 0.001, 0.99, 0.99]
    Placement['Gateway']['SearchCanvasScroll'] = [1, 0.001, 1]
    Placement['Gateway']['ButtonSearch'] = [0.25, 0.9, 0.08, 0.05]
    Placement['Gateway']['ResFrame'] = [0.505, 0.125, 0.45, 0.7]
    Placement['Gateway']['ResSheet'] = [0.5, 0.005, 0.9, 0.9, 0.24, 0.24, 0.18, 0.24, 0.04]
    Placement['Gateway']['ButtonResExp'] = [0.75, 0.9, 0.08, 0.05]
    Placement['Gateway']['ButtonBack'] = [0.005, 0.005, 0.04, 0.04]
    Placement['Gateway']['ExpSheet'] = [0.005, 0.125, 0.475, 0.7, 0.3, 0.65]
    Placement['Gateway']['ButtonImpMod'] = [0.5, 0.9, 0.08, 0.05]
    Placement['Gateway']['TestSheet'] = [0.505, 0.125, 0.475, 0.7, 0.19, 0.19, 0.19, 0.19, 0.19]
    
    # Set to self
    self.Placement = Placement

    return