def f_read_uncertainties_excel(filename):
    """
    Eeads excel file of uncertainties and returns a numpy array of combined uncertainty samples at each measurement point

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        filename : Name of excel file (format "*.xlsx")

    OUTPUTS:
        combined_uncertainties : numpy array of combined uncertainty samples at each measurement point
        num_sources : number of uncertainty sources

    NOTE:
        Requires pandas and numpy
        See MeDIUM HELP for formatting of the excel file

    """

    import pandas as pd
    import numpy as np
    import openpyxl

    # read the uncertainties excel file
    temp = pd.read_excel(filename, sheet_name=None,engine = 'openpyxl')
    num_meas = temp[list(temp)[0]].shape[0]

    # 10^5 samples for each measurement point
    n_unc = 10 ** 5
    combined_uncertainties = np.zeros((n_unc, num_meas))
    num_sources = len(temp.keys())

    for key in temp.keys():
        for sens_num in range(0, len(temp[key])):
            combined_uncertainties[:, sens_num] = combined_uncertainties[:, sens_num] - \
                                                  eval('np.random.' + temp[key]['Type'][sens_num].lower() +
                                                       '(temp[key]["dist_param_1"][sens_num], temp[key]["dist_param_2"][sens_num], n_unc)')
    # note the sign of adding uncertainties in line 35. U_combined  = U_meas - U_model

    # return combined uncertainty samples at each measurement point as a numpy array
    return num_sources, combined_uncertainties
