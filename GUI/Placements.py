#-----------------------------------------------------------------------------------------
#
#   Placements.py
#
#   PURPOSE: Get the coordinates and size of each widget based on screen size
#
#   INPUTS:
#       self    structure containing all GUI information
#-----------------------------------------------------------------------------------------
def Placements(self, res):
    # Initialize Placement
    Placement = {
                'HomePage':{},
                'General':{},
                'Data':{},
                'Characterization':{},
                'Optimization':{},
                'Analysis':{},
                'Visualization':{}
                }
    
    # 2560 x 1440
    if res == "2560x1440":
        # -- Home Page
        Placement['HomePage']['Title'] = [0.5, 0.005, 0.9]
        Placement['HomePage']['Logo'] = [0.999, 0.045, 0.8]
        Placement['HomePage']['Frame1'] = [0.5, 0.5, 3, 400, 300]
        Placement['HomePage']['Button1'] = [0.5, 0.25, 18]
        Placement['HomePage']['Button2'] = [0.5, 0.75, 18]

        # -- General Page
        startx = 0.003
        delx = 0.1425
        starty = 0.13
        btnw = 25

        Placement['General']['Button1'] = [startx+delx*0, starty, btnw]
        Placement['General']['Button2'] = [startx+delx*1, starty, btnw]
        Placement['General']['Button3'] = [startx+delx*2, starty, btnw]
        Placement['General']['Button4'] = [startx+delx*3, starty, btnw]
        Placement['General']['Button5'] = [startx+delx*4, starty, btnw]
        Placement['General']['Button6'] = [startx+delx*5, starty, btnw]
        Placement['General']['Button7'] = [startx+delx*6, starty, btnw]
        Placement['General']['Button8'] = [startx, 0.975, 10]

        # -- Data
        Placement['Data']['Combo1'] = [0.685, 0.275]
        Placement['Data']['Label1'] = [0.735, 0.275]
        Placement['Data']['Combo2'] = [0.785, 0.275]
        Placement['Data']['Button1'] = [0.855, 0.27, 6]
        Placement['Data']['Label2'] = [startx, 0.60]
        Placement['Data']['Sheet1'] = [startx, 0.63, 700, 400, 12, 110, 90, 90, 130, 130, 105]
        Placement['Data']['Combo3'] = [0.765, 0.275]
        Placement['Data']['Sheet2'] = [startx, 0.225, 700, 450, 12, 25, 90, 80, 90, 90, 90, 100, 90]
        Placement['Data']['Button2'] = [startx + delx*0, 0.18, btnw]
        Placement['Data']['Button3'] = [startx + delx*1, 0.18, btnw]
        Placement['Data']['Figure1'] = [0.75, 0.32, 7, 5, 125]
        Placement['Data']['Toolbar1'] = [0.765, 0.8]

        # -- Characterization
        Placement['Characterization']['Combo1'] = [0.685, 0.275]
        Placement['Characterization']['Label1'] = [0.735, 0.275]
        Placement['Characterization']['Combo2'] = [0.785, 0.275]
        Placement['Characterization']['Button1'] = [0.855, 0.27, 6]
        Placement['Characterization']['Label2'] = [startx, 0.60]
        Placement['Characterization']['Sheet1'] = [startx, 0.63, 700, 400, 12, 110, 90, 90, 130, 130, 105]
        Placement['Characterization']['Combo3'] = [0.765, 0.275]
        Placement['Characterization']['Label3'] = [startx, 0.22]
        Placement['Characterization']['Sheet2'] = [startx, 0.245, 730, 450, 12, 90, 80, 90, 90, 90, 100, 90, 70]
        Placement['Characterization']['Button2'] = [0.765, 0.85, 18]
        Placement['Characterization']['Sheet3'] = [0.5, 0.4, 220, 400, 12, 100, 100]
        Placement['Characterization']['Button3'] = [0.5, 0.9, 18]
        Placement['Characterization']['Button4'] = [0.74, 0.9, 8]
        Placement['Characterization']['Button5'] = [0.79, 0.9, 8]

        # -- Optimization
        Placement['Optimization']['Label1'] = [0.265, 0.205]
        Placement['Optimization']['Combo1'] = [0.39, 0.205]
        Placement['Optimization']['Label2'] = [0.615, 0.205]
        Placement['Optimization']['Combo2'] = [0.74, 0.205]
        Placement['Optimization']['Sheet1'] = [0.325, 0.33, 750, 700, 12, 90, 65, 110, 110, 110, 120, 95]
        Placement['Optimization']['Sheet2'] = [0.675, 0.33, 750, 700, 12, 90, 65, 110, 110, 110, 120, 95]
        Placement['Optimization']['Label3'] = [0.265, 0.25]
        Placement['Optimization']['Combo3'] = [0.39, 0.25]
        Placement['Optimization']['Label4'] = [0.615, 0.25]
        Placement['Optimization']['Combo4'] = [0.74, 0.25]
        Placement['Optimization']['Label5'] = [0.925, 0.205]
        Placement['Optimization']['Slider1'] = [0.925, 0.25, 250]
        Placement['Optimization']['Button1'] = [startx + delx*0, 0.925, btnw]
        Placement['Optimization']['Button2'] = [startx + delx*1, 0.925, btnw]
        Placement['Optimization']['Button3'] = [startx + delx*2, 0.925, btnw]
        Placement['Optimization']['Button4'] = [startx + delx*3, 0.925, btnw]
        Placement['Optimization']['Button5'] = [0.024, 0.275, 12]
        Placement['Optimization']['Label6'] = [0.05, 0.205]
        Placement['Optimization']['Combo5'] = [0.125, 0.205]

        # -- Analysis
        Placement['Analysis']['Label1'] = [0.265, 0.205]
        Placement['Analysis']['Combo1'] = [0.39, 0.205]
        Placement['Analysis']['Label2'] = [0.615, 0.205]
        Placement['Analysis']['Combo2'] = [0.74, 0.205]
        Placement['Analysis']['Sheet1'] = [0.325, 0.33, 300, 600, 12, 90, 90, 100]
        Placement['Analysis']['Sheet2'] = [0.675, 0.33, 300, 600, 12, 90, 90, 100]
        Placement['Analysis']['Label3'] = [0.265, 0.25]
        Placement['Analysis']['Combo3'] = [0.39, 0.25]
        Placement['Analysis']['Label4'] = [0.615, 0.25]
        Placement['Analysis']['Combo4'] = [0.74, 0.25]
        Placement['Analysis']['Button1'] = [startx + delx*0, 0.925, btnw]
        Placement['Analysis']['Button2'] = [startx + delx*1, 0.925, btnw]
        Placement['Analysis']['Button3'] = [startx + delx*2, 0.925, btnw]
        Placement['Analysis']['Button4'] = [startx + delx*3, 0.925, btnw]
        Placement['Analysis']['Button5'] = [0.024, 0.275, 12]
        Placement['Analysis']['Label6'] = [0.05, 0.205]
        Placement['Analysis']['Combo5'] = [0.125, 0.205]

        # -- Visuzalization
        Placement['Visualization']['Combo1'] = [0.685, 0.275]
        Placement['Visualization']['Label1'] = [0.735, 0.275]
        Placement['Visualization']['Combo2'] = [0.785, 0.275]
        Placement['Visualization']['Button1'] = [0.855, 0.27, 6]
        Placement['Visualization']['Label2'] = [0.08, 0.21]
        Placement['Visualization']['Sheet1'] = [0.2, 0.245, 800, 270, 12, 90, 80, 90, 90, 90, 100, 90, 70, 70]
        Placement['Visualization']['Label3'] = [0.08, 0.595]
        Placement['Visualization']['Sheet2'] = [0.195, 0.63, 730, 240, 12, 90, 80, 90, 90, 90, 100, 90, 70]
        Placement['Visualization']['Figure1'] = [0.75, 0.32, 7, 5, 125]
        Placement['Visualization']['Toolbar1'] = [0.765, 0.8]

    # 1536 x 960
    if res == "1536x960":
        # -- Home Page
        Placement['HomePage']['Title'] = [0.5, 0.005, 0.9]
        Placement['HomePage']['Logo'] = [0.999, 0.045, 0.8]
        Placement['HomePage']['Frame1'] = [0.5, 0.5, 3, 400, 300]
        Placement['HomePage']['Button1'] = [0.5, 0.25, 18]
        Placement['HomePage']['Button2'] = [0.5, 0.75, 18]

        # -- General Page
        startx = 0.0045
        delx = 0.1425
        starty = 0.13
        btnw = 14

        Placement['General']['Button1'] = [startx+delx*0, starty, btnw]
        Placement['General']['Button2'] = [startx+delx*1, starty, btnw]
        Placement['General']['Button3'] = [startx+delx*2, starty, btnw]
        Placement['General']['Button4'] = [startx+delx*3, starty, btnw]
        Placement['General']['Button5'] = [startx+delx*4, starty, btnw]
        Placement['General']['Button6'] = [startx+delx*5, starty, btnw]
        Placement['General']['Button7'] = [startx+delx*6, starty, btnw]
        Placement['General']['Button8'] = [startx, 0.965, 10]

        # -- Data
        Placement['Data']['Combo1'] = [0.67, 0.275]
        Placement['Data']['Label1'] = [0.735, 0.275]
        Placement['Data']['Combo2'] = [0.8, 0.275]
        Placement['Data']['Button1'] = [0.9, 0.265, 6]
        Placement['Data']['Label2'] = [startx, 0.59]
        Placement['Data']['Sheet1'] = [startx, 0.63, 700, 240, 12, 110, 90, 90, 130, 130, 105]
        Placement['Data']['Combo3'] = [0.765, 0.275]
        Placement['Data']['Sheet2'] = [startx, 0.25, 700, 270, 12, 25, 90, 80, 90, 90, 90, 100, 90]
        Placement['Data']['Button2'] = [startx + delx*0, 0.21, 20]
        Placement['Data']['Button3'] = [startx + delx*1 + 0.05, 0.21, 20]
        Placement['Data']['Figure1'] = [0.75, 0.37, 5, 3.6, 125]
        Placement['Data']['Toolbar1'] = [0.765, 0.85]

        # -- Characterization
        Placement['Characterization']['Combo1'] = [0.67, 0.275]
        Placement['Characterization']['Label1'] = [0.735, 0.275]
        Placement['Characterization']['Combo2'] = [0.8, 0.275]
        Placement['Characterization']['Button1'] = [0.9, 0.265, 6]
        Placement['Characterization']['Label2'] = [startx, 0.59]
        Placement['Characterization']['Sheet1'] = [startx, 0.63, 700, 240, 12, 110, 90, 90, 130, 130, 105]
        Placement['Characterization']['Combo3'] = [0.765, 0.275]
        Placement['Characterization']['Label3'] = [startx, 0.22]
        Placement['Characterization']['Sheet2'] = [startx, 0.245, 730, 270, 12, 90, 80, 90, 90, 90, 100, 90, 70]
        Placement['Characterization']['Button2'] = [0.765, 0.9, 12]
        Placement['Characterization']['Sheet3'] = [0.5, 0.4, 220, 400, 12, 100, 100]
        Placement['Characterization']['Button3'] = [0.5, 0.9, 18]
        Placement['Characterization']['Button4'] = [0.74, 0.96, 8]
        Placement['Characterization']['Button5'] = [0.79, 0.96, 8]

        # -- Optimization
        Placement['Optimization']['Label1'] = [0.28, 0.205]
        Placement['Optimization']['Combo1'] = [0.42, 0.205]
        Placement['Optimization']['Label2'] = [0.6, 0.205]
        Placement['Optimization']['Combo2'] = [0.74, 0.205]
        Placement['Optimization']['Sheet1'] = [0.255, 0.33, 750, 400, 12, 90, 65, 110, 110, 110, 120, 95]
        Placement['Optimization']['Sheet2'] = [0.75, 0.33, 750, 400, 12, 90, 65, 110, 110, 110, 120, 95]
        Placement['Optimization']['Label3'] = [0.28, 0.2725]
        Placement['Optimization']['Combo3'] = [0.42, 0.2725]
        Placement['Optimization']['Label4'] = [0.6, 0.2725]
        Placement['Optimization']['Combo4'] = [0.74, 0.2725]
        Placement['Optimization']['Label5'] = [0.9, 0.205]
        Placement['Optimization']['Slider1'] = [0.9, 0.28, 250]
        Placement['Optimization']['Button1'] = [startx + delx*0, 0.8825, btnw]
        Placement['Optimization']['Button2'] = [startx + delx*1, 0.8825, btnw]
        Placement['Optimization']['Button3'] = [startx + delx*2, 0.8825, btnw]
        Placement['Optimization']['Button4'] = [startx + delx*3, 0.8825, btnw]
        Placement['Optimization']['Button5'] = [0.0125, 0.28, 12]
        Placement['Optimization']['Label6'] = [0.055, 0.205]
        Placement['Optimization']['Combo5'] = [0.16, 0.205]

        # -- Analysis
        Placement['Analysis']['Label1'] = [0.28, 0.205]
        Placement['Analysis']['Combo1'] = [0.42, 0.205]
        Placement['Analysis']['Label2'] = [0.6, 0.205]
        Placement['Analysis']['Combo2'] = [0.74, 0.205]
        Placement['Analysis']['Sheet1'] = [0.35, 0.33, 300, 400, 12, 90, 90, 100]
        Placement['Analysis']['Sheet2'] = [0.675, 0.33, 300, 500, 12, 90, 90, 100]
        Placement['Analysis']['Label3'] = [0.28, 0.2725]
        Placement['Analysis']['Combo3'] = [0.42, 0.2725]
        Placement['Analysis']['Label4'] = [0.6, 0.2725]
        Placement['Analysis']['Combo4'] = [0.74, 0.2725]
        Placement['Analysis']['Label5'] = [0.9, 0.205]
        Placement['Analysis']['Slider1'] = [0.9, 0.28, 250]
        Placement['Analysis']['Button1'] = [startx + delx*0, 0.8825, btnw]
        Placement['Analysis']['Button2'] = [startx + delx*1, 0.8825, btnw]
        Placement['Analysis']['Button3'] = [startx + delx*2, 0.8825, btnw]
        Placement['Analysis']['Button4'] = [startx + delx*3, 0.8825, btnw]
        Placement['Analysis']['Button5'] = [0.0125, 0.28, 12]
        Placement['Analysis']['Label6'] = [0.055, 0.205]
        Placement['Analysis']['Combo5'] = [0.16, 0.205]

        # -- Visualization
        Placement['Visualization']['Combo1'] = [0.67, 0.275]
        Placement['Visualization']['Label1'] = [0.735, 0.275]
        Placement['Visualization']['Combo2'] = [0.8, 0.275]
        Placement['Visualization']['Button1'] = [0.9, 0.265, 6]
        Placement['Visualization']['Label2'] = [0.0725, 0.21]
        Placement['Visualization']['Sheet1'] = [0.274, 0.245, 800, 270, 12, 90, 80, 90, 90, 90, 100, 90, 70, 70]
        Placement['Visualization']['Label3'] = [0.06, 0.595]
        Placement['Visualization']['Sheet2'] = [0.2525, 0.63, 730, 240, 12, 90, 80, 90, 90, 90, 100, 90, 70]
        Placement['Visualization']['Figure1'] = [0.75, 0.37, 5, 3.6, 125]
        Placement['Visualization']['Toolbar1'] = [0.765, 0.85]


    else:
        Placements(self, "1536x960")


    # Set to self
    self.Placement = Placement

    return