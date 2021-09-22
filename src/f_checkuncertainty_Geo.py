def checkuncertainty_Geo(finalpathuncertaintyinput):
    """
        Check the Uncertainties(Geo).xlsx file for any error in values and format

        Developed by :   WANG Ze-Zhou (ETH Singapore)
        Contact :        e0054291@u.nus.edu
        Date:            August 03, 2021

        INPUTS:
            finalpathuncertaintyinput : directory of the Uncertainties(Geo).xlsx.

        OUTPUTS:
            numberofsensor : number of sensors involved in the studied problem.
            numberofmodelinstance : number of initial model instances involved in the studied problem.

        NOTE:

        """

    import numpy
    import openpyxl
    import pandas
    from PyQt5 import QtWidgets

    #####3D effects
    excelfileuncertaintyinput = pandas.read_excel(finalpathuncertaintyinput,sheet_name = '3D Effects', engine = 'openpyxl')

    excelfileuncertaintyinput_array_ = excelfileuncertaintyinput.to_numpy()[1:10000,2:6]

    sizedata = numpy.shape(excelfileuncertaintyinput_array_)

    Effect_3D = []
    Effect_3D_check = []

    for i in range(0, sizedata[1]):
        for s in range(0,sizedata[0]):
            excelsheetuncertaintyvalue_ = excelfileuncertaintyinput_array_[s, i]
            if numpy.isnan(excelsheetuncertaintyvalue_) == False:
                Effect_3D_check_ = 0
            else:
                Effect_3D_check_ = 1

            Effect_3D_check = numpy.append(Effect_3D_check, Effect_3D_check_)
            Effect_3D = numpy.append(Effect_3D, excelsheetuncertaintyvalue_)

    ##########Measurement
    excelfileuncertaintyinput2 = pandas.read_excel(finalpathuncertaintyinput, sheet_name='Measurement Uncertainty', engine='openpyxl')

    excelfileuncertaintyinput_array_2 = excelfileuncertaintyinput2.to_numpy()[0:10000, 0:2]

    sizedata = numpy.shape(excelfileuncertaintyinput_array_2)

    Meas_Unc = []
    Meas_Unc_check = []

    for i in range(0, sizedata[0]):
        excelsheetuncertaintyvalue2_ = excelfileuncertaintyinput_array_2[i, 1]
        if numpy.isnan(excelsheetuncertaintyvalue2_) == False:
            Meas_Unc_check_ = 0
        else:
            Meas_Unc_check_ = 1
        Meas_Unc_check = numpy.append(Meas_Unc_check, Meas_Unc_check_)
        Meas_Unc = numpy.append(Meas_Unc, excelsheetuncertaintyvalue2_)


    ##########check non number
    Meas_Unc_check = Meas_Unc_check[numpy.logical_not(numpy.isnan(Meas_Unc))]
    Effect_3D_check = Effect_3D_check[numpy.logical_not(numpy.isnan(Effect_3D))]
    Meas_Unc = Meas_Unc[numpy.logical_not(numpy.isnan(Meas_Unc))]
    Effect_3D = Effect_3D[numpy.logical_not(numpy.isnan(Effect_3D))]


    if numpy.sum(Meas_Unc_check)==0 and numpy.sum(Effect_3D_check)==0:
        maxvalue = numpy.amax(Meas_Unc)
        minvalue = numpy.amin(Meas_Unc)

        numberofmeasurementperstage = (maxvalue - minvalue+1)

        numberofstage = len(Meas_Unc)/numberofmeasurementperstage

        numberofmeasurementperstage = numberofmeasurementperstage.astype(numpy.int64)
        numberofstage = numberofstage.astype(numpy.int64)

    else:
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("The file contains non numeric data. Please inspect the file")
        msg.setWindowTitle('Error')
        msg.exec_()


    return numberofmeasurementperstage,numberofstage
