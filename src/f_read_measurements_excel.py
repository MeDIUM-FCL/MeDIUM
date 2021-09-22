def f_read_measurements_excel(filename):
    """
    Read excel file of measurements

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        filename : Name of excel file (format "*.xlsx")

    OUTPUTS:
        measurements : numpy array of measurements

    NOTE:
        Requires pandas and numpy
        See MeDIUM HELP for formatting of the excel file

    """
    import pandas as pd
    import openpyxl
    measurements = pd.read_excel(filename, header=None,engine = 'openpyxl').to_numpy()

    # return numpy array of measurements
    return measurements
