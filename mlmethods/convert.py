from pathlib import Path
import json
import numpy as np
import pandas as pd

GLOBAL_MAX_SENSOR = 7
GLOBAL_MAX_CONNECT = 3

generatedDataFile = Path(r'/Users/jayrsood/Documents/3rd Year/medicaliot/medicaliot/datagen/generated.json')
iomtDataFile = Path(r'/Users/jayrsood/Documents/3rd Year/medicaliot/medicaliot/datagen/IoMT.json')

def formatStringList(value_list, hashtable):
    value_key_list = []
    for string in range(0, len(value_list)):
        value_key = getKeyFromValue(value_list[string], hashtable)
        value_key_list.append(value_key)
    return value_key_list


def getKeyFromValue(value, hashtable):
    for key, potential_value in hashtable.items():
        if value == potential_value:
            return key
    raise KeyError

def populateHashtable(iomtdata):
    '''
    Converts string components of IoMT.json file into hashtable to be used in array
    '''
    name_hashtable = {}
    cpu_hashtable = {0:'0'}
    sensor_hashtable = {0:'0'}
    connect_hashtable = {0:'0'}

    with open(iomtdata, 'r') as f:
        iomt_dict = json.load(f)

    for dev_key in range(0, len(iomt_dict)):
        current_device = "Device_" + str(dev_key)

#Populate Name hashtable
        name_hashtable[dev_key] = iomt_dict[current_device]["Name"]

#Populate CPU hashtable
        for cpu_key in range(0, len(iomt_dict[current_device]["Attributes"]["CPU"])):
            if not(iomt_dict[current_device]["Attributes"]["CPU"][cpu_key] in cpu_hashtable.values()):
                insert_point = list(cpu_hashtable.keys())
                insert_point = insert_point[-1]
                cpu_hashtable[insert_point + 1] = iomt_dict[current_device]["Attributes"]["CPU"][cpu_key]

#Populate Sensor hashtable
        for sensor_key in range(0, len(iomt_dict[current_device]["Attributes"]["Sensors"])):
            if not(iomt_dict[current_device]["Attributes"]["Sensors"][sensor_key] in sensor_hashtable.values()):
                insert_point = list(sensor_hashtable.keys())
                insert_point = insert_point[-1]
                sensor_hashtable[insert_point + 1] = iomt_dict[current_device]["Attributes"]["Sensors"][sensor_key]

#Populate Connectivity hashtable
        for connect_key in range(0, len(iomt_dict[current_device]["Attributes"]["Connectivity"])):
            if not(iomt_dict[current_device]["Attributes"]["Connectivity"][connect_key] in connect_hashtable.values()):
                insert_point = list(connect_hashtable.keys())
                insert_point = insert_point[-1]
                connect_hashtable[insert_point + 1] = iomt_dict[current_device]["Attributes"]["Connectivity"][connect_key]

    del cpu_hashtable[0]
    del sensor_hashtable[0]
    del connect_hashtable[0]

    return name_hashtable, cpu_hashtable, sensor_hashtable, connect_hashtable

def conversion(generated, name_hashtable, cpu_hashtable, sensor_hashtable, connect_hashtable):
    '''
    Converts generated.json file into numpy array for input to ML algorithms
    '''
    to_convert = []

#Opening generated file:
    with open(generated, 'r') as f:
        convert_dict = json.load(f)

    for device in range(0, len(convert_dict)):
        device_array = [0,0,0,0,0,0,0,-1]
        current_device = 'Device ' + str(device)
        current_value_list = list(convert_dict[current_device].values())

    #Deals with integer values of generated.json
        device_array[1] = [convert_dict[current_device]["Width"]]
        device_array[2] = [convert_dict[current_device]["Length"]]
        device_array[3] = [convert_dict[current_device]["Height"]]
        device_array[4] = [convert_dict[current_device]["Weight"]]

    #Deals with string values of generated.json
        try:
            device_array[0] = formatStringList(current_value_list[0], cpu_hashtable)
            device_array[5] = formatStringList(current_value_list[5], sensor_hashtable)
            device_array[6] = formatStringList(current_value_list[6], connect_hashtable)

            if len(current_value_list) > 7:
                name_list = []
                name_list.append(current_value_list[7])
                device_array[7] = formatStringList(name_list, name_hashtable)

            to_convert.append(device_array)
        except KeyError:
            print("Key not found in dictionary!")

    return to_convert

def flattenListForML(list):
    output_list = []

#Setup lists for incoming data, populate with 0's
    for i in range(0, len(list)):
        output_list.append([0,0,0,0,0])
    #The +1 is for the CLASS at the end of list.
    for entry in range(0, len(output_list)):
        for j in range(0, (GLOBAL_MAX_SENSOR + GLOBAL_MAX_CONNECT + 1)):
            output_list[entry].append(0)

#Copies non string entries to new list
    for record in range(0, len(list)):
        delist = []
        for list_item in range(0,5):
            output_list[record][list_item] = list[record][list_item][0]

        #Pulls all actual lists from record into delist
        for element in range(5,len(list[record]) - 1):
            delist.append(list[record][element])

        #Transfers elements of delist to new ML friendly structure
        if len(delist) != 0:
            sensor_head_pointer = 5
            connect_head_pointer = 12
            for sensor_element in range(0, len(delist[0])):
                output_list[record][sensor_head_pointer] = delist[0][sensor_element]
                sensor_head_pointer += 1

            for connect_element in range(0, len(delist[1])):
                output_list[record][connect_head_pointer] = delist[1][connect_element]
                connect_head_pointer += 1

        #Transfers CLASS to new ML friendly structure
        output_list[record][15] = list[record][7][0]

    return output_list

def convert(return_nametable):

    nametable, cputable, sensortable, connectable = populateHashtable(iomtDataFile)
    to_flatten = conversion(generatedDataFile, nametable, cputable, sensortable, connectable)
    converted_list = np.asarray(flattenListForML(to_flatten))

    # for item in list(nametable.items()):
    #     print(item)
    # print("\n")
    # for item in list(cputable.items()):
    #     print(item)
    # print("\n")
    # for item in list(sensortable.items()):
    #     print(item)
    # print("\n")
    # for item in list(connectable.items()):
    #     print(item)
    # print("\n")

    np.savetxt("ml_data.csv", converted_list, delimiter = ',', fmt = '%1d')

    if return_nametable == True:
        return nametable

    print("Conversion complete.")
