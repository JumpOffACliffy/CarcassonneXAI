# receive the list of moves
# create logic to return appropriate copilot suggestion

from pygameCarcassonneDir.pygameFunctions import get_logger

class Copilot:
    def __init__(self, hasBeenWarnedMonastery=False):
        self.hasBeenWarnedMonastery = hasBeenWarnedMonastery

        self.logger = get_logger()
        self.recommendationsGiven = 0


    def placeMeeple(self, Carcassonne):
        """
        Copilot function to determine if the player should place a meeple, and if so on which feature. 
        """
        recommendedMeeple = 'none'

        availableMoves = Carcassonne.availableMoves()  # returns unsorted list of all legal moves
        availableMeeples = Carcassonne.Meeples[0]  # the number of meeples the player has remaining

        if availableMeeples == 0:  # short circuit if the player has no meeples remaining
            recommendedMeeple = 'no meeples left'
            return recommendedMeeple

        for move in availableMoves:
            if availableMeeples > 0 and move.MeepleInfo is not None:
                if move.MeepleInfo[0] == 'Monastery':
                    recommendedMeeple = 'monastery'
                    return recommendedMeeple  # short circuit here on monastery

        # Proceed with MCTS search for farms/cities/roads
        player = Carcassonne.p2
        mctsMoves = player.listActions(Carcassonne)  # returns sorted list of moves based on MCTS Q score
        bestMove = mctsMoves[0].Move
        bestMoveQ = mctsMoves[0].Q
        bestMeeple = bestMove.MeepleInfo[0] if bestMove.MeepleInfo else None  # sets bestMeeple to the best move's meeple, or None

        for move in mctsMoves:
            print(f"Move: {move.Move}, Q: {round(move.Q, 3)}")
            self.logger.info(f"Move: {move.Move}, Q: {round(move.Q, 3)}")

        # Find the next best move that does not involve placing a meeple
        bestNoMeepleMoveQ = None
        for move in mctsMoves[1:]:
            if move.Move.MeepleInfo is None:  # No meeple placement
                bestNoMeepleMoveQ = move.Q
                break

        if bestNoMeepleMoveQ is None:
            return recommendedMeeple  # This should never happen since there is always a move without a meeple

        # Use both magnitude and difference of Q scores for comparison
        Q_RATIO_THRESHOLD = 0.33  # Adjust the ratio threshold as needed
        Q_DIFFERENCE_THRESHOLD = 2.0  # Define a minimum difference to trigger a recommendation

        # Dynamic adjustment based on current game state
        targetRecommendations = 7
        totalTurns = 35  # Assuming each player plays 35 turns
        turnsPassed = (Carcassonne.Turn // 2)  # Convert to individual player turns

        expectedRecommendationsSoFar = (turnsPassed / totalTurns) * targetRecommendations
        shortfall = expectedRecommendationsSoFar - self.recommendationsGiven

        # Adjust thresholds dynamically
        if shortfall > 0:  # Need to make more recommendations
            Q_RATIO_THRESHOLD -= shortfall * 0.03  # Decrease the ratio threshold to be more lenient
            Q_DIFFERENCE_THRESHOLD -= shortfall * 0.2  # Decrease the difference threshold
        elif shortfall < 0:  # Already ahead on recommendations
            Q_RATIO_THRESHOLD += abs(shortfall) * 0.03  # Increase the ratio threshold to be stricter
            Q_DIFFERENCE_THRESHOLD += abs(shortfall) * 0.2  # Increase the difference threshold

        # Ensure bestMoveQ is never exactly zero for the calculation
        if abs(bestMoveQ) == 0:
            bestMoveQ = 0.01

        # Calculate the ratio |A - B| / |A| where A is bestMoveQ and B is bestNoMeepleMoveQ
        Q_ratio = abs(bestMoveQ - bestNoMeepleMoveQ) / abs(bestMoveQ)

        # Also check the absolute difference between the Q scores
        Q_difference = abs(bestMoveQ - bestNoMeepleMoveQ)

        # Recommend only if both the ratio AND difference exceed their respective thresholds
        if (Q_ratio >= Q_RATIO_THRESHOLD and Q_difference >= Q_DIFFERENCE_THRESHOLD) and bestMove.MeepleInfo is not None:
            if bestMeeple == 'G':
                recommendedMeeple = 'farmer'
            elif bestMeeple == 'C':
                recommendedMeeple = 'city'
            elif bestMeeple == 'R':
                recommendedMeeple = 'road'

        # Log and return the recommendation
        print(f'Copilot Best Q: {round(bestMoveQ, 3)}')
        print(f'Copilot Recommended Meeple: {recommendedMeeple}')
        print(f'Best No Meeple Q: {round(bestNoMeepleMoveQ, 3)}')
        print(f"Q ratio: {Q_ratio}")
        print(f"Q difference: {Q_difference}")
        
        # self.logger.info(bestMoveQ)

        self.logger.info(f'Copilot Best Q: {round(bestMoveQ, 3)}')
        self.logger.info(f'Best No Meeple Q: {round(bestNoMeepleMoveQ, 3)}')
        self.logger.info(f"Q ratio: {Q_ratio}")
        self.logger.info(f"Q difference: {Q_difference}")
        self.logger.info(f'Copilot Recommended Meeple: {recommendedMeeple}')

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
