def f_read_model_predictions_excel_Geo(filename):
    """
    Read excel file of model predictions

    Developed by :   WANG Ze Zhou (ETH Singapore)
    Contact :        e0054291@u.nus.edu
    Date:            August 04, 2021

    INPUTS:
        filename : Name of excel file (format "*.xlsx")

    OUTPUTS:
        numberpara:Number of material parameters
        finalnumberofmeas: Number of measurement data
        numberofinstance: Number of initial model instances
        inputpara: values of initial model instances
    NOTE:
        Requires pandas and numpy
        See MeDIUM HELP for formatting of the excel file

    """
    import pandas as pd
    import numpy as np

    # read data from excel file into a panda data frame
    excel_data_df = pd.read_excel(filename,engine = 'openpyxl')
    headers = excel_data_df.columns

    headercheck = []
    for header in headers:
        if 'parameter' in header.lower():
            headdata = 1
            headercheck = np.append(headercheck, headdata)
        else:
            headdata = 0
    numberpara = np.sum(headercheck)

    excel_data = excel_data_df.to_numpy()
    location = np.argwhere(~np.isnan(excel_data))

    numberofinstance = np.max(location[:,0])+1
    numberofmeas = np.max(location[:,1])+1
    finalnumberofmeas = numberofmeas-2
    prediction = np.zeros((numberofinstance, numberofmeas))

    sizedata = np.shape(location)
    for i in range(sizedata[0]):
        prediction[location[i,0],location[i,1]] = excel_data[location[i,0],location[i,1]]

    inputpara = prediction[:,0:int(numberpara)]
    finalprediction = prediction[:,int(numberpara):numberofmeas]

    maxinput = []
    mininput = []
    for i in range(0,int(numberpara)):
        maxinput_ = np.max(inputpara[:,i])
        maxinput = np.append(maxinput, maxinput_)
        mininput_ = np.min(inputpara[:, i])
        mininput = np.append(mininput, mininput_)

    return numberpara,finalnumberofmeas,numberofinstance,inputpara,finalprediction


