#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# UnitConversion.py
#
# PURPOSE: Convert units
#
# INPUTS:
#   source_unit     Unit of the source value
#   source_value    Source Value
#   target_unit     Target Desired Unit
#   admin_dir       Admin directory containing the unit library
# OUTPUTS:
#   taret_val       Value in the target unit
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------

def UnitConversion(source_unit, source_value, target_unit, admin_dir):
    
    # Import Modules
    import json
    import os

    # Load the library
    unit_lib = os.path.join(admin_dir, 'UnitConversion',"unit_library.json")
    f = open(unit_lib, 'r', encoding='utf-8')
    U = json.load(f)

    # Convert to Global Variable
    data = U[source_unit]
    val = eval(data[0].replace('x', str(source_value)))
    
    data = U[target_unit]
    target_val = eval(data[1].replace('x', str(val)))

    return target_val