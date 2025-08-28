def WriteDSG_GVIPS_TISO_OPT(self, temp_dir):
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # PURPOSE: Write the DGS Input file for compare for Isototropic 
    #
    # INPUTS:
    #   self        GUI data structure
    #   temp_dir    Temporary Direcotry
    # OUTPUTS:
    #   Param       List of parameter names
    #   Param_U     List of parameter units
    #   Param_N     List of parameter numbers
    #   P_Elas      List of elastic parameter values
    #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Import modules
    import os

    # Import functions
    from Model.UnitConversion import UnitConversion

    # Create the DGS file
    fname_dgs = os.path.join(temp_dir,'comp.dsg')
    file = open(fname_dgs, "w") 
    file.write("$ This is the file to run compare\n")
    
    # Write the number of tests
    file.write("EXPR:\n")
    line = ' ' + str(len(self.Compare['Characterization'].keys()))
    for i in range(len(self.Compare['Characterization'].keys())):
        line = line + '  ' + str(i+1)
    line = line + '\n'
    file.write(line)

    # Write the number of parameters
    file.write("NDV:\n")
    NDV = 9*int(self.Compare['Model']['N'])
    file.write(' ' + str(NDV)+ '\n')
    Param = []   # Initialize parameter list
    Param_V = [] # Initialize list of parameter values
    Param_U = [] # Initialize list of parameter units
    Param_N = [] # Initialize list of parameter number
    PN = 1

    # Write the Parameter Values
    file.write("INIT:\n")

    # -- Get elastic parameters
    VE = []
    for i in range(len(self.Compare['Model']['VE_Param'])):
        VE.append(self.Compare['Model']['VE_Param'][i][0])

    # -- Save EL
    P_Elas = []
    val = float(self.Compare['Model']['VE_Param'][VE.index('EL')][3])
    unit = self.Compare['Model']['VE_Param'][VE.index('EL')][1]
    val = UnitConversion(unit, val, 'MPa')
    P_Elas.append(val)

    # -- Save ET
    val = float(self.Compare['Model']['VE_Param'][VE.index('ET')][3])
    unit = self.Compare['Model']['VE_Param'][VE.index('ET')][1]
    val = UnitConversion(unit, val, 'MPa')
    P_Elas.append(val)

    # -- Save vL
    val = float(self.Compare['Model']['VE_Param'][VE.index('νL')][3])
    P_Elas.append(val)

    # -- Save GL
    val = float(self.Compare['Model']['VE_Param'][VE.index('GL')][3])
    unit = self.Compare['Model']['VE_Param'][VE.index('GL')][1]
    val = UnitConversion(unit, val, 'MPa')
    P_Elas.append(val)

    # -- Get the list of viscoplastic parameters

    line = ' '

    VP = []
    for i in range(len(self.Compare['Model']['VP_Param'])):
        VP.append(self.Compare['Model']['VP_Param'][i][0])

    # -- Write κ
    val = float(self.Compare['Model']['VP_Param'][VP.index('κ')][3])
    unit = self.Compare['Model']['VP_Param'][VP.index('κ')][1]
    val = UnitConversion(unit, val, 'MPa')
    line = line + ' ' + str(val)
    Param.append('κ')
    Param_V.append(val)
    Param_U.append('MPa')
    Param_N.append(PN)
    PN = PN+1

    # -- Write n
    val = float(self.Compare['Model']['VP_Param'][VP.index('n')][3])
    line = line + ' ' + str(val)
    Param.append('n')
    Param_V.append(val)
    Param_U.append('')
    Param_N.append(PN)
    PN = PN+1

    # -- Write μ
    val = float(self.Compare['Model']['VP_Param'][VP.index('μ')][3])
    unit = self.Compare['Model']['VP_Param'][VP.index('μ')][1]
    val = UnitConversion(unit, val, 'MPa-s')
    line = line + ' ' + str(val)
    Param.append('μ')
    Param_V.append(val)
    Param_U.append('MPa-s')
    Param_N.append(PN)
    PN = PN+1

    # -- Write m
    for i in range(int(self.Compare['Model']['N'])):
        val = float(self.Compare['Model']['VP_Param'][VP.index('m' + str(i+1))][3])
        line = line + ' ' + str(val)
        Param.append('m' + str(i+1))
        Param_V.append(val)
        Param_U.append('')
        Param_N.append(PN)
        PN = PN+1

    # -- Write β
    for i in range(int(self.Compare['Model']['N'])):
        val = float(self.Compare['Model']['VP_Param'][VP.index('β' + str(i+1))][3])
        line = line + ' ' + str(val)
        Param.append('β' + str(i+1))
        Param_V.append(val)
        Param_U.append('')
        Param_N.append(PN)
        PN = PN+1

    # -- Write R
    for i in range(int(self.Compare['Model']['N'])):
        val = float(self.Compare['Model']['VP_Param'][VP.index('R' + str(i+1))][3])
        unit = self.Compare['Model']['VP_Param'][VP.index('R' + str(i+1))][1]
        val = UnitConversion(unit, val, '1/s')
        line = line + ' ' + str(val)
        Param.append('R' + str(i+1))
        Param_V.append(val)
        Param_U.append('1/s')
        Param_N.append(PN)
        PN = PN+1

    # -- Write H
    for i in range(int(self.Compare['Model']['N'])):
        val = float(self.Compare['Model']['VP_Param'][VP.index('H' + str(i+1))][3])
        unit = self.Compare['Model']['VP_Param'][VP.index('H' + str(i+1))][1]
        val = UnitConversion(unit, val, 'MPa')
        line = line + ' ' + str(val)
        Param.append('H' + str(i+1))
        Param_V.append(val)
        Param_U.append('MPa')
        Param_N.append(PN)
        PN = PN+1

    # -- Write ξ
    val = float(self.Compare['Model']['VP_Param'][VP.index('ξ')][3])
    line = line + ' ' + str(val)
    Param.append('ξ')
    Param_V.append(val)
    Param_U.append('')
    Param_N.append(PN)
    PN = PN+1

    # -- Write ζ
    val = float(self.Compare['Model']['VP_Param'][VP.index('ζ')][3])
    line = line + ' ' + str(val)
    Param.append('ζ')
    Param_V.append(val)
    Param_U.append('')
    Param_N.append(PN)
    PN = PN+1

    # -- Write line to file
    line = line + '\n'
    file.write(line)

    # Write Lower Bound
    ACT = []
    file.write("LOWE:\n")
    line = ' '
    for i in range(len(Param_V)):
        val = Param_V[i]
        if i < len(Param):
            P = Param[i]
            if P in VP:
                if self.Compare['Model']['VP_Param'][VP.index(P)][5] == 'Active':
                    ACT.append(i+1)
                    val = self.Compare['Model']['VP_Param'][VP.index(P)][2]
                    unit = self.Compare['Model']['VP_Param'][VP.index(P)][1]
                    try:
                        val = UnitConversion(unit, val, Param_U[i])
                    except:
                        pass

        line = line + ' ' + str(val)
    line = line + '\n'
    file.write(line)

    # Write Upper Bound
    file.write("UPPE:\n")
    line = ' '
    for i in range(len(Param_V)):
        val = Param_V[i]
        if i < len(Param):
            P = Param[i]
            if P in VP:
                if self.Compare['Model']['VP_Param'][VP.index(P)][5] == 'Active':
                    val = self.Compare['Model']['VP_Param'][VP.index(P)][4]
                    unit = self.Compare['Model']['VP_Param'][VP.index(P)][1]
                    try:
                        val = UnitConversion(unit, val, Param_U[i])
                    except:
                        pass

        line = line + ' ' + str(val)
    line = line + '\n'
    file.write(line)

    # Write active parameters
    file.write("SUBP:\n")
    line = ' 1 ' + str(len(ACT))
    for i in ACT:
        line = line + ' ' + str(i)
    line = line + '\n'
    file.write(line)
    file.write(' 0 0\n')

    # Write LINK
    file.write("LINK:\n")
    for i in range(len(self.Compare['Characterization'].keys())):
        line = ' ' + str(i+1) + ' ' + str(NDV)
        for j in range(NDV):
            line = line + ' ' + str(j+1)
        line = line + '\n'
        file.write(line)

    # Write FACT
    file.write("FACT:\n")
    for i in range(len(self.Compare['Characterization'].keys())):
        line = ' ' + str(i+1) +  ' ' + str(NDV) + ' '
        for j in range(NDV):
            line = line + ' ' + str(1.0)
        line = line + '\n'
        file.write(line)

    # Write Weights
    weights = []
    for key in self.Compare['Characterization'].keys():
        weights.append(self.Compare['Characterization'][key]['RelWeight'])
    tot = sum(weights)
    for i in range(len(weights)):
        weights[i] = weights[i]/tot

    file.write("MDO:\n")
    line = ' '
    for i in range(len(weights)):
        line = line + ' ' + str(weights[i])
    line = line + '\n'
    file.write(line)

    # Write OBJS
    file.write("OBJS:\n")
    line = ' '
    for i in range(len(weights)):
        line = line + ' ' + str(1.0)
    line = line + '\n'
    file.write(line)

    # Write ERR
    file.write("ERR:\n")
    file.write("  2\n")

    # Close the file
    file.close()

    # Set all Parameters
    P = Param 

    return P, Param_U, Param_N, P_Elas
