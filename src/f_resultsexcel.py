def f_resultsexcel(parameters,predictions,EDMFresults,multiplier,confidencelevel,holdoutindices):
    """
            Perform EDMF analysis with all uploaded files and intermediate results

            Developed by :   WANG Ze-Zhou (ETH Singapore)
            Contact :        e0054291@u.nus.edu
            Date:            August 20, 2020

            INPUTS:
                parameters : initial model instances.
                predictions : predictions of initial model instances.
                EDMFresults: results of EDMF analysis. 1 represents candidate model. 0 represents falsified models.
                multiplier : the uncertainty multiplier used.
                confidencelevel: target reliability of identification.
                holdoutindices: the indices of the measurements excluded from the EDMF analysis.

            OUTPUTS:
                an excel file is created under the "Results" folder. The file name is in the format of:
                    CMS_multiplier_confidencelevel_holdoutindices.xlsx

            NOTE:

            """
    import xlsxwriter
    import os
    import numpy
    print('import done')
    print('wzz')
    ####creat excel file
    currentpath = os.getcwd()
    secondarypath = '\Results'
    if holdoutindices==[]:
        filenname = '\CMS_UncMultiplier=' + str(multiplier) + "_phi=" + str(confidencelevel)+".xlsx"
    else:
        filenname = '\CMS_UncMultiplier='+str(multiplier)+"_phi="+str(confidencelevel)+"_HoldoutIndices="+str(holdoutindices)+".xlsx"

    finalpath = os.path.abspath(currentpath + secondarypath + filenname)
    print(finalpath)
    print(holdoutindices)
    workbook = xlsxwriter.Workbook(finalpath)
    worksheet = workbook.add_worksheet("result")
    print("path done")
    ####prepare data label
    alltitle = list()
    for i in range(0,len(numpy.transpose(parameters))):
        alltitle.append("Parameter")

    for i in range(0,len(numpy.transpose(predictions))):
        alltitle.append("Predictions")

    alltitle.append('EDMF results')

    ######prepare data
    alldata = numpy.transpose(numpy.concatenate((numpy.transpose(parameters),numpy.transpose(predictions),numpy.transpose(EDMFresults))))

    print("data done")
    #####write to excel
    for idx,label in enumerate(alltitle):
        worksheet.write(0,idx,alltitle[idx])

    row = 1
    for col,data in enumerate(numpy.transpose(alldata)):
        worksheet.write_column(row, col, data)

    workbook.close()