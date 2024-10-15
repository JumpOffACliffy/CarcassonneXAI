# receive the list of moves
# create logic to return appropriate copilot suggestion

def Copilot(Carcassonne):

    player = Carcassonne.p2
    available_moves = player.listActions(Carcassonne)
    print(f"It is player: {Carcassonne.playerSymbol}\'s turn")
    # player = Carcassonne.p1 # reset to correct player's turn

    available_meeples = Carcassonne.Meeples[0]
    print(f"Available meeples: {available_meeples}")

    bestMove = available_moves[0].Move


    # Monastery Logic
    if bestMove.MeepleInfo is not None:
        if available_meeples > 0 and bestMove.MeepleInfo[0] == 'Monastery':
            # prompt user to place a meeple on the monastery
            print('It\'s generally a good strategy to always place a meeple on a Monastery!')

    monasteryTilesRemaining = Carcassonne.TileQuantities[15] + Carcassonne.TileQuantities[20]
    # i want this to call if the user selects a meeple on the tile, and they should only be prompted once(?)
    if available_meeples < 3 and monasteryTilesRemaining > 2:
        # prompt user to consider saving a meeple for a future monastery
        print("It might be worth hanging onto a meeple in case you draw a Monastery")
