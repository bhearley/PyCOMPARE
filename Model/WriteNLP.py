#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# WriteNLP.py
#
# PURPOSE: Write the NLP file
#
# INPUTS:  
#   temp_dir    Temporary Directory
#   mode        "Opt" or "Analy" - mode for COMPARE
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def WriteNLP(temp_dir, mode):
    # Import Modules
    import os

    # Create the file
    fname_sim = os.path.join(temp_dir, 'comp.nlp')
    file = open(fname_sim, "w") 
    file.write("NPRINT = 4\n")
    file.write("IMERIT = 0\n")
    file.write("ILQL   = 1\n")
    file.write("ACCUR  = 1.0e-3\n")
    file.write("IFINIT = 0\n")
    file.write("NMAXFU = 10\n")
    if mode == 'Opt':
        file.write("NANALY = 0\n")
    else:
        file.write("NANALY = 1\n")

    # Close the file
    file.close()