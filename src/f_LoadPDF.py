def LoadPDF(Pagenumber):
    """
        Open the help document.

        Developed by :   WANG Ze-Zhou (ETH Singapore)
        Contact :        e0054291@u.nus.edu
        Date:            July 27, 2020
        INPUTS:
            Pagenumber : Pagenumber of the relevant content

        NOTE:
        This code search Adobe. If not found, IE is launched.
        """

    import os
    import subprocess
    import webbrowser

    #########search applications
    searchpath = 'C:\Program Files (x86)'
    name = 'Acrobat.exe'
    result = []
    for root, dirs, files in os.walk(searchpath):
        if name in files:
            result.append(os.path.join(root, name))
    try:
        path_to_acrobat = result[0]
        currentpath = os.getcwd()
        secondarypath = '\Documentations'
        print(secondarypath)
        filenname = '\MeDIUM_Help.pdf'
        path_to_pdf = os.path.abspath(currentpath + secondarypath + filenname)
        print(path_to_pdf)
        process = subprocess.Popen([path_to_acrobat, '/A', 'page='+ str(Pagenumber), path_to_pdf], shell=False, stdout=subprocess.PIPE)
        process.wait()
    except:
        currentpath = os.getcwd()
        secondarypath = '\Documentations'
        print(secondarypath)
        filenname = '\MeDIUM_Help.pdf#page='+str(Pagenumber)
        finalpath= currentpath + secondarypath + filenname
        print(finalpath)
        webbrowser.open_new_tab(finalpath)
