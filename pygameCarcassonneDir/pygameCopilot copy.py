# receive the list of moves
# create logic to return appropriate copilot suggestion

from pygameCarcassonneDir.pygameFunctions import get_logger

class Copilot:
    def __init__(self, hasBeenWarnedMonastery=False):
        self.hasBeenWarnedMonastery = hasBeenWarnedMonastery

        self.logger = get_logger()
        self.bestQsSeenSoFar = []


    def placeMeeple(self, Carcassonne):
        """
        Copilot function to determine if the player should place a meeple, and if so on which feature. 
        """
        recommendedMeeple = 'none'

        availableMoves = Carcassonne.availableMoves() # returns unsorted list of all legal moves
        availableMeeples = Carcassonne.Meeples[0] # the number of meeples the player has remaining

        if availableMeeples == 0: # short circuit if the player has no meeples remaining
            recommendedMeeple = 'no meeples left'
            return recommendedMeeple

        for move in availableMoves:
            if availableMeeples > 0 and move.MeepleInfo is not None:
                if move.MeepleInfo[0] == 'Monastery':
                    recommendedMeeple = 'monastery'
                    return recommendedMeeple # short circuit here on monastery
                    
        
        # if no monastery was found, now proceed with MCTS search for farms/cities/roads
        """
        WE NEED TO DYNAMICALLY SET Q OR ELSE THIS IS NEVER GOING TO WORK
        """
        player = Carcassonne.p2
        mctsMoves = player.listActions(Carcassonne) # returns sorted list of moves based on MCTS Q score
        bestMove = mctsMoves[0].Move
        bestMoveQ = mctsMoves[0].Q
        bestMeeple = bestMove.MeepleInfo[0] if bestMove.MeepleInfo else None #sets bestMeeple to the best meeple, or none if none
        
        for move in mctsMoves:
            print(f"Move: {move.Move}, Q: {round(move.Q, 3)}")
        
        # find the next best move that does not recommend placing a meeple
        Q_RATIO_THRESHOLD = 0.33  # Adjust the ratio threshold as needed
        Q_DIFFERENCE_THRESHOLD = 2.0  # Define a minimum difference to trigger a recommendation

        

        # Check the ratio using the correct formula
        if abs(bestMoveQ) > 0:  # Check if bestMoveQ is non-zero
            Q_ratio = abs(bestMoveQ - bestNoMeepleMoveQ) / abs(bestMoveQ)
        else:
            Q_ratio = abs(bestMoveQ - bestNoMeepleMoveQ) / 0.01  # approximate if bestMoveQ is zero

        # Also check the absolute difference between the Q scores
        Q_difference = abs(bestMoveQ - bestNoMeepleMoveQ)

        if availableMeeples > 0 and bestMove.MeepleInfo is not None: 
            bestMeeple = bestMove.MeepleInfo[0]
            if bestMeeple == 'G':
                recommendedMeeple = 'farmer'
                #print('Now would be a good time to place a farmer.')
            if bestMeeple == 'C':
                recommendedMeeple = 'city'
                #print('You should place a meeple in a city.')
            if bestMeeple == 'R':
                recommendedMeeple = 'road'
                #print('You should claim a road.')

        print(f"Q ratio: {Q_ratio}")
        print(f"Q difference: {Q_difference}")

        print(f'Copilot Recommended Meeple: {recommendedMeeple}')
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
