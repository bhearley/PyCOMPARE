#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# WriteSIM.py
#
# PURPOSE: Write the simulation *.in files for each test
#
# INPUTS:  
#   self        GUI Data structure
#   TestData    Test Data 
#   temp_dir    Temporary Directory
#   ct_file     File Count
#   mod         Model Number
#   Param       List of Parameter names
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def WriteSIM(self, TestData, temp_dir, ct_file, mod, Param):
    # Import Modules
    import os
    import numpy as np
    from decimal import Decimal

    # Create the file
    fname_sim = os.path.join(temp_dir, 'sim' + str(ct_file) + '.in')
    file = open(fname_sim, "w") 
    file.write("input file\n")

    # Write *PRINT
    file.write("*PRINT\n")
    file.write(" NPL=0  %\n")

    # Write *LOAD
    file.write("*LOAD\n")
    ECON = []
    FCON = []
    for i in range(len(TestData['Control_All'])):
        if TestData['Control_All'][i] == 'Strain':
            ECON.append('1')
            FCON.append('0')
        else:
            ECON.append('0')
            FCON.append('1')
    line = ' ECON=' + ECON[0] + ' ' + ECON[1] + ' ' + ECON[2] + ' FCON=' + FCON[0] + ' ' + FCON[1] + ' ' + FCON[2] + '\n'
    file.write(line)

    # Write *MECH
    file.write("*MECH\n")
    npts = len(TestData['Reduced Data']['Time'])
    file.write(" NPTW1=     " + str(npts) + "\n")
    # -- Write Time
    ct = 0
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(TestData['Reduced Data']['Time'][ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write LO1
    file.write(" LO1=\n")
    if TestData['Control_All'][0] == 'Free':
        array = np.zeros(shape=(npts,))
    else:
        array = TestData['Reduced Data'][TestData['Control_All'][0]][11]
    ct = 0
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write LO2
    file.write(" LO2=\n")
    if TestData['Control_All'][1] == 'Free':
        array = np.zeros(shape=(npts,))
    else:
        array = TestData['Reduced Data'][TestData['Control_All'][1]][22]
    ct = 0
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write LO3
    file.write(" LO3=\n")
    if TestData['Control_All'][2] == 'Free':
        array = np.zeros(shape=(npts,))
    else:
        array = TestData['Reduced Data'][TestData['Control_All'][2]][12]
    ct = 0
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)
    
    # Write *STEP
    file.write("*STEP\n")
    file.write(" NPTS=     " + str(npts) + "\n")
    # -- Write Time
    ct = 0
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(TestData['Reduced Data']['Time'][ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    file.write(" STP=\n")
    # -- Write Time
    ct = 1
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(TestData['Reduced Data']['Time'][ct]-TestData['Reduced Data']['Time'][ct-1]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # Write *MODEL
    file.write('*MODEL\n')
    file.write(' MODL=' + str(mod) + '\n')
    if TestData['Angle'] > 0:
        ang = '+' + '%.8E' % Decimal(str(TestData['Angle']))
    else:
        ang = '%.8E' % Decimal(str(TestData['Angle']))
    file.write(' NEL= ' + str(self.Compare['Model']['M']) + ' NVP= ' + str(self.Compare['Model']['M']) + ' BET=' + ang + ' NDM=1\n')
 
    # Write *MATL
    file.write('*MATL\n')
    file.write(' NPHI=    ' + str(len(Param)) +'\n')
    file.write(' NMSR=    ' + str(npts-1) + '\n')
    # -- Write Time
    ct = 1
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(TestData['Reduced Data']['Time'][ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write SIGX
    file.write(" SIGX=\n")
    if TestData['Control_All'][0] == 'Free':
        array = np.ones(shape=(npts,))*-9.99999000E+005
    else:
        if TestData['Control_All'][0] == 'Strain':
            array = TestData['Reduced Data']['Stress'][11]
        if TestData['Control_All'][0] == 'Stress':
            array = TestData['Reduced Data']['Strain'][11]
    ct = 1
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write SIGY
    file.write(" SIGY=\n")
    if TestData['Control_All'][1] == 'Free':
        array = np.ones(shape=(npts,))*-9.99999000E+005
    else:
        if TestData['Control_All'][1] == 'Strain':
            array = TestData['Reduced Data']['Stress'][22]
        if TestData['Control_All'][1] == 'Stress':
            array = TestData['Reduced Data']['Strain'][22]
    ct = 1
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # -- Write SIGXY
    file.write(" SIGXY=\n")
    if TestData['Control_All'][2] == 'Free':
        array = np.ones(shape=(npts,))*-9.99999000E+005
    else:
        if TestData['Control_All'][2] == 'Strain':
            array = TestData['Reduced Data']['Stress'][12]
        if TestData['Control_All'][2] == 'Stress':
            array = TestData['Reduced Data']['Strain'][12]
    ct = 1
    while ct < npts:
        ctr = 0
        line = ''
        while ctr < 5:
            line = line + ' ' + '%.8E' % Decimal(str(array[ct]))
            ct = ct + 1
            if ct == npts:
                break
            ctr = ctr + 1
        line = line + '\n'
        file.write(line)

    # Write *END
    file.write("*END\n")

    # Close the file
    file.close()