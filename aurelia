from math import comb

def rateHand(a, b, c, d, e): #finds the best hand out of the 5 cards given
    cardsOut = a + b + c + d + e
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4] + cardsOut[6] + cardsOut[8]
    suitsList[0] = a[1]
    suitsList[1] = b[1]
    suitsList[2] = c[1]
    suitsList[3] = d[1]
    suitsList[4] = e[1]
    for i in range(0, 5, 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14 #highRanksList (A = 14) (for royal straights and figuring out highest rank)
                LRL[i] = 1 #lowRanksList (A = 1) (for A-5 straights)
            elif x == "K":
                HRL[i] = 13
                LRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
                LRL[i] = 12
            elif x == "J":
                HRL[i] = 11
                LRL[i] = 11
            elif x == "T":
                HRL[i] = 10
                LRL[i] = 10
        else:
            HRL[i] = int(x)
            LRL[i] = int(x)
    HRL.sort(reverse=True)
    LRL.sort(reverse=True)
    if (a[1] == b[1] and b[1] == c[1] and c[1] == d[1] and d[1] == e[1] and e[1] == a[1]):
        #flush
        if ("A" in cardsOut and "K" in cardsOut and "Q" in cardsOut and "J" in cardsOut and "T" in cardsOut): #if it's a flush and you have all these cards it's a royal flush
            return("RF")
        else:
            #check for straight flush, which can be done by checking if all adjacent cards are 1 apart since the list has been sorted
            if ((HRL[0] - HRL[1] == HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == 1) or (LRL[0] - LRL[1] == LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == 1)):
                return("SF")
            else:
                return("F")
    else:
        if HRL[0] == HRL[3] or HRL[1] == HRL[4]: #since it's sorted, the only way cards this far apart would be the same is if also all the cards between them are the same
            return("4K")
        if (HRL[0] == HRL[2] and HRL[3] == HRL[4]) or (HRL[0] == HRL[1] and HRL[2] == HRL[4]): #using the same principle to check for a full house
            return("FH")
        if ((HRL[0] - HRL[1] == HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == 1) or (LRL[0] - LRL[1] == LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == 1)): #same principle as earlier checking for a straight flush
            return("S")
        if (HRL[0] == HRL[2] or HRL[1] == HRL[3] or HRL[2] == HRL[4]): #same principle as four of a kind
            return("3K")
        if (HRL[0] == HRL[1]): # if the first two cards are a pair
            if (HRL[2] == HRL[3] or HRL[3] == HRL[4]): #there are two possibilities for the placement of a second pair in the 5 known cards (2-2-1 or 2-1-2)
                return("2P")
            else:
                return("P") # but if there is the first pair and not one in those later spots it's got to be just a pair
        elif HRL[1] == HRL[2]: #same thing but with the 1-2-2 possibility
            if HRL[3] == HRL[4]:
                return("2P")
            else:
                return("P")
        elif (HRL[2] == HRL[3] or HRL[3] == HRL[4]): #there are other possibilities for just a pair, like being at the end (1-1-1-2)
            return("P")
        else:
            if max(HRL) == 14: #this is only reached if you pass every better hand and find nothing, so it just checks what the highest card you can see is
                return("HCA")
            elif max(HRL) == 13:
                return("HCK")
            elif max(HRL) == 12:
                return("HCQ")
            elif max(HRL) == 11:
                return("HCJ")
            elif max(HRL) == 10:
                return("HCT")
            else:
                return("HC" + str(max(HRL)))

def ratePotentialFlop(): #this function checks for the potential of your hand: if you have 4/5 cards for a royal flush, for example
    RFP = 0
    SFP = 0
    FKP = 0
    FHP = 0
    FP = 0
    SP = 0
    TKP = 0
    TPP = 0
    PP = 0
    cardCount = 52 - (2*playerCount) - 3
    othersHave = 0
    othersGet = 0
    willGet = 0
    suitsList = [h1[1], h2[1], c1[1], c2[1], c3[1]]
    HRL = [0, 0, 0, 0, 0]
    
    cardsOut = h1 + h2 + c1 + c2 + c3
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4] + cardsOut[6] + cardsOut[8]
    for i in range(0, 5, 1): #same setting up of variables
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14
            elif x == "K":
                HRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
            elif x == "J":
                HRL[i] = 11
            elif x == "T":
                HRL[i] = 10
        else:
            HRL[i] = int(x)
    HRL.sort(reverse=True)
    
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"] #list of all possible straights
    #royal flush
    royal = "AKQJT"
    j = 0
    for sf in straights:
        if sf == royal:
            j = 1
    
        for i in ranksOut:
            l = sf.find(i) #location
            if l != -1:
                sf = sf[0:l] + sf[l + 1:len(sf)]
        goalCards = len(sf)
        othersHave = comb(52, (2*playerCount - 2))
        othersGet = 0
        for i in range (1, goalCards, 1):
            othersGet += comb(2*(playerCount - 1), i)
        willGet = comb(2, goalCards)/comb(cardCount, 2)
        odds = willGet * (1 - (othersGet/othersHave))#royal flush prob # prob of NOT get = 1 - prob get
        if j != 0:
            RFP = odds
        else:
            SFP += odds
        j = 0
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    for s in straights:
        for i in ranksOut:
            l = s.find(i) #location
            if l != -1:
                s = s[0:l] + s[l + 1:len(s)]
        goalCards = len(s)
        #odds will be off because accounting for if other players have some of the cards that would give you the hand but you don't need All Of Them is hard
        SP += 4*comb(2, goalCards)/comb(cardCount, 2)
    
    #count suits
    maxSuited = 1
    streak = 1
    suitsList.sort()
    for i in range (1, len(suitsList), 1):
        if suitsList[i] == suitsList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak > maxSuited:
            maxSuited = streak
    goalCards = 5 - maxSuited
    if goalCards > 0:
        FP += (13 - maxSuited)*comb(2, goalCards)/comb(cardCount, 2)
    else:
        FP = 1
    
    ranksList = [0, 0, 0, 0, 0]
    for i in range(0, len(ranksList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                ranksList[i] = 14
            elif x == "K":
                ranksList[i] = 13
            elif x == "Q":
                ranksList[i] = 12
            elif x == "J":
                ranksList[i] = 11
            elif x == "T":
                ranksList[i] = 10
        else:
            ranksList[i] = int(x)
    ranksList.sort()
    maxSame = 1
    streak = 1
    for i in range (1, len(ranksList), 1):
        if ranksList[i] == ranksList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak == maxSame and maxSame == 2:
            TPP = 1
        if (streak == 3 and maxSame == 2) or (streak == 2 and maxSame == 3):
            FHP = 1
        if streak > maxSame:
            maxSame = streak

    #4kind
    goalCards = 4 - maxSame
    FKP += comb(2, goalCards)/comb(cardCount, 2)
    #3kind
    goalCards = 3 - maxSame
    TKP += comb(2, goalCards)/comb(cardCount, 2)
    #pair is wack
    if maxSame == 1:
        PP = 5*(3*comb(2, 1)/comb(cardCount, 2))
        TPP = 5*(comb(2, 1)/comb(cardCount, 2))*4*(comb(2, 1)/comb(cardCount - 1, 2))
    else:
        if TPP != 1:
            TPP = 5*(comb(2,1)/comb(cardCount, 2))
        PP = 1
    
    #let's try full house
    if maxSame == 1:
        FHP = 0
    else:
        if maxSame == 2:
            FHP = 3*comb(2, 2)/comb(cardCount,2)
        elif maxSame == 3 and FHP != 1:
            FHP = 2*comb(2,1)/comb(cardCount,2)
        else:
            FHP = 0 #nobody gaf because you have four of a kind
    probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
    return probList

def rateOthersFlop():
    RFP = 0
    SFP = 0
    FKP = 0
    FHP = 0
    FP = 0
    SP = 0
    TKP = 0
    TPP = 0
    PP = 0
    cardCount = 52 - (2*playerCount) - 3
    othersHave = 0
    othersGet = 0
    willGet = 0
    suitsList = [c1[1], c2[1], c3[1]]
    HRL = [0, 0, 0]
    
    cardsOut = c1 + c2 + c3
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4]
    for i in range(0, len(suitsList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14
            elif x == "K":
                HRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
            elif x == "J":
                HRL[i] = 11
            elif x == "T":
                HRL[i] = 10
        else:
            HRL[i] = int(x)
    HRL.sort(reverse=True)
    
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    #royal flush
    royal = "AKQJT"
    j = 0
    for sf in straights:
        if sf == royal:
            j = 1
    
        for i in ranksOut:
            l = sf.find(i) #location
            if l != -1:
                sf = sf[0:l] + sf[l + 1:len(sf)]
        goalCards = len(sf)
        othersHave = comb(52, (2*playerCount - 2))
        othersGet = 0
        for i in range (1, goalCards, 1):
            othersGet += comb(2*(playerCount - 1), i)
        willGet = comb(2, goalCards)/comb(cardCount, 2)
        odds = willGet * (1 - (othersGet/othersHave))#royal flush prob # prob of NOT get = 1 - prob get
        if j != 0:
            RFP = odds
        else:
            SFP += odds
        j = 0
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    for s in straights:
        for i in ranksOut:
            l = s.find(i) #location
            if l != -1:
                s = s[0:l] + s[l + 1:len(s)]
        goalCards = len(s)
        #odds will be off because accounting for if other players have some of the cards that would give you the hand but you don't need All Of Them is hard
        SP += 4*comb(2, goalCards)/comb(cardCount, 2)
    
    #count suits
    maxSuited = 1
    streak = 1
    suitsList.sort()
    for i in range (1, len(suitsList), 1):
        if suitsList[i] == suitsList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak > maxSuited:
            maxSuited = streak
    goalCards = 5 - maxSuited
    if goalCards > 0:
        FP += (13 - maxSuited)*comb(2, goalCards)/comb(cardCount, 2)
    else:
        FP = 1
    
    ranksList = [0, 0, 0]
    for i in range(0, len(ranksList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                ranksList[i] = 14
            elif x == "K":
                ranksList[i] = 13
            elif x == "Q":
                ranksList[i] = 12
            elif x == "J":
                ranksList[i] = 11
            elif x == "T":
                ranksList[i] = 10
        else:
            ranksList[i] = int(x)
    ranksList.sort()
    maxSame = 1
    streak = 1
    for i in range (1, len(ranksList), 1):
        if ranksList[i] == ranksList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak == maxSame and maxSame == 2:
            TPP = 1
        if (streak == 3 and maxSame == 2) or (streak == 2 and maxSame == 3):
            FHP = 1
        if streak > maxSame:
            maxSame = streak

    #4kind
    goalCards = 4 - maxSame
    FKP += comb(2, goalCards)/comb(cardCount, 2)
    #3kind
    goalCards = 3 - maxSame
    TKP += comb(2, goalCards)/comb(cardCount, 2)
    #pair is wack
    if maxSame == 1:
        PP = 5*(3*comb(2, 1)/comb(cardCount, 2))
        TPP = 5*(comb(2, 1)/comb(cardCount, 2))*4*(comb(2, 1)/comb(cardCount - 1, 2))
    else:
        if TPP != 1:
            TPP = 3*(comb(2,1)/comb(cardCount, 2))
        PP = 1
    
    #let's try full house
    if maxSame == 1:
        FHP = 0
    else:
        if maxSame == 2:
            FHP = 3*comb(2, 2)/comb(cardCount,2)
        elif maxSame == 3 and FHP != 1:
            FHP = 2*comb(2,1)/comb(cardCount,2)
        else:
            FHP = 0 #this probability doesnt matter anymore because you actively have four of a kind which is a better hand
    probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
    return probList

def rateTurnHand():
    cardsOut = h1 + h2 + c1 + c2 + c3 + c4
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4] + cardsOut[6] + cardsOut[8] + cardsOut[10]
    suitsOut = [cardsOut[1], cardsOut[3], cardsOut[5], cardsOut[7], cardsOut[9], cardsOut[11]]
    HRL = [0, 0, 0, 0, 0, 0]
    LRL = [0, 0, 0, 0, 0, 0]
    for i in range(0, 6, 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14
                LRL[i] = 1
            elif x == "K":
                HRL[i] = 13
                LRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
                LRL[i] = 12
            elif x == "J":
                HRL[i] = 11
                LRL[i] = 11
            elif x == "T":
                HRL[i] = 10
                LRL[i] = 10
        else:
            HRL[i] = int(x)
            LRL[i] = int(x)
    HRL.sort(reverse=True)
    LRL.sort(reverse=True)
    suitsOut.sort()
    if (suitsOut[0] == suitsOut[4] or suitsOut[1] == suitsOut[5]):
        flushSuit = suitsOut[2]
        
        #flush
        if (("A" + flushSuit) in cardsOut and ("K" + flushSuit) in cardsOut and ("Q" + flushSuit) in cardsOut and ("J" + flushSuit) in cardsOut and ("T" + flushSuit) in cardsOut):
            return("RF")
        else:
            #check for straight flush
            if (((HRL[0] - HRL[1] == HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == 1) or (LRL[0] - LRL[1] == LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == 1)) or ((HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == HRL[4] - HRL[5] == 1) or (LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == LRL[4] - LRL[5] == 1))):
                return("SF")
            else:
                return("F")
    else:
        if HRL[0] == HRL[3] or HRL[1] == HRL[4] or HRL[2] == HRL[5]:
            return("4K")
        same3 = False
        same2 = False
        for c in HRL:
            if (HRL.count(c) == 3):
                same3 = True
            elif (HRL.count(c) == 2):
                same2 = True
        if (same3 and same2):
            return("FH")
        if (((HRL[0] - HRL[1] == HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == 1) or (LRL[0] - LRL[1] == LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == 1)) or ((HRL[1] - HRL[2] == HRL[2] - HRL[3] == HRL[3] - HRL[4] == HRL[4] - HRL[5] == 1) or (LRL[1] - LRL[2] == LRL[2] - LRL[3] == LRL[3] - LRL[4] == LRL[4] - LRL[5] == 1))):
            return("S")
        if (HRL[0] == HRL[2] or HRL[1] == HRL[3] or HRL[2] == HRL[4] or HRL[3] == HRL[5]):
            return("3K")
        if (HRL[0] == HRL[1]):
            if (HRL[2] == HRL[3] or HRL[3] == HRL[4] or HLR[4] == HRL[5]):
                return("2P")
            else:
                return("P")
        elif (HRL[1] == HRL[2]):
            if (HRL[3] == HRL[4] or HRL[4] == HRL[5]):
                return("2P")
        elif (HRL[2] == HRL[3]):
            if (HRL[4] == HRL[5]):
                return("2P")
        for c in HRL:
            if (HRL.count(c) == 2):
                return("P")
        else:
            if max(HRL) == 14:
                return("HCA")
            elif max(HRL) == 13:
                return("HCK")
            elif max(HRL) == 12:
                return("HCQ")
            elif max(HRL) == 11:
                return("HCJ")
            elif max(HRL) == 10:
                return("HCT")
            else:
                return("HC" + str(max(HRL)))


def ratePotentialTurn():
    RFP = 0
    SFP = 0
    FKP = 0
    FHP = 0
    FP = 0
    SP = 0
    TKP = 0
    TPP = 0
    PP = 0
    cardCount = 52 - (2*playerCount) - 4
    othersHave = 0
    othersGet = 0
    willGet = 0
    suitsList = [h1[1], h2[1], c1[1], c2[1], c3[1], c4[1]]
    HRL = [0, 0, 0, 0, 0, 0]
    
    cardsOut = h1 + h2 + c1 + c2 + c3 + c4
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4] + cardsOut[6] + cardsOut[8] + cardsOut[10]
    for i in range(0, 6, 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14
            elif x == "K":
                HRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
            elif x == "J":
                HRL[i] = 11
            elif x == "T":
                HRL[i] = 10
        else:
            HRL[i] = int(x)
    HRL.sort(reverse=True)
    
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    #royal flush
    royal = "AKQJT"
    j = 0
    for sf in straights:
        if sf == royal:
            j = 1
    
        for i in ranksOut:
            l = sf.find(i) #location
            if l != -1:
                sf = sf[0:l] + sf[l + 1:len(sf)]
        goalCards = len(sf)
        othersHave = comb(52, (2*playerCount - 2))
        othersGet = 0
        for i in range (1, goalCards, 1):
            othersGet += comb(2*(playerCount - 1), i)
        willGet = comb(2, goalCards)/comb(cardCount, 2)
        odds = willGet * (1 - (othersGet/othersHave))#royal flush prob # prob of NOT get = 1 - prob get
        if j != 0:
            RFP = odds
        else:
            SFP += odds
        j = 0
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    for s in straights:
        for i in ranksOut:
            l = s.find(i) #location
            if l != -1:
                s = s[0:l] + s[l + 1:len(s)]
        goalCards = len(s)
        #odds will be off because accounting for if other players have some of the cards that would give you the hand but you don't need All Of Them is hard
        SP += 4*comb(2, goalCards)/comb(cardCount, 2)
    
    #count suits
    maxSuited = 1
    streak = 1
    suitsList.sort()
    for i in range (1, len(suitsList), 1):
        if suitsList[i] == suitsList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak > maxSuited:
            maxSuited = streak
    goalCards = 5 - maxSuited
    if goalCards > 0:
        FP += (13 - maxSuited)*comb(2, goalCards)/comb(cardCount, 2)
    else:
        FP = 1
    
    ranksList = [0, 0, 0, 0, 0, 0]
    for i in range(0, len(ranksList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                ranksList[i] = 14
            elif x == "K":
                ranksList[i] = 13
            elif x == "Q":
                ranksList[i] = 12
            elif x == "J":
                ranksList[i] = 11
            elif x == "T":
                ranksList[i] = 10
        else:
            ranksList[i] = int(x)
    ranksList.sort()
    maxSame = 1
    streak = 1
    for i in range (1, len(ranksList), 1):
        if ranksList[i] == ranksList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak == maxSame and maxSame == 2:
            TPP = 1
        if (streak == 3 and maxSame == 2) or (streak == 2 and maxSame == 3):
            FHP = 1
        if streak > maxSame:
            maxSame = streak

    #4kind
    goalCards = 4 - maxSame
    FKP += comb(2, goalCards)/comb(cardCount, 2)
    #3kind
    goalCards = 3 - maxSame
    TKP += comb(2, goalCards)/comb(cardCount, 2)
    #pair is wack
    if maxSame == 1:
        PP = 6*(3*comb(2, 1)/comb(cardCount, 2))
        TPP = 6*(comb(2, 1)/comb(cardCount, 2))*4*(comb(2, 1)/comb(cardCount - 1, 2))
    else:
        if TPP != 1:
            TPP = 6*(comb(2,1)/comb(cardCount, 2))
        PP = 1
    
    #let's try full house
    if maxSame == 1:
        FHP = 0
    else:
        if maxSame == 2:
            FHP = 3*comb(2, 2)/comb(cardCount,2)
        elif maxSame == 3 and FHP != 1:
            FHP = 2*comb(2,1)/comb(cardCount,2)
        else:
            FHP = 0 #nobody gaf because you have four of a kind
    probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
    return probList #DEFFFFinitely needs testing #TEST RAHHHH
    
def rateOthersTurn():
    RFP = 0
    SFP = 0
    FKP = 0
    FHP = 0
    FP = 0
    SP = 0
    TKP = 0
    TPP = 0
    PP = 0
    cardCount = 52 - (2*playerCount) - 4
    othersHave = 0
    othersGet = 0
    willGet = 0
    suitsList = [c1[1], c2[1], c3[1], c4[1]]
    HRL = [0, 0, 0, 0]
    
    cardsOut = c1 + c2 + c3 + c4
    ranksOut = cardsOut[0] + cardsOut[2] + cardsOut[4] + cardsOut[6]
    for i in range(0, len(suitsList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                HRL[i] = 14
            elif x == "K":
                HRL[i] = 13
            elif x == "Q":
                HRL[i] = 12
            elif x == "J":
                HRL[i] = 11
            elif x == "T":
                HRL[i] = 10
        else:
            HRL[i] = int(x)
    HRL.sort(reverse=True)
    
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    #royal flush
    royal = "AKQJT"
    j = 0
    for sf in straights:
        if sf == royal:
            j = 1
    
        for i in ranksOut:
            l = sf.find(i) #location
            if l != -1:
                sf = sf[0:l] + sf[l + 1:len(sf)]
        goalCards = len(sf)
        othersHave = comb(52, (2*playerCount - 2))
        othersGet = 0
        for i in range (1, goalCards, 1):
            othersGet += comb(2*(playerCount - 1), i)
        willGet = comb(2, goalCards)/comb(cardCount, 2)
        odds = willGet * (1 - (othersGet/othersHave))#royal flush prob # prob of NOT get = 1 - prob get
        if j != 0:
            RFP = odds
        else:
            SFP += odds
        j = 0
    straights = ["AKQJT", "KQJT9", "QJT98", "JT987", "T9876", "98765", "87654", "76543", "65432", "5432A"]
    for s in straights:
        for i in ranksOut:
            l = s.find(i) #location
            if l != -1:
                s = s[0:l] + s[l + 1:len(s)]
        goalCards = len(s)
        #odds will be off because accounting for if other players have some of the cards that would give you the hand but you don't need All Of Them is hard
        SP += 4*comb(2, goalCards)/comb(cardCount, 2)
    
    #count suits
    maxSuited = 1
    streak = 1
    suitsList.sort()
    for i in range (1, len(suitsList), 1):
        if suitsList[i] == suitsList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak > maxSuited:
            maxSuited = streak
    goalCards = 5 - maxSuited
    if goalCards > 0:
        FP += (13 - maxSuited)*comb(2, goalCards)/comb(cardCount, 2)
    else:
        FP = 1
    
    ranksList = [0, 0, 0, 0]
    for i in range(0, len(ranksList), 1):
        x = ranksOut[i]
        if x in "AKQJT":
            if x == "A":
                ranksList[i] = 14
            elif x == "K":
                ranksList[i] = 13
            elif x == "Q":
                ranksList[i] = 12
            elif x == "J":
                ranksList[i] = 11
            elif x == "T":
                ranksList[i] = 10
        else:
            ranksList[i] = int(x)
    ranksList.sort()
    maxSame = 1
    streak = 1
    for i in range (1, len(ranksList), 1):
        if ranksList[i] == ranksList[i - 1]:
            streak += 1
        else:
            streak = 1
        if streak == maxSame and maxSame == 2:
            TPP = 1
        if (streak == 3 and maxSame == 2) or (streak == 2 and maxSame == 3):
            FHP = 1
        if streak > maxSame:
            maxSame = streak

    #4kind
    goalCards = 4 - maxSame
    FKP += comb(2, goalCards)/comb(cardCount, 2)
    #3kind
    goalCards = 3 - maxSame
    TKP += comb(2, goalCards)/comb(cardCount, 2)
    #pair is wack
    if maxSame == 1:
        PP = 4*(3*comb(2, 1)/comb(cardCount, 2))
        TPP = 4*(comb(2, 1)/comb(cardCount, 2))*4*(comb(2, 1)/comb(cardCount - 1, 2))
    else:
        if TPP != 1:
            TPP = 4*(comb(2,1)/comb(cardCount, 2))
        PP = 1
    
    #let's try full house
    if maxSame == 1:
        FHP = 0
    else:
        if maxSame == 2:
            FHP = 3*comb(2, 2)/comb(cardCount,2)
        elif maxSame == 3 and FHP != 1:
            FHP = 2*comb(2,1)/comb(cardCount,2)
        else:
            FHP = 0 #nobody gaf because you have four of a kind
    probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
    return probList #DEFFFFinitely needs testing # test this one also
    
def rateFinalHand():
    suited = (h1[1] == h2[1])
    hand = h1[0] + h2[0]

    cardSlots = [h1, h2, c1, c2, c3, c4, c5]
    handList = []
    comboList = []
    currentList = [h1, h2, c1, c2, c3]

    for i in range (0, 5):
        if (i < 5):
            for j in range(1, len(cardSlots)):
                if not(cardSlots[len(cardSlots) - j] in currentList):
                    hold1 = currentList[i]
                    currentList[i] = cardSlots[len(cardSlots) - j]
                    handCheckList = [currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]]
                    handCheckList.sort()
                    comboList.append(str(handCheckList))
                    handList.append(rateHand(currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]))
                    for k in range (0, 5):
                        if (k < 5):
                            for l in range(1, len(cardSlots)):
                                if not(cardSlots[len(cardSlots) - l] in currentList):
                                    hold2 = currentList[k]
                                    currentList[k] = cardSlots[len(cardSlots) - l]
                                    handCheckList = [currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]]
                                    handCheckList.sort()
                                    comboList.append(str(handCheckList))
                                    handList.append(rateHand(currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]))
                                    currentList[k] = hold2
                        else:
                            handCheckList = [currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]]
                            handCheckList.sort()
                            comboList.append(str(handCheckList))
                            handList.append(rateHand(currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]))
                    currentList[i] = hold1
        else:
            handCheckList = [currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]]
            handCheckList.sort()
            comboList.append(str(handCheckList))
            handList.append(rateHand(currentList[0], currentList[1], currentList[2], currentList[3], currentList[4]))
    
    index = -1

    if handList.count("RF") > 0:
        return("Royal Flush: " + str(comboList[handList.index("RF")]))
    elif handList.count("SF") > 0:
        if handList.count("SF") > 1:
            sfs = []
            indices = []
            for i in range (0, len(handList)):
                if handList[i] == "SF":
                    indices.append(i)
                    if "K" in comboList[i]:
                        sfs.append(13)
                    elif "Q" in comboList[i]:
                        sfs.append(12)
                    elif "J" in comboList[i]:
                        sfs.append(11)
                    elif "T" in comboList[i]:
                        sfs.append(10)
                    elif "9" in comboList[i]:
                        sfs.append(9)
                    elif "8" in comboList[i]:
                        sfs.append(8)
                    elif "7" in comboList[i]:
                        sfs.append(7)
                    elif "6" in comboList[i]:
                        sfs.append(6)
                    elif "5" in comboList[i]:
                        sfs.append(5)
                    index = indices[sfs.index(max(sfs))]
        else:
            index = handList.index("SF")
        return("Straight Flush: " + str(comboList[index]))
    elif handList.count("4K") > 0:
        if handList.count("4K") > 1:
            ranks = []
            indices = []
            for i in range(0, len(handList)):
                if handList[i] == "4K":
                    if comboList[i][2] != comboList[i][8]:
                        r = comboList[i][2]
                    else:
                        r = comboList[i][26]
                    x = 0
                    if r in "AKQJT":
                        if r == "A":
                            x = 14
                        elif r == "K":
                            x = 13
                        elif r == "Q":
                            x = 12
                        elif r == "J":
                            x = 11
                        else:
                            x = 10
                    else:
                        x = int(r)
                    ranks.append(x)
                    indices.append(i)
            index = indices[ranks.index(max(ranks))]
        else:
            index = handList.find("4K")
        return("Four of a Kind: " + str(comboList[index]))
    elif handList.count("FH") > 0:
        if handList.count("FH") > 1:
            highRanks = []
            lowRanks = []
            indices = []
            for i in range(0, len(handList)):
                if handList[i] == "FH":
                    a = comboList[i][2]
                    b = comboList[i][20]
                    x = 0
                    y = 0
                    if not(a in "AQJKT"):
                        x = int(a)
                    else:
                        if a == "A":
                            x = 14
                        if a == "K":
                            x = 13
                        if a == "Q":
                            x = 12
                        if a == "J":
                            x = 11
                        if a == "T":
                            x = 10
                    if not(b in "AQJKT"):
                        y = int(b)
                    else:
                        if b == "A":
                            y = 14
                        if b == "K":
                            y = 13
                        if b == "Q":
                            y = 12
                        if b == "J":
                            y = 11
                        if b == "T":
                            y = 10
                    highRanks.append(max(x, y))
                    lowRanks.append(min(x, y))
                    indices.append(i)
            if highRanks.count(max(highRanks)) > 1:
                maxLow = 0
                for i in range(0, len(highRanks)):
                    if highRanks[i] == max(highRanks):
                        if lowRanks[i] > maxLow:
                            maxLow = lowRanks[i]
                index = indices[lowRanks.index(maxLow)]
            else:
                index = indices(highRanks.index(max(highRanks)))
        else:
            index = handList.index("FH")
        return("Full House: " + str(comboList[index]))
    elif handList.count("F") > 0:
        indices = []
        ranks1 = []
        ranks2 = []
        ranks3 = []
        ranks4 = []
        ranks5 = []
        for i in range(0, len(handList)):
            if handList[i] == "F":
                sIndex = ["h", "c", "d", "s"]
                h = comboList[i].count("h")
                c = comboList[i].count("c")
                d = comboList[i].count("d")
                s = comboList[i].count("s")
                sCount = [h, c, d, s]
                suit = sIndex[sCount.index(max(sCount))]
                exList = []
                for j in range(2, 30, 6):
                    if comboList[i][j + 1] == suit:
                        ex = comboList[i][j]
                        if not(ex in "AQJKT"):
                            exList.append(int(ex))
                        else:
                            if ex == "A":
                                exList.append(14)
                            elif ex == "K":
                                exList.append(13)
                            elif ex == "Q":
                                exList.append(12)
                            elif ex == "J":
                                exList.append(11)
                            else:
                                exList.append(10)
                ranks1.append(max(exList))
                ranks5.append(min(exList))
                exList.remove(max(exList))
                exList.remove(min(exList))
                ranks2.append(max(exList))
                ranks4.append(min(exList))
                exList.remove(max(exList))
                ranks3.append(max(exList))
                indices.append(i)
        high2 = 1
        high3 = 1
        high4 = 1
        high5 = 1
        for x in range(0, len(ranks1)):
            if ranks1[x] == max(ranks1):
                if ranks2[x] > high2:
                    high2 = ranks2[x]
                    if ranks3[x] > high3:
                        high3 = ranks3[x]
                        if ranks4[x] > high4:
                            high4 = ranks4[x]
                            if ranks5[x] > high5:
                                high5 = ranks5[x]
        index = indices[ranks5.index(high5)]
        return("Flush: " + str(comboList[index]))
    elif handList.count("S") > 0:
        if handList.count("SF") > 1:
            shs = []
            indices = []
            for i in range (0, len(handList)):
                if handList[i] == "S":
                    indices.append(i)
                    if "K" in comboList[i]:
                        shs.append(13)
                    elif "Q" in comboList[i]:
                        shs.append(12)
                    elif "J" in comboList[i]:
                        shs.append(11)
                    elif "T" in comboList[i]:
                        shs.append(10)
                    elif "9" in comboList[i]:
                        shs.append(9)
                    elif "8" in comboList[i]:
                        shs.append(8)
                    elif "7" in comboList[i]:
                        shs.append(7)
                    elif "6" in comboList[i]:
                        shs.append(6)
                    elif "5" in comboList[i]:
                        shs.append(5)
                    index = indices[sfs.index(max(shs))]
        else:
            index = handList.index("S")
        return("Straight: " + str(comboList[index]))
    elif handList.count("3K") > 0:
        if handList.count("3K") > 1:
            ranks1 = []
            ranks2 = []
            indices = []
            for i in range(0, len(handList)):
                if handList[i] == "3K":
                    if comboList[i][2] == comboList[i][8]:
                        r1 = comboList[i][20]
                        r2 = comboList[i][26]
                    elif comboList[i][8] == comboList[i][14]:
                        r1 = comboList[i][2]
                        r2 = comboList[i][26]
                    else:
                        r1 = comboList[i][2]
                        r2 = comboList[i][8]
                    x = 0
                    y = 0
                    if r1 in "AKQJT":
                        if r1 == "A":
                            x = 14
                        elif r1 == "K":
                            x = 13
                        elif r1 == "Q":
                            x = 12
                        elif r1 == "J":
                            x = 11
                        else:
                            x = 10
                    else:
                        x = int(r1)
                    if r2 in "AKQJT":
                        if r2 == "A":
                            y = 14
                        elif r2 == "K":
                            y = 13
                        elif r2 == "Q":
                            y = 12
                        elif r2 == "J":
                            y = 11
                        else:
                            y = 10
                    else:
                        y = int(r2)
                    ranks1.append(max(x,y))
                    ranks2.append(min(x,y))
                    indices.append(i)
            if ranks1.count(max(ranks1)) > 1:
                max2 = 0
                for i in range(0, len(ranks1)):
                    if ranks1[i] == max(ranks1):
                        if ranks2[i] > max2:
                            max2 = ranks2[i]
                index = indices[ranks2.index(max2)]
            else:
                index = indices[ranks1.index(max(ranks1))]
        else:
            index = handList.find("3K")
        return("Three of a Kind: " + str(comboList[index]))
    elif handList.count("2P") > 0:
        if handList.count("2P") > 1:
            highRanks = []
            lowRanks = []
            xRanks = []
            indices = []
            for i in range(0, len(handList)):
                if handList[i] == "2P":
                    a = comboList[i][8]
                    b = comboList[i][20]
                    x = 0
                    y = 0
                    z = 0
                    if not(a in "AQJKT"):
                        x = int(a)
                    else:
                        if a == "A":
                            x = 14
                        if a == "K":
                            x = 13
                        if a == "Q":
                            x = 12
                        if a == "J":
                            x = 11
                        if a == "T":
                            x = 10
                    if not(b in "AQJKT"):
                        y = int(b)
                    else:
                        if b == "A":
                            y = 14
                        if b == "K":
                            y = 13
                        if b == "Q":
                            y = 12
                        if b == "J":
                            y = 11
                        if b == "T":
                            y = 10
                    highRanks.append(max(x, y))
                    lowRanks.append(min(x, y))
                    indices.append(i)
                    for j in range(2, 30, 6):
                        if comboList[i].count(comboList[i][j]) == 1:
                            ex = comboList[i][j]
                            if ex in "AKQJT":
                                if ex == "A":
                                    z = 14
                                elif ex == "K":
                                    z = 13
                                elif ex == "Q":
                                    z = 12
                                elif ex == "J":
                                    z = 11
                                else:
                                    z = 10
                            else:
                                z = int(ex)
                            xRanks.append(z)
            if highRanks.count(max(highRanks)) > 1:
                maxLow = 0
                for i in range(0, len(highRanks)):
                    if highRanks[i] == max(highRanks):
                        if lowRanks[i] > maxLow:
                            maxLow = lowRanks[i]
                if lowRanks.count(maxLow) > 1:
                    maxEx = 0
                    for i in range(0, len(highRanks)):
                        if highRanks[i] == max(highRanks) and lowRanks[i] == max(lowRanks):
                            if xRanks[i] > maxEx:
                                maxEx = xRanks[i]
                    index = indices[xRanks.index(maxEx)]
                else:
                    index = indices[lowRanks.index(maxLow)]
            else:
                index = indices(highRanks.index(max(highRanks)))
        else:
            index = handList.index("2P")
        return("Two Pair: " + str(comboList[index])) 
    elif handList.count("P") > 0:
        indices = []
        highList = []
        lowList = []
        midList = []
        exList = []
        for i in range(0, len(handList)):
            if handList[i] == "P":
                exList = []
                for j in range(2, 30, 6):
                    if comboList[i].count(comboList[i][j]) == 1:
                        ex = comboList[i][j]
                        if not(ex in "AQJKT"):
                            exList.append(int(ex))
                        else:
                            if ex == "A":
                                exList.append(14)
                            elif ex == "K":
                                exList.append(13)
                            elif ex == "Q":
                                exList.append(12)
                            elif ex == "J":
                                exList.append(11)
                            else:
                                exList.append(10)
                highList.append(max(exList))
                lowList.append(min(exList))
                where = [0, 1, 2]
                where.remove(exList.index(max(exList)))
                where.remove(exList.index(min(exList)))
                midList.append(exList[where[0]])
                indices.append(i)
        highMid = 0
        highLow = 0
        for x in range(0, len(highList)):
            if highList[x] == max(highList):
                if midList[x] > highMid:
                    highMid = midList[x]
                    if lowList[x] > highLow:
                        highLow = lowList[x]
                        index = indices[x]
        return("Pair: " + str(comboList[index]))
    else:
        output = "High Card "
        r = 14
        while (len(output) == 10):
            for i in range(0, len(handList)):
                if len(output) == 10:
                    if r == 14:
                        if handList[i] == "HCA":
                            output = output + "Ace: "
                    if r == 13:
                        if handList[i] == "HCK":
                            output = output + "King: "
                    if r == 12:
                        if handList[i] == "HCQ":
                            output = output + "Queen: "
                    if r == 11:
                        if handList[i] == "HCJ":
                            output = output + "Jack: "
                    if r == 10:
                        if handList[i] == "HCT":
                            output = output + "10: "
                    else:
                        if str(r) in handList[i]:
                            output = output + str(r) + " "
            r -= 1
        indices = []
        ranks1 = []
        ranks2 = []
        ranks3 = []
        ranks4 = []
        ranks5 = []
        for i in range(0, len(handList)):
            if "HC" in handList[i]:
                exList = []
                for j in range(2, 30, 6):
                    ex = comboList[i][j]
                    if not(ex in "AQJKT"):
                        exList.append(int(ex))
                    else:
                        if ex == "A":
                            exList.append(14)
                        elif ex == "K":
                            exList.append(13)
                        elif ex == "Q":
                            exList.append(12)
                        elif ex == "J":
                            exList.append(11)
                        else:
                            exList.append(10)
                ranks1.append(max(exList))
                ranks5.append(min(exList))
                exList.remove(max(exList))
                exList.remove(min(exList))
                ranks2.append(max(exList))
                ranks4.append(min(exList))
                exList.remove(max(exList))
                ranks3.append(max(exList))
                indices.append(i)
        high2 = 0
        high3 = 0
        high4 = 0
        high5 = 0
        for x in range(0, len(ranks1)):
            if ranks1[x] == max(ranks1):
                if ranks2[x] > high2:
                    high2 = ranks2[x]
                if ranks2[x] == 13:
                    if ranks3[x] > high3:
                        high3 = ranks3[x]
                        if ranks4[x] > high4:
                            high4 = ranks4[x]
                            if ranks5[x] > high5:
                                high5 = ranks5[x]
                                
        index = indices[ranks5.index(high5)]
    
        return(output + str(comboList[index])) 

c1 = ""
c2 = ""
c3 = ""
c4 = ""
c5 = ""
playerCount = 6
HRL = [0, 0, 0, 0, 0] #hiRanksList
LRL = [0, 0, 0, 0, 0] #loRanksList
cardsOut = ""
ranksOut = ""
suitsList = ["", "", "", "", ""]



print("Guide: ten of hearts = Th, ace of spades = As, 2 of diamonds = 2d\n")
n = (input("What stage are you in?\t (P = pre-flop, F = flop, T = turn, R = river) \n"))

#in your hands
h1 = input("What is the first card in your hand?\n")
h2 = input("What is the second card in your hand?\n")
suited = (h1[1] == h2[1])
hand = h1[0] + h2[0]
if suited:
    hand += "s"
else:
    hand += "o"
#print(hand)

if (n == "P"):
    #print("Pre-flop")
    if (h1[0] == h2[0]) or (suited and "A" in hand) or (h1[0] in "AKQJT" and h2[0] in "AKQJT") or (h1[0] in "AKQJT" or h2[0] in "AKQJT") and ((h1[0] in "89") or ((h2[0] in "89")) and suited) or ((not(h1[0] in "AKQJT") or h2[0] in "AKQJT")) and ((abs(int(h1[0]) - int(h2[0])) == 1) and suited) or (hand == "97s"):
        print("Raise half the post!")
    else:
        print("Fold!")
elif (n == "F"):
    #print("Flop")
    c1 = input("What is the first card on the table?\n")
    c2 = input("What is the next card on the table?\n")
    c3 = input("What is the last card on the table?\n")
    birdInHand = rateHand(h1, h2, c1, c2, c3)
    probList = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    value = 0
    if birdInHand == "RF":
        value = 100
    elif birdInHand == "SF":
        if probList[1] != 0:
            value = 99
        else:
            value = 90
    elif birdInHand == "4K":
        value = 90
    else: 
        if birdInHand == "FH":
            value = 80
        elif (birdInHand == "F" or birdInHand == "S"):
            value = 75
        elif (birdInHand == "3K"):
            value = 65
        elif (birdInHand == "2P"):
            value = 55
        elif (birdInHand == "P"):
            value = 45
        else:
            value = 25
        #probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
        probList = ratePotentialFlop()
        value += (probList[0]*500 + probList[1]*400 + probList[2]*300 + probList[3]*200 + probList[4]*100 + probList[5]*100 + probList[6]*90 + probList[7]*75 + probList[8]*50)
        theirList = rateOthersFlop()
        value -= (theirList[0]*500 + theirList[1]*400 + theirList[2]*300 + theirList[3]*200 + theirList[4]*100 + theirList[5]*100 + theirList[6]*90 + theirList[7]*75 + theirList[8]*50)
    if (value >= 150):
        print("All in!")
    elif (value >= 100):
        print("Raise twice the post!")
    elif (value >= 75):
        print("Raise the post!")
    elif (value >= 50):
        print("Raise half the post!")
    elif (value < 25):
        print("Fold!")
    else:
        print("Check!")
elif (n == "T"):
    c1 = input("What is the first flop card on the table?\n")
    c2 = input("What is the second flop card on the table?\n")
    c3 = input("What is the third flop card on the table?\n")
    c4 = input("What is the new, fourth card on the table?\n")
    birdInHand = rateTurnHand()
    probList = [1, 1, 1, 1, 1, 1, 1, 1, 1]
    value = 0
    if birdInHand == "RF":
        value = 100
    elif birdInHand == "SF":
        if probList[1] != 0:
            value = 99
        else:
            value = 90
    elif birdInHand == "4K":
        value = 90
    else: 
        if birdInHand == "FH":
            value = 80
        elif (birdInHand == "F" or birdInHand == "S"):
            value = 75
        elif (birdInHand == "3K"):
            value = 65
        elif (birdInHand == "2P"):
            value = 55
        elif (birdInHand == "P"):
            value = 45
        else:
            value = 25
        #probList = [RFP, SFP, FKP, FHP, FP, SP, TKP, TPP, PP]
        probList = ratePotentialTurn()
        value += probList[0]*500 + probList[1]*400 + probList[2]*300 + probList[3]*200 + probList[4]*100 + probList[5]*100 + probList[6]*90 + probList[7]*75 + probList[8]*50
        theirList = rateOthersTurn()
        value -= theirList[0]*500 + theirList[1]*400 + theirList[2]*300 + theirList[3]*200 + theirList[4]*100 + theirList[5]*100 + theirList[6]*90 + theirList[7]*75 + theirList[8]*50
    #print(value)
    if (value >= 100):
        print("All in!")
    elif (value >= 90):
        print("Raise twice the post!")
    elif (value >= 75):
        print("Raise the post!")
    elif (value < 25):
        print("Fold!")
    else:
        print("Check!")
    #print("turn")
elif (n == "R"):
    c1 = input("What is the first card on the table?\n")
    c2 = input("What is the second card on the table?\n")
    c3 = input("What is the third card on the table?\n")
    c4 = input("What is the fourth card on the table?\n")
    c5 = input("What is the fifth and final card?\n")
    result = rateFinalHand()
    birdInHand = result[0:result.index(":")]
    print(result)
    if birdInHand == "Royal Flush" or birdInHand == "Straight Flush" or birdInHand == "Four of a Kind":
        print("All in!")
    elif birdInHand == "Full House" or birdInHand == "Flush" or birdInHand == "Straight":
        print("Raise 3/2 of the post!")
    elif birdInHand == "Three of a Kind" or birdInHand == "Two Pair":
        print("Raise the post!")
    elif birdInHand == "Pair":
        print("Check!")
    else:
        if birdInHand in "AceKingQueen":
            print("Raise half the post!")
        elif bridInHand in "Jack":
            print("Check!")
        else:
            print("Fold!")
    
    #print("river")
else:
    print("Double-check your formatting and try again.")



