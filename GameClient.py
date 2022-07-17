import Snake.game as snake
import SnakeAI.game as snakeAI
import Tetris.game as tetris

class GameClient():
    def __init__(self) -> None:
        pass

def select_game():
    game_chosen = input("Select the game you want to play:\n1)Snake\n2)Tetris\n")

    if game_chosen == "1":
        return snake.Game() 
    elif game_chosen == "2":
        return tetris.Game() 
    else: 
        return tetris.Game() 
    

if __name__ == '__main__':
    print("\n\n---------------------------------------------\n\n")
    game_over = False
    quit = False
    game = select_game()

    while game_over == False:
        game_over = game.playStep()

        
    