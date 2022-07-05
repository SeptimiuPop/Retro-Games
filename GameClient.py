import Snake.game as snake
import SnakeAI.game as snakeAI

class GameClient():
    def __init__(self) -> None:
        pass

if __name__ == '__main__':
    game_over = False
    g = snake.Game()
    while game_over == False:
        game_over = g.playStep()
    snake.pygame.quit()
    