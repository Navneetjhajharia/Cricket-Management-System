#JSON for file management
import json
#Miscellaneous operating system interfaces
import os
import matplotlib.pyplot as plt
import random

def Intersection(lst1,lst2):
    if (lst1 == None or lst2 == None):
        lst3 = []
    else:
        lst3 = [value for value in lst1 if value in lst2]
    return lst3 

#Function that returns data from JSON         
def ReadFromJSON(path,key):
    global Path
    with open(Path + path) as f:
        data = json.load(f)
        if(key == ''):
            return data
        else:
            return data[key]

#Function that writes data to JSON
def WriteToJSON(path,data):
    global Path
    if (os.path.isfile(Path + path) and os.access(Path + path, os.R_OK)):
        with open(Path + path,'w') as jsonFile:
            jsonFile.write(json.dumps(data))
    
def FileCheckerAndCreator(path, data,x = 0):
    if not (os.path.isfile(path) and os.access(path, os.R_OK)):
        with open(path,'w') as jsonFile:
            jsonFile.write(json.dumps(data))
    elif(x == 1):
        print("File already exists! Try a Different name!")

def End_Program():
    global i
    print("Ending Program!")
    i = 1

def FirstTeam(t,mc,ms,te,tour,mpet):
    EligibleTeams = []
    noOfDaysLowest = 0
    if(tour["Number of Teams"] <= 4):
        noOfDaysLowest = 0
    else:
        noOfDaysLowest = 1
    tlist1 = []
    #Check if team has had enough rest period and append to list
    for i in t:
        if ms[i] >= noOfDaysLowest:
            tlist1.append(i)   
    #Check for the team(s) which have played the lowest number of games and break the loop if intersection is found
    for i in range(0 ,mpet):
        lowestNoOfGames = min(mc.values()) + i
        tlist2 = [key for key in mc if mc[key] == lowestNoOfGames and mc[key] <= mpet]
        #Check intersection of both lists
        EligibleTeams = Intersection(tlist1,tlist2)
        #Check if
        if(EligibleTeams != None):
            if(len(EligibleTeams) != 0):
                break
    #Return a random team from the list of eligible teams   
    return random.choice(EligibleTeams)

def SecondTeam(t,mc,ms,te,tour,mpet,nm,t1):
    EligibleTeams = []
    noOfDaysLowest = 0
    if(tour["Number of Teams"] <= 4):
        noOfDaysLowest = 0
    else:
        noOfDaysLowest = 1
    tlist1 = []
    #Check if team has had enough rest period and append to list
    for i in t:
        if(i == t1):
            continue
        else:
            if ms[i] >= noOfDaysLowest:
                tlist1.append(i)
    #Check for team(s) that have played lower than the number of matches maximum between the first team
    tlist3 = []
    for i in t:
        if(i == t1):
            continue
        else:
            if te[i][t1] < nm:
                tlist3.append(i)
    #Check for the team(s) which have played the lowest number of games and break the loop if intersection is found
    for i in range(0 ,mpet):
        lowestNoOfGames = min(mc.values()) + i
        tlist2 = [key for key in mc if mc[key] == lowestNoOfGames and mc[key] <= mpet]
        #Check intersection of both lists
        temp = Intersection(tlist1,tlist2)
        EligibleTeams = Intersection(temp,tlist3)

        if(len(EligibleTeams) != 0):
            break
    #Return a random team from the list of eligible teams
    if(len(EligibleTeams) == 0):
        return EligibleTeams
    else:
        return random.choice(EligibleTeams)

def Generate_Timetable(t):
    global Loaded_Tournament
    noOfMatchesBetweenEachTeam = int(input("Enter number of matches between each team: "))
    matchesPerEachTeam = noOfMatchesBetweenEachTeam * (t["Number of Teams"] - 1)
    totalNoOfMatches = int((t["Number of Teams"] * (t["Number of Teams"] - 1)) /2 * noOfMatchesBetweenEachTeam)
    teams = []
    y = t["Teams"]
    for i in range(0, t["Number of Teams"]):
        teams.append(y[i][str(i+1)])
    matchesCompletedForEachTeam = dict.fromkeys(teams)
    matchesSinceLastPlayedForEachTeam = dict.fromkeys(teams)
    teamsEachTeamHasPlayedAgainst = dict.fromkeys(teams)
    for i in teams:
        matchesCompletedForEachTeam[i] = 0
        matchesSinceLastPlayedForEachTeam[i] = 1000
        temp = teams.copy()
        temp.remove(i)
        teamsEachTeamHasPlayedAgainst[i] = dict.fromkeys(temp)
        for j in teamsEachTeamHasPlayedAgainst[i]:
            teamsEachTeamHasPlayedAgainst[i][j] = 0

    n = 0
    x = 1
    while x > 0:
        team1 = FirstTeam(teams, matchesCompletedForEachTeam, matchesSinceLastPlayedForEachTeam
                          , teamsEachTeamHasPlayedAgainst, t, matchesPerEachTeam)
        team2 = SecondTeam(teams, matchesCompletedForEachTeam, matchesSinceLastPlayedForEachTeam
                           , teamsEachTeamHasPlayedAgainst, t, matchesPerEachTeam, noOfMatchesBetweenEachTeam, team1)
        # Check if valid match
        if (len(team2) != 0):
            # Match is valid
            matchesCompletedForEachTeam[team1] += 1
            matchesCompletedForEachTeam[team2] += 1
            matchesSinceLastPlayedForEachTeam[team2] = 0
            matchesSinceLastPlayedForEachTeam[team2] = 0
            for j in matchesSinceLastPlayedForEachTeam:
                if j == team1 or j == team2:
                    continue
                else:
                    matchesSinceLastPlayedForEachTeam[j] += 1
            teamsEachTeamHasPlayedAgainst[team1][team2] += 1
            teamsEachTeamHasPlayedAgainst[team2][team1] += 1
            print(str(n + 1) + ".", team1, "vs", team2)
            n += 1
        if(n == totalNoOfMatches):
            x = 0

def Process_Command(command):
    global Path, Loaded_Tournament
    if(command == "help"):
        print("==========\nCommands:\n(Commands are not case sensitive)\n", "Help: Displays this", "Create Tournament: Starts process of creating a new tournament",
              "Load Tournament: Loads the tournament into the program to use other commands!", "Generate Timetable: Generates timetable for the tournament"
              , "End Program: Ends the program " , sep="\n" , end = "\n==========\n")
    elif(command == "create tournament"):
        print("Creating new tournament")
        name = input("Enter Name of Tournament: ")
        noTeamsX = (input("Enter Number of Teams(Integer >= 2): "))
        try:
            noTeams = int(noTeamsX)
        except ValueError:
            print("You did not enter an integer!")
            return
        if noTeams < 2:
            print("Number of teams is lesser than 2! Cancelling creation of tournament!")
            return
        teams = []
        for i in range(0, noTeams):
            teams.append(input("Enter name of team " + str(i+1) + ": "))
        FileCheckerAndCreator(Path+"\\"+str(name)+".json",{"Name": name, "Number of Teams": noTeams},1)
        add = ReadFromJSON("\\" +str(name)+".json","")
        add.update({"Teams":[]})
        x = 0
        for i in teams:
            x += 1
            add["Teams"].append({x : i})
        WriteToJSON("\\" +str(name)+".json",add)
        data = ReadFromJSON("/Tournaments.json","")
        data["Tournaments"] += 1
        temp = data["Tournament Names"]
        temp.append({data["Tournaments"] : str(name)})
        WriteToJSON("/Tournaments.json", data)
        print("Successfully created tournament:", str(name))
        
    #Load Tournament Command
    elif(command == "load tournament"):
        name = input("Enter Name Of Tournamnet: ")
        if(os.path.isfile(Path + "\\" + name + ".json") and os.access(Path + "\\" + name + ".json", os.R_OK)):
            with open(Path + "\\" + name + ".json") as f:
                Loaded_Tournament = json.load(f)
            print("Tournament has been successfully loaded!")
        else:
            print("Tournament does not exist!")
    elif(command == "generate timetable"):
        if not (Loaded_Tournament == 0):
            Generate_Timetable(Loaded_Tournament)
        else:
            print("No tournament loaded!")
    elif(command == "end program"):
        End_Program()
    #Command not recognized
    else:
        print("Command Not Recognized!")
    

def Main():
    #Main
    command = (input("Enter Command Here(use help for all commands): ")).lower()
    Process_Command(command)

i = 0
print("==========\nTournament Management system for Cricket Tournaments\n==========")
Path = os.getcwd()
Loaded_Tournament = 0
FileCheckerAndCreator(Path+"\\Tournaments.json",{"Tournaments": 0,"Tournament Names":[]})
if ReadFromJSON("/Tournaments.json", "Tournaments") == 0:
    print("No tournaments found! Please create one!")
    Loaded_Tournament = 0
while 1 > i:
    Main()
