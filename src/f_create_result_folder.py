def f_create_result_folder(secondarypath):
    """
            Perform EDMF analysis with all uploaded files and intermediate results

            Developed by :   WANG Ze-Zhou (ETH Singapore)
            Contact :        e0054291@u.nus.edu
            Date:            August 04, 2021

            INPUTS:
                the input contains the secondary path of the folder to be created

            OUTPUTS:
                a folder named given in the input is created under the directory of the software. This folder
                contains results of the EDMF calculation

            NOTE:

            """
    import os
    currentpath = os.getcwd()
    finalpath = os.path.abspath(currentpath + secondarypath)
    if not os.path.exists(finalpath):
        os.makedirs(finalpath)