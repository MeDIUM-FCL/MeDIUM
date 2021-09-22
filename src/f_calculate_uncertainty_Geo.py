def calculateuncertainty(numberofsensor,numberofmodelinstance,finalpathuncertaintyinput,finalpathprediction):
    """
        Calculate geotechnical uncertainties for the subsequent EDMF analysis

        Developed by :   WANG Ze-Zhou (ETH Singapore)
        Contact :        e0054291@u.nus.edu
        Date:            August 03, 2021

        INPUTS:
            numberofsensor : number of sensors involved in the studied problem.
            numberofmodelinstance : number of initial model instances involved in the studied problem.
            finalpathuncertaintyinput : directory of the Uncertainties(Geo).xlsx.
            finalpathprediction : directory of the Prediction(Geo).xlsx.

        OUTPUTS:
            Unc_combinedmean : mean of combined uncertainties.
            Unc_combinedstd : standard deviation of combined uncertainties.

        NOTE:
            Outputs will be pasted in an excel file under the software directory. Subsequent EDMF analysis
            will automatically read this excel file.

        """

    import numpy
    import os
    import xlrd
    from openpyxl import load_workbook
    import pandas
    import xlsxwriter

    #####load input file
    currentpath = os.getcwd()
    excelfileuncertaintyinput = pandas.read_excel(finalpathuncertaintyinput,sheet_name = '3D Effects', engine = 'openpyxl')

    ##########read inputs 3D
    excelsheetuncertainty1 = excelfileuncertaintyinput.to_numpy()[1:10000,2:6]
    Effects_3D = numpy.zeros((numberofsensor,4))

    for i in range(0,numberofsensor):
        for s in range(0,4):
            excelsheetuncertaintyvalue_= excelsheetuncertainty1[i,s]
            Effects_3D[i][s] = excelsheetuncertaintyvalue_

    ##########read inputs Meas
    excelfileuncertaintyinput2 = pandas.read_excel(finalpathuncertaintyinput,sheet_name = 'Measurement Uncertainty', engine = 'openpyxl')
    excelsheetuncertainty2 = excelfileuncertaintyinput2.to_numpy()[0:10000, 0:2]
    Meas_Unc = numpy.zeros((numberofsensor,1))

    for i in range(0,numberofsensor):
        excelsheetuncertaintyvalue2_= excelsheetuncertainty2[i,1]
        Meas_Unc[i][0] = excelsheetuncertaintyvalue2_

    #########load predictions
    excelfileprediction = pandas.read_excel(finalpathprediction,sheet_name = 'Prediction', engine = 'openpyxl')


    excelsheetprediction = excelfileprediction.to_numpy()
    prediction = numpy.zeros((numberofmodelinstance, numberofsensor))
    for i in range(0,numberofmodelinstance):
        for s in range(0,numberofsensor):
            excelsheetpredictionvalue_= excelsheetprediction[i,s+2]
            prediction[i][s] = excelsheetpredictionvalue_


    #########linear regression
    coemat = numpy.zeros((2,2))
    ymat = numpy.zeros((2,1))
    Effects_3Dmean = numpy.zeros((numberofmodelinstance,numberofsensor))
    Effects_3Dstd = numpy.zeros((numberofmodelinstance,numberofsensor))
    for i in range(0,numberofsensor):
        coemat[0][0] = Effects_3D[i][3]
        coemat[1][0] = Effects_3D[i][2]
        coemat[0][1] = 1
        coemat[1][1] = 1
        inv_coemat = numpy.linalg.inv(coemat)
        ymat[0][0] = Effects_3D[i][3]-Effects_3D[i][1]
        ymat[1][0] = Effects_3D[i][2]-Effects_3D[i][0]
        coe = numpy.dot(inv_coemat,ymat)

        for s in range(0,numberofmodelinstance):
            Effects_3Dmean[s][i] = prediction[s][i]*coe[0][0]+coe[1][0]

    Effects_3Dstd = 0.13*Effects_3Dmean

    ########measurement uncertainty
    Meas_Uncmean = numpy.zeros((numberofsensor,1))
    Meas_Uncstd = 0.0001*Meas_Unc*1000


    ########combine uncertainty
    Unc_combinedmean = Effects_3Dmean;
    Unc_combinedstd = numpy.zeros((numberofmodelinstance,numberofsensor))

    for i in range(0,numberofsensor):
        for s in range(0,numberofmodelinstance):
            Unc_combinedstd[s][i] = (Effects_3Dstd[s][i]**2+Meas_Uncstd[i][0]**2)**0.5

    return Unc_combinedmean,Unc_combinedstd
