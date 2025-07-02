import random
box = dict()
emptyboxes=lines=[]
player=comp=""
class Colors:
    RED = '\033[91m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    ENDC = '\033[0m'
playercolor=Colors.YELLOW
compcolor=Colors.RED
difficulty=5
keepscore=True
score=[0,0,0]

def printboard():
    global box
    print(" _ _ _ _ _ _")
    print(f"| {format(box["1"])} | {format(box["2"])} | {format(box["3"])} |")
    print("|- - - - - -|")
    print(f"| {format(box["4"])} | {format(box["5"])} | {format(box["6"])} |")
    print("|- - - - - -|")
    print(f"| {format(box["7"])} | {format(box["8"])} | {format(box["9"])} |")
    print(" - - - - - - ")
def compmove():
    global comp, player, emptyboxes, lines, difficulty
    preferredlines=[]
    preferredboxes=[]
    maxcount=-1
    defensemode=0

    # Scenario 1 : Opponent has 2/3 in a straight line and Computer doesn't
    for x in range(0,8):
        if lines[x].count(player)<1:
            maxcount=max(lines[x].count(comp), maxcount)
        if lines[x].count(player)==2 and lines[x].count(comp)==0:
            defensemode=1
    if maxcount==2: defensemode=0

    # Scenarios 2-5 : Opponent can get 2/3 on 2 different lines in a move
    if defensemode==0:
        if box["5"]==player and (box["1"]==player or box["3"]==player or box["7"]==player or box["9"]==player):
            defensemode=2
        elif box["5"]==comp and ((box["1"]==player and (box["9"]==player or box["6"]==player or ["8"]==player)) or (box["3"]==player and (box["4"]==player or box["7"]==player or ["8"]==player)) or (box["7"]==player and (box["2"]==player or box["6"]==player or ["3"]==player)) or (box["9"]==player and (box["1"]==player or box["2"]==player or ["4"]==player))):
            defensemode=3
        elif (box["2"]==player and box["4"]==player) or (box["4"]==player and box["8"]==player) or (box["6"]==player and box["8"]==player) or (box["2"]==player and box["6"]==player):
            defensemode=4
        elif box["5"]!=comp and (box["2"]==player or box["4"]==player or box["6"]==player or box["8"]==player):
            defensemode=5

    defensemode=min(defensemode,int(difficulty))

    if defensemode>0:
        # print(f"{Colors.RED}DEFENSE MODE: {defensemode}{Colors.ENDC}")
        match defensemode:
            case 1:
                for x in range(0,8):
                    if lines[x].count(player)==2:
                        for y in range(0,len(emptyboxes)):
                            if lines[x].count(emptyboxes[y])>0:
                                preferredboxes.append(emptyboxes[y])
            case 2:
                if box["1"]==player or box["9"]==player: preferredboxes=["3","7"]
                elif box["3"]==player or box["7"]==player: preferredboxes=["1","9"]
            case 3:
                if (box["1"]==player and box["9"]==player) or (box["3"]==player and box["7"]==player):
                    preferredboxes=["2","4","6","8"]
                elif box["1"]==player:
                    if box["6"]==player: preferredboxes=["2","3","9"]
                    if box["8"]==player: preferredboxes=["4","7","9"]
                elif box["3"]==player:
                    if box["4"]==player: preferredboxes=["2","1","7"]
                    if box["8"]==player: preferredboxes=["6","7","9"]
                elif box["7"]==player:
                    if box["6"]==player: preferredboxes=["8","3","9"]
                    if box["2"]==player: preferredboxes=["4","1","3"]
                elif box["9"]==player:
                    if box["2"]==player: preferredboxes=["1","3","6"]
                    if box["4"]==player: preferredboxes=["1","7","8"]
                for x in range(0,len(preferredboxes)):
                    if box[preferredboxes[x]]==player or box[preferredboxes[x]]==comp:
                        preferredboxes=[]
                        break
            case 4:
                if box["2"]==player and box["4"]==player:
                    if box["3"]==3 and box["7"]==7: preferredboxes=["1"]
                    if box["6"]==6 and box["8"]==8: preferredboxes=["5"]
                elif box["8"]==player and box["4"]==player:
                    if box["1"]==1 and box["9"]==9: preferredboxes=["7"]
                    if box["6"]==6 and box["2"]==2: preferredboxes=["5"]
                elif box["2"]==player and box["6"]==player:
                    if box["1"]==1 and box["9"]==9: preferredboxes=["3"]
                    if box["8"]==8 and box["4"]==4: preferredboxes=["5"]
                elif box["8"]==player and box["6"]==player:
                    if box["3"]==3 and box["7"]==7: preferredboxes=["9"]
                    if box["4"]==4 and box["2"]==2: preferredboxes=["5"]
            case 5:
                preferredboxes=["5"]
        x=0
        while x<len(preferredboxes):
            if not preferredboxes[x] in emptyboxes: preferredboxes.pop(x)
            x+=1
    if defensemode==0 or preferredboxes==[]:
        if maxcount>-1:
            for x in range(0,8):
                if lines[x].count(comp)==maxcount and lines[x].count(player)<1:
                    preferredlines.append(lines[x])
            maxcount=-1
            for x in range(0,len(emptyboxes)):
                boxcount=0
                for y in range(0,len(preferredlines)):
                    if preferredlines[y].count(emptyboxes[x])>0: boxcount+=1
                maxcount=max(maxcount,boxcount)
            if maxcount>-1:
                for x in range(0, len(emptyboxes)):
                    boxcount = 0
                    for y in range(0, len(preferredlines)):
                        if preferredlines[y].count(emptyboxes[x]) > 0: boxcount += 1
                    if boxcount==maxcount: preferredboxes.append(emptyboxes[x])
            else: preferredboxes=emptyboxes
        else: preferredboxes=emptyboxes
    # print(f"Preferred boxes: {preferredboxes}")
    fillbox(random.choice(preferredboxes),comp)
def playermove():
    global emptyboxes, player
    x=input("Choose a box: ")
    if not x in box or not x in emptyboxes:
        print("\nInvalid input.")
        playermove()
    else: fillbox(x,player)
def newturn():
    global turn, player, emptyboxes, lines, turncount
    if turn==player: turncount+=1
    for x in range(0,8):
        if lines[x]=="XXX": endgame("X")
        elif lines[x]=="000": endgame("0")
    if emptyboxes==[] : endgame("Nobody")
    else:
        print(f"Turn {turncount}\n{turn}'s turn.")
        if turn==player:
            printboard()
            playermove()
        else:
            compmove()
            printboard()
        if turn=="X": turn="0"
        else: turn="X"
        newturn()
def fillbox(n,x):
    global emptyboxes,lines
    box[n]=x
    emptyboxes.remove(n)
    for y in range(0,8): lines[y]=lines[y].replace(n,x)
def startgame():
    global emptyboxes, lines, player, comp, turn, turncount
    turncount=0
    emptyboxes = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    lines = ["123", "456", "789", "147", "258", "369", "159", "357"]
    for x in emptyboxes: box.update({x: int(x)})
    turn = "X"

    player = input("Choose X or 0\n")
    if player=="x": player="X"
    if player == "X":
        comp = "0"
        newturn()
    elif player == "0":
        comp = "X"
        newturn()
    else:
        print("Invalid input.")
        startgame()
def endgame(winner):
    global player, comp, playercolor, compcolor, score
    printboard()
    if winner==player:
        winner="Player"
        if keepscore: score[0]+=1
        winnercolor=playercolor
    elif winner==comp:
        winner="Computer"
        if keepscore: score[1]+=1
        winnercolor=compcolor
    else:
        winner="Nobody"
        if keepscore: score[2]+=1
        winnercolor = Colors.ENDC
    print(f"{winnercolor}{winner} wins.{Colors.ENDC}")
    if keepscore: print(f"Score: {playercolor}P:{score[0]} {compcolor}C:{score[1]} {Colors.ENDC}D:{score[2]}")
    x=input("Start a new game?\n")
    if x=="Yes" or x=="Y" or x=="y": startgame()
    else: mainmenu()
def format(x):
    global player, comp, playercolor, compcolor
    if x==player: return f"{playercolor}{x}{Colors.ENDC}"
    elif x==comp: return f"{compcolor}{x}{Colors.ENDC}"
    else: return x
def settings():
    global playercolor, compcolor, difficulty, keepscore, score
    select=""
    match input(f"{playercolor}1. Player color{Colors.ENDC} \n{compcolor}2. Computer color{Colors.ENDC}\n3. Difficulty: {difficulty_qualifier(difficulty)}\n4. Keep score: {keepscore}\n5. Back\n"):
        case "1": select="Player"
        case "2": select="Computer"
        case "3":
            new_difficulty = input("Choose Difficulty (1-5): ")
            if not new_difficulty in ["1","2","3","4","5"]: print("Invalid input.")
            else: difficulty = new_difficulty
        case "4":
            keepscore=not keepscore
            score = [0, 0, 0]
            settings()
        case "5": mainmenu()
        case _: settings()
    if select!="":
        match input(f"Select {select} color:\n1. Red\n2. Blue\n3. Yellow\n4. Green\n5. Cyan\n6. White\n"):
            case "1": newcolor=Colors.RED
            case "2": newcolor=Colors.BLUE
            case "3": newcolor=Colors.YELLOW
            case "4": newcolor=Colors.GREEN
            case "5": newcolor=Colors.CYAN
            case "6": newcolor=Colors.ENDC
        if select=="Player": playercolor=newcolor
        else: compcolor=newcolor
    settings()
def mainmenu():
    match input("1. Start game\n2. Settings\n3. Exit\n"):
        case "1": startgame()
        case "2": settings()
        case "3": exit()
        case _: mainmenu()
def difficulty_qualifier(difficulty):
    if difficulty=="1": return "1 (Easy)"
    if difficulty=="2": return "2 (Medium)"
    if difficulty=="3": return "3 (Hard)"
    if difficulty=="4": return "4 (Challenging)"
    else: return "5 (Impossible)"

if __name__ == "__main__":
    mainmenu()