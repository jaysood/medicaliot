from pathlib import Path
import json
import numpy as np

dataFile = Path(r'/Users/jayrsood/Documents/3rd Year/medicaliot/medicaliot/datagen/generated.json')

def conversion(generated):
    '''
    Converts generated.json file into numpy array for input to ml algorithms
    '''
    with open(generated, 'r') as f:
        convert_dict = json.load(f)

    device_array = []

    for device in range(0, len(convert_dict)):
        current_device = 'Device ' + str(device)
        device_array.append(
        [[convert_dict[current_device]["RAM"]],
        [convert_dict[current_device]["Height"]],
        [convert_dict[current_device]["Length"]],
        [convert_dict[current_device]["Width"]],
        [convert_dict[current_device]["Weight"]]
        ])


    numpy_device_array = np.asarray(device_array, dtype=np.float32)

    print(numpy_device_array)

conversion(dataFile)
