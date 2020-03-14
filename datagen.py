import math
import random
import sys
import os

data = [0,0,0,0,0]
monitor = ["blood","glucose","CO2","mmHg","yeet"]

def initialise():
    print("Warning this tool removes all previously generated data! Please save in a different directory if required!")
    decision = input("Proceed? (Y/N): ")
    if ((decision == 'Y') or (decision == 'y')):
        if(os.path.isfile('generated.txt')):
            print("Data deleted.")
            os.remove("generated.txt")
        else:
            print("No data found, continuing!")
    else:
        print("Goodbye!")
        sys.exit()

def randomise():
    for i in range(len(data)):
        data[i] = random.randint(1,10)
    data[4] = monitor[random.randint(0,len(monitor)-1)]

def fileIO(generated):
    dataFile = open("generated.txt", "a")
    dataFile.write(generated + "\n")
    dataFile.close()

def main() :
    initialise()
    try:
        noRecords = int(input("Enter number of entries to generate:"))
    except ValueError:
        print("Please enter an integer.")
        sys.exit()
    print("Generating " + str(noRecords) + " entries...")

    for i in range(noRecords):
        randomise()
        fileIO(str(data))

    print("Data generated!")

main()
