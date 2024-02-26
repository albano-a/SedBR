# Functions that are used in SedBR
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import json
from litologias import *


def abrir_paleta():
    return lithologies_name, lithologies_num

def intervalo(prof):
    """
    This function calculates the spacing between samples.
    It takes a list of sample depths (prof) as input and returns a dictionary
    where the keys are the unique sample depths and the values are the spacings.
    """
    # Convert the list of sample depths to a DataFrame for easier manipulation
    sample_depths_df = pd.DataFrame(prof, columns=['prof'])

    # Initialize variables
    unique_depths = []
    spacings = []
    counter = 0

    # Loop over the unique sample depths
    for depth in sample_depths_df.prof.unique():
        unique_depths.append(depth)

        # Calculate the spacing
        if len(unique_depths) == 2:
            spacings.append(unique_depths[-1] - unique_depths[0 + counter])
            spacings.append(unique_depths[-1] - unique_depths[0 + counter])
        elif len(unique_depths) > 2:
            spacings.append(unique_depths[-1] - unique_depths[1 + counter])
            counter += 1

    # Create a dictionary where the keys are the unique sample depths and the values are the spacings
    depth_spacing_dict = {unique_depths[0]: spacings[0]}
    for i in range(1, len(spacings)):
        depth_spacing_dict[unique_depths[i]] = spacings[i]

    return depth_spacing_dict

def porcentagem(porcentagem):
    """
    This function validates a percentage value.

    It checks if the input is an integer between 10 and 100 and divisible by 10.
    If it is, the function returns the input as an integer.
    If it's not, the function returns 0.

    Args:
        percentage (int): The input percentage to validate.

    Returns:
        int: The validated percentage, or 0 if the input is not valid.
    """
    if 10 <= porcentagem <= 100 and porcentagem % 10 == 0:
        return int(porcentagem)
    else:
        return 0

def cod_shortname(mnemonico):
    """
    This function checks if a given mnemonic is present in the keys of
    the 'lithologies_name' dictionary.

    The function takes a mnemonic as input, converts it to uppercase,
    and checks if it is a key in the 'lithologies_name' dictionary.
    If the mnemonic is found, it is returned as is. If it is not found,
    a message is printed to the console and the function returns None.

    Args:
        mnemonico (str): The mnemonic to check.

    Returns:
        str: The input mnemonic in uppercase if it is found in the
        'lithologies_name' dictionary. Otherwise, None.

    Note:
        This function relies on the global variable 'lithologies_name',
        which should be a dictionary.
    """
    if mnemonico.upper() in lithologies_name.keys():
        return mnemonico.upper()
    else:
        print("mnemonico não identificado:",mnemonico)

def granulometria(x, y=np.nan):
    """
    This function maps lithology codes (x) and possibly a secondary parameter (y)
    to a granulometry value.

    Args:
        x (str): The primary lithology code.
        y (str, optional): The secondary parameter. Defaults to np.nan.

    Returns:
        float: The corresponding granulometry value.
    """
    granulometry_map = {
        'AND': 0, 'BAS': 0, 'ARS': 0, 'CRN': 0, 'CRV': 0, 'CHT': 0, 'CIM': 0,
        'DIA': 0, 'GIP': 0, 'GNA': 0, 'GRN': 0, 'HAL': 0, 'INI': 0, 'IGB': 0,
        'MSD': 0, 'SNI': 0, 'SLX': 0, 'TQD': 0, 'CLC': 0,
        'CAL': 1.5,
        'GRS': 5, 'CRE': 5,
        'PKS': 4,
        'MDS': 2,
        'WKS': 3,
        'ARG': 1, 'AGT': 1, 'AGN': 1, 'AGL': 1, 'AGC': 1, 'AGB': 1, 'CLU': 1,
        'FLH': 1, 'MRG': 1, 'ESF': 1, 'LMT': 1,
        'AGS': 2, 'CSI': 2, 'FLS': 2, 'SLT': 2,
        'ARO': 5.5, 'CRU': 5.5, 'CGL': 5.5, 'COQ': 5.5, 'DMT': 5.5, 'BRC': 5.5, 'BRV': 5.5, 'BLT': 5.5, 'CRU': 5.5
    }

    if x in granulometry_map:
        return granulometry_map[x]
    elif x in ['ARL', 'ARC', 'ARF', 'ART', 'ARE', 'ARN']:
        y_map = {'MFN': 2.5, 'FNO': 3, 'MED': 3.5, 'GRO': 4, 'MGR': 4.5, 'CGO': 5}
        return y_map.get(y, 3.5)
    else:
        return 0

def Dados():
    """
    This function reads data from an Excel, CSV or TXT file and processes it.

    The function reads data from a file specified by the global variable 'filepath'.
    The data is expected to have four columns: "PROF", "LITO", "%", and "GRAN".
    These columns represent depth, lithology, percentage, and granulometry, respectively.

    The function processes the depth data to fill in any missing values.
    If a depth value is missing (NaN), it is replaced with the previous depth value.

    Returns:
        tuple: A tuple containing four numpy arrays. The arrays represent depth, lithology, percentage, and granulometry, respectively.

    Raises:
        FileNotFoundError: If the file specified by 'filepath' does not exist.
        pd.errors.ParserError: If the file is not a valid Excel, CSV or TXT file.
        KeyError: If the file does not contain the expected columns.
    """
    # Determine the file type from the file extension
    _, file_extension = os.path.splitext(filepath)
    file_extension = file_extension.lower()

    # Read the file based on its type
    if file_extension == '.xlsx':
        data = pd.read_excel(filepath)
    elif file_extension in ['.csv', '.txt']:
        data = pd.read_csv(filepath)
    else:
        raise ValueError(f'Unsupported file type: {file_extension}')

    # Process the data
    data = pd.DataFrame(np.array([data[data.columns[0]], data[data.columns[1]], data[data.columns[2]], data[data.columns[3]]]).T)
    data.columns = ["PROF", "LITO", "%", "GRAN"]
    Prof = np.array(data.PROF)
    for i in range(len(Prof)):
        if np.isnan(Prof[i]) != True:
            pass
        else:
            while (np.isnan(Prof[i]) == True):
                Prof[i] = Prof[i - 1]

    return Prof, data.LITO, data['%'], data.GRAN
