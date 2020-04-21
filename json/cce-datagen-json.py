import argparse
import time
import faker
import json

fake = faker.Faker()

parser = argparse.ArgumentParser(description='Generate random CCE data')
parser.add_argument('hours', help='Specify the total number of hours for which you want to create sample data', type=int)
args = parser.parse_args()

total_hours = args.hours # Duration in hours that sample data set should span
sample_interval_mins = 10 # Sample set collection interval in minutes
sample_interval_secs = sample_interval_mins * 60 # Sample set collection interval in seconds
total_mins = 60 * total_hours # Total hours to create sample data
record_sets = total_mins / sample_interval_mins # Number of unique sample records to create
time_now = int(time.time()) # Current time in epoch

fridge_id = "1000039914437726336"
fridge_sn = "14D-1179"

cce_id = "CCE-id-1234"


def generate_DE3(): # This is the compartment temp reported by black box
    uid = "bbid-2056x"
    code = "DE3"
    unit = "C"
    value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    return uid,code,unit,value

def generate_DE7():
    uid = "uid1"
    code = "DE7"
    unit = "C"
    value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    return uid,code,unit,value

def generate_DE0():
    uid = "uid2"
    code = "DE0"
    unit = "C"
    value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    return uid,code,unit,value

def generate_DE1():
    uid = "uid3"
    code = "DE1"
    unit = "C"
    value = fake.pyfloat(left_digits=2, right_digits=2, positive=False, min_value=None, max_value=None)
    return uid,code,unit,value

def generate_DY0():
    uid = "uid4"
    code = "DY0"
    unit = "h"
    value = fake.random_int(1,999)
    return uid,code,unit,value

def generate_MN0():
    uid = "uid5"
    code = "MN0"
    unit = "m"
    value = fake.random_int(0,10)
    return uid,code,unit,value

def generate_VO1():
    uid = "uid6"
    code = "VO1"
    unit = "m"
    value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=600.0)
    return uid,code,unit,value

def generate_VO2():
    uid = "uid7"
    code = "VO2"
    unit = "Vrms"
    value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=999)
    return uid,code,unit,value

def generate_VO3():
    uid = "uid8"
    code = "VO3"
    unit = "Vdc"
    value = fake.pyfloat(left_digits=2, right_digits=1, positive=True, min_value=0, max_value=99)
    return uid,code,unit,value

def generate_W0():
    uid = "uid9"
    code = "W0"
    unit = "W"
    value = fake.pyfloat(left_digits=4, right_digits=1, positive=True, min_value=0, max_value=9999)
    return uid,code,unit,value

def generate_PP0():
    uid = "uid10"
    code = "PP0"
    unit = "Hz"
    value = fake.pyfloat(left_digits=3, right_digits=1, positive=True, min_value=0, max_value=300.0)
    return uid,code,unit,value

def generate_MN2():
    uid = "uid11"
    code = "MN2"
    unit = "m"
    value = fake.random_int(0,10)
    return uid,code,unit,value

def generate_MN3():
    uid = "uid12"
    code = "MN3"
    unit = "m"
    value = fake.random_int(0,10)
    return uid,code,unit,value

def generate_CO0():
    uid = "uid13"
    code = "CO0"
    unit = "m"
    value = fake.random_int(0,255)
    return uid,code,unit,value

def generate_AL(): # Cheating by using random 8-digit int
    uid = "uid14"
    code = "AL"
    unit = "bit"
    value = fake.random_int(10000000,99999999)
    return uid,code,unit,value

def generate_AA(): # Cheating by using random 8-digit int
    uid = "uid15"
    code = "AA"
    unit = "bit"
    value = fake.random_int(10000000,99999999)
    return uid,code,unit,value

function_list = [generate_DE7, generate_DE0, generate_DE1, generate_DY0, generate_MN0, generate_VO1, generate_VO2, generate_VO3, generate_W0, generate_PP0, generate_MN2, generate_MN3, generate_CO0, generate_AL, generate_AA]

if __name__ == '__main__':

    records_dict = {}


    while record_sets > 0:
        records_dict[time_now] = {}

        for func in function_list:
            ref_uid, ref_code, ref_unit, ref_value = func()
            records_dict[time_now][ref_code] = ref_value
            records_dict[time_now]['uid'] = cce_id
        time_now += sample_interval_secs
        record_sets -= 1

    #print(json.dumps(records_dict, indent = 4, sort_keys=True))
    
    with open('output_compressor.json', 'w') as json_file:
        json.dump(records_dict, json_file)

