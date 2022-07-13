import Snake.game as snake
import SnakeAI.game as snakeAI
import Tetris.game as tetris

class GameClient():
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    game_over = False
    g = tetris.Game()
    while game_over == False:
        game_over = g.playStep()
    tetris.pygame.quit()
    