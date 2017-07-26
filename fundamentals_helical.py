"""
Author: Markus Stabrin 2017/07/26 (markus.stabrin@mpi-dortmund.mpg.de)

This software is issued under a joint BSD/GNU license. You may use the
source code in this file under either license. However, note that the
complete EMAN2 and SPHIRE software packages have some GPL dependencies,
so you are responsible for compliance with the licenses of these packages
if you opt to use BSD licensing. The warranty disclaimer below holds
in either instance.

This complete copyright notice must be included in any revised version of the
source code. Additional authorship citations may be added, but existing
author citations must be preserved.

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
"""


def calculate_priors(tracker, params_file, index_file):
    """Calculate prior values for the parameters"""

    data = import_stack(stack=stack_name, index=index_file, params=params_file, typ='sphire')
    main(
        file_name=stack_name,
        data=data,
        tolerance_psi=30,
        tolerance_theta=15,
        tolerance_filament=0.2,
        window_size=3,
        typ='sphire',
        plot=True,
        output_dir=iteration_dir,
        params=params_file
        )


def import_stack(stack, params=None, index=None, typ='sphire'):
    """Import the original stack and create a substack"""
    # Check angle range, import arrays
    if typ == 'sphire':
        angle_max = 360
        angle_min = 0

        if isinstance(stack, basestring):
            original_stack = read_sphire.get_sphire_stack(stack)
        else:
            original_stack = stack
        parameter = get_sphire_file('params', params)
        indices = get_sphire_file('index', index)

        substack = original_stack[indices]
        array = combine_arrays([substack, parameter])

        stack_id = 'source_n'
        mic_name, filament_name, particle_id = \
            original_stack.dtype.names

        angle_name = [
            ['psi', 'psi_prior', 'psi_rot'],
            ['theta', 'theta_prior', 'theta_rot']
            ]

        output_names = list(parameter.dtype.names)
        del original_stack, parameter, indices

    elif typ == 'relion':
        angle_max = 180
        angle_min = -180

        array, header, path = read_star.import_star_file(stack)

        stack_id = 'source_n'
        filament_name = '_rlnHelicalTubeID'
        mic_name = '_rlnMicrographName'
        particle_id = '_rlnImageName'
        angle_name = [
            ['_rlnAnglePsi', '_rlnAnglePsiPrior', '_rlnAnglePsiRotated'],
            ['_rlnAngleTilt', '_rlnAngleTiltPrior', '_rlnAngleTiltRotated']
            ]

        output_names = list(array.dtype.names)
        array_stack_id = np.empty(len(array), dtype=[(stack_id, '<i8')])
        array_stack_id[stack_id] = np.arange(len(array))
        array = combine_arrays([array, array_stack_id])

    else:
        print('Unreachable code!')
        return 'Unreachable code!'

    return [array, stack_id, mic_name, filament_name, particle_id, angle_name, output_names, angle_max, angle_min]
