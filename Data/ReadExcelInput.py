#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# ReadExcelInput.py
#
# PURPOSE: Read an Excel Input File and perform error checking.
#
# INPUTS
#   df      pandas dataframe containing input data
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def ReadExcelInput(df):
    # Import Modules
    import pandas as pd 

    # Preallocate the error flag and message
    flag  = 0
    msg = ''
    data = {}

    # Check for a test name 
    if pd.isna(df.values[1][2]):
        flag = 1
        msg = msg + 'ERROR: Missing Test Name.  '
    else:
        data['name'] = df.values[1][2]

    # Check for Test Type 
    if pd.isna(df.values[2][2]):
        flag = 1
        msg = msg + 'ERROR: Missing Test Type.  '
    else:
        data['test_type'] =  df.values[2][2]
    
    # Check for Temperature 
    if pd.isna(df.values[3][2]):
        flag = 1
        msg = msg + 'ERROR: Missing Test Temperature.  '
    else:
        try:
            data['temp'] =  int(df.values[3][2])
        except:
            flag = 1
            msg = msg + 'ERROR: Invalid temperature value.  '

    # Check for Anisotropy Angle 
    if pd.isna(df.values[4][2]):
        flag = 1
        msg = msg + 'ERROR: Anisotropy Angle.  '
    else:
        try:
            data['angle'] =  float(df.values[4][2])
        except:
            flag = 1
            msg = msg + 'ERROR: Invalid anisotropy angle value.  '

    # Get the Control in each direction
    C11 = df.values[5][2] # 11 Control
    C22 = df.values[6][2] # 22 Control
    C12 = df.values[7][2] # 12 Control
    Control = [C11, C22, C12]

    # Check for control in each direction
    cflag = 0
    for i in range(len(Control)):
        if pd.isna(Control[i]):
            Control[i] = 'Free'
        else:
            cflag = 1
    if cflag == 0:
        flag = 1
        msg = msg + 'ERROR: At least one control mode must be defined.  '
    else:
        data['control_all'] = Control

    # Get Specific Test Information
    data['stage_type'] = []
    data['load_dir'] = []
    data['load_rate'] = []
    data['control'] = []
    data['target'] = []

    if pd.isna(df.values[2][4]) == False:
        i = 2
        while pd.isna(df.values[i][4]) == False:
            data['load_dir'].append(df.values[i][5])
            if df.values[i][6] == 'Strain':
                data['control'].append(df.values[i][6])
                data['load_rate'].append([df.values[i][7],'1/s'])

                if df.values[i][8] == 'Time':
                    data['stage_type'].append('Relaxation')
                    data['target'].append([df.values[i][9], 's'])
                else:
                    data['stage_type'].append('Tensile')
                    if df.values[i][8] == 'Strain':
                        data['target'].append([df.values[i][9], '-'])
                    else:
                        data['target'].append([df.values[i][9], 'MPa'])

            else:
                data['control'].append(df.values[i][6])
                data['load_rate'].append([df.values[i][7],'MPa/s'])

                if df.values[i][8] == 'Time':
                    data['stage_type'].append('Creep')
                    data['target'].append([df.values[i][9], 's'])
                else:
                    data['stage_type'].append('Tensile')
                    if df.values[i][8] == 'Strain':
                        data['target'].append([df.values[i][9], '-'])
                    else:
                        data['target'].append([df.values[i][9], 'MPa'])

            i = i+1

    # Preallocate Arrays
    data['Time'] = []
    data['Strain'] = {}
    data['Stress'] = {}

    # Get the Time Array
    start_time = df.values[i][11]
    if start_time == None:
        flag = 1
        msg = msg + 'ERROR: No Time Data Given.  '
    else:
        df_numeric = df["Unnamed: 11"].apply(pd.to_numeric, errors='coerce')
        data['Time'] = df_numeric.values[1:df.values.shape[0]]

    # Get Stress and Strain Arrays
    for i in range(12,18):
        if pd.isna(df.values[1][i]) == False:
            name = df.values[0][i].split(' ')
            var = name[0]
            dir = int(name[1])
            df_numeric = df["Unnamed: " + str(i)].apply(pd.to_numeric, errors='coerce')
            data[var][dir] = df_numeric.values[1:df.values.shape[0]]
            
    return data, flag, msg