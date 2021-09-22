def f_holdout_validation(ims_predictions, is_candidate, combined_uncertainties, measurements, unc_amplifier, validation_indices):
    """
    Check with information from held out sensors whether canidate instances are valid

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        ims_predictions : numpy array with each column containing predictions at each measurement point for each model instance
        is_candidate : array of 1s [candidate model instance] and 0s [falsified model instance]
        combined_uncertainties : numpy array with each column containing combined uncertainty samples for each measurement point
        measurements : row of measurement points
        unc_amplifier : multiplier for uncertainty to assess sensitivity of results to uncertainty definitions
        validation_indices : measurement points held out for validation. None [] for no validation


    OUTPUTS:
        cms_bounds : Bounds of predictions by candidate model instances at validation measurement points; Size number_validation_indices x 2
        ims_bounds : Bounds of predictions by initial model instances at validation measurement points; Size number_validation_indices x 2
        validation_measurements : Measured value at validation points
        validation_check_cms : Logical array indicating whether bounds of candidate model predictions include measured value
        validation_check_ims : Logical array indicating whether bounds of initial model predictions include measured value

    NOTE:
        Requires prior results from EDMF using f_falsify_models
        Requires function f_calculate_thresholds
        95th percentile bounds of combined uncertainty are added to the bounds of predictions from cms and ims
        Requires numpy

    """
    import numpy as np
    from f_calculate_thresholds import f_calculate_thresholds
    print("Inside f_holdout_validation function")

    validation_indices = validation_indices - 1
    validation_ims_predictions = ims_predictions[:, validation_indices]
    validation_measurements = measurements[:, validation_indices]
    combined_uncertainties = combined_uncertainties * unc_amplifier
    combined_uncertainties = combined_uncertainties[:, validation_indices]
    print("Validation measurements are: {}".format(validation_measurements))
    # calculate thresholds for uncertainty at validation-measurement points
    thresholds = f_calculate_thresholds(combined_uncertainties, 0.95)

    # calculate predictions of CMS at validation-measurement points
    temp = np.hstack((validation_ims_predictions, is_candidate))
    validation_cms_predictions = np.array([])
    for i in range(0, len(temp)):
        if temp[i][temp.shape[1] - 1] == 1 and validation_cms_predictions.size == 0:
            validation_cms_predictions = np.array(validation_ims_predictions[i])
        elif temp[i][temp.shape[1] - 1] == 1:
            validation_cms_predictions = np.vstack(
                (validation_cms_predictions, np.array(validation_ims_predictions[i])))
        else:
            pass

    # calculate bounds of predictions by IMS including combined uncertainty
    ims_bounds = np.arange(0, validation_indices.__len__() * 2).reshape(validation_indices.__len__(), 2)
    for sensID in range(0, validation_indices.__len__()):
        ims_bounds[sensID, :] = [np.min(validation_ims_predictions[:, sensID]) + thresholds[sensID, 0],
                                 np.max(validation_ims_predictions[:, sensID]) + thresholds[sensID, 1]]

    # calculate bounds of predictions by CMS including combined uncertainty
    cms_bounds = np.arange(0, validation_indices.__len__() * 2).reshape(validation_indices.__len__(), 2)
    for sensID in range(0, validation_indices.__len__()):
        cms_bounds[sensID, :] = [np.min(validation_cms_predictions[:, sensID]) + thresholds[sensID, 0],
                                 np.max(validation_cms_predictions[:, sensID]) + thresholds[sensID, 1]]

    # check whether cms bounds include validation-measurement points
    check_upper = validation_measurements <= cms_bounds[:, 1]
    check_lower = validation_measurements >= cms_bounds[:, 0]
    validation_check_cms = check_lower * check_upper

    # check whether ims bounds include validation-measurement points
    check_upper = validation_measurements <= ims_bounds[:, 1]
    check_lower = validation_measurements >= ims_bounds[:, 0]
    validation_check_ims = check_lower * check_upper

    return cms_bounds, ims_bounds, validation_measurements, validation_check_cms, validation_check_ims
