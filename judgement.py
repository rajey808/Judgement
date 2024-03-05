import random

lowestNumber = 6
playerCount = 4
cardOrder = ["2","3","4","5","6","7","8","9","10","11","12","13","14"]


def createDeck():
    deck = []
    for suit in ["H","S","D","C"]:
        for card in range (5,15):
            deck.append(suit+str(card))
    return deck

def shuffleDeck(deck):
    random.shuffle(deck)
    return deck

def dealCards(players, deck):
    suitOrder = ["H","S","D","C"]
    cardOrder = ["2","3","4","5","6","7","8","9","10","11","12","13","14"]

    for index, card in enumerate(deck):
        if index % 4 == 0:
            players["P1"].append(card)
        elif index % 4 == 1:
            players["P2"].append(card)
        elif index % 4 == 2:
            players["P3"].append(card)
        else:
            players["P4"].append(card)

    #print(f"Cards unordered: {players}")


    for player in players:
        sortedHand = []
        #print(f"{player}")
        for suit in suitOrder: 
            filteredHand = [x for x in players[player] if x[0] == suit]
            filteredHand.sort(key=lambda c:cardOrder.index(c[1:]))
            sortedHand.append(filteredHand)
        
        flatList = [x for y in sortedHand for x in y]
        players[player] = flatList
         

def playRound(players, orderedPlayers, graveyard, trumpSuit, potentialWins, winCount):
    currentPile = []
    for currentPlayer in orderedPlayers:
        #print(f"Current Player: {currentPlayer}")
        cardToPlay = getBestCard(graveyard, players[currentPlayer], currentPile, trumpSuit, potentialWins, winCount, currentPlayer)
        player, currentPile = playCard(players[currentPlayer], currentPile, cardToPlay)
        players[currentPlayer] = player

    for x in currentPile : graveyard.append(x)
    print(f"current pile:{currentPile}")
    print(f"graveyard:{graveyard}")
    winningPlayer = roundWinner(currentPile, orderedPlayers, trumpSuit)

    return graveyard, winningPlayer

def playCard(player, currentPile, cardToPlay):

    player.remove(cardToPlay)
    currentPile.append(cardToPlay)

    '''if not currentPile:
        card = random.choice(player)
        player.remove(card)
        currentPile.append(card)
    else:
        roundSuit = currentPile[0][0]
        filteredCards = [x for x in player if x[0] == roundSuit]
        if filteredCards :
            card = random.choice(filteredCards)
            player.remove(card)
            currentPile.append(card)
        else:
            card = random.choice(player)
            player.remove(card)
            currentPile.append(card)'''

    return player, currentPile

def roundWinner(currentPile, orderedPlayers, trumpSuit):
    bestCard = None
    roundSuit = currentPile[0][0]

    for card in currentPile:
        if not bestCard:
            bestCard = card
        else:
            if card[0] == roundSuit:
                if int(card[1:]) > int(bestCard[1:]):
                    bestCard = card
            elif card[0] == trumpSuit:
                if bestCard[0] == trumpSuit:
                    if int(card[1:]) > int(bestCard[1:]):
                        bestCard = card
                else:
                    bestCard = card               
    
    index = currentPile.index(bestCard)
    winningPlayer = orderedPlayers[index]
    print(f"Winning Player: {winningPlayer}, Card Played: {bestCard}")
    return winningPlayer

def orderPlayers(winningPlayer):
    orderedPlayers = []
    if winningPlayer == "P1": orderedPlayers = ["P1","P2", "P3", "P4"]
    elif winningPlayer == "P2": orderedPlayers = ["P2","P3", "P4", "P1"]
    elif winningPlayer == "P3": orderedPlayers = ["P3","P4", "P1", "P2"]
    elif winningPlayer == "P4": orderedPlayers = ["P4","P1", "P2", "P3"]
    else : orderedPlayers = ["P1","P2", "P3", "P4"]
    return orderedPlayers

def countWins(winningPlayer, winCounts):
    if winningPlayer == "P1": winCounts['P1'] += 1
    elif winningPlayer == "P2": winCounts['P2'] += 1
    elif winningPlayer == "P3": winCounts['P3'] += 1
    else: winCounts['P4'] += 1

    return winCounts

def getBestCardForSuite(graveyard, playerCard, suit):
    filteredCard = [x for x in playerCard if x[0] == suit]
    filteredGraveyard = [x for x in graveyard if x[0] == suit]
    cardToPlay = None
    highestCard = True

    if filteredCard:
        filteredCard.sort(key=lambda c:cardOrder.index(c[1:]))
        bestCardInSuit = filteredCard[-1]
        worstCardInSuite = filteredCard[0]
        filteredGraveyard.sort(key=lambda c:cardOrder.index(c[1:]))
        higherCardInGraveyard = True

        # If a card higher than your card is not in the graveyard, play your lowest card
        for x in range(int(bestCardInSuit[1:])+1, 15):
            if x in filteredGraveyard:
                continue
            else:
                higherCardInGraveyard = False
                break

        if higherCardInGraveyard : 
            cardToPlay = bestCardInSuit
            highestCard = True
        else: 
            highestCard = False
            cardToPlay = worstCardInSuite
    else:
        cardToPlay = None
        highestCard = False

    return cardToPlay, highestCard


def getBestCard(graveyard, player, currentPile, trumpsuit, potentialWins, winCount, currentPlayer):
    discardPile = graveyard + currentPile
    currentBestCard = None
    currentLowestCard = None
    cardToPlay = None
    
    roundSuit = None
    if currentPile:
            roundSuit = currentPile[0][0]   

    if potentialWins[currentPlayer] == winCount[currentPlayer]:
        # if the current player has completed making his round wins this suit, don't try to win any more rounds (e.g. try to play lowest card)

        # if there is a round suit, play worst card of suit

        roundSuitCards = [x for x in player if x[0] == roundSuit]
        roundTrumpCards = [x for x in player if x[0] == trumpsuit]
        higherTrumpOnField = False
        if roundSuitCards:
            # if current pile exists, then play your highest card lower than than highest card in the current pile
            roundSuitCards.sort(key=lambda c:cardOrder.index(c[1:]))

            currentPileFiltered = [x for x in currentPile if x[0] == roundSuit]
            currentPileFiltered.sort(key=lambda c:cardOrder.index(c[1:]))

            for currentPileCard in currentPileFiltered:
                for roundSuitCard in roundSuitCards:
                    if roundSuitCard[1:] < currentPileCard[1:]:
                        currentLowestCard = roundSuitCard

            cardToPlay = currentLowestCard

        elif not roundSuitCards and trumpsuit in currentPile and roundTrumpCards and currentPile:
            # if there is a trump suit in the current pile, play a your highest lower trump
            roundTrumpCards.sort(key=lambda c:cardOrder.index(c[1:]))

            trumpsInPile = [x for x in currentPile if x[0] == trumpsuit]
            trumpsInPile.sort(key=lambda c:cardOrder.index(c[1:]))

            for highestTrump in trumpsInPile:
                '''TO DO'''
                pass

        elif not roundSuitCards and not roundTrumpCards:
            '''TO DO '''
        else:
            # if starting the round, play lowest card in hand
            worstSuitCards = []
            hCards = [x for x in player if x[0] == 'H']
            hCards.sort(key=lambda c:cardOrder.index(c[1:]))
            worstSuitCards.append(hCards[0])
            sCards = [x for x in player if x[0] == 'S']
            sCards.sort(key=lambda c:cardOrder.index(c[1:]))
            worstSuitCards.append(sCards[0])
            dCards = [x for x in player if x[0] == 'D']
            dCards.sort(key=lambda c:cardOrder.index(c[1:]))
            worstSuitCards.append(dCards[0])
            cCards = [x for x in player if x[0] == 'C']
            cCards.sort(key=lambda c:cardOrder.index(c[1:]))
            worstSuitCards.append(cCards[0])

            currentLowestCard = random.choice(worstSuitCards)

        cardToPlay = currentLowestCard

    else:
   

        if not roundSuit:
            # Find best card in hand and see if its larger than highest unknown card
            
            randomCardList = []

            # Get the best or worst card for each suit
            hCard, hHighest = getBestCardForSuite(graveyard, player, 'H')
            if hCard : randomCardList.append(hCard)
            sCard, sHighest = getBestCardForSuite(graveyard, player, 'S')
            if sCard : randomCardList.append(sCard)
            dCard, dHighest = getBestCardForSuite(graveyard, player, 'D')
            if dCard : randomCardList.append(dCard)
            cCard, cHighest = getBestCardForSuite(graveyard, player, 'C')
            if cCard : randomCardList.append(cCard)
            
            cardToPlay = None

            # If the player has the best card of the suit, play it, else play a random card
            if hHighest :
                cardToPlay = hCard
            elif sHighest :
                cardToPlay = sCard
            elif dHighest :
                cardToPlay = dCard
            elif cHighest :
                cardToPlay = cCard
            else :
                cardToPlay = random.choice(randomCardList)
            
        elif roundSuit:
            filteredCards = [x for x in player if x[0] == roundSuit]

            if not filteredCards:
                trumpCardsInHand = [x for x in player if x[0] == trumpsuit]
                trumpCardsInHand.sort(key=lambda c:cardOrder.index(c[1:]))

                filteredTrumpCardsInPile = [x for x in currentPile if x[0] == trumpsuit]
                filteredTrumpCardsInPile.sort(key=lambda c:cardOrder.index(c[1:]))
                
                if filteredTrumpCardsInPile:
                    highestTrumpInPile = filteredTrumpCardsInPile[-1]
                    for x in trumpCardsInHand:
                        if int(x[1:]) > int(highestTrumpInPile[1:]):
                            cardToPlay = x

                if not cardToPlay: 
                    tempCards = [x for x in player if x not in trumpCardsInHand]
                    if tempCards:
                        cardToPlay = tempCards[0]
                    else:
                        cardToPlay = trumpCardsInHand[0]
            else: 

                # When to play your highest card
                # all cards higher than your best card are in the graveyard
                # all unknown cards are lower than your best card
                
                allCardListSuit = []
                for x in range(lowestNumber, 15):
                    allCardListSuit.append(roundSuit+str(x))

                #print(f"Filtered Unsorted Cards: {filteredCards}")
                filteredCards.sort(key=lambda c:cardOrder.index(c[1:]))
                #print(f"Filtered Sorted Cards: {filteredCards}")
                currentLowestCard = filteredCards[0]
                currentBestCard = filteredCards[-1]
                
                #print(f"Current Best and Worst Card: {currentBestCard}, {currentLowestCard}")
                if graveyard :
                    graveyardFiltered = [x for x in graveyard if x[0] == roundSuit]
                    graveyardFiltered.sort(key=lambda c:cardOrder.index(c[1:]))
                else :
                    graveyardFiltered = []
                
                higherUnknownCard = False
                # if any of the unknown cards are higher than your best card then play lowest card
                unKnownCardsInSuit = [x for x in allCardListSuit if x not in graveyardFiltered]
                for x in unKnownCardsInSuit:
                    if int(x[1:]) > int(currentBestCard[1:]):
                        higherUnknownCard = True
                        break

                higherCardInGraveyard = True
                # if all cards higher than your best card are in the graveyard then play your highest card
                for x in range(int(currentBestCard[1:])+1, 15):
                    if x in graveyardFiltered:
                        continue
                    else:
                        higherCardInGraveyard = False
                        break
                
                higherCardInPile = False
                # if any card in the current pile is greater than your best card then play your lowest card            
                currentPileFiltered = [x for x in currentPile if x[0] == roundSuit]
                for x in currentPileFiltered:
                    if int(x[1:]) > int(currentBestCard[1:]):
                        higherCardInPile = True
                        break

                trumpInCurrentPile = False
                if trumpsuit in currentPile:
                    trumpInCurrentPile = True

                #print(f"Graveyard Pile: {graveyard}")
                #print(f"Current Pile: {currentPile}")

                higherThanCardInPile = False
                # if you are the last player to play, and all cards in current pile lower than your cards then get your lowest card higher than current pile of the same suit
                if len(currentPile) == playerCount - 1:
                    highestCardInCurrentPile = "N1"
                    for x in currentPileFiltered:
                        if int(x[1:]) > int(highestCardInCurrentPile[1:]):
                            highestCardInCurrentPile = x

                    for x in filteredCards:
                        if int(x[1:]) > int(highestCardInCurrentPile[1:]): 
                            cardToPlay = x
                            higherThanCardInPile = True
                            break

                # remember to combine higherCardInGraveyard boolean with current pile boolean as well
                
                if higherThanCardInPile and not trumpInCurrentPile:
                    pass
                elif (higherCardInGraveyard or not graveyardFiltered) and not higherCardInPile and not higherUnknownCard and not trumpInCurrentPile:
                    cardToPlay = currentBestCard
                else: 
                    cardToPlay = currentLowestCard

        #print(f"Card to Play: {cardToPlay}")
    return cardToPlay

def calculatePotentialRoundWins(player, trumpSuit, currentTotal):
    potentialWins = 0
    for card in player:
        if '13' in card or '14' in card or card[0] == trumpSuit:
            potentialWins += 1
    
    if potentialWins > 0 :
        potentialWins -= 1

    if currentTotal + potentialWins == 10:
        if potentialWins == 0:
            potentialWins += 1
        else:
            potentialWins -= 1

    currentTotal = currentTotal + potentialWins

    return potentialWins, currentTotal

def main():

    trumpSuit = ["H","S","D","C","N"]
    trumpSuit = ["H"]
    for trump in trumpSuit:
    
        deck = createDeck()
        deck = shuffleDeck(deck)
        graveyard = []
        #print(f"Deck: {deck}")

        players = {"P1":[],"P2":[], "P3":[], "P4":[]}
        dealCards(players, deck)
        print(f"Player Cards: {players}")
        
        winningPlayer = None
        orderedPlayers = orderPlayers(winningPlayer)
        winCount = {"P1":0,"P2":0, "P3":0, "P4":0}
        currentTotal = 0
        potentialWinsP1, currentTotal = calculatePotentialRoundWins(players['P1'],trumpSuit, currentTotal)
        potentialWinsP2, currentTotal = calculatePotentialRoundWins(players['P2'],trumpSuit, currentTotal)
        potentialWinsP3, currentTotal = calculatePotentialRoundWins(players['P3'],trumpSuit, currentTotal)
        potentialWinsP4, currentTotal = calculatePotentialRoundWins(players['P4'],trumpSuit, currentTotal)

        potentialWins = {"P1":potentialWinsP1,"P2":potentialWinsP2, "P3":potentialWinsP3, "P4":potentialWinsP4}

    '''
        for x in range(10):
            print(f"Round: {x+1}")
            graveyard, winningPlayer = playRound(players,orderedPlayers, graveyard, trump, potentialWins, winCount)
            orderedPlayers = orderPlayers(winningPlayer)
            winCount = countWins(winningPlayer, winCount)
            #print(f"Round Winner: {winningPlayer}")
    
        print(f"Wins: {winCount}")
    '''

if __name__ == "__main__":
    main()