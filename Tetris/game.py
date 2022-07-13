from enum import Enum
import pygame
import random


from Snake.game import BLOCK_SIZE


pygame.init()
font = pygame.font.Font('./Assets/arial.ttf', 25)

CLOCK_SPEED = 30
BLOCK_SPEED = 5
BLOCK_SIZE = 20


COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)

class Blocks(Enum):
    L =[[1,0,0],
        [1,0,0],
        [1,1,0]]

    B =[[1,1],
        [1,1]]

    Z =[[1,1,0],
        [0,1,1]]

    I =[[0,1,0],
        [0,1,0],
        [0,1,0]]

    T = [[1,1,1],
         [0,1,0]] 



class Game:

    def __init__(self, width=200, height=480):
        self.window = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()

        self.GAME_OVER = False
        self.w = width
        self.h = height

        self.descend_clock = 0
        self.is_descending = False
        self.piece = Blocks.I
        self.x = 0
        self.y = 0


    def playStep(self):

        self.clock.tick(CLOCK_SPEED)
        self.descend_clock += 1

        self._render()
        self._handle_events()
        
        if self.is_descending or (self.descend_clock % 20 == 0):
            self.descend_clock = 0
            self._descend()

        return self.GAME_OVER


    def _render(self):
        self.window.fill((0,0,0))
        pygame.draw.rect(self.window, COLOR_BLUE,(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.window, COLOR_RED,(self.x+3, self.y+3, BLOCK_SIZE-6, BLOCK_SIZE-6))

        # text = font.render("Score: " + str(0), True, (255,255,255))
        # self.window.blit(text, [0, 0])
        
        pygame.display.update()
    
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.GAME_OVER = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.GAME_OVER = True
                if event.key == pygame.K_DOWN:
                    self.is_descending = True
                if event.key == pygame.K_LEFT:
                    self._move_left()
                if event.key == pygame.K_RIGHT:
                    self._move_right()
                if event.key == pygame.K_r:
                    self._rotate()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.is_descending = False
                 

    def _move_left(self):
        if self.x - BLOCK_SIZE >= 0:
            self.x -= BLOCK_SIZE

    def _move_right(self):
        if self.x + BLOCK_SIZE < self.w:
            self.x += BLOCK_SIZE
    
    def _rotate(self):
        fig = [
        [1,3,5,7], # I
        [2,4,5,7], # Z
        [3,5,4,6], # S
        [3,5,4,7], # T
        [2,3,5,7], # L
        [3,5,7,6], # J
        [2,3,4,5], # O
        ]
        for i in range(7):
            print()
            for j in range(4):
                print(fig[i][j]%2, fig[i][j]/2)

        pass

    def _descend(self):
        if self.y + BLOCK_SIZE < self.h:
            self.y += BLOCK_SIZE