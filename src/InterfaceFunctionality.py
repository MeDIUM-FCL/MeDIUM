from PyQt5 import QtWidgets, QtCore
from GUI_Design import Ui_MainWindow
import numpy as np
import matplotlib.pyplot as plt
import shelve
import inspect

# Can initialize variables here as well

combined_uncertainty = np.array([])


class InterfaceWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    def __init__(self):
        super().__init__()
        # set up software display
        self.setupUi(self)
        self.show()

        # initialize variables for the software
        self.filename_meas = []
        self.filename_modelpredictions = []
        self.filename_combuncertainties = []

        self.number_measurements = []
        self.number_parameters = []
        self.number_predictions = []
        self.number_measurements_unc = []
        self.Uncertaintyresults_Geo = []
        self.number_ims = []
        self.number_cms = []
        self.measurements = []
        self.ims_parameters = []
        self.ims_predictions = []
        self.combined_uncertainties = []
        self.phi = 0.95
        self.unc_amplifier = 1
        self.cms = []
        self.is_candidate = []
        self.precision = []

        self.what_if_number_cms = []
        self.what_if_cms = []
        self.what_if_is_candidate = []
        self.what_if_validation_text = ""

        self.checkboxvariable = 0  ####0 is default analysis 1 is geotechnical analysis
        self.numberofstage = []
        self.numberofmeasurementperstage = []

        # *** Changes to the "*.ui" file *** #
        # Section Measurements
        self.PathForMeasurements.setToolTip('Use the browse button to upload an excel file that contains measurements')
        self.BrowseMeasurements.setToolTip('Browse for an excel file that contains measurements')
        self.help_input_measurements.setToolTip('Help uploading measurements')

        self.help_input_measurements.clicked.connect(self.help_read_measurements_file)
        self.BrowseMeasurements.clicked.connect(self.read_measurements)

        # Section Initial Model Instances
        self.PathForModelPredictions.setToolTip(
            'Use the browse button to upload an excel file that contains model predictions')
        self.BrowseModelPredictions.setToolTip('Browse for an excel file that contains model predictions')
        self.help_input_predictions.setToolTip('Help uploading model predictions')

        self.BrowseModelPredictions.clicked.connect(self.read_model_predictions)

        self.help_input_predictions.clicked.connect(self.help_read_predictions_file)

        # Section Uncertainty Estimations
        self.PathForUncertainties.setToolTip(
            'Use the browse button to upload an excel file that contains uncertainty definitions.')
        self.BrowseUncertainties.setToolTip('Browse for an excel file that contains uncertainty definitions')
        self.help_input_uncertainties.setToolTip('Help uploading uncertainty definitions')

        self.BrowseUncertainties.clicked.connect(self.read_uncertainties)
        self.help_input_uncertainties.clicked.connect(self.help_read_uncertainties_file)

        # Section EDMF
        self.perform_edmf.setToolTip('Falsify model instances using measurements')
        self.help_edmf.setToolTip('Help for performing EDMF')
        self.perform_edmf.clicked.connect(self.falsify_models)
        self.help_edmf.clicked.connect(self.help_perform_edmf)

        # Section Cross-validate
        self.perform_holdout.setToolTip('Carry out holdout cross-validation')
        self.get_holdout_indices.setToolTip(
            'Provide indices of measurement points to be held out (from interpretation) for validation.')
        self.help_validate.setToolTip('Help perform cross-validation')

        self.perform_holdout.clicked.connect(self.validate_holdout)
        self.help_validate.clicked.connect(self.help_perform_validate)

        # Section Whatif Scenarios
        self.slider_phi_value.setToolTip('Change target reliability of identification.')
        self.slider_unc_amplifier.setToolTip('Change uncertainty magnitude by the selected factor.')
        self.redo_edmf.setToolTip('Perform EDMF for the selected interpretation scenario.')
        self.perform_holdout_again.setToolTip('Perform holdout validation for the selected interpretation scenario.')
        self.help_whatif.setToolTip('Click for help.')

        self.slider_phi_value.valueChanged[int].connect(self.get_phi_value)
        self.slider_unc_amplifier.valueChanged[int].connect(self.get_uncamplifier_value)
        self.redo_edmf.clicked.connect(self.reperform_edmf)
        self.perform_holdout_again.clicked.connect(self.reperform_holdout)
        self.help_whatif.clicked.connect(self.help_perform_whatif_scenarios)

        # ====== check box ======= #
        self.geotechnical_application.setToolTip('Check it for geotechnical application')
        self.geotechnical_application.toggled.connect(self.Checkbox_Geo)

        #########load Help document
        self.actionDocumentation.triggered.connect(self.openhelpdoc)
        self.actionVersion.triggered.connect(self.displayversion)
        self.title_information.clicked.connect(self.displayversion)

        ########file menu
        self.actionSave_Session.triggered.connect(self.save_all_variables)

    ##########functions
    from f_create_result_folder import f_create_result_folder
    f_create_result_folder('/Results')

    from f_displayversion import displayversion

    def msgButtonClick(self, i):
        if i.text() == "More Help":
            from f_LoadPDF import LoadPDF
            LoadPDF(self.help_doc_page)
        pass

    def openhelpdoc(self):
        from f_LoadPDF import LoadPDF
        LoadPDF(1)

    def show_message_box(self, messagetext, titletext):
        self.msg = QtWidgets.QMessageBox()
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.setText(messagetext)
        self.msg.setWindowTitle(titletext)
        self.msg.exec_()

    # --------------------------------------------------------------------------
    # *** Check if geotechnical analysis is selected ***
    def Checkbox_Geo(self):
        if self.geotechnical_application.isChecked():
            del self.checkboxvariable
            self.checkboxvariable = 1
            print('Geotechnical analysis is selected')
            print(self.checkboxvariable)

        else:
            del self.checkboxvariable
            self.checkboxvariable = 0
            print('Default analysis is selected')
            print(self.checkboxvariable)

    # --------------------------------------------------------------------------
    # *** browse measurements file ***
    def read_measurements(self):
        from f_read_measurements_excel import f_read_measurements_excel
        self.filename_meas = QtWidgets.QFileDialog.getOpenFileName()
        try:
            self.pathnamemeasurement = str(self.filename_meas[0])
            self.PathForMeasurements.setText(self.pathnamemeasurement)
            self.measurements = f_read_measurements_excel(self.pathnamemeasurement)
            size_of_var = np.shape(self.measurements)
            self.number_measurements = int(size_of_var[1])
            content_to_print = 'Successfully uploaded data from measurements file.\nNumber of measurements uploaded is: {}.'.format(
                self.number_measurements)
            self.MeasFileContents.setText(str(content_to_print))
        except:
            self.PathForMeasurements.setText("Enter the path for file that contains measurement data")
            self.MeasFileContents.clear()
            if self.filename_meas:
                self.measurements = []

        from f_check_inputs import f_check_inputs
        self.checkinputs = f_check_inputs(self.filename_meas, self.filename_modelpredictions,
                                          self.filename_combuncertainties, self.measurements, self.ims_predictions,
                                          self.combined_uncertainties, self.checkboxvariable, self.numberofstage,
                                          self.numberofmeasurementperstage)
        print(self.checkinputs)
        return self.measurements

    # *** help regarding measurements file ***
    def help_read_measurements_file(self):
        brief_text = 'Provide as input an excel file (.xlsx) that contains measurements.'
        informative_text = 'The file provided should have a single row with one measurement value in each column.' \
                           '\nFor example, a row of deflection measurements (mm) could be : 2 \t 7 \t 14' \
                           '\nWhen measurements from multiple load tests are available, include them in the same row with one measurement value in each column.' \
                           '\nEach column in the row is a deflection value measured by a sensor.' \
                           '\nFor more details and examples, see ''More Help'', Section 3.1.'

        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        self.help_doc_page = '14'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            pass

    # --------------------------------------------------------------------------
    # *** browse model predictions file ***
    def read_model_predictions(self):
        if self.checkboxvariable == 1:
            from f_read_model_predictions_excel_Geo import f_read_model_predictions_excel_Geo
            self.filename_modelpredictions = QtWidgets.QFileDialog.getOpenFileName()
            print('read done')
            try:
                self.pathnameprediction = str(self.filename_modelpredictions[0])
                self.PathForModelPredictions.setText(self.pathnameprediction)
                temp = f_read_model_predictions_excel_Geo(self.pathnameprediction)
                print(temp)
                self.number_predictions = temp[1]
                self.number_parameters = temp[0]
                self.number_ims_samples = temp[2]
                self.ims_parameters = temp[3]
                self.ims_predictions = temp[4]
                content_to_print = "Successfully uploaded data from initial model instances and predictions file.\n" \
                                   "Number of parameters: {} \nNumber of model prediction locations " \
                                   "(should be equal to number of measurements uploaded): {} \nNumber of " \
                                   "model instances uploaded: {}" \
                                   "\n\nInitial bounds of model parameters are the bounds of proability distribution assumed for each parameter varied in the uploaded file." \
                                   "For example, the first parameter in the uploaded file has a lower bound equal to {} and an upper bound equal to {}." \
                                   "\n\nInitial parameter bounds \t Min: {}" \
                                   "\t Max: {}".format(self.number_parameters,
                                                       self.number_predictions,
                                                       self.number_ims_samples,
                                                       np.min(self.ims_parameters[:, 0], 0),
                                                       np.max(self.ims_parameters[:, 0], 0),
                                                       np.min(self.ims_parameters, 0),
                                                       np.max(self.ims_parameters, 0))
                print('display done')
                print(content_to_print)

                self.ModelPredFileContents.setText(str(content_to_print))
            except:
                self.PathForModelPredictions.setText("Enter the path for file that contains predictions")
                self.ModelPredFileContents.clear()
                if self.filename_modelpredictions:
                    self.number_predictions = []
                    self.number_parameters = []
                    self.number_ims_samples = []
                    self.ims_parameters = []
                    self.ims_predictions = []

            from f_check_inputs import f_check_inputs
            self.checkinputs = f_check_inputs(self.filename_meas, self.filename_modelpredictions,
                                              self.filename_combuncertainties, self.measurements, self.ims_predictions,
                                              self.combined_uncertainties, self.checkboxvariable, self.numberofstage,
                                              self.numberofmeasurementperstage)
            print(self.checkinputs)
            return self.ims_parameters, self.ims_predictions
        else:
            from f_read_model_predictions_excel import f_read_model_predictions_excel
            self.filename_modelpredictions = QtWidgets.QFileDialog.getOpenFileName()
            try:
                self.pathnameprediction = str(self.filename_modelpredictions[0])
                self.PathForModelPredictions.setText(self.pathnameprediction)
                temp = f_read_model_predictions_excel(self.pathnameprediction)
                self.ims_parameters = np.ndarray.astype(temp['parameters'], int)
                self.ims_predictions = np.around(temp['predictions'], 2)
                self.number_predictions = np.shape(self.ims_predictions)[1]
                self.number_parameters = np.shape(self.ims_parameters)[1]
                self.number_ims_samples = np.shape(self.ims_predictions)[0]
                content_to_print = "Successfully uploaded data from initial model instances and predictions file.\n" \
                                   "Number of parameters: {} \nNumber of model prediction locations " \
                                   "(should be equal to number of measurements uploaded): {} \nNumber of " \
                                   "model instances uploaded: {}" \
                                   "\n\nInitial bounds of model parameters are the bounds of proability distribution assumed for each parameter varied in the uploaded file." \
                                   "For example, the first parameter in the uploaded file has a lower bound equal to {} and an upper bound equal to {}." \
                                   "\n\nInitial parameter bounds \t Min: {}" \
                                   "\t Max: {}".format(self.number_parameters,
                                                       self.number_predictions,
                                                       self.number_ims_samples,
                                                       np.min(self.ims_parameters[:, 0], 0),
                                                       np.max(self.ims_parameters[:, 0], 0),
                                                       np.min(self.ims_parameters, 0),
                                                       np.max(self.ims_parameters, 0))
                print(content_to_print)

                self.ModelPredFileContents.setText(str(content_to_print))
            except:
                self.PathForModelPredictions.setText("Enter the path for file that contains predictions")
                self.ModelPredFileContents.clear()
                if self.filename_modelpredictions:
                    self.number_predictions = []
                    self.number_parameters = []
                    self.number_ims_samples = []
                    self.ims_parameters = []
                    self.ims_predictions = []

            from f_check_inputs import f_check_inputs
            self.checkinputs = f_check_inputs(self.filename_meas, self.filename_modelpredictions,
                                              self.filename_combuncertainties, self.measurements, self.ims_predictions,
                                              self.combined_uncertainties, self.checkboxvariable, self.numberofstage,
                                              self.numberofmeasurementperstage)

            print(self.checkinputs)
            return self.ims_parameters, self.ims_predictions

    # *** help regarding predictions file ***
    def help_read_predictions_file(self):
        brief_text = 'Provide as input an excel file (.xlsx) that contains the initial model instances and predictions at measurement each location.'
        informative_text = 'The file provided should have columns = number of parameters (p) + number of measurement locations (m).' \
                           '\nEach row includes one instance of model evaluation (input parameters and output model predictions). ' \
                           'The first p-columns in a row correspond to the parameter values provided as input to the physics-based model. ' \
                           'These initial model instances form the initial model set (IMS). The subsequent m-columns in a row are model ' \
                           'predictions (in same order as measurements provided as input). The number of rows is equal to number of ' \
                           'simulations that are sampled using the model. For appropriate identification, the parameter space should be explored sufficiently. ' \
                           '\nFor more details, refer to "More Help", Section 3.2.'

        print(informative_text)
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        self.help_doc_page = '16'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        self.returnValue = self.msgBox.exec()
        if self.returnValue == QtWidgets.QMessageBox.Ok:
            pass

    # --------------------------------------------------------------------------
    # *** browse uncertainties file ***
    def read_uncertainties(self):
        if self.checkboxvariable == 1:
            self.filename_combuncertainties = QtWidgets.QFileDialog.getOpenFileName()
            try:
                from f_checkuncertainty_Geo import checkuncertainty_Geo
                self.pathnameuncertainty_Geo = str(self.filename_combuncertainties[0])
                self.checkuncertainty_Geo_data = checkuncertainty_Geo(self.pathnameuncertainty_Geo)
                print('Read geotechnical uncertainties')
                self.PathForUncertainties.setText(self.pathnameuncertainty_Geo)
                content_to_print_Geo = 'You have selected the excel file for geotechnical analysis. \n \
                Number of measurements per excavation stage: {} \n \
                Number of excavation stages: {}'.format(self.checkuncertainty_Geo_data[0],
                                                        self.checkuncertainty_Geo_data[1])
                self.UncertaintiesFileContent.setText(str(content_to_print_Geo))
                self.numberofstage = self.checkuncertainty_Geo_data[1]
                self.numberofmeasurementperstage = self.checkuncertainty_Geo_data[0]
            except:
                self.PathForUncertainties.setText("Enter the path for file that contains uncertainties")
                self.UncertaintiesFileContent.clear()
                if self.filename_combuncertainties:
                    self.combined_uncertainties = []
            from f_check_inputs import f_check_inputs
            self.checkinputs = f_check_inputs(self.filename_meas, self.filename_modelpredictions,
                                              self.filename_combuncertainties, self.measurements, self.ims_predictions,
                                              self.combined_uncertainties, self.checkboxvariable, self.numberofstage,
                                              self.numberofmeasurementperstage)
            print(self.checkinputs)
            return self.pathnameuncertainty_Geo
        else:
            print('Read default uncertainties')
            import matplotlib.pyplot as plt
            from f_read_uncertainties_excel import f_read_uncertainties_excel
            self.filename_combuncertainties = QtWidgets.QFileDialog.getOpenFileName()
            try:
                pathname = str(self.filename_combuncertainties[0])
                print(pathname)
                self.PathForUncertainties.setText(pathname)
                num_sources, self.combined_uncertainties = f_read_uncertainties_excel(pathname)
                number_measurements_unc = np.shape(self.combined_uncertainties)[1]
                number_combunc_samples = np.shape(self.combined_uncertainties)[0]
                content_to_print = 'Number of uncertainty sources provided as input at each measurement location:  {}' \
                                   '\n\nInput uncertainty distributions from various sources are sampled using Monte Carlo sampling. Samples of uncertainties from multiple sources at each measurement location are added together to obtain the combined uncertainty at each measurement location. \nThe combined uncertainty is used to calculate thresholds, which are then used to assess compatibility between model predictions and measurements. The number of uncertainty samples generated affects the calculation of threshold values (numerical errors)' \
                                   '\n\nNumber of uncertainty samples generated:  {}' \
                                   '\n\nTypically, the most important source of uncertainty is modelling assumptions. Parameters in the model that are important to model response are selected in the model class for updating. Uncertainty in model response related to model parameters not included in the model class for updating has to be included in uncerainty estimation along with other sources such as measurement noise.'.format(
                    num_sources, number_combunc_samples)
                self.UncertaintiesFileContent.setText(str(content_to_print))
            except:
                self.PathForUncertainties.setText(
                    "Enter the path for file that contains uncertainty definitions at sensor locations")
                self.UncertaintiesFileContent.clear()
                if self.filename_combuncertainties:
                    self.combined_uncertainties = []
            from f_check_inputs import f_check_inputs
            self.checkinputs = f_check_inputs(self.filename_meas, self.filename_modelpredictions,
                                              self.filename_combuncertainties, self.measurements, self.ims_predictions,
                                              self.combined_uncertainties, self.checkboxvariable, self.numberofstage,
                                              self.numberofmeasurementperstage)
            print(self.checkinputs)
            return self.combined_uncertainties

    #  *** help regarding uncertainties file ***
    def help_read_uncertainties_file(self):
        brief_text = 'Provide as input an excel file (.xlsx) that contains uncertainty definitions.'
        informative_text = 'The file provided should have as many excel sheets as number of uncertainty sources. ' \
                           'One excel sheet for each source of uncertainty .' \
                           '\nEach excel sheet provides estimation of each source uncertainty for all measurement locations.' \
                           '\nThe first row should be as: \nSensor Index \tDistribution type \tDistribution Param1 (eg: lower bound) \tDistribution Param2 (eg: upper bound) ' \
                           '\nSecond row onwards, each row should provide the uncertainty distribution details.' \
                           '\nIf the distribution type is "normal", then Distribution Param1 is "mean" and Distribution Param2 is "standard deviation".' \
                           '\nFor more details, refer to "Help", Section 3.3.'

        print(informative_text)
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        if self.checkboxvariable == 0:
            self.help_doc_page = '18'
        else:
            self.help_doc_page = '20'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            pass

    # --------------------------------------------------------------------------
    # *** EDMF ***
    def falsify_models(self):
        if self.checkboxvariable == 1:
            plt.close('all')
            from f_calculate_uncertainty_Geo import calculateuncertainty
            self.Uncertaintyresults_Geo = calculateuncertainty(self.number_measurements, self.number_ims_samples,
                                                               self.pathnameuncertainty_Geo, self.pathnameprediction)
            from f_EDMF_Geo import EDMFanalysis
            self.EDMFresults_Geo = EDMFanalysis(self.number_measurements, self.number_ims_samples, self.Uncertaintyresults_Geo[0],
                                                self.Uncertaintyresults_Geo [1],[],
                                                self.pathnameprediction, self.pathnamemeasurement, 0.95,
                                                1, [])
            print('EDMF done')

            ################################################################################
            ################################################################################
            self.cms = self.EDMFresults_Geo[4]
            print(self.cms)
            self.is_candidate = self.EDMFresults_Geo[2]
            print(self.is_candidate)
            ####I call the variables that you need from my function so that I do not need to change
            ####anything to my function. In this fasify_models function, from "content_to_print" onward,
            ####the code is formatted exactly the same for both applications. You should be able to simplify
            ####this function. I will also do this for validation parts and what-if parts.
            ##################################################################################
            ################################################################################
            if self.cms.shape[0] == 0:
                mincms = 0
                maxcms = 0
            else:
                mincms = np.min(self.cms, 0)
                maxcms = np.max(self.cms, 0)
            content_to_print = 'Number of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                               '\nFalsification rate = (Number of initial ' \
                               'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                               '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                               'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                               '\n\n An unexpectedly high falsification rate could also be due to:\n' \
                               '- Outliers in measurement data\n' \
                               '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                               '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                               'A low falsification rate could be indicative of:\n' \
                               '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                               '- Conservative estimations of uncertainties\n\n' \
                               'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                               'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                               ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses that are compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                .format(
                self.number_ims_samples,
                self.cms.shape[0],
                np.round((self.number_ims_samples - self.cms.shape[0]) * 100 / self.number_ims_samples, 2),
                mincms,
                maxcms)
            self.summary_for_edmf_2.setText(str(content_to_print))
        else:
            print('Default EDMF analysis')
            from f_falsify_models import f_falsify_models
            from f_norm_scale import f_norm_scale
            try:
                self.cms, self.is_candidate = f_falsify_models(self.ims_parameters, self.ims_predictions,
                                                               self.combined_uncertainties, self.measurements, 0.95,
                                                               1, [], [])
                if self.cms.shape[0] == 0:
                    mincms = 0
                    maxcms = 0
                else:
                    mincms = np.min(self.cms, 0)
                    maxcms = np.max(self.cms, 0)

                content_to_print = 'Number of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                   '\nFalsification rate = (Number of initial ' \
                                   'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                   '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                   'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                                   '\n\n An unexpectedly high falsification rate could also be due to:\n' \
                                   '- Outliers in measurement data\n' \
                                   '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                   '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                   'A low falsification rate could be indicative of:\n' \
                                   '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                   '- Conservative estimations of uncertainties\n\n' \
                                   'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                                   'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                   ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses that are compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                    .format(
                    self.number_ims_samples,
                    self.cms.shape[0],
                    np.round((self.number_ims_samples - self.cms.shape[0]) * 100 / self.number_ims_samples, 2),
                    mincms,
                    maxcms)
                self.summary_for_edmf_2.setText(str(content_to_print))
            except:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setText("Check inputs entered in Inputs tab")
                self.msgBox.setInformativeText("Unable to perform EDMF. Check inputs provided.")
                self.msgBox.setWindowTitle('WARNING!')
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.buttonClicked.connect(self.msgButtonClick)
                returnValue = self.msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass

        if self.checkboxvariable == 1 and len(self.EDMFresults_Geo[4]) != 0:
            print('Geotechnical EDMF analsysis')
            from f_postanalysis_Geo import postanalysisplot
            self.postresults = postanalysisplot(self.EDMFresults_Geo, self.Uncertaintyresults_Geo,
                                                self.checkuncertainty_Geo_data[1],
                                                self.checkuncertainty_Geo_data[0])
            print('EDMF is Completed')

        elif self.checkboxvariable == 0 and len(self.cms) != 0:
            print("Default analysis selection")
            from f_parallel_axis_plot import f_parallel_axis_plot
            f_parallel_axis_plot(self.ims_parameters, self.cms)
            plt.show()
            print("Plot generated")

        elif self.checkboxvariable == 1 and self.checkinputs['value'] == True and len(self.EDMFresults_Geo[4]) == 0:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.setText("Candidate model set is empty")
            self.msgBox.setInformativeText(
                "Check uncertainty estimations, model class for identification and analyse for outliers in data.")
            self.msgBox.setWindowTitle('WARNING!')
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msgBox.buttonClicked.connect(
                self.msgButtonClick)  # print("Candidate model set is empty. Revise uncertainty estimations and model class for identification.")
            returnValue = self.msgBox.exec()
            if returnValue == QtWidgets.QMessageBox.Ok:
                pass

        elif self.checkboxvariable == 0 and self.checkinputs['value'] == True and len(self.cms) == 0:
            self.msgBox = QtWidgets.QMessageBox()
            self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
            self.msgBox.setText("Candidate model set is empty")
            self.msgBox.setInformativeText(
                "Check uncertainty estimations, model class for identification and analyse for outliers in data.")
            self.msgBox.setWindowTitle('WARNING!')
            self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.msgBox.buttonClicked.connect(
                self.msgButtonClick)  # print("Candidate model set is empty. Revise uncertainty estimations and model class for identification.")
            returnValue = self.msgBox.exec()
            if returnValue == QtWidgets.QMessageBox.Ok:
                pass

        else:
            pass

    # *** help perform EDMF ***
    def help_perform_edmf(self):
        brief_text = 'Perform data-interpretation using error-domain model falsification'
        informative_text = 'Error-domain model falsification rejects model instances uploaded by user that exhibit ' \
                           'behaviour (response) that is incompatible with measurements (observations). The criteria for ' \
                           'compatibility is determined based on the reliability of identification.' \
                           '\nRefer to Section 4 in "Help" for more details on performing EDMF. '

        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        self.help_doc_page = '23'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            pass

    # --------------------------------------------------------------------------
    # *** hold out cross validation ***
    def validate_holdout(self):
        if self.checkboxvariable == 1:
            print('Validation of geotechnical EDMF analysis')
            plt.close('all')
            input_text = self.get_holdout_indices.text()
            try:
                from f_get_validation_index import get_validate_indice
                validation_indices = get_validate_indice(input_text)
                print(validation_indices)

                if np.amax(validation_indices) > self.number_measurements or np.amin(validation_indices) <= 0:
                    self.show_message_box("Indices exceed the maximum or minimum number of measurements", "Warning")
                else:
                    from f_calculate_uncertainty_Geo import calculateuncertainty
                    self.Uncertaintyresults_Geo_Validation = calculateuncertainty(self.number_measurements,
                                                                                  self.number_ims_samples,
                                                                                  self.pathnameuncertainty_Geo,
                                                                                  self.pathnameprediction)
                    print('Uncertainty Calculation is Completed')
                    from f_EDMF_Geo import EDMFanalysis
                    self.EDMFresults_Geo_Validation = EDMFanalysis(self.number_measurements,
                                                                   self.number_ims_samples,self.Uncertaintyresults_Geo_Validation[0],
                                                                   self.Uncertaintyresults_Geo_Validation[1],
                                                                   validation_indices, self.pathnameprediction,
                                                                   self.pathnamemeasurement, 0.95,
                                                                   1, self.get_holdout_indices.text())
                    print('EDMF is Completed')
                    ####################################################################
                    ####################################################################
                    holdout_cms = self.EDMFresults_Geo_Validation[4]
                    holdout_is_candidate = self.EDMFresults_Geo_Validation[2]
                    ####################################################################
                    ####################################################################
                    #############a new function for my application. It produces the results necessary
                    ############for precision and accuracy calculation
                    from f_holdout_validation_Geo import holdout_validation_Geo
                    cms_bounds, ims_bounds, validation_measurements, validation_check_cms, validation_check_ims \
                        = holdout_validation_Geo(self.EDMFresults_Geo_Validation,
                                                 self.Uncertaintyresults_Geo_Validation,
                                                 self.checkuncertainty_Geo_data[1],
                                                 self.checkuncertainty_Geo_data[0],
                                                 validation_indices)

                    precision = np.round((np.mean(
                        np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))) - np.mean(
                        np.diff(cms_bounds) / np.transpose(np.absolute(validation_measurements)))) / np.mean(
                        np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))), 2) * 100
                    accuracy = np.sum(validation_check_cms) * 100 / validation_measurements.shape[1]
                    ####################################################################
                    ####################################################################
                    ####from "content_to_print" onward,
                    ####the code is formatted exactly the same for both applications. You should be able to simplify
                    ####this function. I will also do this for validation parts and what-if parts..
                    ##################################################################################
                    ################################################################################
                    if holdout_cms.shape[0] == 0:
                        mincms = 0
                        maxcms = 0
                    else:
                        mincms = np.min(holdout_cms, 0)
                        maxcms = np.max(holdout_cms, 0)
                    content_to_print = 'Number of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                       '\nFalsification rate = (Number of initial ' \
                                       'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                       '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                       'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                                       'An unexpectedly high falsification rate could also be due to:\n' \
                                       '- Outliers in measurement data\n' \
                                       '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                       '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                       'A low falsification rate could be indicative of:\n' \
                                       '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                       '- Conservative estimations of uncertainties\n\n' \
                                       'Precision of structural identification (Average reduction in prediction uncertainty): {} %' \
                                       '\nAccuracy of structural identification (Number of cases where updated predictions include measurement value out of all measurements left out): {} %' \
                                       'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                                       'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                       '\n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses that are compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                                       '\n\nSee figure "Cross-Validation Plot" for visualization of cross-validation results. ' \
                                       '\nIn the figure,\nIMS predictions: Initial model set predictions' \
                                       '(predictions with prior parameter ranges)' \
                                       '\nCMS predictions: Candidate model set predictions with parameter instances ' \
                                       'that exhibit behaviour that is compatible with observations, as assessed using ' \
                                       'EDMF.\nMeasurement: Recorded measurement value at location ' \
                                       'held out from interpretation' \
                                       '\nIf the solutions obtained are found to be accurate based on cross-validation, then the validated CMS may be used to predict structural response at unmeasured locations under new and future scenarios to support decision making.' \
                        .format(
                        self.number_ims_samples,
                        holdout_cms.shape[0],
                        np.round((self.number_ims_samples - holdout_cms.shape[0]) * 100 / self.number_ims_samples, 2),
                        mincms,
                        maxcms, precision, accuracy)
                    self.summary_validation_results.setText(str(content_to_print))
                    if len(self.EDMFresults_Geo_Validation[4]) != 0:
                        from f_postanalysis_validation_Geo import postanalysisplot_validation
                        self.postresults_val = postanalysisplot_validation(self.EDMFresults_Geo_Validation,
                                                                           self.Uncertaintyresults_Geo_Validation,
                                                                           self.checkuncertainty_Geo_data[1],
                                                                           self.checkuncertainty_Geo_data[0],
                                                                           validation_indices)
                    else:
                        self.show_message_box("All initial model instances are falsified", "Warning")
                        content_to_print = 'Numer of candidate models: 0'
                        self.summary_for_edmf_2.setText(str(content_to_print))
            except:
                self.show_message_box(
                    "Indices are not entered according to the prescribed format. Refer to 'What's this?' for more information",
                    "Error")

        else:
            print('Validation of default EDMF analysis')
            from f_falsify_models import f_falsify_models
            from f_holdout_validation import f_holdout_validation
            from f_plot_holdout_validation import f_plot_holdout_validation
            # read input indices and covert to numpy array
            try:
                input_text = self.get_holdout_indices.text()
                from f_get_validation_index import get_validate_indice
                validation_indices = get_validate_indice(input_text) - 1
                print(validation_indices)

                if len(validation_indices) != 0:
                    # perform edmf excluding sensors held out for validation
                    holdout_cms, holdout_is_candidate = f_falsify_models(self.ims_parameters, self.ims_predictions,
                                                                         self.combined_uncertainties, self.measurements,
                                                                         0.95, 1,
                                                                         validation_indices,
                                                                         self.get_holdout_indices.text())
                    if len(holdout_cms) != 0:
                        cms_bounds, ims_bounds, validation_measurements, validation_check_cms, validation_check_ims = \
                            f_holdout_validation(self.ims_predictions, holdout_is_candidate,
                                                 self.combined_uncertainties,
                                                 self.measurements, 1, validation_indices)
                        from f_parallel_axis_plot import f_parallel_axis_plot
                        plt.close('all')
                        f_parallel_axis_plot(self.ims_parameters, holdout_cms)
                        precision = np.round((np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))) - np.mean(
                            np.diff(cms_bounds) / np.transpose(np.absolute(validation_measurements)))) / np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))), 2) * 100
                        accuracy = np.sum(validation_check_cms) * 100 / validation_measurements.shape[1]
                        if holdout_cms.shape[0] == 0:
                            mincms = 0
                            maxcms = 0
                        else:
                            mincms = np.min(holdout_cms, 0)
                            maxcms = np.max(holdout_cms, 0)
                        content_to_print = 'Number of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                           '\nFalsification rate = (Number of initial ' \
                                           'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                           '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                           'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                                           'An unexpectedly high falsification rate could also be due to:\n' \
                                           '- Outliers in measurement data\n' \
                                           '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                           '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                           'A low falsification rate could be indicative of:\n' \
                                           '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                           '- Conservative estimations of uncertainties\n\n' \
                                           'Precision of structural identification (Average reduction in prediction uncertainty): {} %' \
                                           '\nAccuracy of structural identification (Number of cases where updated predictions include measurement value out of all measurements left out): {} %' \
                                           'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                                           'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                           '\n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses that are compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                                           '\n\nSee figure "Cross-Validation Plot" for visualization of cross-validation results. ' \
                                           '\nIn the figure,\nIMS predictions: Initial model set predictions' \
                                           '(predictions with prior parameter ranges)' \
                                           '\nCMS predictions: Candidate model set predictions with parameter instances ' \
                                           'that exhibit behaviour that is compatible with observations, as assessed using ' \
                                           'EDMF.\nMeasurement: Recorded measurement value at location ' \
                                           'held out from interpretation' \
                                           '\nIf the solutions obtained are found to be accurate based on cross-validation, then the validated CMS may be used to predict structural response at unmeasured locations under new and future scenarios to support decision making.' \
                            .format(
                            self.number_ims_samples,
                            holdout_cms.shape[0],
                            np.round((self.number_ims_samples - holdout_cms.shape[0]) * 100 / self.number_ims_samples,
                                     2),
                            mincms,
                            maxcms, precision, accuracy)
                        self.summary_validation_results.setText(str(content_to_print))
                        f_plot_holdout_validation(cms_bounds, ims_bounds, validation_measurements, validation_indices)
                    elif len(holdout_cms) == 0:
                        self.msgBox = QtWidgets.QMessageBox()
                        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                        self.msgBox.setText("No candidate models found")
                        self.msgBox.setInformativeText(
                            "Check uncertainty estimations provided as input and the model class. No candidate models "
                            "were found for measurements included to perform EDMF.")
                        self.msgBox.setWindowTitle('WARNING!')
                        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msgBox.buttonClicked.connect(self.msgButtonClick)
                        returnValue = self.msgBox.exec()
                        if returnValue == QtWidgets.QMessageBox.Ok:
                            pass
            except:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setText("Input validation indices")
                self.msgBox.setInformativeText(
                    "Input validation indices in the correct format (separator = ' ,'). \nFor example: 1, 2, 10, 30")
                self.msgBox.setWindowTitle('WARNING!')
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.buttonClicked.connect(self.msgButtonClick)
                returnValue = self.msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass
        return self.cms, self.is_candidate

    def help_perform_validate(self):
        brief_text = 'Perform holdout validation with one/multiple sensors.'
        informative_text = 'Please enter the indices of measurements to be excluded for validation. Two types of formats are permitted:' \
                           '\nEnter the indices of measurements and separate them by a comma, e.g. 1,3,15.' \
                           '\nEnter the indices of groups of measurements, e.g. 1-10' \
                           '\nThe combination of these two formats is also permitted, e.g. 1-10,16,18,20-28.'

        print(informative_text)
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        self.help_doc_page = '28'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            pass

    # --------------------------------------------------------------------------
    # *** Get value of Phi for EDMF from slider ***
    def get_phi_value(self, value):
        if value == 10:
            self.phi = 0.99
        elif value < 10:
            self.phi = value * 0.05 + 0.5
        else:
            self.phi = 0.95
        print(self.phi)

    # --------------------------------------------------------------------------
    # *** Uncertainty amplifier value ***
    def get_uncamplifier_value(self, value):
        self.unc_amplifier = value * 0.1 + 0.5
        print(self.unc_amplifier)

    #####save session
    def save_all_variables(self):
        option = QtWidgets.QFileDialog.Options()
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "All Files(*)",
                                                     options=option)
        filename = file[0]
        my_shelf = shelve.open(filename, 'n')  # 'n' for new

        for key in dir(InterfaceWindow):
            if not inspect.ismodule(globals()[key]):
                my_shelf[key] = globals()[key]

    # --------------------------------------------------------------------------
    # *** Repeform EDMF ***
    def reperform_edmf(self):
        if self.checkboxvariable == 1:
            print('Geotechnical EDMF analsysis')
            plt.close('all');
            from f_calculate_uncertainty_Geo import calculateuncertainty
            self.Uncertaintyresults_Geo = calculateuncertainty(self.number_measurements, self.number_ims_samples,
                                                               self.pathnameuncertainty_Geo, self.pathnameprediction)
            print('Uncertainty Calculation is Completed')
            from f_EDMF_Geo import EDMFanalysis
            self.EDMFresults_Geo_Re = EDMFanalysis(self.number_measurements, self.number_ims_samples, self.Uncertaintyresults_Geo[0],
                                                   self.Uncertaintyresults_Geo[1],[],
                                                   self.pathnameprediction, self.pathnamemeasurement, self.phi,
                                                   self.unc_amplifier, [])
            print('EDMF is Completed')
            ################################################################################
            ################################################################################
            self.cms = self.EDMFresults_Geo_Re[4]
            self.is_candidate = self.EDMFresults_Geo_Re[2]
            ####I call the variables that you need from my function so that I do not need to change
            ####anything to my function. In this fasify_models function, from "content_to_print" onward,
            ####the code is formatted exactly the same for both applications. You should be able to simplify
            ####this function. I will also do this for validation parts and what-if parts.
            ##################################################################################
            ################################################################################
            if self.cms.shape[0] == 0:
                mincms = 0
                maxcms = 0
            else:
                mincms = np.min(self.cms, 0)
                maxcms = np.max(self.cms, 0)

            content_to_print = 'EDMF SUMMARY' \
                               '\nTarget reliability of identification chosen: {}' \
                               '\nMultiply uncertainty provided in the input uncertainties file by factor: {}' \
                               '\nNumber of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                               '\nFalsification rate = (Number of initial model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                               '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                               'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                               'An unexpectedly high falsification rate could also be due to:\n' \
                               '- Outliers in measurement data\n' \
                               '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                               '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                               'A low falsification rate could be indicative of:\n' \
                               '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                               '- Conservative estimations of uncertainties\n\n' \
                               'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                               'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                               ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                .format(self.phi, np.round(self.unc_amplifier, 2), self.number_ims_samples, self.cms.shape[0],
                        np.round((self.number_ims_samples - self.cms.shape[0]) * 100 / self.number_ims_samples, 2),
                        mincms,
                        maxcms)
            self.summary_whatif.setText(str(content_to_print))
            if len(self.EDMFresults_Geo_Re[4]) != 0:
                print('Geotechnical EDMF analsysis')
                from f_postanalysis_Geo import postanalysisplot
                self.postresults = postanalysisplot(self.EDMFresults_Geo_Re, self.Uncertaintyresults_Geo,
                                                    self.checkuncertainty_Geo_data[1],
                                                    self.checkuncertainty_Geo_data[0])
                print('EDMF is Completed')
            else:
                self.show_message_box("All initial model instances are falsified", "Warning")
                content_to_print = 'Numer of candidate models: 0'
                self.summary_for_edmf_2.setText(str(content_to_print))
        else:
            from f_falsify_models import f_falsify_models
            plt.close('all')
            from f_norm_scale import f_norm_scale
            try:
                self.cms, self.is_candidate = f_falsify_models(self.ims_parameters, self.ims_predictions,
                                                               self.combined_uncertainties, self.measurements, self.phi,
                                                               self.unc_amplifier, [], [])
                if self.cms.shape[0] == 0:
                    mincms = 0
                    maxcms = 0
                else:
                    mincms = np.min(self.cms, 0)
                    maxcms = np.max(self.cms, 0)

                content_to_print = 'EDMF SUMMARY' \
                                   '\nTarget reliability of identification chosen: {}' \
                                   '\nMultiply uncertainty provided in the input uncertainties file by factor: {}' \
                                   '\nNumber of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                   '\nFalsification rate = (Number of initial model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                   '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                   'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                                   'An unexpectedly high falsification rate could also be due to:\n' \
                                   '- Outliers in measurement data\n' \
                                   '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                   '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                   'A low falsification rate could be indicative of:\n' \
                                   '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                   '- Conservative estimations of uncertainties\n\n' \
                                   'See figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set. \n\n' \
                                   'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                   ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                    .format(
                    self.phi,
                    np.round(self.unc_amplifier, 2),
                    self.number_ims_samples,
                    self.cms.shape[0],
                    np.round((self.number_ims_samples - self.cms.shape[0]) * 100 / self.number_ims_samples, 2),
                    mincms,
                    maxcms)
                self.summary_whatif.setText(str(content_to_print))
            except:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setText("Check inputs entered in Inputs tab")
                self.msgBox.setInformativeText("Unable to perform EDMF. Check inputs provided.")
                self.msgBox.setWindowTitle('WARNING!')
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.buttonClicked.connect(self.msgButtonClick)
                returnValue = self.msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass

            if self.checkboxvariable == 0 and len(self.cms) != 0:
                print("Default analysis selection")
                from f_parallel_axis_plot import f_parallel_axis_plot
                f_parallel_axis_plot(self.ims_parameters, self.cms)
                plt.show()
                print("Plot generated")

            else:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                self.msgBox.setText("Candidate model set is empty")
                self.msgBox.setInformativeText("Revise uncertainty estimations and model class for identification.")
                self.msgBox.setWindowTitle('WARNING!')
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.buttonClicked.connect(self.msgButtonClick)
                # print("Candidate model set is empty. Revise uncertainty estimations and model class for identification.")
                returnValue = self.msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass

    # --------------------------------------------------------------------------
    # *** Repeform Holdout validation ***
    def reperform_holdout(self):
        if self.checkboxvariable == 1:
            print('Validation of geotechnical EDMF analysis')
            plt.close('all')
            # input_text = self.get_holdout_indices.text()
            text, ok = QtWidgets.QInputDialog.getText(self, 'Holdout validation', 'Enter validation indices:')
            if ok:
                self.input_text_redo = text
                print(self.input_text_redo)
            try:
                if not self.input_text_redo:
                    validation_indices = []
                    self.show_message_box("No index is entered", "Warning")
                else:
                    from f_get_validation_index import get_validate_indice
                    validation_indices = get_validate_indice(self.input_text_redo)
                    print(validation_indices)

                    if np.amax(validation_indices) > self.number_measurements or np.amin(validation_indices) <= 0:
                        self.show_message_box("Indices exceed the maximum or minimum number of measurements", "Warning")
                    else:
                        from f_calculate_uncertainty_Geo import calculateuncertainty
                        self.Uncertaintyresults_Geo_Validation = calculateuncertainty(self.number_measurements,
                                                                                      self.number_ims_samples,
                                                                                      self.pathnameuncertainty_Geo,
                                                                                      self.pathnameprediction)
                        print('Uncertainty Calculation is Completed')
                        from f_EDMF_Geo import EDMFanalysis
                        self.EDMFresults_Geo_Validation_Re = EDMFanalysis(self.number_measurements,
                                                                          self.number_ims_samples,self.Uncertaintyresults_Geo_Validation[0],
                                                                          self.Uncertaintyresults_Geo_Validation[1],
                                                                          validation_indices, self.pathnameprediction,
                                                                          self.pathnamemeasurement, self.phi,
                                                                          self.unc_amplifier, self.input_text_redo)
                        print('EDMF is Completed')
                        ####################################################################
                        ####################################################################
                        holdout_cms = self.EDMFresults_Geo_Validation_Re[4]
                        holdout_is_candidate = self.EDMFresults_Geo_Validation_Re[2]
                        ####################################################################
                        ####################################################################
                        #############a new function for my application. It produces the results necessary
                        ############for precision and accuracy calculation
                        from f_holdout_validation_Geo import holdout_validation_Geo
                        cms_bounds, ims_bounds, validation_measurements, validation_check_cms, validation_check_ims \
                            = holdout_validation_Geo(self.EDMFresults_Geo_Validation,
                                                     self.Uncertaintyresults_Geo_Validation,
                                                     self.checkuncertainty_Geo_data[1],
                                                     self.checkuncertainty_Geo_data[0],
                                                     validation_indices)

                        precision = np.round((np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))) - np.mean(
                            np.diff(cms_bounds) / np.transpose(np.absolute(validation_measurements)))) / np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))), 2) * 100

                        accuracy = np.sum(validation_check_cms) * 100 / validation_measurements.shape[1]
                        ####################################################################
                        ####################################################################
                        ####from "content_to_print" onward,
                        ####the code is formatted exactly the same for both applications. You should be able to simplify
                        ####this function. I will also do this for validation parts and what-if parts.
                        ##################################################################################
                        ################################################################################
                        if holdout_cms.shape[0] == 0:
                            mincms = 0
                            maxcms = 0
                        else:
                            mincms = np.min(holdout_cms, 0)
                            maxcms = np.max(holdout_cms, 0)
                        content_to_print = 'VALIDATION SUMMARY' \
                                           '\n\nTarget reliability of identification chosen: {}' \
                                           '\nMultiply uncertainty provided in the input uncertainties file by factor: {}' \
                                           '\nNumber of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                           '\nFalsification rate = (Number of initial ' \
                                           'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                           '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                           'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation' \
                                           '\nAn unexpectedly high falsification rate could also be due to:\n' \
                                           '- Outliers in measurement data\n' \
                                           '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                           '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                           'A low falsification rate could be indicative of:\n' \
                                           '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                           '- Conservative estimations of uncertainties' \
                                           '\n\nPrecision of structural identification (Average reduction in prediction uncertainty): {} %' \
                                           '\nAccuracy of structural identification (Number of cases where updated predictions include measurement value out of all measurements left out): {} %' \
                                           '\n\nSee figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set obtained without using measurements retained for validation. \n\n' \
                                           'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                           ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                                           '\n\nSee figure "Cross-Validation Plot" for visualization of cross-validation results. ' \
                                           '\nIn the figure,\nIMS predictions: Initial model set predictions' \
                                           '(predictions with prior parameter ranges)' \
                                           '\nCMS predictions: Candidate model set predictions with parameter instances ' \
                                           'that exhibit behaviour that is compatible with observations, as assessed using ' \
                                           'EDMF.\nMeasurement: Recorded measurement value at location ' \
                                           'held out from interpretation' \
                                           '\nIf the solutions obtained are found to be accurate based on cross-validation, then the validated CMS may be used to predict structural response at unmeasured locations under new and future scenarios to support decision making.' \
                            .format(
                            np.round(self.phi, 2),
                            np.round(self.unc_amplifier, 2),
                            self.number_ims_samples,
                            holdout_cms.shape[0],
                            np.round((self.number_ims_samples - holdout_cms.shape[0]) * 100 / self.number_ims_samples,
                                     2),
                            mincms,
                            maxcms,
                            np.round(precision, 2), accuracy)
                        self.summary_whatif.setText(str(content_to_print))
                        if len(self.EDMFresults_Geo_Validation_Re[4]) != 0:
                            from f_postanalysis_validation_Geo import postanalysisplot_validation
                            self.postresults_val = postanalysisplot_validation(self.EDMFresults_Geo_Validation_Re,
                                                                               self.Uncertaintyresults_Geo_Validation,
                                                                               self.checkuncertainty_Geo_data[1],
                                                                               self.checkuncertainty_Geo_data[0],
                                                                               validation_indices)
                        else:
                            self.show_message_box("All initial model instances are falsified", "Warning")
            except:
                self.show_message_box(
                    "Indices are not entered according to the prescribed format. Refer to 'What's this?' for more information",
                    "Error")
        else:
            text, ok = QtWidgets.QInputDialog.getText(self, 'Holdout validation', 'Enter validation indices:')
            if ok:
                self.what_if_validation_text = text
                print(self.what_if_validation_text)

            try:
                from f_falsify_models import f_falsify_models
                from f_holdout_validation import f_holdout_validation
                from f_plot_holdout_validation import f_plot_holdout_validation
                # read input indices and covert to numpy array
                input_text = self.what_if_validation_text
                from f_get_validation_index import get_validate_indice
                validation_indices = get_validate_indice(input_text) - 1
                print(validation_indices)
                plt.close('all')
                if len(validation_indices) != 0:
                    # perform edmf excluding sensors held out for validation
                    holdout_cms, holdout_is_candidate = f_falsify_models(self.ims_parameters, self.ims_predictions,
                                                                         self.combined_uncertainties, self.measurements,
                                                                         self.phi, self.unc_amplifier,
                                                                         validation_indices,
                                                                         self.what_if_validation_text)
                    if len(holdout_cms) != 0:
                        cms_bounds, ims_bounds, validation_measurements, validation_check_cms, validation_check_ims = \
                            f_holdout_validation(self.ims_predictions, holdout_is_candidate,
                                                 self.combined_uncertainties,
                                                 self.measurements, self.unc_amplifier, validation_indices)
                        from f_parallel_axis_plot import f_parallel_axis_plot
                        f_parallel_axis_plot(self.ims_parameters, holdout_cms)

                        precision = np.round((np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))) - np.mean(
                            np.diff(cms_bounds) / np.transpose(np.absolute(validation_measurements)))) / np.mean(
                            np.diff(ims_bounds) / np.transpose(np.absolute(validation_measurements))), 2) * 100
                        accuracy = np.sum(validation_check_cms) * 100 / validation_measurements.shape[1]
                        if holdout_cms.shape[0] == 0:
                            mincms = 0
                            maxcms = 0
                        else:
                            mincms = np.min(holdout_cms, 0)
                            maxcms = np.max(holdout_cms, 0)

                        content_to_print = 'VALIDATION SUMMARY' \
                                           '\n\nTarget reliability of identification chosen: {}' \
                                           '\nMultiply uncertainty provided in the input uncertainties file by factor: {}' \
                                           '\nNumber of initial model instances provided:  {} \nNumber of candidate models: {} ' \
                                           '\nFalsification rate = (Number of initial ' \
                                           'model instances - Number of candidate models) * 100 / Number of initial model instances = {} % ' \
                                           '\n\nUpdated parameter bounds \nMinimum:\t{} \nMaximum:\t{}\n\n' \
                                           'A high falsification rate is indicative of informative measurements and good selection of parameters for data interpretation\n' \
                                           'An unexpectedly high falsification rate could also be due to:\n' \
                                           '- Outliers in measurement data\n' \
                                           '- Poor estimations of uncertainties and prior distributions of parameters\n' \
                                           '- Poor exploration of parameter spaces for solutions (insufficient samples of initial model instances)\n\n' \
                                           'A low falsification rate could be indicative of:\n' \
                                           '- Uninformative measurements with respect to parameters that were chosen for data interpretation\n' \
                                           '- Conservative estimations of uncertainties\n\n' \
                                           '\n\nPrecision of structural identification (Average reduction in prediction uncertainty): {} %' \
                                           '\nAccuracy of structural identification (Number of cases where updated predictions include measurement value out of all measurements left out): {} %' \
                                           '\n\nSee figure "Parallel Axis Plot - EDMF" for visualization of the candidate model set obtained without using measurements retained for validation. \n\n' \
                                           'A parallel axis plot is a tool (type of plot) to visualize a multi-dimensional space. In this plot, each dimension (parameter) is represented as a vertical axis. Lines connecting points on each of these vertical axis represent the coordinates of a point in the multi-dimensional space along each of these axis.' \
                                           ' \n\nIn the parallel axis plot, candidate model instances (candidate model set, CMS) identified using EDMF are shown as green lines. Model instances in the CMS provide responses compatible with measurements (within threshold bounds). Using instances in the CMS, the user may predict accurately structural behaviour for future scenarios to support decision making.' \
                                           '\n\nSee figure "Cross-Validation Plot" for visualization of cross-validation results. ' \
                                           '\nIn the figure,\nIMS predictions: Initial model set predictions' \
                                           '(predictions with prior parameter ranges)' \
                                           '\nCMS predictions: Candidate model set predictions with parameter instances ' \
                                           'that exhibit behaviour that is compatible with observations, as assessed using ' \
                                           'EDMF.\nMeasurement: Recorded measurement value at location ' \
                                           'held out from interpretation' \
                                           '\nIf the solutions obtained are found to be accurate based on cross-validation, then the validated CMS may be used to predict structural response at unmeasured locations under new and future scenarios to support decision making.' \
                            .format(
                            np.round(self.phi, 2),
                            np.round(self.unc_amplifier, 2),
                            self.number_ims_samples,
                            holdout_cms.shape[0],
                            np.round((self.number_ims_samples - holdout_cms.shape[0]) * 100 / self.number_ims_samples,
                                     2),
                            mincms,
                            maxcms,
                            np.round(precision, 2), accuracy)
                        self.summary_whatif.setText(str(content_to_print))
                        f_plot_holdout_validation(cms_bounds, ims_bounds, validation_measurements, validation_indices)
                        plt.show()
                    elif len(holdout_cms) == 0:
                        self.msgBox = QtWidgets.QMessageBox()
                        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
                        self.msgBox.setText("No candidate models found")
                        self.msgBox.setInformativeText(
                            "Check uncertainty estimations provided as input and the model class. No candidate models "
                            "were found for measurements included to perform EDMF.")
                        self.msgBox.setWindowTitle('WARNING!')
                        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        self.msgBox.buttonClicked.connect(self.msgButtonClick)
                        returnValue = self.msgBox.exec()
                        if returnValue == QtWidgets.QMessageBox.Ok:
                            pass
            except:
                self.msgBox = QtWidgets.QMessageBox()
                self.msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                self.msgBox.setText("Input validation indices")
                self.msgBox.setInformativeText(
                    "Input validation indices in the correct format (separator = ' ,'). \nFor example: 1, 2, 10, 30")
                self.msgBox.setWindowTitle('WARNING!')
                self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
                self.msgBox.buttonClicked.connect(self.msgButtonClick)
                returnValue = self.msgBox.exec()
                if returnValue == QtWidgets.QMessageBox.Ok:
                    pass

    def help_perform_whatif_scenarios(self):
        brief_text = 'Evaluate other possible scenarios.'
        informative_text = 'Use the sliders to vary uncertainty magnitudes and target reliability of identification' \
                           '\nUncertainty magnitudes are multiplied by the factor selected using the slider' \
                           '\nSee "Help" section XX for details on importance of target reliability of identification ' \
                           'and uncertainty on identification solutions. '

        print(informative_text)
        self.msgBox = QtWidgets.QMessageBox()
        self.msgBox.setWindowModality(True)
        self.msgBox.setIcon(QtWidgets.QMessageBox.Information)
        self.msgBox.setText(brief_text)
        self.msgBox.setInformativeText(informative_text)
        self.msgBox.setWindowTitle('Help!')
        self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Close | QtWidgets.QMessageBox.Help)
        buttonhelp = self.msgBox.button(QtWidgets.QMessageBox.Help)
        buttonhelp.setText('More Help')
        buttonok = self.msgBox.button(QtWidgets.QMessageBox.Close)
        buttonok.setText('Ok')
        self.help_doc_page = '32'
        self.msgBox.buttonClicked.connect(self.msgButtonClick)

        returnValue = self.msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            pass
