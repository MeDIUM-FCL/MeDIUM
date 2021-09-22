def f_resultsexcel_Geo(parameters,predictions,EDMFresults,multiplier,confidencelevel,holdoutindices):
    """
            Perform EDMF analysis with all uploaded files and intermediate results

            Developed by :   WANG Ze-Zhou (ETH Singapore)
            Contact :        e0054291@u.nus.edu
            Date:            August 03, 2021

            INPUTS:
                parameters : initial model instances.
                predictions : predictions of initial model instances.
                EDMFresults: results of EDMF analysis. 1 represents candidate model. 0 represents falsified models.
                multiplier : the uncertainty multiplier used.
                confidencelevel: target reliability of identification.
                holdoutindices: the indices of the measurements excluded from the EDMF analysis.

            OUTPUTS:
                an excel file is created under the "Results" folder. The file name is in the format of:
                    CMS_Geo_multiplier_confidencelevel_holdoutindices.xlsx

            NOTE:

            """
    import xlsxwriter
    import os
    import numpy

    ####creat excel file
    currentpath = os.getcwd()
    secondarypath = '\Results'
    if holdoutindices==[]:
        filenname = '\CMS_Geo_UncMultiplier=' + str(multiplier) + "_phi=" + str(confidencelevel)+".xlsx"
    else:
        filenname = '\CMS_Geo_UncMultiplier='+str(multiplier)+"_phi="+str(confidencelevel)+"_HoldoutIndices="+str(holdoutindices)+".xlsx"

    finalpath = os.path.abspath(currentpath + secondarypath + filenname)

    workbook = xlsxwriter.Workbook(finalpath)
    worksheet = workbook.add_worksheet("result")

    ####prepare data label
    alltitle = list()
    for i in range(0,len(numpy.transpose(parameters))):
        alltitle.append("Parameter")

    for i in range(0,len(numpy.transpose(predictions))):
        alltitle.append("Predictions")

    alltitle.append('EDMF results')

    ######prepare data
    alldata_sub = numpy.transpose(numpy.concatenate((numpy.transpose(parameters),numpy.transpose(predictions),numpy.transpose(EDMFresults))))

    #####write to excel
    for idx,label in enumerate(alltitle):
        worksheet.write(0,idx,alltitle[idx])

    sizedata = numpy.shape(alldata_sub)
    for i in range(0,sizedata[0]-1):
        for s in range(0,sizedata[1]-1):
            worksheet.write(i+1,s,alldata_sub[i][s])

    workbook.close()



