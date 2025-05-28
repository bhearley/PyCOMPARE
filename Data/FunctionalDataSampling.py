#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# FunctionalDataSampling.py
#
# PURPOSE: Separate the test data insto stages.
#
# INPUTS
#   data      Dictionary containing test arrays (time, strain, stress)
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def FunctionalDataSampling(data):
    # Import Modules
    import numpy as np

    # Determine Stage indices
    index = []
    for i in range(len(data['load_dir'])):
        ld_i = data['load_dir'][i]
        time = data['Time']
        strain = data['Strain'][int(ld_i)]
        stress = data['Stress'][int(ld_i)]
        target = data['target'][i][0]
        if data['target'][i][1] == '-':
            vec = np.array(strain)
        elif data['target'][i][1] == 'MPa':
            vec = np.array(stress)
        else:
            vec = np.array(time)
            if i >0:
                target = target + time[index[-1]]

        # Find where the target is met
        if data['load_rate'][i][0] >= 0:
            idx = np.where(vec >= target)[0]
        else:
            idx = np.where(vec <= target)[0]
        if len(index) > 0:
                idx2 = np.where(np.array(idx) > index[-1])
                if len(idx2) > 0:
                    try:
                        index.append(int(idx[idx2[0]]))    
                    except:
                        index.append(int(idx[idx2[0][0]])) 
        elif len(idx) > 0: 
            index.append(int(idx[0]))

    return index