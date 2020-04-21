import argparse
import time
import faker
import csv
import json
import pandas as pd
from collections import OrderedDict
from functools import singledispatch
import os
import yaml
import gzip
import shutil

fake = faker.Faker()

'''
parser = argparse.ArgumentParser(description='Generate random CCE data')
parser.add_argument('hours', help='Specify the total number of hours for which you want to create sample data', type=int)
args = parser.parse_args()
'''

parser = argparse.ArgumentParser(description='Generate random CCE data')
parser.add_argument('days', help='Specify the interval in days for which you want to create sample data', type=int)
args = parser.parse_args()

total_days = args.days
total_hours = 24 * total_days # Duration in hours that sample data set should span
#total_hours = args.hours
sample_interval_mins = 10 # Sample set collection interval in minutes
sample_interval_secs = sample_interval_mins * 60 # Sample set collection interval in seconds
total_mins = 60 * total_hours # Total hours to create sample data
record_sets = total_mins / sample_interval_mins # Number of unique sample records to create
time_now = int(time.time()) # Current time in epoch

csvFilePath = 'output/output_csv.csv'
tempJsonPath = 'output/tempJson.json'
jsonFilePath1 = 'output/output_json1.json'
jsonFilePath2 = 'output/output_json2.json'
yamlFilePath1 = 'output/output_yaml1.yml'
yamlFilePath2 = 'output/output_yaml2.yml'
reportFilePath = 'output/report.txt'

fridge_sn = "14D-1179"
cce_id = "CCE-id-1234"
bb_id = "bbid-2056x"

fieldnames = ['ts', 'f_uid', 'bb_uid', 'DE3', 'cce_uid', 'DE7', 'DE0', 'DE1', 'DY0', 'MN0', 'VO1', 'VO2', 'VO3', 'W0', 'PP0', 'MN2', 'MN3', 'CO0', 'AL', 'AA']

def write_DE3(): # This is the compartment temp reported by black box
    
    de3_value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    writer.writerow({'ts': time_now + 100, 'f_uid': fridge_sn, 'bb_uid': bb_id, 'DE3': de3_value})

def write_records():
    
    de7_value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    de0_value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    de1_value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    dy0_value = fake.random_int(1,999)
    mn0_value = fake.random_int(0,10)
    vo1_value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=600.0)
    vo2_value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=999)
    vo3_value = fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=99)
    w0_value = fake.pyfloat(left_digits=4, right_digits=1, positive=True, min_value=0, max_value=9999)
    pp0_value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=300.0)
    mn2_value = fake.random_int(0,10)
    mn3_value = fake.random_int(0,10)
    co0_value = fake.random_int(0,255)
    al_value = fake.random_int(10000000,99999999)
    aa_value = fake.random_int(10000000,99999999)
    writer.writerow({'ts': time_now, 'f_uid': fridge_sn, 'cce_uid': cce_id, 'DE7': de7_value, 'DE0': de0_value, 'DE1': de1_value, 'DY0': dy0_value, 'MN0': mn0_value, 'VO1': vo1_value, 'VO2': vo2_value, 'VO3': vo3_value, 'W0': w0_value, 'PP0': pp0_value, 'MN2': mn2_value, 'MN3': mn3_value, 'CO0': co0_value, 'AL': al_value, 'AA': aa_value})


def write_json1():
    df = pd.read_csv(csvFilePath)
    jsonresult = df.to_json(orient='records')
    rows = json.loads(jsonresult)

    # Remove the null values in data set
    new_rows = [
        OrderedDict([
            (key, row[key]) for key in df.columns
            if (key in row) and pd.notnull(row[key])
        ])
        for row in rows
    ]
    new_json_output = json.dumps(new_rows)
    
    # output new data set with null values removed
    with open(jsonFilePath1, 'w') as outfile:
        outfile.write(new_json_output)


def write_json2():

    df = pd.read_csv(csvFilePath, index_col='ts')
    df.to_json(tempJsonPath, orient='index')

    @singledispatch
    def remove_null_bool(ob):
        return ob

    @remove_null_bool.register(list)
    def _process_list(ob):
        return [remove_null_bool(v) for v in ob]

    @remove_null_bool.register(dict)
    def _process_list(ob):
        return {k: remove_null_bool(v) for k, v in ob.items()
                if v is not None and v is not True and v is not False}

    with open('output/tempJson.json') as json_file:
        data = json.load(json_file)
        output_data = json.dumps(remove_null_bool(data), sort_keys=True)
        with open("output/output_json2.json", "w") as f:
            f.write(output_data)
    os.remove(tempJsonPath)

def write_yaml1():
    with open(jsonFilePath1, 'r') as f:
        jsonData = json.load(f)
    
    with open(yamlFilePath1, 'w') as y_out:
        yaml.dump(jsonData, y_out, default_flow_style=False)

def write_yaml2():
    with open(jsonFilePath2, 'r') as f:
        jsonData = json.load(f)
    
    with open(yamlFilePath2, 'w') as y_out:
        yaml.dump(jsonData, y_out, default_flow_style=False)

def zip_output(target):
    with open(target, 'rb') as f_in:
        with gzip.open(target + '.gz', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

def create_final_report():
    f_out = open(reportFilePath, 'w')
    f_out.write("Type,Uncompressed,Compressed\n")
    f_out.write("csv,{0},{1}\n".format(os.stat(csvFilePath).st_size, os.stat(csvFilePath + '.gz').st_size))
    f_out.write("json1,{0},{1}\n".format(os.stat(jsonFilePath1).st_size, os.stat(jsonFilePath1 + '.gz').st_size))
    f_out.write("json2,{0},{1}\n".format(os.stat(jsonFilePath2).st_size, os.stat(jsonFilePath2 + '.gz').st_size))
    f_out.write("yaml1,{0},{1}\n".format(os.stat(yamlFilePath1).st_size, os.stat(yamlFilePath1 + '.gz').st_size))
    f_out.write("yaml2,{0},{1}\n".format(os.stat(yamlFilePath2).st_size, os.stat(yamlFilePath2 + '.gz').st_size))
    f_out.close()

if __name__ == '__main__':
    
    # Write CSV
    with open(csvFilePath, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while record_sets > 0:
            write_DE3()
            write_records()
            time_now += sample_interval_secs
            record_sets -= 1
    csv_file.close()

    # Write JSON format 1
    write_json1()

    # Write JSON format 2
    write_json2()

    # Convert JSON1 to YAML1
    write_yaml1()

    # Convert JSON2 to YAML2
    write_yaml2()

    # Compress CSV results
    zip_output(csvFilePath)
    zip_output(jsonFilePath1)
    zip_output(jsonFilePath2)
    zip_output(yamlFilePath1)
    zip_output(yamlFilePath2)

    # Create File Size Report
    create_final_report()