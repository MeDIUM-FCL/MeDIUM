from PyQt5 import QtWidgets
import numpy as np

def read_measurements(self):
    from f_read_measurements_excel import f_read_measurements_excel
    filename = QtWidgets.QFileDialog.getOpenFileName()
    try:
        pathnamemeasurement = str(filename[0])
        PathForMeasurements.setText(self.pathnamemeasurement)
        measurements = f_read_measurements_excel(self.pathnamemeasurement)
        size_of_var = np.shape(self.measurements)
        self.number_measurements = int(size_of_var[1])
        content_to_print = ' Number of measurements uploaded is: {}.'.format(self.number_measurements)
        MeasFileContents.setText(str(content_to_print))
    except:
        PathForMeasurements.setText("Enter path for file containing measurement data")
        MeasFileContents.clear()
    from f_check_inputs import f_check_inputs
    checkinputs = f_check_inputs(measurements, ims_predictions,
                                      combined_uncertainties, checkboxvariable, numberofstage,
                                      numberofmeasurementperstage)
    print(checkinputs)
    return measurements
