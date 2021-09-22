def f_calculate_thresholds(combined_uncertainties, phi=0.95):
    """
    Calculates EDMF thresholds for provided target reliability of identification

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        combined_uncertainties : numpy array with each column containing combined uncertainty samples for each measurement point
        phi : target reliability of identification

    OUTPUTS:
        thresholds : numpy array with each row containing lower and upper bound uncertainty threshold values for each measurement point

    NOTE:
        Requires numpy

    """
    import numpy as np
    # set phi
    phi = float(phi) ** (1 / combined_uncertainties.shape[1])       # float to ensure value is numeric not list
    print("Phi = ", phi)        # Check Phi

    # Initialize search
    step_size = 1
    length = int((1 - phi) * combined_uncertainties.shape[0] / step_size)
    perc_calculation = np.zeros(shape=(length, 3))
    thresholds = np.zeros(shape=(combined_uncertainties.shape[1], 2))

    print("*** Starting search for thresholds ***")
    for sens_num in range(0, combined_uncertainties.shape[1]):
        temp_array = np.sort(combined_uncertainties[:, sens_num])       # sort samples in ascending order
        for iter_num in range(0, length):
            temp = np.zeros(shape=(1, 3))
            endA_init_samples = np.arange(0, 1 + (iter_num * step_size))        # end A is for the lower bound
            endB_init_samples = np.arange(len(endA_init_samples), len(endA_init_samples) +
                                          np.around(phi * len(temp_array)), dtype=int)      # end B is for the upper bound
            temp[0, 0] = np.max(temp_array[endA_init_samples])
            temp[0, 1] = np.max(temp_array[endB_init_samples])
            # calculate percentile range for each step
            temp[0, 2] = np.max(temp_array[endB_init_samples]) - np.max(temp_array[endA_init_samples])
            perc_calculation[iter_num, :] = temp

        threshold_idx = np.where(perc_calculation[:, 2] ==
                                 np.amin(perc_calculation[:, 2]))       # get index of lowest percentile range
        # EDMF thresholds corresponding to lowest percentile range
        thresholds[sens_num, :] = perc_calculation[threshold_idx, [0, 1]]

    print(thresholds)

    return thresholds
    # numpy array with size number_measurements x 2
