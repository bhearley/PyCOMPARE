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
                'Characterization':{}
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
        Placement['Characterization']['Button4'] = [0.725, 0.9, 12]
        Placement['Characterization']['Sheet3'] = [0.5, 0.4, 220, 400, 12, 100, 100]
        Placement['Characterization']['Button5'] = [0.5, 0.9, 12]




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
        Placement['Characterization']['Button4'] = [0.725, 0.9, 12]
        Placement['Characterization']['Sheet3'] = [0.5, 0.4, 220, 400, 12, 100, 100]
        Placement['Characterization']['Button5'] = [0.5, 0.9, 12]


    else:
        Placements(self, "1536x960")


    # Set to self
    self.Placement = Placement

    return