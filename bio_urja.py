import pandas as pd
import matplotlib.pyplot as plt
from colorama import init
init()
from prettytable import PrettyTable 
csv_file_path = "input_data.csv"
data = pd.read_csv(csv_file_path)
list = []

'''
Create a data structure that includes the following fields for each wind farm:
1. ID, represented as WindFarm-Name (e.g., E1, E2, etc.).
2. Weight, which represents the forecast divided by capacity. This value is fixed for each farm.
3. Capacity.
4. Forecast.
'''

for row in data.values:
    list.append({"id": row[0], "weight": row[1] / row[2], "forecast": row[1], "capacity": row[2]})

ids = [item['id'] for item in list]
capacities = [item['capacity'] for item in list]
cur_forecast_sums = []


'''Creating a limit'''
LIMIT = int(input("Enter the Limit: (+-50): "))


'''Error in percentage ratio limit '''
Percentage_ratio = int(input("Enter the range: (+-8) "))

''' Function that swap the elements'''
def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]
    

'''Function that ask the user for continuation of the process'''
def cont():
    while True:
        temp = input("Q(Quit): ").strip()
        if not temp:
            return True  # User pressed Enter to continue
        elif temp.lower() == 'Q':
            return False  # User typed 'q' to quit

'''
Create a function that computes the sum of values within each region to determine the regional ratios. 
Then, calculate the desired target ratio and find the difference between the two ratios.
'''
def calculated(d_obj):
    westSum = 0
    eastSum = 0
    southSum = 0
    northSum = 0

    for obj in d_obj:
        fChar = obj["id"][0]

        if fChar == 'E':
            eastSum += obj["forecast"]
        elif fChar == 'N':
            northSum += obj["forecast"]
        elif fChar == 'W':
            westSum += obj["forecast"]
        elif fChar == 'S':
            southSum += obj["forecast"]

    # Total sum of all regions 
    total = westSum + eastSum + southSum + northSum

    westRegion = (westSum * 100) / total
    eastRegion = (eastSum * 100) / total
    southRegion = (southSum * 100) / total
    northRegion = (northSum * 100) / total


    # Desired target values
    targetWest = 2000
    targetEast = 2800
    targetSouth = 6500
    targetNorth = 1500
    totalOriginal = targetEast + targetNorth + targetSouth + targetWest

    # Calculated original ratio percentage
    Originalwest = (targetWest * 100) / totalOriginal
    Originaleast = (targetEast * 100) / totalOriginal
    Originalsouth = (targetSouth * 100) / totalOriginal
    Originalnorth = (targetNorth * 100) / totalOriginal

    print(Originalwest)
    print(Originaleast)
    print(Originalsouth)
    print(Originalnorth)


    # Difference in original ratio percentage and sample ratio percentage
    diffEast = Originaleast - eastRegion
    diffWest = Originalwest - westRegion
    diffSouth = Originalsouth - southRegion
    diffNorth = Originalnorth - northRegion
    Diff_Total_error = abs(diffWest) + abs(diffEast) + abs(diffSouth) + abs(diffNorth)
    print("Difference between Original and Sample test case East",diffEast)
    print("Difference between Original and Sample test case West",diffWest)
    print("Difference between Original and Sample test case South",diffSouth)
    print("Difference between Original and Sample test case North",diffNorth)
    print(f"West Sample test case Sum: {westSum} West Original Sum:{Originalwest}")
    print(f"WEST Ratio Percentage: {westRegion}")
    print(f"East Sample test case Sum: {eastSum} East Original Sum:{Originaleast}")
    print(f"EAST Ratio Percentage: {eastRegion}")
    print(f"North Sample test case Sum: {northSum} North Original Sum:{Originalnorth}")
    print(f"NORTH Ratio Percentage: {northRegion}")
    print(f"South Sample test case Sum: {southSum} South Original Sum:{Originalsouth}")
    print(f"SOUTH Ratio Percentage: {southRegion}")
    print(f"Total: {total}")

    '''For minimal error'''
    if(Diff_Total_error >= Percentage_ratio*4):
       print("FAILED RATIO MISMATCH")
    else:
        print("SUCCESSFULL")


'''Function that generates the permuations of all the data's in csv files!!'''
def gen_per(nums, start=0):
    if start == len(nums) - 1:
        yield nums.copy() 
    else:
        for i in range(start, len(nums)):
            swap(nums, start, i)
            
            yield from gen_per(nums, start + 1)
            
            swap(nums, start, i)

'''
The user needs to specify the acceptable limit and error margin to meet the output conditions.
Implement a validation function that identifies the closest permutation and displays the desired output.
'''
def validate(d,RANGE):
    if(RANGE >= 12000 - LIMIT and RANGE <= 12000 + LIMIT):
        table = PrettyTable()
        table.field_names = d[0].keys()
        for row in d:
            table.add_row(row.values())
        print(table)
        print(RANGE)
        calculated(d)
        if(not cont()):
            return False
    return True

for perm in gen_per(capacities):
    sum = 0
    for i in range(len(perm)):
        list[i]["capacity"] = perm[i]
        list[i]["forecast"] = list[i]["weight"]*perm[i] 
        sum += list[i]["weight"]*perm[i]
    cur_forecast_sums.append(sum)
    out = validate(list, sum)
    if(not out):
        plt.plot(cur_forecast_sums)
        plt.show()
        df = pd.DataFrame(list)
        df.to_csv("output_data.csv", index=False)
        break