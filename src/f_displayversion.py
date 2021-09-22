from PyQt5 import QtWidgets


def displayversion(self):
    # brief_text = 'MeDIUM \n Measurement Data Interpretation using Uncertain Models \n for \nSafe and Sustainable Asset Management'
    brief_text = '<!DOCTYPE html> <title>Text Example</title> <style> div.container { } div.container p { text-align: ' \
                 'center; font-family: Arial; font-size: 12px;font-style: normal;font-weight: bold;text-decoration: ' \
                 'none;text-transform: none; } </style><div class="container"> <p>MeDIUM</p> <p>Measurement Data ' \
                 'Interpretation using Uncertain Models</p> <p>for </p> <p>Safe and Sustainable Asset Management</p> <p ' \
                 'align="left" style=" margin-top:10px; margin-bottom:50px; margin-left:0px; margin-right:0px; ' \
                 '-qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; ' \
                 'font-size:8.25pt; font-style: normal; font-weight: normal; ">MeDIUM is a software implementation of a methodology called error-domain model falsification (EDMF), with additions to perform cross-validation and what-if analysis.</span></p>' \
                 '</div> '
    informative_text = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" ' \
                       '"http://www.w3.org/TR/REC-html40/strict.dtd"> <html><head><meta name="qrichtext" content="1" ' \
                       '/><style type="text/css"> p, li { white-space: pre-wrap; } </style></head><body style=" ' \
                       'font-family:''MS Shell Dlg 2''; font-size:8pt; font-weight:400; font-style:normal;"> <p ' \
                       'align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; ' \
                       '-qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; ' \
                       'font-size:8.25pt; font-weight:600;">Acknowledgements</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Numa Bertola</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">James Brownjohn</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Eugen Brühwiler</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Wenjun Cao</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Alberto Costa</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">James A. Goulet</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Alain Nussbamer</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Maria Papadopolou</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Romain Pasquier</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Marco Proverbio</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Yves Reuland</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Didier Vernay</span></p> ' \
                       '<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:''MS Shell Dlg 2''; font-size:8.25pt;"><br /></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt; font-weight:600;">Industry and Research Partners</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Main Roads Western Australia</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Curtin University, Australia</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Indian Institute of Technology, Madras, India </span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Land Transport Authority, Singapore</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">University of Cambridge, UK</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">University of Exeter, UK</span></p>' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Tufts University, USA</span></p>' \
                       '<p align="center" style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:''MS Shell Dlg 2''; font-size:8.25pt;"><br /></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt; font-weight:600;">Funding</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Singapore-ETH Center (SEC) (Contract no. FI 370074011-370074016)</span></p> ' \
                       '<p align="center" style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:''MS Shell Dlg 2''; font-size:8.25pt;">Swiss National Science Foundation (Contract no. 200020-169026)</span></p></body></html>'

    self.msgBox = QtWidgets.QMessageBox()
    self.msgBox.setWindowModality(False)
    self.msgBox.setIcon(QtWidgets.QMessageBox.NoIcon)
    self.msgBox.setText(brief_text)
    self.msgBox.setInformativeText(informative_text)
    self.msgBox.setWindowTitle('About')
    self.msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
    self.msgBox.buttonClicked.connect(self.msgButtonClick)
    returnValue = self.msgBox.exec()
    if returnValue == QtWidgets.QMessageBox.Ok:
        pass
