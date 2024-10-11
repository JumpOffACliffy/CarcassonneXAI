import sys
import os
import pygame

# add 'Carcassonne' directory to sys.path
sys.path.append(os.path.join(os.getcwd()))
print(sys.path)
print(os.getcwd())

# import local scripts
from player.Player import HumanPlayer, RandomPlayer
from player.MCTS_Player import MCTSPlayer
from player.MCTS_RAVE_Player import MCTS_RAVEPlayer
from player.MCTS_ES_Player import MCTS_ES_Player
from player.Star1_Player import Star1
from player.Star2_5_Player import Star2_5

from Carcassonne_Game.Carcassonne import CarcassonneState
from Carcassonne_Game.Tile import Tile

from pygameCarcassonneDir.pygameNextTile import nextTile
from pygameCarcassonneDir.pygameFunctions import (
    playMove,
    setup_logging
)


# list of player available to choose from
PLAYERS = [
    ("Human", HumanPlayer()),
    ("Random", RandomPlayer()),
    ("MCTS", MCTSPlayer(isTimeLimited=False, timeLimit=5)),
    ("RAVE", MCTS_RAVEPlayer(isTimeLimited=True, timeLimit=5)),
]

PLAYER1 = [HumanPlayer()]
PLAYER2 = [HumanPlayer()]

AI_MOVE_EVENT = pygame.USEREVENT + 1
AI_DELAY = 1000  # ms


# main game loop without any display logic
def PlayGame(p1, p2):
    global CLOCK
    pygame.init()
    CLOCK = pygame.time.Clock()
    
    Carcassonne = CarcassonneState(p1, p2)
    NT = nextTile(Carcassonne, None, RunInit=False)  # No display passed here
    done = False
    player = Carcassonne.p1
    isGameOver = False
    isStartOfGame = isStartOfTurn = hasSomethingNew = True
    selectedMove = [16, 0, 0, 0, None]
    rotation = 0
    newRotation = False
    numberSelected = 0

    if player.isAIPlayer:
        pygame.time.set_timer(AI_MOVE_EVENT, AI_DELAY)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not isGameOver:
                if player.isAIPlayer and event.type == AI_MOVE_EVENT:
                    player, selectedMove = playMove(
                        NT,
                        player,
                        Carcassonne,
                        NT.nextTileIndex,
                        isStartOfGame,
                        ManualMove=None,
                    )
                    NT = nextTile(Carcassonne, None, RunInit=False)  # No display
                    isStartOfTurn = True
                    hasSomethingNew = True
                    isStartOfGame = False
                    isGameOver = Carcassonne.isGameOver
                    if isGameOver:
                        pygame.time.set_timer(AI_MOVE_EVENT, 0)
                    else:
                        pygame.time.wait(AI_DELAY)
                        break
                else:
                    # Handle human player input (can simulate this if needed)
                    pass

        if isGameOver:
            logger.info(f'Winner - Player: {Carcassonne.winner}')
            logger.info(f'Scores - Player 1: {Carcassonne.Scores[0]}, Player 2: {Carcassonne.Scores[1]}')
            print(f"Winner: Player {Carcassonne.winner}, Scores:  P1: {Carcassonne.Scores[0]} - P2: {Carcassonne.Scores[1]}")
            done = True

        CLOCK.tick(60)


if __name__ == "__main__":
    for i in range(2):  # Run the game X times
        print(f"Starting game {i+1}")
        logger = setup_logging()
        p1 = MCTSPlayer(isTimeLimited=True, timeLimit=1)
        p2 = MCTSPlayer(isTimeLimited=True, timeLimit=1)
        # p1 = RandomPlayer()
        # p2 = RandomPlayer()
        PlayGame(p1, p2)
        print(f"Finished game {i+1}")
