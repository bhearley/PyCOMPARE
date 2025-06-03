#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Search.py
#
# PURPOSE: Search for records
#
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Search(self):
    # Import Modules
    from tkinter import messagebox
    from GRCMI import UnitConversion

    # Get search criteria
    srch_crit = []

    # -- Material names
    mat_names = self.text_mat.get("1.0", "end-1c").split(';')

    # -- Test Type
    flag_type = 0
    test_type = [self.combo_type.get()]
    if test_type[0] == '':
        test_type = []
    if len(test_type) > 0:
        flag_type = 1
        attribute = self.table.attributes['Test Type']
        search = attribute.search_criterion(contains_all=test_type)
        srch_crit.append(search)

    # -- Variable Load Test Type
    vl_test_type = [self.combo_gtype.get()]
    if vl_test_type[0] == '':
        vl_test_type = []
    if len(vl_test_type) > 0:
        flag_type = 1
        attribute = self.table.attributes['Variable Load Test Type']
        search = attribute.search_criterion(contains_all=vl_test_type)
        srch_crit.append(search)

    # Get records list
    try:
        records_type = self.table.search_for_records_where(srch_crit) 
    except:
        pass

    # -- Numeric Searches
    SearchAttributes = {'Test Temperature':['Test Temperature'],
                        'Strain Rate':['Strain Rate','Compressive Strain Rate', 'Shear Strain Rate'],
                        'Stress Rate':['Strain Rate','Compressive Strain Rate', 'Shear Strain Rate'],
                        'Creep Stress':['Creep Stress (11 axis)', 'Creep Stress (22 axis)', 'Creep Stress (33 axis)',
                                        'Compressive Creep Stress (11 axis)', 'Compressive Creep Stress (22 axis)', 'Compressive Creep Stress (33 axis)',
                                        'Shear Creep Stress (12 axis)', 'Shear Creep Stress (13 axis)', 'Shear Creep Stress (23 axis)'],
                        'Relaxation Strain':['Relaxation Constant Strain (11 axis)', 'Relaxation Constant Strain (22 axis)', 'Relaxation Constant Strain (33 axis)',
                                        'Compressive Relaxation Constant Strain (11 axis)', 'Compressive Relaxation Constant Strain (22 axis)', 'Compressive Relaxation Constant Strain (33 axis)',
                                        'Shear Relaxation Constant Strain (12 axis)', 'Shear Relaxation Constant Strain (13 axis)', 'Shear Relaxation Constant Strain (23 axis)']
                                        
                        }
    
    records_num = []
    flag_num = 0
    for i in range(len(self.srch_vals)):
        rec_i = []      # Preallocate list of records that meet the requirment for attribute i
        rec_temp = []   # Preallocate list of records that meet all requirements
        if self.srch_vals[i][3].get() != '':
            # - Set the flag
            flag_num = 1

            # - Get the name
            name = self.srch_vals[i][0].cget("text").split(":")[0]

            # - Check for units
            units = self.srch_vals[i][2].get()
            if units == '':
                messagebox.showerror(message = 'Not units defined for ' + name)
                return
            
            # - Get selection
            opt = self.srch_vals[i][3].get()

            # -- Equals
            if opt == 'equals':
                # Get the value
                val = self.srch_vals[i][4].get()

                # Check that a valid value exists
                if val == '':
                    messagebox.showerror(message = 'Missing value for ' + name)
                    return
                
                # Create search bounds (allow 1% error for unit conversion)
                lb = float(val)*0.99 
                ub = float(val)*1.01

            # -- Greater Than
            if opt == 'is greater than':
                # Get the value
                val = self.srch_vals[i][4].get()

                # Check that a valid value exists
                if val == '':
                    messagebox.showerror(message = 'Missing value for ' + name)
                    return
                
                # Create search bounds (allow 1% error for unit conversion)
                lb = float(val)*0.99 
                ub = None

            # -- Less Than
            if opt == 'is less than':
                # Get the value
                val = self.srch_vals[i][4].get()

                # Check that a valid value exists
                if val == '':
                    messagebox.showerror(message = 'Missing value for ' + name)
                    return
                
                # Create search bounds (allow 1% error for unit conversion)
                lb = None 
                ub = float(val)*1.01

            # -- Is Between
            if opt == 'is between':
                # Get the value
                val1 = self.srch_vals[i][4].get()

                # Check that a valid value exists
                if val1 == '':
                    messagebox.showerror(message = 'Missing value for ' + name)
                    return
                
                # Get the value
                val2 = self.srch_vals[i][6].get()

                # Check that a valid value exists
                if val2 == '':
                    messagebox.showerror(message = 'Missing value for ' + name)
                    return
                
                # Create search bounds (allow 1% error for unit conversion)
                lb = float(val1)*0.99 
                ub = float(val2)*1.01

            # Loop through possible attributes
            for att in SearchAttributes[name]:
                # -- Get the attribute
                attribute = self.table.attributes[att]

                # -- Define Lower Bound Search
                if lb is not None:
                    lb = UnitConversion(units, lb, attribute.unit)
                    lb_search = attribute.search_criterion(greater_than=lb)

                # -- Define Upper Bound Search
                if ub is not None:
                    ub = UnitConversion(units, ub, attribute.unit)
                    ub_search = attribute.search_criterion(less_than=ub)

                # -- Search
                recs = self.table.search_for_records_where([lb_search, ub_search])

                if len(recs) > 0:
                    rec_i = rec_i + recs

            # Update list of records that meet all attributes
            if records_num == []:
                records_num = rec_i
            else:
                for rec in rec_i:
                    for rec_all in records_num:
                        if rec.attributes['Specimen ID'].value == rec_all.attributes['Specimen ID'].value:
                            rec_temp.append(rec)
                records_num = rec_temp

    # Preallocate records out
    records_out_temp = []

    # Get records that meet number and type requirements
    # -- Both Type and Numeric Criteria
    if flag_type == 1 and flag_num == 1:
        for rec1 in records_type:
            for rec2 in records_num:
                if rec1.attributes['Specimen ID'].value == rec2.attributes['Specimen ID'].value:
                    records_out_temp.append(rec1)
    # -- Only Numeric Criteria
    elif flag_type == 0 and flag_num == 1:
        records_out_temp = records_num
    # -- Only Type Criteria
    elif flag_type == 1 and flag_num == 0:
        records_out_temp = records_type
    # -- Only name criteria
    else:
        attribute = self.table.attributes['Test Temperature']
        any_search = attribute.search_criterion(greater_than=-1)
        records_out_temp = self.table.search_for_records_where([any_search])

    # Get the records that meet all requirements
    records_out = []
    for record in records_out_temp:
        flag = 0
        mat_name = record.attributes['Material Name'].value
        for mat in mat_names:
            if mat in mat_name:
                flag = 1

        if flag == 1:
            records_out.append(record)

    return records_out