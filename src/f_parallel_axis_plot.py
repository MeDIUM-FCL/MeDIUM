def f_parallel_axis_plot(ims_parameters, cms_parameters):
    """
    Check with information from held out sensors whether canidate instances are valid

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020

    INPUTS:
        input_array : numpy array with each column containing predictions at each measurement point for each model instance
        number_ims : array of 1s [candidate model instance] and 0s [falsified model instance]
        number_cms : numpy array with each column containing combined uncertainty samples for each measurement point

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
    import matplotlib.pyplot as plt
    import numpy as np
    from f_norm_scale import f_norm_scale

    array_original = np.vstack((ims_parameters, cms_parameters))
    input_array = f_norm_scale(array_original)
    del array_original

    number_ims = ims_parameters.shape[0]
    number_cms = cms_parameters.shape[0]

    fig = plt.figure(figsize=(6, 4))
    fig.canvas.set_window_title('Parallel Axis Plot - EDMF')
    font = {'family': 'sans serif',
            'weight': 'normal',
            'size': 10}
    plt.rc('font', **font)
    ax = fig.add_subplot(1, 1, 1, frameon=False)

    for i in range(0, number_ims):
        ax.plot(input_array[i, :], linestyle='solid', linewidth=6, color='lightgray', alpha=1,
                label='Initial model set')
    for i in range(0, number_cms):
        ax.plot(input_array[number_ims + i, :], linestyle='solid', linewidth=1.5, color='g',
                label='Candidate model set')

    # Parameter axis
    xaxis_labels = []
    for i in range(0, input_array.shape[1]):
        ax.axvline(i, color='k', ymin=0.05, ymax=0.95, linestyle='solid', linewidth=1)
        xaxis_labels += ["Parameter " + str(i + 1)]

    ax.set_xticks([i for i in range(0, input_array.shape[1])])
    ax.set_xticklabels(xaxis_labels)
    ax.set_yticklabels(['min', 'max'])
    ax.set_yticks([-1, 1])

    temp_handles, temp_labels = ax.get_legend_handles_labels()
    labels = [temp_labels[0], temp_labels[number_ims]]
    handles = [temp_handles[0], temp_handles[number_ims]]
    fig.legend(handles, labels, bbox_to_anchor=(0.5, 0), loc='lower center', ncol=3, handleheight=2.4)

    plt.tight_layout()
    plt.subplots_adjust(bottom=0.20)
    # plt.show()
    print('File run complete')
