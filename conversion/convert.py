from pathlib import Path
import json
import numpy as np

generatedDataFile = Path(r'/Users/jayrsood/Documents/3rd Year/medicaliot/medicaliot/datagen/generated.json')
iomtDataFile = Path(r'/Users/jayrsood/Documents/3rd Year/medicaliot/medicaliot/datagen/IoMT.json')

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
    device_array = [0,0,0,0,0,0,0,0]

#Opening generated file:
    with open(generated, 'r') as f:
        convert_dict = json.load(f)

    for device in range(0, len(convert_dict)):
        current_device = 'Device ' + str(device)

        try:
            device_array[0] = getKeyFromValue(convert_dict[current_device]["CPU"][0], cpu_hashtable)
        except KeyError:
            print("One or more key(s) not in hashtable.")

    # for device in range(0, len(convert_dict)):
    #     current_device = 'Device ' + str(device)
    #     device_array.append([
    #     [convert_dict[current_device]["Width"]],
    #     [convert_dict[current_device]["Length"]],
    #     [convert_dict[current_device]["Height"]],
    #     [convert_dict[current_device]["Weight"]],
    #     ])

    #Convert to numpy array
    numpy_device_array = np.asarray(device_array, dtype=np.float32)

    print(numpy_device_array)
    print(cpu_hashtable)




nametable, cputable, sensortable, connectable = populateHashtable(iomtDataFile)
conversion(generatedDataFile, nametable, cputable, sensortable, connectable)
