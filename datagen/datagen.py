import math, random, sys, os, json
# TODO - ram in incrments of 256 and also testing vs training mode.
# also misc validation
def initialise_tool():
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
        random_dict["Device " + str(i)] = sub_dict

    # Dumps to json file:
    with open('generated.json', 'w+') as filew:
        json.dump(random_dict, filew, indent = 2)


def randomValueFromDict(generator):
    #not complete, weird sensor behaviour, try catch needed
    outlist = []

    if len(generator) == 1:
        return generator
    elif isinstance(generator[0],int):
        return random.randint(generator[0],generator[1])
    elif isinstance(generator[0],str) and len(generator) > 1:
        for i in range(0,random.randint(0,len(generator))):
            outlist.append(generator[i])
        return outlist
    else:
        print("Check IoMT.json file! Data possibly corrupt.")
        sys.exit()


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
