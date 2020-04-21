import json
import pandas as pd
from pandas.io.json import json_normalize #package for flattening json in pandas df

'''
with open('output_combined_format3.json') as f_input:
    df = pd.read_json(f_input)

df.to_csv('output_combined_csv.csv', index=False)
'''

with open('output_combined_format1.json') as f:
    d = json.load(f)

flattened_json = json_normalize(d['ts'])

print(flattened_json)