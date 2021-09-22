def holdout_validation_Geo(EDMFresults,Uncertaintyresults,
                                numberofexcavationstage,numberofmeasurementperstage,
                                ID_excluded):
    """
        Check with information from held out sensors whether canidate instances are valid

        Developed by :   WANG Ze-Zhou (ETH Singapore)
        Contact :        e0054291@u.nus.edu
        Date:            August 24, 2020

        INPUTS:
            EDMFresults : Results of EDMF analysis
            Uncertaintyresults : Results of geotechnical uncertainty calculation
            numberofexcavationstage: number of excavation stages
            numberofmeasurementperstage : number of measurements per excavation stage
            ID_excluded: index of measurement to be excluded from the cros-validation analysis.

        OUTPUTS:
            cms_bounds : Bounds of predictions by candidate model instances at validation measurement points; Size number_validation_indices x 2
            ims_bounds : Bounds of predictions by initial model instances at validation measurement points; Size number_validation_indices x 2
            validation_measurements : Measured value at validation points
            validation_check_cms : Logical array indicating whether bounds of candidate model predictions include measured value
            validation_check_ims : Logical array indicating whether bounds of initial model predictions include measured value

        NOTE:

        """

    import matplotlib.pyplot as plt
    import numpy as np
    import math

    #####post analysis
    Uncertaintymean = Uncertaintyresults[0]
    Uncertaintystd = Uncertaintyresults[1]
    Prediction2D = EDMFresults[0]
    Measurement = EDMFresults[1]
    falsificationresults = EDMFresults[2]
    IMS = EDMFresults[3]

    ########CMS
    CMSID = np.where(falsificationresults == 1)
    CMS = IMS[CMSID[0], :]

    ########prediction and measurement
    CMSprediction2D = Prediction2D[CMSID[0], :]
    CMSuncertaintymean = Uncertaintymean[CMSID[0], :]
    CMSuncertaintystd = Uncertaintystd[CMSID[0], :]
    CMSprediction3D = CMSprediction2D - CMSuncertaintymean
    CMSprediction3Dave = sum(CMSprediction3D) / len((CMSprediction3D))

    CMSprediction3Dstdave = []
    for i in range(0, len(np.transpose(CMSprediction3D))):  ##200
        CMSprediction3Dstdave_ = []
        for s in range(0, len(CMSprediction3D)):  ###125
            predictiondata = CMSprediction3D[s, i]
            uncertaintymeandata = CMSuncertaintymean[s, i]
            uncertaintystddata = CMSuncertaintystd[s, i]
            samplesdata = np.random.normal(predictiondata - uncertaintymeandata, uncertaintystddata, 100)
            CMSprediction3Dstdave_ = np.append(CMSprediction3Dstdave_, samplesdata)
        CMSprediction3Dstdave = np.append(CMSprediction3Dstdave, np.std(CMSprediction3Dstdave_))

    ##########all predictions
    IMSprediction2D = Prediction2D
    IMSuncertaintymean = Uncertaintymean
    IMSuncertaintystd = Uncertaintystd
    IMSprediction3D = IMSprediction2D - IMSuncertaintymean
    IMSprediction3Dave = sum(IMSprediction3D) / len((IMSprediction3D))

    IMSprediction3Dstdave = []
    for i in range(0, len(np.transpose(IMSprediction3D))):  ##200
        IMSprediction3Dstdave_ = []
        for s in range(0, len(IMSprediction3D)):  ###1426
            predictiondata = IMSprediction3D[s, i]
            uncertaintymeandata = IMSuncertaintymean[s, i]
            uncertaintystddata = IMSuncertaintystd[s, i]
            samplesdata = np.random.normal(predictiondata - uncertaintymeandata, uncertaintystddata, 100)
            IMSprediction3Dstdave_ = np.append(IMSprediction3Dstdave_, samplesdata)
        IMSprediction3Dstdave = np.append(IMSprediction3Dstdave, np.std(IMSprediction3Dstdave_))


    ##########all plots
    ID_excluded = np.transpose(ID_excluded)
    cms_bounds = np.zeros((len(ID_excluded),2))
    ims_bounds = np.zeros((len(ID_excluded), 2))
    validation_measurements = np.zeros((1,len(ID_excluded)))

    validation_check_cms = np.zeros((len(ID_excluded), 1))
    validation_check_ims = np.zeros((len(ID_excluded), 1))

    for i in range(0, len(ID_excluded)):
        cms_bounds[i][0] = CMSprediction3Dave[ID_excluded[i]-1] - 3 * CMSprediction3Dstdave[ID_excluded[i]-1]
        cms_bounds[i][1] = CMSprediction3Dave[ID_excluded[i] - 1] + 3 * CMSprediction3Dstdave[ID_excluded[i] - 1]

        ims_bounds[i][0] = IMSprediction3Dave[ID_excluded[i] - 1] - 3 * IMSprediction3Dstdave[ID_excluded[i] - 1]
        ims_bounds[i][1] = IMSprediction3Dave[ID_excluded[i] - 1] + 3 * IMSprediction3Dstdave[ID_excluded[i] - 1]

        validation_measurements[0][i] = Measurement[ID_excluded[i]-1]

        ####check
        checkuppercms = validation_measurements[0][i] <= cms_bounds[i][1]
        checklowercms = validation_measurements[0][i] >= cms_bounds[i][0]
        checkupperims = validation_measurements[0][i] <= ims_bounds[i][1]
        checklowerims = validation_measurements[0][0] >= ims_bounds[i][0]

        validation_check_cms[i][0] = checkuppercms*checklowercms
        validation_check_ims[i][0] = checkupperims * checklowerims


    return cms_bounds,ims_bounds,validation_measurements,validation_check_cms, validation_check_ims

