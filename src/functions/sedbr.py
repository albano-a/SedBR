# Functions that are used in SedBR
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import copy
import json
from src.dictionaries.litologias import *


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

def validate_lithology_mnemonic(mnemonico):
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

def map_lithology_to_granulometry(x, y=np.nan):
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

def processed_data(fname):
    """
    This function reads data from an Excel, CSV or TXT file and processes it.

    The function reads data from a file specified by the global variable 'fname'.
    The data is expected to have four columns: "PROF", "LITO", "%", and "GRAN".
    These columns represent depth, lithology, percentage, and granulometry, respectively.

    The function processes the depth data to fill in any missing values.
    If a depth value is missing (NaN), it is replaced with the previous depth value.

    Returns:
        tuple: A tuple containing four numpy arrays. The arrays represent depth,
        lithology, percentage, and granulometry, respectively.

    Raises:
        FileNotFoundError: If the file specified by 'fname' does not exist.
        pd.errors.ParserError: If the file is not a valid Excel, CSV or TXT file.
        KeyError: If the file does not contain the expected columns.
    """
    # Determine the file type from the file extension
    _, file_extension = os.path.splitext(fname)
    file_extension = file_extension.lower()

    # Read the file based on its type
    if file_extension == '.xlsx':
        data = pd.read_excel(fname)
    elif file_extension in ['.csv', '.txt']:
        data = pd.read_csv(fname)
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

def sort_lithology_by_type(list_of_lists):
    """
    This function appends a numerical value to each sublist in 'a' based on the
    first element of the sublist, and then sorts 'a' based on these appended values.

    Args:
        a (list): A list of lists. Each sublist is expected to have a string as
        its first element.

    Returns:
        list: The input list 'a', sorted based on the appended numerical values.
    """
    lithology_map = {
        'AGT': 1, 'AGC': 1, 'AGL': 1, 'AGB': 1, 'ARG': 1,  # Argilas
        'FLH': 2, 'FLS': 2, 'MRG': 2, 'TOL': 2,  # Folhelhos
        'SLT': 3, 'AGS': 3, 'TOS': 3,  # siltes
        'ARN': 4, 'ARE': 4, 'ARL': 4, 'ARF': 4, 'ART': 4, 'ARC': 4,  # areias
        'CGL': 5, 'ARO': 5, 'BRC': 5, 'DMT': 5,
        'CAL': 6, 'CLC': 6, 'CHT': 6, 'DOL': 6,  # calcario
        'CLU': 7, 'MDS': 7,  # Cal argilitO
        'WKS': 7.5,
        'CSI': 8, 'PKS': 8,  # Cal siltito
        'CRE': 9, 'GRS': 9,  # Cal arenito
        'CRU': 10, 'COQ': 10, 'BLT': 10  # Cal rudito
    }

    for sublist in list_of_lists:
        sublist.append(lithology_map.get(sublist[0], 999))

    list_of_lists.sort(key=lambda x: x[-1])

    return list_of_lists

def sum_lithology_percentages(lithology_list):
    """
    This function sums the percentages of similar lithologies in a given list.

    The function iterates over a list of lists,
    where each sublist represents a lithology and its percentage.
    If it finds two sublists with the same lithology, it adds their
    percentages together and sets the percentage of the first sublist to 0.

    Args:
        lithology_list (list): A list of lists. Each sublist is expected to have a lithology as its first element and a percentage as its second element.

    Returns:
        list: The input list 'lithology_list', with the percentages of similar lithologies summed together.
    """
    # Iterate over the lithology list
    for i in range(len(lithology_list)):
        current_lithology = lithology_list[i][0]

        # Compare the current lithology with the rest of the lithologies in the list
        for j in range(len(lithology_list)):
            if i != j and current_lithology == lithology_list[j][0]:
                # If two lithologies are the same, add their percentages together
                lithology_list[j][1] = int(lithology_list[i][1]) + int(lithology_list[j][1])
                # Set the percentage of the first lithology to 0
                lithology_list[i][1] = 0

    return lithology_list

def process_geo_data():
    """
    This function processes geological data and returns two dictionaries.

    The first dictionary, 'l', has depth levels as keys. Each key maps to another dictionary
    with keys "Lito", "Espacamento", and "Granulometria".
    "Lito" maps to a list of lithology codes and their corresponding percentages.
    "Espacamento" maps to the interval between the current depth and the next one.
    "Granulometria" maps to the granulometry of the lithology.

    The second dictionary, 'gnm', has depth levels as keys. Each key maps to a list
    containing the lithology code with the highest percentage and its granulometry.

    The function assumes that the data() function returns a list of four lists: depth
    levels, lithologies, percentages, and granulometries.

    Returns:
        tuple: A tuple containing two dictionaries. The first dictionary
        contains detailed information for each depth level. The second dictionary
        contains the dominant lithology and its granulometry for each depth level.
    """
    # Get data from data function
    prof, lit, perc, granu = processed_data()

    # Calculate intervals
    d = intervalo(prof)

    # Initialize dictionaries
    l = {prof[0]: {
        "Lito": [[validate_lithology_mnemonic(lit[0]), porcentagem(perc[0])]],
        "Espacamento": d[prof[0]],
        "Granulometria": map_lithology_to_granulometry(validate_lithology_mnemonic(lit[0]), granu[0])
    }}
    gnm = {}

    # Initialize lithology list
    g = [[validate_lithology_mnemonic(lit[0]), porcentagem(perc[0]), granu[0]]]

    # Iterate over the data
    for i in range(1, len(prof)):
        # If depth level already exists in dictionary
        if prof[i] in l:
            # If depth level is the same as previous
            if prof[i] == prof[i-1]:
                # Append lithology to list
                l[prof[i]]["Lito"].append([validate_lithology_mnemonic(lit[i]), porcentagem(perc[i])])
                g.append([validate_lithology_mnemonic(lit[i]), porcentagem(perc[i]), granu[i]])
        else:
            # Sum percentages of similar lithologies
            g = sum_lithology_percentages(g)
            # Sort lithologies by percentage in descending order
            g.sort(key=lambda x: int(x[1]), reverse=True)
            # Add dominant lithology and its granulometry to dictionary
            gnm[prof[i-1]] = [g[0][0], map_lithology_to_granulometry(g[0][0], g[0][2])]
            # Reset lithology list
            g = [[validate_lithology_mnemonic(lit[i]), porcentagem(perc[i]), granu[i]]]
            # Add new depth level to dictionary
            l[prof[i]] = {
                "Lito": [[validate_lithology_mnemonic(lit[i]), porcentagem(perc[i])]],
                "Espacamento": d[prof[i]],
                "Granulometria": map_lithology_to_granulometry(validate_lithology_mnemonic(lit[i]), granu[i])
            }

    # Process the last depth level
    g = sum_lithology_percentages(g)
    g.sort(key=lambda x: int(x[1]), reverse=True)
    gnm[prof[i]] = [g[0][0], map_lithology_to_granulometry(g[0][0], g[0][2])]

    # Return dictionaries
    return l, gnm

def convert_depth_lithology_granulometry_to_arrays(gnm):
    """
    This function converts the input dictionary into three numpy arrays.

    The function iterates over the keys of the input dictionary 'gnm'.
    It appends each key to the 'pf' list, and the corresponding lithology
    and granulometry to the 'litg' and 'gran' lists, respectively.
    It then adjusts the first element of the 'pf' list and converts all three
    lists into numpy arrays.

    Args:
        gnm (dict): A dictionary mapping each depth to a list containing lithology and granulometry.

    Returns:
        tuple: A tuple containing three numpy arrays. The first array represents depth, the second represents lithology, and the third represents granulometry.
    """
    # Initialize lists
    pf = [0]
    litg = []
    gran = []

    # Iterate over the keys in the dictionary
    for depth in gnm.keys():
        # Append depth, lithology, and granulometry to their respective lists
        pf.append(depth)
        litg.append(gnm[depth][0])
        gran.append(gnm[depth][1])

    # Adjust the first depth value
    pf[0] = pf[1] - (pf[2] - pf[1])

    # Convert lists to numpy arrays and return
    return np.array(pf), np.array(litg), np.array(gran)

def process_geological_data_arrays(depth, granulo, lithology):
    """
    This function processes three input arrays and returns three output arrays.

    The function iterates over the 'depth' array. For the first element,
    it appends two values to each output array.
    For the remaining elements, it appends one value to each output array.
    After the loop, it appends the last element of each input array to the
    corresponding output array.

    Args:
        depth (array): An array of depth values.
        granulo (array): An array of granulometry values.
        lithology (array): An array of lithology values.

    Returns:
        tuple: A tuple containing three arrays. The first array represents depth,
        the second represents granulometry, and the third represents lithology.
    """
    # Initialize output arrays
    prof_out = []  # depth
    gran_out = []  # granulometry
    lith_out = []  # lithology

    # Iterate over the depth array
    for i in range(len(depth) - 1):
        if i == 0:
            # For the first depth value, append two values to each output array
            prof_out.extend([depth[i+1] - (depth[i+1] - depth[i]), depth[i]])
            gran_out.extend([granulo[i], granulo[i]])
            lith_out.extend([lithology[i], lithology[i]])
        else:
            # For the remaining depth values, append one value to each output array
            gran_out.append(granulo[i])
            prof_out.append(depth[i])
            lith_out.append(lithology[i])

    # Append the last element of each input array to the corresponding output array
    gran_out.append(granulo[-1])
    prof_out.append(depth[-1])
    lith_out.append(lithology[-1])

    # Return output arrays
    return prof_out, gran_out, lith_out
