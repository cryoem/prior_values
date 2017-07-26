import numpy as np


def create_dtype_dict():
    """Create type dictionary"""

    # Open the dictionary file and convert it to a dictionary
    dict_as_string = \
        '_rlnCtfImage    |S200\n' + \
        '_rlnImageName   |S200\n' + \
        '_rlnMicrographName  |S200\n' + \
        '_rlnOriginalParticleName    |S200\n' + \
        '_rlnGroupName   |S200\n' + \
        '_rlnGroupNumber <i8\n' + \
        '_rlnClassNumber <i8\n' + \
        '_rlnNrOfSignificantSamples  <i8\n' + \
        '_rlnRandomSubset    <i8\n' + \
        '_rlnNrOfFrames  <i8\n' + \
        '_rlnHelicalTubeID  <i8\n' + \
        '_rlnVoltage <f8\n' + \
        '_rlnDefocusU    <f8\n' + \
        '_rlnDefocusV    <f8\n' + \
        '_rlnDefocusAngle    <f8\n' + \
        '_rlnSphericalAberration <f8\n' + \
        '_rlnDetectorPixelSize   <f8\n' + \
        '_rlnCtfFigureOfMerit    <f8\n' + \
        '_rlnMagnification   <f8\n' + \
        '_rlnAmplitudeContrast   <f8\n' + \
        '_rlnCoordinateX <f8\n' + \
        '_rlnCoordinateY <f8\n' + \
        '_rlnNormCorrection  <f8\n' + \
        '_rlnOriginX <f8\n' + \
        '_rlnOriginY <f8\n' + \
        '_rlnAngleRot    <f8\n' + \
        '_rlnAngleTilt   <f8\n' + \
        '_rlnAnglePsi    <f8\n' + \
        '_rlnAutopickFigureOfMerit   <f8\n' + \
        '_rlnLogLikeliContribution   <f8\n' + \
        '_rlnMaxValueProbDistribution    <f8\n' + \
        '_rlnParticleSelectZScore    <f8\n' + \
        '_rlnAngleRotPrior   <f8\n' + \
        '_rlnAngleTiltPrior  <f8\n' + \
        '_rlnAnglePsiPrior   <f8\n' + \
        '_rlnOriginXPrior    <f8\n' + \
        '_rlnOriginYPrior    <f8\n' + \
        '_rlnHelicalTrackLength  <f8\n'

    # Split the dictionary to a list
    string_list = dict_as_string.split()

    # Create a dictionary out of the list
    dtype_dict = {
        string_list[number]: string_list[number + 1]
        for number in range(0, len(string_list), 2)
        }

    return dtype_dict


def import_star_file(
        input_star_file
        ):
    """Import the Data from the Star File as a structured Array"""

    # Load type dictionary
    dtype_dict = create_dtype_dict()

    # Create a list for the header information.  Use the built-in
    # function enumerate to go through the lines of the Star file.
    # Just save the names of the header information and stop after
    # the header is over.
    # If no header is found linenumber will stay False
    header_names = []
    linenumber = False
    for linenumber, line in enumerate(
            open(input_star_file, 'r')
            ):
        if line[0] == '_':
            header_names.append(line.split()[0])
        elif linenumber > 4:  # So data_ and loop_ won't abort the loop
            break
        elif linenumber > 50:
            break
        else:
            assert(linenumber <= 50)
            assert(linenumber <= 4)

    # Create a list for the dtype information.  Go through the
    # header_names list and append the dtype of the related column.
    # If there isn't an entry for the name yet it will be written to
    # the dictionary file and saved as float.
    # If no header_names are there set the column to ('column', '|S200')

    dtype_list = []
    if any(header_names):
        for names in header_names:
            try:
                dtype_list.append((names, dtype_dict[names]))
            except:
                dtype_list.append((names, '<f8'))
                dtype_dict.update({names: '<f8'})
    else:
        dtype_list.append(('column', '|S200'))
        linenumber = 0

    # Import the dataInput as a np structured Array.  Skip the lines
    # with header information and set the dtype_list.
    # If linenumber is False there is a input/output error.
    if linenumber:
        data = np.genfromtxt(
            input_star_file,
            skip_header=linenumber,
            dtype=dtype_list
            )

        return data, \
            np.array(header_names), np.array(input_star_file)

    else:
        return None

    assert(False)
