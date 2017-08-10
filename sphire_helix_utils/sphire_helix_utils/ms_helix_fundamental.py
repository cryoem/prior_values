"""
author: markus stabrin 2017/07/26 (markus.stabrin@mpi-dortmund.mpg.de)

this software is issued under a joint bsd/gnu license. you may use the
source code in this file under either license. however, note that the
complete eman2 and sphire software packages have some gpl dependencies,
so you are responsible for compliance with the licenses of these packages
if you opt to use bsd licensing. the warranty disclaimer below holds
in either instance.

this complete copyright notice must be included in any revised version of the
source code. additional authorship citations may be added, but existing
author citations must be preserved.

this program is free software; you can redistribute it and/or modify
it under the terms of the gnu general public license as published by
the free software foundation; either version 2 of the license, or
(at your option) any later version.

this program is distributed in the hope that it will be useful,
but without any warranty; without even the implied warranty of
merchantability or fitness for a particular purpose. see the
gnu general public license for more details.

you should have received a copy of the gnu general public license
along with this program; if not, write to the free software
foundation, inc., 59 temple place, suite 330, boston, ma  02111-1307 usa
"""

import ms_helix_prior as mhp
import ms_helix_lib as mhl


def calculate_priors(
        tracker,
        params_file=None,
        index_file=None,
        typ='sphire',
        tol_psi=30,
        tol_theta=15,
        tol_filament=0.2,
        method='deg',
        plot=False,
        plot_lim=4,
        window_size=3,
        node=0
        ):
    """Calculate prior values for the parameters
    prior_tracker keys:
    array
    order
    micrograph_id
    filament_id
    segment_id
    angle_names
    angle_max
    angle_min
    output_columns
    outlier
    output_file_params
    output_file_index
    output_dir
    idx_angle
    idx_angle_prior
    idx_angle_rot
    array_filament
    """

    # Import the stack and get parameters
    prior_tracker = mhl.import_data(
        tracker=tracker, index_file=index_file, params_file=params_file, typ=typ
        )

    # Create one huge array and sort the array
    prior_tracker = mhl.expand_and_order_array(prior_tracker=prior_tracker)

    # Seperate each filament into an array
    prior_tracker = mhp.get_filaments(prior_tracker=prior_tracker)

    # Add stuff to prior_tracker
    tolerance_list = [tol_theta, tol_psi]
    prior_tracker['plot'] = plot
    prior_tracker['plot_lim'] = plot_lim
    prior_tracker['window_size'] = window_size
    prior_tracker['tol_filament'] = tol_filament
    prior_tracker['node'] = node
    prior_tracker['apply_method'] = method
    # Execute calculation for each angle
    for idx, angle in enumerate(prior_tracker['angle_names']):
        prior_tracker['tolerance'] = tolerance_list[idx]
        prior_tracker['angle_prior'] = angle[prior_tracker['idx_angle_prior']]
        prior_tracker['angle_rot'] = angle[prior_tracker['idx_angle_rot']]
        prior_tracker['angle'] = angle[prior_tracker['idx_angle']]

        # Loop over the filament
        prior_tracker = mhl.loop_filaments(prior_tracker=prior_tracker)

    # Combine arrays and sort the combined array
    prior_tracker = mhl.combine_and_order_filaments(prior_tracker=prior_tracker)

    # Print outliers
    IDX_ANGLE = prior_tracker['idx_angle']
    for angle in prior_tracker['angle_names']:
        column = 'outlier_{0}'.format(angle[IDX_ANGLE])
        print('==>', column, len(prior_tracker['array'][column][prior_tracker['array'][column] == 1]))

    # Identify outliers
    mhl.identify_outliers(prior_tracker=prior_tracker)

    # Write output
    mhl.export_data(prior_tracker=prior_tracker, typ=typ)

    return prior_tracker['array'][prior_tracker['outlier']]

