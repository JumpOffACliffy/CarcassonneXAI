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
        recommendedMeeple = None

        availableMoves = Carcassonne.availableMoves() # returns unsorted list of all legal moves
        availableMeeples = Carcassonne.Meeples[0] # the number of meeples the player has remaining
        #print(f"Available meeples: {availableMeeples}")

        for move in availableMoves:
            #print(f"move: {move}")
            if availableMeeples > 0 and move.MeepleInfo is not None:
                #print(f"meeple info: {move.MeepleInfo[0]}")
                if move.MeepleInfo[0] == 'Monastery':
                    recommendedMeeple = 'monastery'
                    #print('It\'s generally a good strategy to always place a meeple on a Monastery!') #this is going to print multiple times
        
        return recommendedMeeple

    def placeFarmerMeeple(self, Carcassonne):
        recommendedMeeple = None

        player = Carcassonne.p2
        mctsMoves = player.listActions(Carcassonne) # returns sorted list of moves based on MCTS Q score
        # print(f"top move: {mctsMoves[0].Move}")
        availableMeeples = Carcassonne.Meeples[0] # the number of meeples the player has remaining
        bestMove = mctsMoves[0].Move

        if availableMeeples > 0 and bestMove.MeepleInfo is not None:
            bestMeeple = bestMove.MeepleInfo[0]
            if bestMeeple == 'G':
                recommendedMeeple = 'farmer'
                print('Now would be a good time to place a farmer.')
            if bestMeeple == 'C':
                recommendedMeeple = 'city'
                print('You should place a meeple in a city.')
        
        return recommendedMeeple
    

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
                return self.hasBeenWarnedMonastery
    
