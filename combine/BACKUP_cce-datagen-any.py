import argparse
import time
import json
import csv

'''
The following arguments are accepted:
    json1 - will group output by timestamp, then flat key/value pairs. This assumes the device uid can be associated with telemetry code somehow (e.g. DE7 is known to be associated with bb_uid)
    json2 - will group output by timestamp+uid, then key/value pairs.
    csv1
'''
parser = argparse.ArgumentParser(description='Generate random CCE data')
parser.add_argument('output', help='Specify the type of file output desired')
args = parser.parse_args()
output_type = args.output

fridge_file = "output_fridge.csv"
blackbox_file = "output_blackbox.csv"
compressor_file = "output_compressor.csv"

fridge_uid = "UNKNOWN"

records_dict = dict()

def processCompData(file_type):
    with open(compressor_file) as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if file_type == "json1":
                if row[0] in records_dict:
                    records_dict[row[0]][row[2]] = row[3]
                    records_dict[row[0]]['comp_uid'] = row[1]
                    records_dict[row[0]]['fridge_id'] = fridge_uid
                else:
                    records_dict[row[0]] = {}
                    records_dict[row[0]][row[2]] = row[3]
                    records_dict[row[0]]['comp_uid'] = row[1]
                    records_dict[row[0]]['fridge_id'] = fridge_uid
                        
            elif file_type == "json2":
                if row[0] in records_dict:
                    if row[1] in records_dict[row[0]]:
                        records_dict[row[0]][row[1]][row[2]] = row[3]
                    else:
                        records_dict[row[0]][row[1]] = {}
                        records_dict[row[0]][row[1]][row[2]] = row[3]
                else:
                    records_dict[row[0]] = {}
                    records_dict[row[0]][row[1]] = {}
                    records_dict[row[0]][row[1]][row[2]] = row[3]
            else:
                print("Filetype not supported!")

def processBBData(file_type):
    with open(blackbox_file) as csv_file:
        csv_reader = csv.reader(csv_file)
        
        for row in csv_reader:
            if file_type == "json1":
                for row in csv_reader:
                    if row[0] in records_dict:
                        records_dict[row[0]][row[2]] = row[3]
                        records_dict[row[0]]['bb_uid'] = row[1]
                        records_dict[row[0]]['fridge_id'] = fridge_uid
                    else:
                        records_dict[row[0]] = {}
                        records_dict[row[0]][row[2]] = row[3]
                        records_dict[row[0]]['bb_uid'] = row[1]
                        records_dict[row[0]]['fridge_id'] = fridge_uid
            elif file_type == "json2":
                if row[0] in records_dict:
                    if row[1] in records_dict[row[0]]:
                        records_dict[row[0]][row[1]][row[2]] = row[3]
                    else:
                        records_dict[row[0]][row[1]] = {}
                        records_dict[row[0]][row[1]][row[2]] = row[3]
                else:
                    records_dict[row[0]] = {}
                    records_dict[row[0]][row[1]] = {}
                    records_dict[row[0]][row[1]][row[2]] = row[3]
            else:
                print("Filetype not supported!")

def processFridgeData():
    with open(fridge_file) as csv_file:
        csv_reader = csv.reader(csv_file)
    
        for row in csv_reader:
            fridge_uid = row[1]
        
        return(fridge_uid)

def outputCSV():
    pass

def outputJSON(filename):
    with open(filename, 'w') as json_file:
        json.dump(records_dict, json_file, sort_keys=True)

def outputYAML():
    pass


if __name__ == '__main__':
    
    fridge_uid = processFridgeData()

    processCompData(output_type)
    processBBData(output_type)
    
    if output_type == "json1":
        outputJSON("output_combined_format1.json")
    elif output_type =="json2":
        records_dict["fridge_id"] = fridge_uid
        outputJSON("output_combined_format2.json")
    else:
        print("FILETYPE NOT SUPPORTED")

    #print(records_dict)
