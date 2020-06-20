from random import randint, choice

def lcboard(stat):
    """returns the str that represents the board"""
    l1 = " " + " ".join(map(str, range(1,rowsum+1))) + "\n"
    # todo: consider optmizing the printout?\
    #  sth to indicate the row put, and try optimize the situation when rowsum gt 9
    l2 = "\n".join("|"+
        "|".join(stat[row][line] for row in range(1,rowsum+1)) +"|"
        for line in range(linesum,0,-1))
    l3 = "\n-----------------\n"
    return "".join((l1,l2,l3))


def lccheck(rp):
    """check if someone wins or game ties after putting a piece on row"""
    global pieces
    pieces += 1

    lp = stat[rp][0]
    target = stat[rp][lp] * piece_to_win
    strver = "".join(stat[rp][line] for line in range(1, linesum + 1))
    strhor = "".join(stat[row][lp] for row in range(1, rowsum+1))
    strlef = "".join(stat[rp+i][lp+i] for i in range(max(1-rp,1-lp), 1+min(rowsum-rp,linesum-lp)))
    strrig = "".join(stat[rp+i][lp-i] for i in range(max(1-rp, lp-linesum), 1+min(rowsum-rp,lp-1)))

    if target in "|".join((strver,strhor,strlef,strrig)):
        lclog("******* Yeah, I win！^_^" if target[0] == "O" else "******* Alright, you did it. ^_*")
        return True
    elif pieces >= rowsum * linesum:
        lclog("******* Tiegame！@_@")
        return True
    else:
        return False


def lclog(text, needprint=True):
    """print text and write it in the log file"""
    if needprint: print(text)
    if type(idcode) == str or idcode > 0:  # for module test purpose
        with open("SomeChessLog-{}.txt".format(idcode), "a+", encoding="UTF-8") as lg:
            lg.write(text)
            lg.write("\n")


def lcgame():
    """the main game function"""
    start = "Hi,I'm Laura Crauft. I wanna play a chess with you. I use 'O' pieces, you use 'X' pieces.\n" \
            "Game rule:\n Take turns to choose a row number to put your piece. Then your piece will drop down.\n" \
            f"\t Once there are {piece_to_win} pieces together in the same line, that player wins.\n" \
            "That's it. Lets start! Here is the default stat of the board." \

    global stat
    lclog(start)
    lclog(lcboard(stat))

    while True:
        tmp = choice([i for i in range(1,rowsum+1) if stat[i][0]<linesum])
        lclog(">>>My turn! I lay 'O' on row {}.".format(tmp))
        stat[tmp][0] += 1
        stat[tmp][stat[tmp][0]] = "O"
        lclog(lcboard(stat))
        if lccheck(tmp):
            return

        while True:
            tmp = input(">>>Your turn, Choose a row to drop your 'X' (1-{}): ".format(rowsum))
            lclog(">>>Your turn, Choose a row to drop your 'X' (1-{}): ".format(rowsum)+tmp, False)
            try:
                tmp = int(tmp)
            except ValueError:
                lclog("Sorry. I didn't get it. Input again.")
                continue

            if tmp > rowsum or tmp < 1:
                lclog("Row number should be between 1 and 8, please input again.")
                continue
            elif stat[tmp][0] >= linesum:
                lclog("There isn't any space on that row, pls input again.")
                continue

            break

        stat[tmp][0] += 1
        stat[tmp][stat[tmp][0]] = "X"
        lclog(lcboard(stat))
        if lccheck(tmp):
            return


pieces = 0
rowsum, linesum = 8, 6
piece_to_win = 4

stat = [0] + [{j+1:" " for j in range(linesum)} for i in range(rowsum)]
for i in range(rowsum): stat[i+1][0]=0


if __name__ == "__main__":
    while True:
        idcode = randint(10000, 99999)
        if not __import__("os").path.exists("SomeChessLog-{}.txt".format(idcode)):
            break

    lcgame()
    input("press Enter to exit")

else:
    idcode = -1

    def settings():
        global rowsum, linesum, idcode, piece_to_win
        if input("Change Settings? If not, just leave it blank: "):
            rowsum = int(input("new rowsum? ") or rowsum)
            linesum = int(input("new linesum? ") or linesum)
            idcode = input("specify log file id? leave it blank to avoid creating a log file: ") or idcode
            piece_to_win = int(input("change pieces to win? ") or piece_to_win)


    def start():
        global stat
        stat = [0] + [{j + 1: " " for j in range(linesum)} for i in range(rowsum)]
        for i in range(rowsum): stat[i + 1][0] = 0

        lcgame()
        print("-"*50)
        print("Game Ended")
        print("Execute 'settings()' to change settings. \nExecute 'start()' to start a game.\n")


    print("-"*50)
    print("Module imported.")
    print("Execute 'settings()' to change settings. \nExecute 'start()' to start a game.\n")
