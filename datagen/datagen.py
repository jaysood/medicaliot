import math, random, sys, os, json
trainingMode = False

def initialise_tool():
    global trainingMode
    print("Warning this tool removes all previously generated data! Please save in a different directory if required!")
    decision = input("Proceed? (Y/N): ")
    if ((decision == 'Y') or (decision == 'y')):
        if(os.path.isfile('generated.json')):
            print("Data deleted.")
            os.remove("generated.json")
        else:
            print("No data found, continuing!")
    else:
        print("Goodbye!")
        sys.exit()

    print("Do you want to generate testing or training data?")
    mode = int(input("Enter:\n 1) Testing\n 2) Training (With Labels)\n"))

    if mode == 1:
        print("Program will generate test data with no labels\n")
    elif mode == 2:
        trainingMode = True
        print("Program will generate training data with labels\n")
    else:
        print("Please select a valid option")
        sys.exit()


def initialise_json():
    with open('IoMT.json') as f:
        device_dict = json.load(f)
        return [device_dict, len(device_dict.keys())]


def generate(noRecordsToGenerate, dict, noKeys):
    # Picks a random device from the JSON data
    # Generates pseudorandom attribues dependant on device
    random_dict = {}

    # Generate random attributes:
    for i in range(noRecordsToGenerate):
        # Picks a random device to generate attributes:
        sub_dict = {}
        random_index = random.randint(0,noKeys - 1)
        random_device = dict[list(dict.keys())[random_index]]
        for key in random_device["Attributes"]:
            sub_dict[key] =  randomValueFromDict(random_device["Attributes"][key])
        if trainingMode == True:
            sub_dict["Name"] = str(random_device["Name"])
        #Correcting CPU list:
        sub_dict["CPU"] = cpuValueCorrector(sub_dict["CPU"])
        random_dict["Device " + str(i)] = sub_dict

    # Dumps to json file:
    with open('generated.json', 'w+') as filew:
        json.dump(random_dict, filew, indent = 2)


def randomValueFromDict(generator):
    #not complete, weird sensor behaviour, try catch needed
    outlist = []

    if len(generator) == 1:
        return generator
    elif isinstance(generator[0], int):
        return random.randint(generator[0], generator[1])
    elif isinstance(generator[0], str) and len(generator) > 1:
        number_to_generate = random.randint(1,len(generator))
        while number_to_generate > 0:
            random_index = random.randint(0,len(generator) - 1)
            data_to_append = generator[random_index]
            if not(data_to_append in outlist):
                outlist.append(data_to_append)
            number_to_generate -= 1
        return outlist
    else:
        print("Check IoMT.json file! Data possibly corrupt.")
        sys.exit()


def cpuValueCorrector(cpu_list):
    #Checks if CPU list contains more than 1 CPU, deletes the end one if so
    if len(cpu_list) > 1:
        del cpu_list[len(cpu_list) - 1]
        return cpu_list
    else:
        return cpu_list


def main():
    initialise_tool()
    IoMT_Data, lenKeys = initialise_json()
    try:
        noRecords = int(input("Enter number of entries to generate:"))
    except ValueError:
        print("Please enter an integer.")
        sys.exit()
    print("Generating " + str(noRecords) + " entries...")

    generate(noRecords, IoMT_Data, lenKeys)

    print("Data generated!")

main()
