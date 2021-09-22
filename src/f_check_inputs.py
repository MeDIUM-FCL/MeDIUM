def f_check_inputs(filename_meas, filename_modelpredictions, filename_combuncertainties, meas, ims_predictions, combined_uncertainties,checkboxvariable,numberofstage,numberofmeasperstage):
    """
    Check if inputs provided have the same size for number of measurements

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            July 22, 2020

    INPUTS:
        filename_meas : name of input measurements file (null if not yet provided by user)
        filename_modelpredictions : name of input model predictions file (null if not yet provided by user)
        filename_combuncertainties : name of input combined uncertainties file (null if not yet provided by user)
        meas : measurement input provided
        ims_predictions : ims predictions at measurement locations
        combined_uncertainties : output of reading the uncertainties file

    OUTPUTS:
        check['value'] : numpy array with initial set of parameter values
        check['message'] : numpy array of ims predictions at measurement points
    NOTE:
        Use the check['value'] if false to generate a warning message. Content of the warning message dialog is check['message']
        Function does nothing when one of the inputs is not populated

    """

    import numpy
    from PyQt5 import QtWidgets

    if checkboxvariable == 0:
        check = {}
        # if len(numpy.transpose(meas)) != 0 and len(numpy.transpose(ims_predictions)) != 0 and len(numpy.transpose(combined_uncertainties)) != 0:
        if filename_meas and filename_modelpredictions and filename_combuncertainties:
            print('first check is true')
            if len(numpy.transpose(meas)) == len(numpy.transpose(ims_predictions)) == len(numpy.transpose(combined_uncertainties)):
                check['value'] = True
                check['message'] = 'Congratulations! All necessary inputs provided. \nProceed to the data-interpretation tab.'
                brief_text = 'Congratulations! All necessary inputs provided. \nProceed to the data-interpretation tab.'
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText(brief_text)
                msgBox.setWindowTitle('Information')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass
            else:
                check['value'] = False
                check['message'] = 'ERROR\nNumber of measurements according to measurements file = {}\nNumber of measurements according to ims file = {}\nNumber of measurements according to uncertainties file = {}'.format(len(numpy.transpose(meas)), len(numpy.transpose(ims_predictions)), len(numpy.transpose(combined_uncertainties)))
                brief_text = 'ERROR\nNumber of measurements according to measurements file = {}\nNumber of measurements according to ims file = {}\nNumber of measurements according to uncertainties file = {}'.format(len(numpy.transpose(meas)), len(numpy.transpose(ims_predictions)), len(numpy.transpose(combined_uncertainties)))
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText(brief_text)
                msgBox.setWindowTitle('Warning')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass
            return check

    else:
        check = {}
        if filename_meas and filename_modelpredictions and filename_combuncertainties:
            print('first check is true')
            totalmeas_uncer = numberofstage*numberofmeasperstage
            if len(numpy.transpose(meas)) == totalmeas_uncer == len(numpy.transpose(ims_predictions)):
                check['value'] = True
                check['message'] = 'Congratulations! All necessary inputs provided. \nProceed to the data-interpretation tab.'
                brief_text = 'Congratulations! All necessary inputs provided. \nProceed to the data-interpretation tab.'
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText(brief_text)
                msgBox.setWindowTitle('Information')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass
            else:
                check['value'] = False
                check[
                    'message'] = 'ERROR\nNumber of measurements according to measurements file = {}\nNumber of measurements according to ims file = {}\nNumber of measurements according to uncertainties file = {}'.format(
                    len(numpy.transpose(meas)), len(numpy.transpose(ims_predictions)),
                    len(numpy.transpose(combined_uncertainties)))
                brief_text = 'ERROR\nNumber of measurements according to measurements file = {}\nNumber of measurements according to ims file = {}\nNumber of measurements according to uncertainties file = {}'.format(
                    len(numpy.transpose(meas)), len(numpy.transpose(ims_predictions)),
                    len(numpy.transpose(combined_uncertainties)))
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Information)
                msgBox.setText(brief_text)
                msgBox.setWindowTitle('Warning')
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                returnValue = msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass
            return check
