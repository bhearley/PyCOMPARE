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


    else:
        Placements(self, "1536x960")


    # Set to self
    self.Placement = Placement

    return