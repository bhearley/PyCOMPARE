#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# WriteDGS_GVIPS_ANLY.py
#
# PURPOSE: Write the DGS Input file for compare for 4 different model types for Optimization:
#   - Isotropic No Damage (_IN)
#   - Isotropic With Damage (_ID)
#   - Anisotropic No Damage (_AN)
#   - Anisotropic No Damage (_AD)
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def WriteDSG_GVIPS_ANLY_IN(self, temp_dir, tests):
    #----------------------------------------------------------------------------------------------------------------------------------------------------------------
    #
    # PURPOSE: Write the DGS Input file for compare for Isototropic with No Damate
    #
    # INPUTS:
    #   self        GUI data structure
    #   temp_dir    Temporary Direcotry
    # OUTPUTS:
    #   mod         Model Number
    #   Param       List of parameter names
    #   Param_U     List of parameter units
    #   Param_N     List of parameter numbers
    #
    #-----------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Import modules
    import os

    # Import functions
    from UnitConversion.UnitConversion import UnitConversion

    # Set the model number
    mod = 10

    # Create the DGS file
    fname_dgs = os.path.join(temp_dir,'comp.dsg')
    file = open(fname_dgs, "w") 
    file.write("$ This is the file to run compare\n")
    
    # Write the number of tests
    file.write("EXPR:\n")
    line = ' ' + str(len(tests))
    for i in range(len(tests)):
        line = line + '  ' + str(i+1)
    line = line + '\n'
    file.write(line)

    # Write the number of parameters
    file.write("NDV:\n")
    NDV = 2 + 2*int(self.Compare['Model']['M']) + 12 + 9*int(self.Compare['Model']['N'])
    file.write(' ' + str(NDV)+ '\n')
    Param = []   # Initialize parameter list
    Param_V = [] # Initialize list of parameter values
    Param_U = [] # Initialize list of parameter units
    Param_N = [] # Initialize list of parameter number
    PN = 1

    # Write the Parameter Values
    file.write("INIT:\n")
    # -- Get the list of viscoelastic parameters
    VE = []
    for i in range(len(self.Compare['Analysis']['VE_Param'])):
        VE.append(self.Compare['Analysis']['VE_Param'][i][0])

    line = ' '
    # -- Write E
    val = float(self.Compare['Analysis']['VE_Param'][VE.index('E')][2])
    unit = self.Compare['Analysis']['VE_Param'][VE.index('E')][1]
    val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
    line = line + ' ' + str(val)
    Param.append('E')
    Param_V.append(val)
    Param_U.append('MPa')
    Param_N.append(PN)
    PN = PN+1

    # -- Write ν
    val = float(self.Compare['Analysis']['VE_Param'][VE.index('ν')][2])
    line = line + ' ' + str(val)
    Param.append('ν')
    Param_V.append(val)
    Param_U.append('')
    Param_N.append(PN)
    PN = PN+1

    # -- Write M
    for i in range(int(self.Compare['Analysis']['M'])):
        val = float(self.Compare['Analysis']['VE_Param'][VE.index('M' + str(i+1))][2])
        unit = self.Compare['Analysis']['VE_Param'][VE.index('M' + str(i+1))][1]
        val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
        line = line + ' ' + str(val)
        Param.append('M' + str(i+1))
        Param_V.append(val)
        Param_U.append('MPa')
        Param_N.append(PN)
        PN = PN+1

    # -- Write ρ
    for i in range(int(self.Compare['Analysis']['M'])):
        val = float(self.Compare['Analysis']['VE_Param'][VE.index('ρ' + str(i+1))][2])
        unit = self.Compare['Analysis']['VE_Param'][VE.index('ρ' + str(i+1))][1]
        val = UnitConversion(unit, val, 's', os.path.join(os.getcwd()))
        line = line + ' ' + str(val)
        Param.append('ρ' + str(i+1))
        Param_V.append(val)
        Param_U.append('s')
        Param_N.append(PN)
        PN = PN+1

    # -- Get the list of viscoplastic parameters
    VP = []
    for i in range(len(self.Compare['Analysis']['VP_Param'])):
        VP.append(self.Compare['Analysis']['VP_Param'][i][0])

    # -- Write κ
    val = float(self.Compare['Analysis']['VP_Param'][VP.index('κ')][2])
    unit = self.Compare['Analysis']['VP_Param'][VP.index('κ')][1]
    val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
    line = line + ' ' + str(val)
    Param.append('κ')
    Param_V.append(val)
    Param_U.append('MPa')
    Param_N.append(PN)
    PN = PN+1

    # -- Write kb
    for i in range(int(self.Compare['Analysis']['N'])):
        val = float(self.Compare['Analysis']['VP_Param'][VP.index('k' + str(i+1))][2])
        unit = self.Compare['Analysis']['VP_Param'][VP.index('k' + str(i+1))][1]
        val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
        line = line + ' ' + str(val)
        Param.append('k' + str(i+1))
        Param_V.append(val)
        Param_U.append('MPa')
        Param_N.append(PN)
        PN = PN+1

    # -- Write n
    val = float(self.Compare['Analysis']['VP_Param'][VP.index('n')][2])
    line = line + ' ' + str(val)
    Param.append('n')
    Param_V.append(val)
    Param_U.append('')
    Param_N.append(PN)
    PN = PN+1

    # -- Write μ
    val = float(self.Compare['Analysis']['VP_Param'][VP.index('μ')][2])
    unit = self.Compare['Analysis']['VP_Param'][VP.index('μ')][1]
    val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
    line = line + ' ' + str(val)
    Param.append('μ')
    Param_V.append(val)
    Param_U.append('MPa')
    Param_N.append(PN)
    PN = PN+1

    # -- Write m
    for i in range(int(self.Compare['Analysis']['N'])):
        val = float(self.Compare['Analysis']['VP_Param'][VP.index('m' + str(i+1))][2])
        line = line + ' ' + str(val)
        Param.append('m' + str(i+1))
        Param_V.append(val)
        Param_U.append('')
        Param_N.append(PN)
        PN = PN+1

    # -- Write β
    for i in range(int(self.Compare['Analysis']['N'])):
        val = float(self.Compare['Analysis']['VP_Param'][VP.index('β' + str(i+1))][2])
        line = line + ' ' + str(val)
        Param.append('β' + str(i+1))
        Param_V.append(val)
        Param_U.append('')
        Param_N.append(PN)
        PN = PN+1

    # -- Write R
    for i in range(int(self.Compare['Analysis']['N'])):
        val = float(self.Compare['Analysis']['VP_Param'][VP.index('R' + str(i+1))][2])
        unit = self.Compare['Analysis']['VP_Param'][VP.index('R' + str(i+1))][1]
        val = UnitConversion(unit, val, '1/s', os.path.join(os.getcwd()))
        line = line + ' ' + str(val)
        Param.append('R' + str(i+1))
        Param_V.append(val)
        Param_U.append('1/s')
        Param_N.append(PN)
        PN = PN+1

    # -- Write H
    for i in range(int(self.Compare['Analysis']['N'])):
        val = float(self.Compare['Analysis']['VP_Param'][VP.index('H' + str(i+1))][2])
        unit = self.Compare['Analysis']['VP_Param'][VP.index('H' + str(i+1))][1]
        val = UnitConversion(unit, val, 'MPa', os.path.join(os.getcwd()))
        line = line + ' ' + str(val)
        Param.append('H' + str(i+1))
        Param_V.append(val)
        Param_U.append('MPa')
        Param_N.append(PN)
        PN = PN+1

    # -- Write Viscoplastic Damage Parameters
    Param_D = []
    for i in range(int(self.Compare['Analysis']['N'])):
        line = line + ' ' + str(1)
        Param_V.append(1)
        Param_D.append('cd' + str(i+1))
        Param_N.append(PN)
        PN = PN+1
    for i in range(int(self.Compare['Analysis']['N'])):
        line = line + ' ' + str(1e21)
        Param_V.append(1e21)
        Param_D.append('Yd' + str(i+1))
        Param_N.append(PN)
        PN = PN+1
    for i in range(int(self.Compare['Analysis']['N'])):
        line = line + ' ' + str(1e21)
        Param_V.append(1e21)
        Param_D.append('μd' + str(i+1))
        Param_N.append(PN)
        PN = PN+1
    for i in range(int(self.Compare['Analysis']['N'])):
        line = line + ' ' + str(1)
        Param_V.append(1)
        Param_D.append('nd' + str(i+1))
        Param_N.append(PN)
        PN = PN+1
        

    # -- Write Viscoelastic Damage Parameters
    line = line + ' ' + str(1) + ' ' + str(1e21) + ' ' + str(1e21) + ' ' + str(1)
    Param_V.append(1)
    Param_V.append(1e21)
    Param_V.append(1e21)
    Param_V.append(1)
    Param_D.append('ce')
    Param_N.append(PN)
    PN = PN+1
    Param_D.append('Ye')
    Param_N.append(PN)
    PN = PN+1
    Param_D.append('μe')
    Param_N.append(PN)
    PN = PN+1
    Param_D.append('ne')
    Param_N.append(PN)
    PN = PN+1
    

    # -- Write Zeta and Psi
    line = line + ' ' + str(1e-14) + ' ' + str(1e-14)
    Param_V.append(1e-14)
    Param_V.append(1e-14)
    Param_D.append('ξ')
    Param_N.append(PN)
    PN = PN+1
    Param_D.append('ζ')
    Param_N.append(PN)
    PN = PN+1
    

    # -- Write Cutoff strength and stiffness
    line = line + ' ' + str(1e21) + ' ' + str(1e21)
    Param_V.append(1e21)
    Param_V.append(1e21)
    Param_D.append('COS')
    Param_N.append(PN)
    PN = PN+1
    Param_D.append('COE')
    Param_N.append(PN)
    PN = PN+1

    # -- Write dummy
    line = line + ' ' + str(0.01)
    Param_V.append(0.01)
    Param_D.append('DMY')
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
        line = line + ' ' + str(val)
    line = line + '\n'
    file.write(line)

    # Write Upper Bound
    file.write("UPPE:\n")
    line = ' '
    for i in range(len(Param_V)):
        val = Param_V[i]
        line = line + ' ' + str(val)
    line = line + '\n'
    file.write(line)

    # Write active parameters
    file.write("SUBP:\n")
    file.write(' 1 1 1\n')
    file.write(' 0 0\n')

    # Write LINK
    file.write("LINK:\n")
    for i in range(len(tests)):
        line = ' ' + str(i+1) + ' ' + str(NDV)
        for j in range(NDV):
            line = line + ' ' + str(j+1)
        line = line + '\n'
        file.write(line)

    # Write FACT
    file.write("FACT:\n")
    for i in range(len(tests)):
        line = ' ' + str(i+1) +  ' ' + str(NDV) + ' '
        for j in range(NDV):
            line = line + ' ' + str(1.0)
        line = line + '\n'
        file.write(line)

    # Write Weights
    weights = []
    for i in range(len(tests)):
        weights.append(1)
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
    P = Param + Param_D
    
    return mod, P, Param_U, Param_N