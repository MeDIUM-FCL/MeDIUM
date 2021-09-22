def f_read_model_predictions_excel(filename):
    """
    Read excel file of model predictions

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        filename : Name of excel file (format "*.xlsx")

    OUTPUTS:
        data_ims : dictionary
        data_ims['parameters'] : numpy array with initial set of parameter values
        data_ims['predictions'] : numpy array of ims predictions at measurement points
    NOTE:
        Requires pandas and numpy
        See MeDIUM HELP for formatting of the excel file

    """
    import pandas as pd
    import numpy as np
    # read data from excel file into a panda data frame
    excel_data_df = pd.read_excel(filename,engine = 'openpyxl')

    # read headers of the data frame to understand which columns are parameter values and which are prediction values
    headers = excel_data_df.columns

    # initialize dictionary and fill with correct information based on the headers
    data_ims = {'parameters': [], 'predictions': []}
    for header in headers:
        if 'parameter' in header.lower():
            temp = excel_data_df[header].to_numpy()
            if len(data_ims['parameters']) == 0:
                data_ims['parameters'] = temp
            else:
                data_ims['parameters'] = np.vstack([data_ims['parameters'], temp])

        if 'prediction' in header.lower():
            temp = excel_data_df[header].to_numpy()
            if len(data_ims['predictions']) == 0:
                data_ims['predictions'] = temp
            else:
                data_ims['predictions'] = np.vstack([data_ims['predictions'], temp])

    data_ims['parameters'] = np.transpose(data_ims['parameters'])
    data_ims['predictions'] = np.transpose(data_ims['predictions'])

    # return dictionary with numpy arrays of ims-parameters and ims-predictions
    return data_ims
