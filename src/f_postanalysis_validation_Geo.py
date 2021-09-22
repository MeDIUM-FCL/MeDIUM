def postanalysisplot_validation(EDMFresults,Uncertaintyresults,
                                numberofexcavationstage,numberofmeasurementperstage,
                                ID_excluded):
    """
        Plot results of EDMF analysis for cross-validation tab

        Developed by :   WANG Ze-Zhou (ETH Singapore)
        Contact :        e0054291@u.nus.edu
        Date:            July 27, 2020

        INPUTS:
            EDMFresults : Results of EDMF analysis
            Uncertaintyresults : Results of geotechnical uncertainty calculation
            numberofexcavationstage: number of excavation stages
            numberofmeasurementperstage : number of measurements per excavation stage
            ID_excluded: index of measurement to be excluded from the cros-validation analysis.

        OUTPUTS:
            CMSprediction3D : predictions made with candidate models
            CMSprediction3Dave : average predictions made with candidate models
            CMSprediction3Dstdave: standard deviation of predictions made with candidate models

        NOTE:
        All inputs will be read automatically. No manual actions are needed from the user.
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


    print('Plotting of results')

    ##########all plots
    ID_excluded = np.transpose(ID_excluded)
    ####prediction plot
    plotsize = int(math.ceil(len(ID_excluded) / 2))
    print(plotsize)

    fig = plt.figure(1,figsize=(12, 10))
    fig.canvas.set_window_title('Cross-Validation Plot')
    for i in range(0, len(ID_excluded)):
        plt.subplot(plotsize, 2, i+1)
        plt.plot([Measurement[ID_excluded[i]-1], Measurement[ID_excluded[i]-1]], [0, 3], 'r-')
        plt.plot([CMSprediction3Dave[ID_excluded[i]-1] - 3 * CMSprediction3Dstdave[ID_excluded[i]-1],
                  CMSprediction3Dave[ID_excluded[i]-1] - 3 * CMSprediction3Dstdave[ID_excluded[i]-1]], [0, 1], 'b--')
        plt.plot([IMSprediction3Dave[ID_excluded[i]-1] - 3 * IMSprediction3Dstdave[ID_excluded[i]-1],
                  IMSprediction3Dave[ID_excluded[i]-1] - 3 * IMSprediction3Dstdave[ID_excluded[i]-1]], [0, 1.5], 'g-.')

        plt.plot([CMSprediction3Dave[ID_excluded[i]-1] + 3 * CMSprediction3Dstdave[ID_excluded[i]-1],
                  CMSprediction3Dave[ID_excluded[i]-1] + 3 * CMSprediction3Dstdave[ID_excluded[i]-1]], [0, 1], 'b--')
        plt.plot([CMSprediction3Dave[ID_excluded[i]-1] - 3 * CMSprediction3Dstdave[ID_excluded[i]-1],
                  CMSprediction3Dave[ID_excluded[i]-1] + 3 * CMSprediction3Dstdave[ID_excluded[i]-1]], [1, 1], 'b--')


        plt.plot([IMSprediction3Dave[ID_excluded[i]-1] + 3 * IMSprediction3Dstdave[ID_excluded[i]-1],
                  IMSprediction3Dave[ID_excluded[i]-1] + 3 * IMSprediction3Dstdave[ID_excluded[i]-1]], [0, 1.5], 'g-.')
        plt.plot([IMSprediction3Dave[ID_excluded[i]-1] - 3 * IMSprediction3Dstdave[ID_excluded[i]-1],
                  IMSprediction3Dave[ID_excluded[i]-1] + 3 * IMSprediction3Dstdave[ID_excluded[i]-1]], [1.5, 1.5], 'g-.')
        plt.yticks([])
        # plt.legend(['Measured value','Prediction bounds using CMS','Prediction bounds using IMS'])
        plt.xlabel('Wall Deflections(mm)')

    fig.legend(['Measured value','Prediction bounds using CMS','Prediction bounds using IMS'],
               bbox_to_anchor=(0.5, 0.01), borderaxespad=0.05, loc='lower center',
                   ncol=3, handleheight=2.4,fontsize=12)

        ####prediction plot
    scatterstr = ['ro', 'k<', 'g>', 'm*', 'c^', 'r<', 'kx', 'go', 'm<']
    linestr = ['r-', 'k--', 'g:', 'm-.', 'c-', 'r--', 'k:', 'g-.', 'm-']

    fig = plt.figure(2,figsize=(9, 8))
    fig.canvas.set_window_title('Mean wall deflection predictions at all excavation stages')
    for i in range(0, numberofexcavationstage):
        plt.plot(Measurement[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(numberofmeasurementperstage) + 1, scatterstr[i])
        plt.plot(CMSprediction3Dave[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(numberofmeasurementperstage) + 1, linestr[i])
        plt.axis([0, 100, 0, 40])
        plt.xlabel('Wall Deflections(mm)')
        plt.ylabel('Depth(m)')
        plt.gca().invert_yaxis()
        plt.legend(['Stage 1 measurement', 'Stage 1 prediction',
                    'Stage 2 measurement', 'Stage 2 prediction',
                    'Stage 3 measurement', 'Stage 3 prediction',
                    'Stage 4 measurement', 'Stage 4 prediction',
                    'Stage 5 measurement', 'Stage 5 prediction'], loc='upper right', ncol=2, handleheight=2.4,
                   handlelength=2)
        plt.title('Mean wall deflection predictions for all five stages')

    plotsize = int(math.ceil(numberofexcavationstage / 3))
    print(plotsize)

    fig = plt.figure(3,figsize = (18,10))
    fig.canvas.set_window_title('Wall deflection predictions at individual excavation stages')
    for i in range(0, numberofexcavationstage):
        plt.subplot(plotsize, 3, i+1)
        plt.plot(Measurement[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(numberofmeasurementperstage) + 1, 'ro')
        plt.plot(CMSprediction3Dave[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(numberofmeasurementperstage) + 1, 'b-')
        plt.plot(CMSprediction3Dave[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)]
                 - 3 * CMSprediction3Dstdave[
                       0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(40) + 1, 'k--')
        plt.plot(CMSprediction3Dave[0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)]
                 + 3 * CMSprediction3Dstdave[
                       0 + numberofmeasurementperstage * i:numberofmeasurementperstage * (i + 1)],
                 np.arange(40) + 1, 'k--')

        # plt.axis([-inf, 20, 0, 40])
        plt.xlabel('Wall Deflections(mm)')
        plt.ylabel('Depth(m)')
        plt.gca().invert_yaxis()
        plt.title('Stage ' + str(i + 1) + ' results')
    fig.legend(['Measurement', 'Mean predictions', '3-standard deviation bounds'],
               bbox_to_anchor=(0.5, 0.01), borderaxespad=0.05, loc='lower center',
               ncol=3, handleheight=2.4,fontsize=12)
    plt.show()

    return CMSprediction3D, CMSprediction3Dave, CMSprediction3Dstdave

