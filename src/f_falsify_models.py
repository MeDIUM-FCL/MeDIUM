def f_falsify_models(ims_parameters, ims_predictions, combined_uncertainties, measurements, phi, unc_amplifier, to_be_deleted, indextext):
    """
    Falsify model instances based on input measurements, samples, uncertainties and target reliability of identification

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        ims_parameters : numpy array with each column containing parameter samples for each model instance
        ims_predictions : numpy array with each column containing predictions at each measurement point for each model instance
        combined_uncertainties : numpy array with each column containing combined uncertainty samples for each measurement point
        measurements : row of measurement points
        phi : target reliability of identification
        unc_amplifier : multiplier for uncertainty to assess sensitivity of results to uncertainty definitions
        to_be_deleted : measurement points to be held out for validation. None [] for no validation
        indextext: index of measurements to be excluded for EDMF analysis in the original format.

    OUTPUTS:
        cms : parameter values not falsified using measurements; Size number_parameters x number_cms
        is_candidate : array of 1s [candidate model instance] and 0s [falsified model instance]

    NOTE:
        Requires function f_calculate_thresholds
        Requires numpy

    """

    import numpy as np
    from f_calculate_thresholds import f_calculate_thresholds

    # hold out measurements for validation
    to_be_deleted = to_be_deleted
    print(to_be_deleted)
    measurements = np.delete(measurements, to_be_deleted, 1)
    ims_predictions = np.delete(ims_predictions, to_be_deleted, 1)
    combined_uncertainties = combined_uncertainties * unc_amplifier
    combined_uncertainties = np.delete(combined_uncertainties, to_be_deleted, 1)

    num_measurements = measurements.shape[1]
    num_parameters = ims_parameters.shape[1]
    num_samples = ims_parameters.shape[0]
    print("*** Calculating thresholds ***")
    thresholds = f_calculate_thresholds(combined_uncertainties, phi)        # calculate thresholds, CHECK function is available

    # check candidate or not for EACH measurement point
    yes_or_no = np.arange(1, (num_samples * num_measurements) + 1).reshape(num_samples, num_measurements)
    for instance in range(0, num_samples):
        for sens_id in range(0, num_measurements):
            if thresholds[sens_id][0] <= ims_predictions[instance][sens_id] - measurements[0][sens_id] <= \
                    thresholds[sens_id][1]:
                yes_or_no[instance][sens_id] = 1
            else:
                yes_or_no[instance][sens_id] = 0

    # check candidate or not for ALL measurement points
    is_candidate = np.prod(yes_or_no, 1).reshape(num_samples, 1)

    # Assign candidate instances to the 'cms' variable
    cms = np.array([])
    temp = np.hstack((ims_parameters, is_candidate))
    for i in range(0, len(temp)):
        if temp[i][temp.shape[1] - 1] == 1 and cms.size == 0:
            cms = np.array(ims_parameters[i])
        elif temp[i][temp.shape[1] - 1] == 1:
            cms = np.vstack((cms, np.array(ims_parameters[i])))
        else:
            pass
    print(type(cms))
    from f_resultsexcel import f_resultsexcel
    f_resultsexcel(ims_parameters, ims_predictions, is_candidate, unc_amplifier, phi, indextext)
    # return candidate model instances and an array indicating which of the initial instances are candidates
    return cms, is_candidate
