def f_norm_scale(array_original):
    """
    Normalize numpy array between -1 and +1

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        array_original : original array to normalize

    OUTPUTS:
        array_norm : normalized array

    NOTE:
        Requires numpy

    """
    import numpy as np
    # initialize
    array_norm = np.zeros(shape=(array_original.shape[0], array_original.shape[1]))

    # normalize
    for feature in range(0, array_original.shape[1]):
        x_min = np.amin(array_original[:, feature])
        x_max = np.amax(array_original[:, feature])
        x_halfrange = (x_max - x_min) / 2
        x_midpoint = (x_max + x_min) / 2

        for idx in range(0, array_original.shape[0]):
            array_norm[idx, feature] = (array_original[idx, feature] - x_midpoint) / x_halfrange

    # return normalized array
    return array_norm
