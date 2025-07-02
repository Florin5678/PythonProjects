# import math
import random
import csv
import linecache
# from tkinter.messagebox import showerror

filename = "savedata.csv"

budget = startBudget = 5000
day = 1
weekdays = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
lastVisitedArena = 0
championsDefeated = 0
birds = ["Chicken","Turkey","Peacock","Parrot","Ostrich","Awebo","Cassowary"]
# When adding a new bird add it to the functions price, eggchance, eggprice, basestrength, basetrainability, newarenachampions

startWeekday = "Monday"
eggModifier = 1
eggPriceModifier = 2
globalPriceModifier = 1
arenaPrizeModifier = 1
circusPrizeModifier = 1
championPowerModifier = 0.1
effectModifier = 1
globalTrainabilityModifier = 1
globalTrickLearningModifier = 1

ownedBirdNames = []
ownedBirdTypes = []
ownedBirdAge = []
ownedBirdStrength = []
ownedBirdEnergy = []
ownedBirdEffects = []
ownedBirdTalent = []
ownedBirdTricks = []
# for new owned bird stat make sure to update addbird, birddeath, savegame and loadgame

deadBirdNames = []
deadBirdTypes = []
deadBirdAge = []
deadBirdEpitaph = []

consumables = ["Fertility Potion","Energy Potion","Strength Potion","Talent Potion","Trainability Potion","Mystery Potion"]
ownedFertilityPotions = 0
ownedEnergyPotions = 0
ownedStrengthPotions = 0
ownedMysteryPotions = 0
ownedTrainabilityPotions = 0
ownedTalentPotions = 0
# When adding a new consumable update price, addconsumable, feedconsumable, checkbird, addeffect, savegame, loadgame

daysUntilMysteryEggHatches = -1
mysteryPotionsAvailable = 1
lastTalentShow = 0

def landing():
    global budget
    currentWeekday = weekdays[(day + weekdays.index(startWeekday)) % 7 - 1]
    event = weeklyevent(currentWeekday)
    print(f"\nYou have {formatnumber(budget)} coins.")
    print(f"Today is {currentWeekday}, Day {day}.",end=" ")
    if event == "Circus": print(f"The Circus is in Town today!")
    print(f"What do you want to do? \n")
    options = ["Visit the Market","Check Birds","Visit the Arena","Sleep"]
    if len(deadBirdTypes) > 0: options.insert(3,"Visit Bird Graveyard")
    if event == "Circus": options.insert(2,"Visit the Circus")
    for x in options: print(f"{options.index(x)+1}. {x}")
    selectedOption = input()
    if selectedOption == "": landing()
    elif int(selectedOption) > len(options): landing()
    else: selectedOption = options[int(selectedOption)-1]
    if selectedOption == "Visit the Market": market()
    elif selectedOption == "Check Birds": checkbirds()
    elif selectedOption == "Visit the Arena": arena()
    elif selectedOption == "Visit Bird Graveyard": graveyard()
    elif selectedOption == "Sleep": nighttime()
    elif selectedOption == "Visit the Circus": circus()
    else: landing()
def market():
    answer = input(f"The market is bustling with the cries of vendors and the clinks of coins.\nWhat do you want to do?\n\n1. Buy birds\n2. Buy consumables\n3. Leave\n")
    if answer == "1": buybirds()
    elif answer == "2": buyconsumables()
    else: landing()
def buybirds():
    global budget
    print(f"You have {formatnumber(budget)} coins.\nWhat bird do you want to buy?\n")
    for x in birds: print(f"{birds.index(x)+1}. {x} ({price(x)} coins)")
    answer = input(f"\n{len(birds) + 1}. Return\n")
    if answer == "": buybirds()
    else: answer = int(answer)
    if answer > len(birds): market()
    else:
        birdOnSale = birds[answer-1]
        answer = input(f"Do you want to buy a {birdOnSale} for {price(birdOnSale)} coins?\n\n1. Yes\n2. No\n")
        if answer == "1":
            if budget < price(birdOnSale):
                input("You don't have enough coins.")
            else:
                budget = budget - price(birdOnSale)
                addbird(birdOnSale)
                print(f"You have purchased a {birdOnSale}.")
                input(f"You now have {formatnumber(budget)} coins.")
        buybirds()
def buyconsumables():
    global budget
    global mysteryPotionsAvailable
    print(f"You have {formatnumber(budget)} coins.\nWhat consumables do you want to buy?\n")
    for x in consumables:
        if x != "Mystery Potion" or (x == "Mystery Potion" and mysteryPotionsAvailable > 0): print(f"{consumables.index(x)+1}. {x} ({price(x)} coins)")
    returnOptionNo = len(consumables) + 1
    if mysteryPotionsAvailable <= 0: returnOptionNo -= 1
    answer = input(f"\n{returnOptionNo}. Return\n")
    if answer == "": buyconsumables()
    else: answer = int(answer)
    if answer >= returnOptionNo: market()
    else:
        consumableOnSale = consumables[answer-1]
        answer = input(f"Do you want to buy a {consumableOnSale} for {price(consumableOnSale)} coins?\n\n1. Yes\n2. No\n")
        if answer == "1":
            if budget < price(consumableOnSale):
                input("You don't have enough coins.")
            else:
                budget = budget - price(consumableOnSale)
                addconsumable(consumableOnSale)
                print(f"You have purchased a {consumableOnSale}.")
                input(f"You now have {formatnumber(budget)} coins.")
                if consumableOnSale == "Mystery Potion": mysteryPotionsAvailable -= 1
        buyconsumables()
def checkbirds():
    print("Which bird do you want to see?")
    i = 0
    for x in ownedBirdNames:
        i = i + 1
        print(f"{str(i)}. {x}")
    print(f"\n{str(i + 1)}. Return")
    answer = input("")
    if answer == "": checkbirds()
    elif int(answer) <= i: checkbird(int(answer)-1)
    else: landing()
def checkbird(n):
    global ownedFertilityPotions
    global ownedEnergyPotions
    global ownedStrengthPotions
    global ownedTrainabilityPotions
    global ownedMysteryPotions
    global ownedTalentPotions

    print(f"{getbirddata(n, "name")} is a {str(getbirddata(n, "age"))} days old {getbirddata(n, "type")}.")
    if getbirddata(n,"energy") > 5: possibleStatus = ["It is foraging in the yard.","It is happily basking in the sun.","It is sleeping in the barn."]
    else: possibleStatus = ["It is feeling sick.","It is currently tending to its wounds.","It is fast asleep."]
    print(f"{possibleStatus[random.randrange(0, len(possibleStatus))]}\n")
    print(f"Strength: {formatnumber(getbirddata(n, "strength"))}")
    print(f"Egg chance: {int(getbirddata(n, "egg chance"))}%")
    print(f"Energy level: {str(getbirddata(n, "energy") * 10)}%\n")

    options = ["Rename bird", "Train bird", "Return"]
    if getbirddata(n, "tricks")!=" ": options.insert(2, "Check tricks")
    if ownedFertilityPotions + ownedEnergyPotions + ownedStrengthPotions + ownedTrainabilityPotions + ownedMysteryPotions + ownedTalentPotions > 0: options.insert(2, "Feed consumables")
    for x in options: print(f"{options.index(x) + 1}. {x}")
    selectedOption = input()
    if selectedOption == "": checkbirds()
    elif int(selectedOption) > len(options): checkbirds()
    else: selectedOption = options[int(selectedOption) - 1]
    if selectedOption == "Rename bird":
        ownedBirdNames[n] = input("What do you want to name this bird?\n")
        checkbird(n)
    elif selectedOption == "Train bird":
        if getbirddata(n,"energy") > 5:
            input(f"{getbirddata(n, "name")}'s strength has increased!")
            trainbird(n)
            ownedBirdEnergy[n] = ownedBirdEnergy[n] - random.randrange(1,2)
            checkbird(n)
        else:
            input(f"{getbirddata(n,"name")} is too tired to train right now.")
            checkbird(n)
    elif selectedOption == "Feed consumables": feedconsumable(n)
    elif selectedOption == "Check tricks": checktricks(n)
    else: checkbirds()
def nighttime():
    global day
    global ownedBirdEffects
    global daysUntilMysteryEggHatches
    input("You sleep the night...\n")
    day = day + 1
    daysUntilMysteryEggHatches = daysUntilMysteryEggHatches - 1
    for x in range(len(ownedBirdAge)): ownedBirdAge[x] = ownedBirdAge[x] + 1
    for x in range(len(ownedBirdNames)): egg(x)
    for x in range(len(ownedBirdEnergy)):
        if ownedBirdEnergy[x] < 10:
            if ownedBirdEnergy[x] == 9: ownedBirdEnergy[x] = 10
            elif ownedBirdEnergy[x] == 8: ownedBirdEnergy[x] = ownedBirdEnergy[x] + random.randrange(1,2)
            else: ownedBirdEnergy[x] = ownedBirdEnergy[x] + random.randrange(1,3)
    for x in range(len(ownedBirdEffects)):
        if "Mystery Effect" in ownedBirdEffects[x]: ownedBirdEffects[x] = "Mystery Effect"
        else: ownedBirdEffects[x] = " "
    if daysUntilMysteryEggHatches == 0:
        input("The Mystery Egg hatched!")
        addbird("Pterodactyl")
    savegame()
    landing()
def egg(n):
    global budget
    global eggModifier
    global daysUntilMysteryEggHatches
    if random.randrange(1,100) <= getbirddata(n,"egg chance"):
        if "Mystery Effect" in ownedBirdEffects[n]:
            input(f"{ownedBirdNames[n]} laid a Mystery Egg.")
            ownedBirdEffects[n] = ""
            daysUntilMysteryEggHatches = random.randrange(5, 10)
        else:
            input(f"{ownedBirdNames[n]} laid an egg. You get {str(eggprice(ownedBirdTypes[n]))} coins.")
            budget = budget + eggprice(ownedBirdTypes[n])
def price(x):
    # Birds
    if x == "Chicken": return int(1000 * globalPriceModifier)
    elif x == "Turkey": return int(2000 * globalPriceModifier)
    elif x == "Peacock": return int(5000 * globalPriceModifier)
    elif x == "Parrot": return int(8000 * globalPriceModifier)
    elif x == "Ostrich": return int(10000 * globalPriceModifier)
    elif x == "Awebo": return int(25000 * globalPriceModifier)
    elif x == "Cassowary": return int(200000 * globalPriceModifier)

    # Consumables
    elif x == "Fertility Potion": return int(200 * globalPriceModifier)
    elif x == "Energy Potion": return int(500 * globalPriceModifier)
    elif x == "Strength Potion": return int(1000 * globalPriceModifier)
    elif x == "Talent Potion": return int(5000 * globalPriceModifier)
    elif x == "Trainability Potion": return int(10000 * globalPriceModifier)
    elif x == "Mystery Potion": return int(500000 * globalPriceModifier)
def eggchance(x):
    if x == "Chicken": return 35 * eggModifier
    elif x == "Turkey": return 25 * eggModifier
    elif x == "Peacock": return 20 * eggModifier
    elif x == "Parrot": return 15 * eggModifier
    elif x == "Ostrich": return 10 * eggModifier
    elif x == "Awebo": return 5 * eggModifier
    elif x == "Cassowary": return 3 * eggModifier
    elif x == "Pterodactyl": return 1 * eggModifier
def eggprice(x):
    if x == "Chicken": return 50 * eggPriceModifier
    elif x == "Turkey": return 100 * eggPriceModifier
    elif x == "Peacock": return 350 * eggPriceModifier
    elif x == "Ostrich": return 450 * eggPriceModifier
    elif x == "Parrot": return 600 * eggPriceModifier
    elif x == "Awebo": return 5000 * eggPriceModifier
    elif x == "Cassowary": return 7000 * eggPriceModifier
    elif x == "Pterodactyl": return 2500000 * eggPriceModifier
def addbird(bird):
    ownedBirdTypes.append(bird)
    ownedBirdNames.append(defaultname(bird))
    ownedBirdAge.append(0)
    ownedBirdStrength.append(basestrength(bird))
    ownedBirdEnergy.append(10)
    ownedBirdEffects.append(" ")
    ownedBirdTalent.append(basetalent(bird))
    ownedBirdTricks.append(" ")
def addconsumable(x):
    global ownedFertilityPotions
    global ownedEnergyPotions
    global ownedStrengthPotions
    global ownedTrainabilityPotions
    global ownedMysteryPotions
    global ownedTalentPotions

    if x == "Fertility Potion": ownedFertilityPotions += 1
    elif x == "Energy Potion": ownedEnergyPotions += 1
    elif x == "Strength Potion": ownedStrengthPotions += 1
    elif x == "Trainability Potion": ownedTrainabilityPotions += 1
    elif x == "Mystery Potion": ownedMysteryPotions += 1
    elif x == "Talent Potion": ownedTalentPotions += 1
def defaultname(bird):
    x = ownedBirdTypes.count(bird) + deadBirdTypes.count(bird)
    return bird + str(x)
def getbirddata(n,data):
    if data == "name": return ownedBirdNames[n]
    elif data == "age": return ownedBirdAge[n]
    elif data == "type": return ownedBirdTypes[n]
    elif data == "strength":
        if "Strength Boost" in ownedBirdEffects[n]: return int(ownedBirdStrength[n] * 1.6 * effectModifier)
        else: return ownedBirdStrength[n]
    elif data == "egg chance":
        if "Fertility Boost" in ownedBirdEffects[n]: return min(eggchance(ownedBirdTypes[n]) * 3.5 * effectModifier,100)
        else: return eggchance(ownedBirdTypes[n])
    elif data == "energy": return ownedBirdEnergy[n]
    elif data == "trainability":
        if "Trainability Boost" in ownedBirdEffects[n]: return int(basetrainability(ownedBirdTypes[n]) * 1.5 * effectModifier)
        else: return basetrainability(ownedBirdTypes[n])
    elif data == "talent":
        if "Talent Boost" in ownedBirdEffects[n]: return int(ownedBirdTalent[n] * 1.6 * effectModifier)
        else: return ownedBirdTalent[n]
    elif data == "tricks": return ownedBirdTricks[n]
def basestrength(bird):
    if bird == "Chicken": return 5
    elif bird == "Turkey": return 15
    elif bird == "Peacock": return 20
    elif bird == "Ostrich": return 30
    elif bird == "Parrot": return 10
    elif bird == "Awebo": return 50
    elif bird == "Cassowary": return 100
    elif bird == "Pterodactyl": return 3000
def basetrainability(x):
    if x == "Chicken": return 1 * globalTrainabilityModifier
    elif x == "Turkey": return 3 * globalTrainabilityModifier
    elif x == "Peacock": return 2 * globalTrainabilityModifier
    elif x == "Ostrich": return 4 * globalTrainabilityModifier
    elif x == "Parrot": return 3 * globalTrainabilityModifier
    elif x == "Awebo": return 5 * globalTrainabilityModifier
    elif x == "Cassowary": return 9 * globalTrainabilityModifier
    elif x == "Pterodactyl": return 10 * globalTrainabilityModifier
def trainbird(n):
    minPercentImprovement = 2
    maxPercentImprovement = 10
    ownedBirdStrength[n] = int(ownedBirdStrength[n] + max(ownedBirdStrength[n] * random.randrange(minPercentImprovement,maxPercentImprovement)/100 * getbirddata(n, "trainability"), random.randrange(1, 5)))

    if random.randrange(1,101) <= int(getbirddata(n,"talent") * globalTrickLearningModifier):
        trickOptions = ["Jump","Chirp","Shake"]
        trickOptions1 = ["Roll","Burrow","Sing"]
        trickOptions2 = ["Dance","Backflip","Speak"]
        knownTricks = getbirddata(n,"tricks").split(" ")
        if len(knownTricks) > 2: trickOptions += trickOptions1
        if len(knownTricks) > 4: trickOptions += trickOptions2
        for x in knownTricks:
            for y in trickOptions:
                if x == y: trickOptions.remove(y)
        if len(trickOptions) > 0:
            newTrick = trickOptions[random.randrange(0,len(trickOptions))]
            if len(knownTricks) < 1: ownedBirdTricks[n] = newTrick
            else:
                ownedBirdTricks[n] += " " + newTrick
                ownedBirdTricks[n] = ownedBirdTricks[n].strip()
            input(f"{getbirddata(n,"name")} has learned to {newTrick}!")
def arena():
    global day
    global lastVisitedArena
    global championsDefeated
    if day > lastVisitedArena:
        lastVisitedArena = day
        newarenachampions()
        championsDefeated = 0
    print("You entered the shadowy illegal bird fighting grounds. The smell of feathers and blood fills your nostrils.")
    if championsDefeated <3:
        if championsDefeated == 0: count = "third"
        if championsDefeated == 1: count = "second"
        if championsDefeated == 2: count = "first"
        print(f"Today's {count} champion is a {championType[championsDefeated]} called {championName[championsDefeated]} with a Strength of {formatnumber(championPower[championsDefeated])}.\n")
        answer = input("1. Challenge champion\n2. See all champions\n3. Leave\n")
        if answer == "1":
            print("\nChoose your fighter!")
            i = 0
            for x in ownedBirdNames:
                i = i + 1
                print(f"{str(i)}. {x} (Strength: {formatnumber(ownedBirdStrength[ownedBirdNames.index(x)])} | Energy: {ownedBirdEnergy[ownedBirdNames.index(x)]}0%)")
            print(f"\n{str(i + 1)}. Return\n")
            answer = input("")
            if answer == "": arena()
            elif int(answer) <= i: fightchampion(int(answer) - 1,championsDefeated)
            else: arena()
        elif answer == "2":
            i = 2
            while i >= 0:
                if i == 2: print(f"1st place: ", end= "")
                elif i == 1: print(f"2nd place: ", end= "")
                else : print(f"3rd place: ", end= "")
                print(f"{championName[i]} ({championType[i]}) | Strength: {formatnumber(championPower[i])} | Prize: {formatnumber(prize(championPower[i],arenaPrizeModifier*(i+1)))}")
                i = i-1
            input("1. Return\n")
            arena()
        else: landing()
    else:
        input(f"ALL of today's champions have been defeated. Come back tomorrow!\n\n1. Leave\n")
        landing()
def newarenachampions():
    global championType
    global championPower
    global championName
    global championPowerModifier
    champions = 0
    championName = ["", "", ""]
    championType = ["", "", ""]
    championPower = ["", "", ""]
    while(champions < 3):
        championNameOptions = ["Skull Crusher","Death","Destroyer","Scar","Scythe","Ghost","Phantom","Blade","Banshee","Bane","Reaper","Deathwish","Psycho"]
        championName[champions] = championNameOptions[random.randrange(0,len(championNameOptions))]

        if(champions == 0): championTypeOptions = ["Chicken","Turkey","Parrot","Peacock"]
        elif(champions == 1): championTypeOptions = ["Ostrich","Turkey","Parrot"]
        else: championTypeOptions = ["Ostrich","Awebo","Cassowary"]
        championType[champions] = championTypeOptions[random.randrange(0, len(championTypeOptions))]

        if championType[champions] == "Chicken": chanceMod = random.randrange(8,20)
        elif championType[champions] == "Turkey": chanceMod = random.randrange(12,25)
        elif championType[champions] == "Peacock": chanceMod = random.randrange(10,20)
        elif championType[champions] == "Parrot": chanceMod = random.randrange(8,15)
        elif championType[champions] == "Ostrich": chanceMod = random.randrange(15,30)
        elif championType[champions] == "Awebo": chanceMod = random.randrange(20,50)
        elif championType[champions] == "Cassowary": chanceMod = random.randrange(40,75)

        difficultyMultiplier = int(day/10)
        while (difficultyMultiplier > 0):
            chanceMod += chanceMod * difficultyMultiplier/2
            difficultyMultiplier = difficultyMultiplier-1
        championPower[champions] = int(chanceMod * championPowerModifier * random.randrange(7, 10))

        champions = champions + 1
    championPower.sort()
def fightchampion(n,champ):
    global championsDefeated
    global budget
    global arenaPrizeModifier
    input(f"{getbirddata(n,"name")} is fighting {championName[champ]}...")
    birdPower = getbirddata(n,"strength") * getbirddata(n,"energy")
    if birdPower - championPower[champ] > 0:
        championsDefeated = championsDefeated + 1
        prizeCurrent = prize(championPower[champ],arenaPrizeModifier*championsDefeated)
        budget += prizeCurrent
        input(f"{getbirddata(n, "name")} Won!\nYou get {formatnumber(prizeCurrent)} coins!")

        ownedBirdEnergy[n] = max(1,min(9,int(ownedBirdEnergy[n]-championPower[champ]/birdPower*10)))
        # print(f"{getbirddata(n, "name")}'s new Energy is now {getbirddata(n, "energy")}0%")
        arena()
    else:
        input(f"{getbirddata(n, "name")} Died.\n")
        birddeath(n,f"Killed in battle with {championName[champ]}.")
        arena()
def prize(power,modifier):
    return int(int(power) * 2.5 * modifier)
def birddeath(n,COD):
    deadBirdNames.append(ownedBirdNames[n])
    deadBirdTypes.append(ownedBirdTypes[n])
    deadBirdAge.append(ownedBirdAge[n])
    deadBirdEpitaph.append(COD)

    ownedBirdTypes.pop(n)
    ownedBirdNames.pop(n)
    ownedBirdAge.pop(n)
    ownedBirdStrength.pop(n)
    ownedBirdEnergy.pop(n)
    ownedBirdEffects.pop(n)
    ownedBirdTalent.pop(n)
    ownedBirdTricks.pop(n)
def graveyard():
    print("Here lie in sober silence all of the birds who no longer fly nor flutter.\nWhich grave do you want to visit?\n")
    i = 0
    for x in deadBirdNames:
        i = i + 1
        print(f"{str(i)}. {x}")
    print(f"{str(i + 1)}. Return")
    answer = input("")
    if answer == "": graveyard()
    elif int(answer) <= i:
        newAnswer = input(f"{deadBirdNames[int(answer)-1]}, {deadBirdTypes[int(answer)-1]} dead at {deadBirdAge[int(answer)-1]} days.\n{deadBirdEpitaph[int(answer) - 1]}\n\n1. Change Epitaph\n2. Pay respects\n")
        if newAnswer == "1":
            newAnswer = input("What is the new Epitaph?\n\n1. Cancel\n")
            if newAnswer == "1" or newAnswer == "": graveyard()
            else:
                deadBirdEpitaph[int(answer) - 1] = newAnswer
                input("Epitaph changed!")
                graveyard()
        else: graveyard()
    else: landing()
def savegame():
    with open(filename, 'w') as csvfile:
        # Creating a csv writer object
        csvwriter = csv.writer(csvfile)
        # Writing the fields
        csvwriter.writerow([budget,day,lastVisitedArena,daysUntilMysteryEggHatches,mysteryPotionsAvailable,lastTalentShow])
        # Save bird data
        csvwriter.writerow(ownedBirdTypes)
        csvwriter.writerow(ownedBirdNames)
        csvwriter.writerow(ownedBirdAge)
        csvwriter.writerow(ownedBirdStrength)
        csvwriter.writerow(ownedBirdEnergy)
        # Save dead bird data
        csvwriter.writerow(deadBirdTypes)
        csvwriter.writerow(deadBirdNames)
        csvwriter.writerow(deadBirdAge)
        csvwriter.writerow(deadBirdEpitaph)
        # Save consumable data
        csvwriter.writerow([ownedFertilityPotions,ownedEnergyPotions,ownedStrengthPotions,ownedTalentPotions,ownedTrainabilityPotions,ownedMysteryPotions])
        csvwriter.writerow(ownedBirdEffects)
        csvwriter.writerow(ownedBirdTalent)
        csvwriter.writerow(ownedBirdTricks)
def loadgame():
    global budget
    global ownedBirdTypes
    global ownedBirdNames
    global ownedBirdAge
    global ownedBirdStrength
    global ownedBirdEnergy
    global deadBirdTypes
    global deadBirdNames
    global deadBirdAge
    global deadBirdEpitaph
    global day
    global lastVisitedArena
    global ownedFertilityPotions
    global ownedEnergyPotions
    global ownedStrengthPotions
    global ownedTalentPotions
    global ownedTrainabilityPotions
    global ownedMysteryPotions
    global ownedBirdEffects
    global daysUntilMysteryEggHatches
    global ownedBirdTalent
    global ownedBirdTricks
    global mysteryPotionsAvailable
    global lastTalentShow
    with open('savedata.csv', mode='r') as file:
        # Load parameters
        savedValues = linecache.getline('savedata.csv', 1).split(",")
        budget = int(savedValues[0])
        day = int(savedValues[1])
        lastVisitedArena = int(savedValues[2])
        daysUntilMysteryEggHatches = int(savedValues[3])
        mysteryPotionsAvailable = int(savedValues[4])
        lastTalentShow = int(savedValues[5])
        # Load bird data
        ownedBirdTypes = linecache.getline('savedata.csv', 3).split(",")
        ownedBirdTypes = [x for x in ownedBirdTypes if x != "\n"]
        ownedBirdTypes = [x.replace("\n","") for x in ownedBirdTypes]
        ownedBirdNames = linecache.getline('savedata.csv', 5).split(",")
        ownedBirdNames = [x for x in ownedBirdNames if x != "\n"]
        ownedBirdNames = [x.replace("\n","") for x in ownedBirdNames]
        ownedBirdAge = linecache.getline('savedata.csv', 7).split(",")
        ownedBirdAge = [x for x in ownedBirdAge if x != "\n"]
        ownedBirdAge = list(map(int, ownedBirdAge))
        ownedBirdStrength = linecache.getline('savedata.csv', 9).split(",")
        ownedBirdStrength = [x for x in ownedBirdStrength if x != "\n"]
        ownedBirdStrength = list(map(int, ownedBirdStrength))
        ownedBirdEnergy = linecache.getline('savedata.csv', 11).split(",")
        ownedBirdEnergy = [x for x in ownedBirdEnergy if x != "\n"]
        ownedBirdEnergy = list(map(int, ownedBirdEnergy))
        # Load dead bird data
        deadBirdTypes = linecache.getline('savedata.csv', 13).split(",")
        deadBirdTypes = [x for x in deadBirdTypes if x != "\n"]
        deadBirdTypes = [x.replace("\n","") for x in deadBirdTypes]
        deadBirdNames = linecache.getline('savedata.csv', 15).split(",")
        deadBirdNames = [x for x in deadBirdNames if x != "\n"]
        deadBirdNames = [x.replace("\n","") for x in deadBirdNames]
        deadBirdAge = linecache.getline('savedata.csv', 17).split(",")
        deadBirdAge = [x for x in deadBirdAge if x != "\n"]
        deadBirdAge = list(map(int, deadBirdAge))
        deadBirdEpitaph = linecache.getline('savedata.csv', 19).split(",")
        deadBirdEpitaph = [x for x in deadBirdEpitaph if x != "\n"]
        deadBirdEpitaph = [x.replace("\n", "") for x in deadBirdEpitaph]
        # Load consumables and effects data
        savedValues = linecache.getline('savedata.csv', 21).split(",")
        ownedFertilityPotions = int(savedValues[0])
        ownedEnergyPotions = int(savedValues[1])
        ownedStrengthPotions = int(savedValues[2])
        ownedTalentPotions = int(savedValues[3])
        ownedTrainabilityPotions = int(savedValues[4])
        ownedMysteryPotions = int(savedValues[5])
        ownedBirdEffects = linecache.getline('savedata.csv', 23).split(",")
        ownedBirdEffects = [x for x in ownedBirdEffects if x != "\n"]
        ownedBirdEffects = [x.replace("\n","") for x in ownedBirdEffects]
        ownedBirdTalent = linecache.getline('savedata.csv', 25).split(",")
        ownedBirdTalent = [x for x in ownedBirdTalent if x != "\n"]
        ownedBirdTalent = list(map(int, ownedBirdTalent))
        ownedBirdTricks = linecache.getline('savedata.csv', 27).split(",")
        ownedBirdTricks = [x for x in ownedBirdTricks if x != "\n"]
        ownedBirdTricks = [x.replace("\n","") for x in ownedBirdTricks]
def loadgameinquire():
    with open('savedata.csv', mode='r') as file:
        if sum(1 for line in file) <1: landing()
        answer = input("There is previous save data. Do you want to load it?\n\n1. Yes\n2. No\n")
        if answer == "1": loadgame()
        elif answer == "2":
            filename = "savedata.csv"
            # opening the file with w+ mode truncates the file
            f = open(filename, "w+")
            f.close()
        else: loadgameinquire()
def feedconsumable(n):
    global ownedFertilityPotions
    global ownedEnergyPotions
    global ownedStrengthPotions
    global ownedTrainabilityPotions
    global ownedMysteryPotions
    global ownedTalentPotions
    print(f"What do you want to feed {getbirddata(n, "name")}?\n")
    options = []
    if ownedFertilityPotions > 0: options.append("Fertility Potion")
    if ownedEnergyPotions > 0: options.append("Energy Potion")
    if ownedStrengthPotions > 0: options.append("Strength Potion")
    if ownedTalentPotions > 0: options.append("Talent Potion")
    if ownedTrainabilityPotions > 0: options.append("Trainability Potion")
    if ownedMysteryPotions > 0: options.append("Mystery Potion")
    for x in options:
        if x == "Fertility Potion": count = ownedFertilityPotions
        elif x == "Energy Potion": count = ownedEnergyPotions
        elif x == "Strength Potion": count = ownedStrengthPotions
        elif x == "Talent Potion": count = ownedTalentPotions
        elif x == "Trainability Potion": count = ownedTrainabilityPotions
        elif x == "Mystery Potion": count = ownedMysteryPotions
        print(f"{options.index(x)+1}. {x} (owned: {count})")

    answer = input(f"{len(options)+1}. Return\n")
    if answer == "": checkbird(n)
    if int(answer) > len(options): checkbird(n)
    elif options[int(answer)-1] == "Fertility Potion": ownedFertilityPotions -= 1
    elif options[int(answer)-1] == "Energy Potion": ownedEnergyPotions -= 1
    elif options[int(answer)-1] == "Strength Potion": ownedStrengthPotions -= 1
    elif options[int(answer)-1] == "Talent Potion": ownedTalentPotions -= 1
    elif options[int(answer)-1] == "Trainability Potion": ownedTrainabilityPotions -= 1
    elif options[int(answer)-1] == "Mystery Potion": ownedMysteryPotions -= 1
    else: checkbird(n)
    input(f"{getbirddata(n,"name")} gulps down the {options[int(answer)-1]}!\n")
    addeffect(n, options[int(answer) - 1])
    checkbird(n)
def addeffect(n, effect):
    if effect == "Energy Potion": ownedBirdEnergy[n] = min(10,ownedBirdEnergy[n]+5*effectModifier)
    elif effect == "Fertility Potion":
        if ownedBirdEffects[n] == "": ownedBirdEffects[n] = "Fertility Boost"
        else: ownedBirdEffects[n] = ownedBirdEffects[n] + " Fertility Boost"
    elif effect == "Strength Potion":
        if ownedBirdEffects[n] == "": ownedBirdEffects[n] = "Strength Boost"
        else: ownedBirdEffects[n] = ownedBirdEffects[n] + " Strength Boost"
    elif effect == "Talent Potion":
        if ownedBirdEffects[n] == "": ownedBirdEffects[n] = "Talent Boost"
        else: ownedBirdEffects[n] = ownedBirdEffects[n] + " Talent Boost"
    elif effect == "Trainability Potion":
        if ownedBirdEffects[n] == "": ownedBirdEffects[n] = "Trainability Boost"
        else: ownedBirdEffects[n] = ownedBirdEffects[n] + " Trainability Boost"
    elif effect == "Mystery Potion":
        if ownedBirdEffects[n] == "": ownedBirdEffects[n] = "Mystery Effect"
        else: ownedBirdEffects[n] = ownedBirdEffects[n] + " Mystery Effect"
    else: return
def formatnumber(n):
    if n > 1000000000: return str(int(n/1000000000)) + "." + str(int(n % 1000000000 / 10000000)) + "B"
    if n > 1000000: return str(int(n / 1000000)) + "." + str(int(n % 1000000 / 10000)) + "M"
    else: return str(n)
def basetalent(bird):
    if bird == "Chicken": return 7
    elif bird == "Turkey": return 5
    elif bird == "Peacock": return 20
    elif bird == "Ostrich": return 15
    elif bird == "Parrot": return 35
    elif bird == "Awebo": return 20
    elif bird == "Cassowary": return 15
    elif bird == "Pterodactyl": return 30
def trickappeal(trick):
    if trick == "Jump": return 1
    elif trick == "Chirp": return 2
    elif trick == "Shake": return 3
    elif trick == "Roll": return 4
    elif trick == "Burrow": return 5
    elif trick == "Sing": return 6
    elif trick == "Dance": return 7
    elif trick == "Backflip": return 8
    elif trick == "Speak": return 10
    elif trick == "Teleport": return 15
def weeklyevent(day):
    if day == "Saturday": return "Circus"
    else: return ""
def circus():
    global lastTalentShow
    print("At the Circus, the world's most majestic birds are showcasing their talents at the thunderous sound of applause.\n")
    options = ["See show","Leave"]
    if lastTalentShow < day: options.insert(1,"Enlist a bird in the talent show")
    for x in options: print(f"{options.index(x)+1}. {x}")
    answer = input()
    if answer == "1":
        bird = birds[random.randrange(0,len(birds))]
        acts = ["jumps through a ring of fire","sings a heartbreaking lullaby","juggles more than 5 balls at once","swallows a greatsword","eats 50 burgers in 10 minutes","pulls a rabbit from a hat","holds its breath for 30 minutes","hits a bull's eye with 5 knives"]
        act = acts[random.randrange(0,len(acts))]
        input(f"You watch in amazement as a {bird} {act}.\n\n1. Ok")
        circus()
    elif lastTalentShow < day and answer == "2":
            print("\nWhich bird do you want to enlist?")
            i = 0
            for x in ownedBirdNames:
                i = i + 1
                print(f"{str(i)}. {x} (Talent: {getbirddata(ownedBirdNames.index(x),"talent")} | Energy: {getbirddata(ownedBirdNames.index(x),"energy")}0%)")
            answer = input(f"\n{str(i + 1)}. Return\n")
            if answer == "": circus()
            elif int(answer) <= i:
                x = ownedBirdNames[int(answer)-1]
                if getbirddata(int(answer)-1,"tricks") == " ":
                    input(f"{x} doesn't know any tricks.\n\n1. Ok")
                    circus()
                if getbirddata(ownedBirdNames.index(x),"energy") <=5:
                    input(f"{x} is too tired to participate in the talent show.\n\n1. Ok")
                    circus()
                else:
                    ownedBirdEnergy[ownedBirdNames.index(x)] -= 5
                    lastTalentShow = day
                    talentshow(ownedBirdNames.index(x))
            else: circus()
    else: landing()
def talentshow(n):
    global budget
    crowdEnthusiasm = 1
    usedTricks=[]
    noveltyFactor = 1
    round = "first"
    print(f"{getbirddata(n,"name")} stands amid the eager crowd.")
    for i in range(1,4):
        print(f"What will {getbirddata(n,"name")}'s {round} trick be?\n")
        tricks=getbirddata(n,"tricks").split(" ")
        for x in range(0,min(4,len(tricks))): print(f"{x+1}. {tricks[x]}")
        selectedOption = input()
        if selectedOption == "": circus()
        else:
            selectedTrick = tricks[int(selectedOption)-1]
            usedTricks.append(selectedTrick)
            if round == "second" and usedTricks[0] == usedTricks[1]: noveltyFactor = 0.5
            elif round == "third":
                if usedTricks[1] == usedTricks[2]:
                    if usedTricks[0] == usedTricks[1]: noveltyFactor = 0.25
                    else: noveltyFactor = 0.5
            # print(f"Novelty factor is {noveltyFactor}")

            trickAppeal = trickappeal(selectedTrick) * getbirddata(n,"talent") * ((getbirddata(n, "energy")+5)/10) * noveltyFactor
            if trickAppeal <= 50: crowdEnthusiasm -= 1
            elif trickAppeal <= 100: crowdEnthusiasm += 0
            elif trickAppeal <= 200: crowdEnthusiasm += 1
            elif trickAppeal <= 300: crowdEnthusiasm += 2
            else: crowdEnthusiasm += 3
            # print(crowdEnthusiasm)
            if crowdEnthusiasm < 0: input("The crowd is booing and throwing junk at the arena.")
            elif crowdEnthusiasm < 1: input("The crowd is murmuring.")
            elif crowdEnthusiasm < 2: input("The crowd is clapping sporadically.")
            elif crowdEnthusiasm < 3: input("The crowd is clapping.")
            elif crowdEnthusiasm < 4: input("The crowd is standing and clapping enthusiastically.")
            else: input("The crowd is wildly clapping, whistling, and throwing money at the bird.")
            print("")
            if round == "first": round = "second"
            elif round == "second": round = "third"
    if crowdEnthusiasm < 1: input(f"{getbirddata(n,"name")} failed to make an impression on the crowd.")
    else:
        prize = random.randrange(2000,3000) * circusPrizeModifier
        while crowdEnthusiasm > 0:
            prize += prize * crowdEnthusiasm
            crowdEnthusiasm -= 1
        input(f"{getbirddata(n,"name")} collected {formatnumber(prize)} coins from the crowd!")
        budget += prize
    landing()
def checktricks(n):
    print(f"{getbirddata(n,"name")} knows the following tricks:\n")
    tricks = getbirddata(n,"tricks").split(" ")
    for x in tricks: print(f"{tricks.index(x) + 1}. {x}")
    print(f"\nPlease note that only the first four tricks are prepared to be performed. Select two tricks in order to switch. \n{tricks.index(x) + 2}. Return")
    answer1 = input()
    if answer1 == "": checktricks(n)
    else: answer1 = int(answer1)-1
    if answer1 >= len(tricks) or answer1 < 0: checkbird(n)
    else:
        print(f"Which skill do you want to switch {tricks[answer1]} with?")
        for x in tricks: print(f"{tricks.index(x) + 1}. {x}")
        answer2 = input()
        if answer2 == "": checktricks(n)
        else: answer2 = int(answer2) - 1
        if answer2 >= len(tricks) or answer2 < 0: checktricks(n)
        else:
            temp = tricks[answer1]
            tricks[answer1] = tricks[answer2]
            tricks[answer2] = temp
            ownedBirdTricks[n] = ""
            for x in tricks:
                if ownedBirdTricks[n] == "": ownedBirdTricks[n] = x
                else: ownedBirdTricks[n] = ownedBirdTricks[n] + " " + x
            input(f"{tricks[answer1]} and {tricks[answer2]} switched successfully!\n\n1. Ok")
            checktricks(n)

loadgameinquire()
landing()



