import math, random, sys, os, json

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


def generate(dict, noKeys):
    # Picks a random device from the JSON data
    # Generates pseudorandom attribues dependant on device

    # Choose random Device Type:
    random_index = random.randint(0,noKeys - 1)
    random_device = dict[list(dict.keys())[random_index]] #random.choice?()
    random_dict = {}

    # Generate random attributes:
    for key in random_device["Attributes"]:
        random_dict[key] = randomValueFromDict(random_device["Attributes"][key])

    with open('generated.json', 'w+') as filew:
        json.dump(random_dict, filew, indent = 2)
        open into a dictionary containing a list of dictionarys

def randomValueFromDict(generator):
    #not complete, weird sensor behaviour, try catch needed
    outlist = ['yeet']
    if len(generator) == 1:
        return generator
    elif isinstance(generator[0],int):
        return random.randint(generator[0],generator[1])
    elif isinstance(generator[0],str) and len(generator) > 1:
        for i in range(0,random.randint(0,len(generator))):
            outlist.append(generator[i])
        return outlist


def main():
    initialise_tool()
    IoMT_Data, lenKeys = initialise_json()
    try:
        noRecords = int(input("Enter number of entries to generate:"))
    except ValueError:
        print("Please enter an integer.")
        sys.exit()
    print("Generating " + str(noRecords) + " entries...")

    for i in range(noRecords):
        generate(IoMT_Data, lenKeys)

    print("Data generated!")

main()
