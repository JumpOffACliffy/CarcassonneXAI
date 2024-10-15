# receive the list of moves
# create logic to return appropriate copilot suggestion

from pygameCarcassonneDir.pygameFunctions import get_logger

class Copilot:
    def __init__(self, hasBeenWarnedMonastery=False):
        self.hasBeenWarnedMonastery = hasBeenWarnedMonastery

        self.logger = get_logger()


    def placeMonasteryMeeple(self, Carcassonne):
        """
        Do I turn this into a mega function with all promptings? 
        We shall see...
        """
        player = Carcassonne.p2

        print(f"It is player {Carcassonne.playerSymbol}\'s turn")
        # self.logger.info(f"It is player: {Carcassonne.playerSymbol}\'s turn")
        available_moves = player.listActions(Carcassonne)
        # player = Carcassonne.p1 # reset to correct player's turn

        # for move in available_moves:
        #     self.logger.info(f"Move: {move.Move}, Q: {round(move.Q, 3)}")
        #     print(f"(copilot) Move: {move.Move}, Q: {round(move.Q, 3)}")

        available_meeples = Carcassonne.Meeples[0]
        #print(f"Available meeples: {available_meeples}")

        bestMove = available_moves[0].Move
        if bestMove.MeepleInfo is not None:
            if available_meeples > 0 and bestMove.MeepleInfo[0] == 'Monastery':
                # prompt user to place a meeple on the monastery
                print('It\'s generally a good strategy to always place a meeple on a Monastery!')

    def placeFarmerMeeple(self, Carcassonne):
        player = Carcassonne.p2
        available_moves = player.listActions(Carcassonne)
        
        available_meeples = Carcassonne.Meeples[0]


    def saveMeepleForMonastery(self, Carcassonne, tileIndex):
        """
        Prompts the player to save their meeples for a future monastery. 
        Will only prompt the player once per game.
        Procs if they are looking to place a meeple and only have 2 left, and there are 2 or more monasteries left in the deck. 
        """
        if not self.hasBeenWarnedMonastery:
            monasteryTilesRemaining = Carcassonne.TileQuantities[15] + Carcassonne.TileQuantities[20]
            available_meeples = Carcassonne.Meeples[0]

            if available_meeples <= 2 and monasteryTilesRemaining >= 2 and tileIndex != 15 and tileIndex != 20:
                # prompt user to consider saving a meeple for a future monastery
                print("It might be worth hanging onto a meeple in case you draw a Monastery")
                self.hasBeenWarnedMonastery = True
    
