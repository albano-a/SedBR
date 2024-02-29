import csv
import json
from litologias import *

# Função para achatar dicionários aninhados
def flatten_dict(dd, separator='_', prefix=''):
    return { prefix + separator + k if prefix else k : v
             for kk, vv in dd.items()
             for k, v in flatten_dict(vv, separator, kk).items()
             } if isinstance(dd, dict) else { prefix : dd }

# Achatando os dicionários
flat_lithologies_num = [flatten_dict(i) for i in lithologies_num.values()]
flat_lithologies_name = [flatten_dict(i) for i in lithologies_name.values()]

# Escrevendo o dicionário lithologies_num achatado em um arquivo .csv
keys = flat_lithologies_num[0].keys()
with open('lithologies_num.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(flat_lithologies_num)

# Escrevendo o dicionário lithologies_name achatado em um arquivo .csv
keys = flat_lithologies_name[0].keys()
with open('lithologies_name.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(flat_lithologies_name)