def f_plot_holdout_validation(cms_bounds, ims_bounds, validation_measurements, validation_indices):
    """
    Plot a figure to compare updated and prior predictions with measurements at selected locations

    Developed by :   Sai G.S. Pai (ETH Singapore)
    Contact :        saiganesh89@gmail.com
    Date:            June 30, 2020
    """
    
    import matplotlib.pyplot as plt
    import numpy as np

    # Plot validation results
    num_columns = 3
    if validation_measurements.shape[1] // num_columns >= 1 and validation_measurements.shape[
        1] % num_columns != 0:
        num_rows = (validation_measurements.shape[1] // num_columns) + 1
    elif validation_measurements.shape[1] // num_columns >= 1 and validation_measurements.shape[
        1] % num_columns == 0:
        num_rows = (validation_measurements.shape[1] // num_columns)
    else:
        num_rows = 1

    # plot figure for predictions without uncertainties
    fig = plt.figure(figsize=(6, 1.2 * num_rows + 1))
    fig.canvas.set_window_title('Cross-Validation Plot')
    font = {'family': 'sans serif',
            'weight': 'normal',
            'size': 10}
    plt.rc('font', **font)
    for i in range(0, validation_measurements.shape[1]):
        ax = fig.add_subplot(num_rows, num_columns, i + 1)

        # Initial model set
        limit = 1 / (ims_bounds[i, 1] - ims_bounds[i, 0])
        ax.plot([ims_bounds[i, 0], ims_bounds[i, 0], ims_bounds[i, 1], ims_bounds[i, 1]],
                [0, limit, limit, 0],
                color='lightgray', linewidth=3, linestyle='solid', label='IMS prediction')

        # Candidate model set
        limit = 1 / (cms_bounds[i, 1] - cms_bounds[i, 0])
        ax.plot([cms_bounds[i, 0], cms_bounds[i, 0], cms_bounds[i, 1], cms_bounds[i, 1]],
                [0, limit, limit, 0],
                color='g', linewidth=2, linestyle='dashed', label='CMS prediction')
        ax.set_xlabel("Resp @ sensor: " + str(validation_indices[i] + 1))
        ax.set_ylabel("PDF")

        # Measured value
        ax.axvline(validation_measurements[0][i], color='k', linestyle='dashdot', linewidth=3,
                   label='Measurement')
        handles, labels = ax.get_legend_handles_labels()

    fig.legend(handles, labels, bbox_to_anchor=(0.5, -0.025), borderaxespad=0.05, loc='lower center',
               ncol=3, handleheight=2.4)
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.35 - ((num_rows - 1) * 0.1), top=0.9, hspace=0.7)
    plt.show()

