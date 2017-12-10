# Kyle Marcus Enriquez
#
# This program calculates the highest possible total satisfaction rating from every person
# in a group travelling to various locations. Each person achieves full satisfaction if all
# desired locations are travelled to while they only achieve partial satisfaction if their group
# was unable to go to a location he/she wanted to go to. Each location has an opening, closing
# and duration time.
#
# This program takes as input the following:
#   people(n)
#   locations(m)
#   preferences(o)
#   schedule(location, x, y, z)
#   allPreferences(people, location)
#
#   people(n) - the number of people as input where n is a positive non-zero integer.
#   locations(m) - the number of locations as input where m is a positive non-zero integer.
#   preferences(o) - the total number of preferences from all the people from people(n) where o is a
#       positive non-zero integer.
#   schedule(location1, x, y, z) - the schedule of location1 where x is the opening time, y is the
#       closing time, and z is the duration time. This input must be repeated m times. Times must be
#       in military format and location1 must be an integer 0 < location1 <= m. This input must be
#       repeated m times for every location.
#   allPreferences(person, location2) - implies that person desires to go to location2. location2
#       must be an integer 0 < location2 <= m and person must be an integer 0 < person <= n.

import sys
import math

def CheckIfEmpty(str):
    if not str.strip():
        return True
    else:
        return False

def GetNonEmptyLine(str):
    while True:
        if CheckIfEmpty(str) == False:
            return str[str.index("(") + 1:str.rindex(")")]
        else:
            str = f.readline()

def getTotalPrefs(list):
    ret = []
    i = 0
    while i < people:
        ret.append(0)
        i = i + 1
    for pref in list:
        ret[pref[0]-1] = ret[pref[0]-1] + 1
    return ret

def getLatestTime(list):
    max = 0
    for item in list:
        if item[3] > max:
            max = item[3]
    return max

def getFirstTime(list, schedule):
    for item in schedule:
        if item[0] == list[0][1]:
            return item[2]

filename = sys.argv[1]
f = open(filename, "r")

people = f.readline()
people = int(GetNonEmptyLine(people))

locations = f.readline()
locations = int(GetNonEmptyLine(locations))

preferences = f.readline()
preferences = int(GetNonEmptyLine(preferences))

# Now for the preferences
i = 1
schedule = []

# Get all the locations preferred by each person
while i <= locations:
    temp = f.readline()
    temp = GetNonEmptyLine(temp)
    temp = temp.split(",")
    temp = list(map(int,temp))
    schedule.append(temp)
    i = i + 1

allPrefs = []
i = 1
while i <= preferences:
    temp = f.readline()
    temp = GetNonEmptyLine(temp)
    temp = temp.split(",")
    temp = list(map(int, temp))
    allPrefs.append(temp)
    i = i + 1

currentTime = 0
maxTime = 0
maxTimeLoc = 0
startLocation = 0
prev = 99
for group in schedule:
    if group[2] < prev:
        prev = group[2]
        currentTime = group[2]
        startLocation = group[0]
    if group[3] > maxTime:
        maxTime = group[3]
        maxTimeLoc = group[0]


# values for test1
satisfaction1 = []
visited1 = []
p = 0
while p < people:
    satisfaction1.append(0)
    p = p + 1


# values for test2
satisfaction2 = []
visited2 = []
p = 0
while p < people:
    satisfaction2.append(0)
    p = p + 1

#values for test3
satisfaction3 = []
visited3 = []
p = 0
while p < people:
    satisfaction3.append(0)
    p = p + 1


# GET ALL MINIMUM SATISFACTIONS, FIND THE MAXIMUM
# CREATE A LIST OF LOCATIONS ALREADY VISITED THEN CHECK

# TEST1: Top to bottom on people list

time1 = currentTime
for pref in allPrefs:

    #If we have already visited the location, continue with the other preferences
    if pref[1] in visited1:
        continue

    #Else, check if we have time to visit the next location
    else:
        for item in schedule:
            if item[0] == pref[1]:
                #If we have time to visit the location before it closes
                if item[1] + time1 <= item[3]:
                    time1 = time1 + item[1]
                    visited1.append(pref[1])
                    break

#Check all places visited
for place in visited1:
    for pref in allPrefs:
        if place == pref[1]:
            satisfaction1[pref[0]-1] = satisfaction1[pref[0]-1] + 1

#Retrieve total amount of preferences
totalPrefs = getTotalPrefs(allPrefs)

i = 0
while i < len(totalPrefs):
    if satisfaction1[i] == totalPrefs[i]:
        satisfaction1[i] = locations
    i = i + 1

latestTime = getLatestTime(schedule)
# ---TEST1 END

# ---TEST2 START
# THIS TEST ALTERNATES FROM PERSON TO PERSON
prevPerson = 0
escape = 0
allPrefsCopy = list(allPrefs)

time1 = getFirstTime(allPrefsCopy, schedule)
numIterations = 0
while True:
    for pref in allPrefsCopy:
        #If list is empty
        if not allPrefsCopy:
            escape = 1
            break

        #If no other choice but to escape
        if numIterations == preferences:
            escape = 1
            break

        #If location was already visited, continue
        if pref[1] in visited2:
            satisfaction2[pref[0] - 1] = satisfaction2[pref[0] - 1] + 1
            allPrefsCopy.remove(pref)
            numIterations = numIterations + 1
            continue

        #If this is the preference of the same person, continue
        elif pref[0] == prevPerson:
            numIterations = numIterations + 1
            continue

        #elif cannot go to location due to time constraints
        for item in schedule:
            if item[0] == pref[1]:
                if time1 + item[1] > item[3]:
                    numIterations = numIterations + 1
                    continue
                else:
                    prevPerson = pref[0]
                    visited2.append(item[0])
                    satisfaction2[pref[0] - 1] = satisfaction2[pref[0] - 1] + 1
                    time1 = time1 + item[1]
                    allPrefsCopy.remove(pref)
                    numIterations = 0
                    break
    if escape == 1:
        break
i = 0
while i < len(totalPrefs):
    if satisfaction2[i] == totalPrefs[i]:
        satisfaction2[i] = locations
    i = i + 1

#TEST3
time1 = 99
timeIsSet = 0
maxIterations = 0
for item in schedule:
    if item[2] < time1:
        time1 = item[2]
scheduleCopy = list(schedule)
while True:
    earliest = 99
    minSatisfaction = 99
    choices = []
    priority = []
    firstPriority = 0
    temp = []

    #Find the earliest time in schedule
    for item in scheduleCopy:
        if item[2] < earliest:
            earliest = item[2]

    if timeIsSet == 0:
        time1 = earliest
        timeIsSet = 1

    #Get the locations with the earliest times and remove from list

    i = 0
    while i < len(schedule):
        for item in scheduleCopy:
            if earliest == item[2]:
                choices.append(item[0])
                scheduleCopy.remove(item)
        i = i + 1

    #Get the people who want to go to the current choices
    for x in choices:
        for person in allPrefs:
            if person[1] == x:
                priority.append(person[0])

    #Get person with lowest satisfaction
    for person in priority:
        if satisfaction3[person-1] < minSatisfaction:
            minSatisfaction = satisfaction3[person-1]
            firstPriority = person

    #Go to location
    for x in choices:
        for pref in allPrefs:
            if firstPriority == pref[0] and x == pref[1]:
                for item in schedule:
                    if item[0] == x:
                        if time1 + item[1] <= item[3]:
                            time1 = time1 + item[1]
                            visited3.append(x)
                            temp.append(x)
                            break
                    else:
                        continue
            else:
                continue


    #ADD THE SATISFACTIONS
    for person in allPrefs:
        if person[1] in temp:
            satisfaction3[person[0]-1] = satisfaction3[person[0]-1] + 1

    #If out of locations to go
    if not scheduleCopy:
        break
    maxIterations = maxIterations + 1
    if maxIterations == preferences:
        break


#FINAL COMPARISON
final = 999
if min(satisfaction1) > min(satisfaction2):
    final = min(satisfaction1)
else:
    final = min(satisfaction2)
if min(satisfaction3) > final:
    final = min(satisfaction3)

print("satisfaction(", final, ")", sep="")