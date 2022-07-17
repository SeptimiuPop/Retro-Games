from enum import Enum
import pygame
import random
from collections import namedtuple


pygame.init()
font = pygame.font.Font('./Assets/arial.ttf', 25)

Point = namedtuple('Point', 'x, y')

CLOCK_SPEED = 30
BLOCK_SIZE = 20


COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)

fig = [ [1,3,5,7], # I
        [2,4,5,7], # Z
        [3,5,4,6], # Z'
        [3,5,4,7], # T
        [2,3,5,7], # L
        [3,5,7,6], # L'
        [2,3,4,5]] # O



class Game:

    def __init__(self, width=200, height=480):
        self.window = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()

        self.BLOCK_SPEED = 20
        self.GAME_OVER = False
        self.score = 0 
        self.w = width
        self.h = height

        self.board_h = int(self.h/BLOCK_SIZE)
        self.board_w = int(self.w/BLOCK_SIZE)

        self.descend_clock = 0
        self.speed_clock = 0
        self.is_descending = False
        
        self.placed_blocks = {}
        for i in range(self.board_h):
            self.placed_blocks[i] = []

        self._gen_shape()
        


    def playStep(self):

        self.clock.tick(CLOCK_SPEED)
        self.descend_clock += 1
        self.speed_clock += 1


        self._render()
        self._handle_events()
        
        if self.is_descending or (self.descend_clock % self.BLOCK_SPEED == 0):
            self.descend_clock = 0
            self._move(0,1,0)

        if self.BLOCK_SPEED > 5 and self.speed_clock % 1000 == 0:
            self.speed_clock = 0
            self.BLOCK_SPEED -= 1

        return self.GAME_OVER


    def _render(self):
        self.window.fill((0,0,0))

        for point in self.shape:
            pygame.draw.rect(self.window, COLOR_RED,(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.window, COLOR_GREEN,(point.x+3, point.y+3, BLOCK_SIZE-6, BLOCK_SIZE-6))

        for i in range(self.board_h):
            for point in self.placed_blocks[i]:
                pygame.draw.rect(self.window, COLOR_RED,(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(self.window, COLOR_GREEN,(point.x+3, point.y+3, BLOCK_SIZE-6, BLOCK_SIZE-6))

        text = font.render("Score: " + str(self.score), True, (255,255,255))
        self.window.blit(text, [0, 0])
        
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
                    self._move(1,0,-1)
                if event.key == pygame.K_RIGHT:
                    self._move(1,0,1)
                if event.key == pygame.K_UP:
                    self._rotate()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    self.is_descending = False
                 

    def _gen_shape(self):
        self.shape = []
        n = random.randint(0,6)
        for i in range(4): 
            x = int(fig[n][i] % 2) * BLOCK_SIZE + self.w/2
            y = int(fig[n][i] / 2) * BLOCK_SIZE + 0
            self.shape.append(Point(x,y))
            if Point(x,y) in self.placed_blocks[int(y/BLOCK_SIZE)]:
                self.GAME_OVER = True
            

    def _move(self, dx, dy, direction):
        tmp = []
        for i in range(4):
            x = self.shape[i].x + BLOCK_SIZE * dx * direction
            y = self.shape[i].y + BLOCK_SIZE * dy

            tmp.append(Point(x,y))
            if self._is_colision(x,y,direction): 
                return
        self.shape = tmp

    
    def _rotate(self):
        tmp = []
        pivot=self.shape[1]
        for i in range(4):
            # Translate points to pos (0,0) relative to the pivot
            x = self.shape[i].x - pivot.x
            y = self.shape[i].y - pivot.y

            # Rotate by 90* and translate back to original position
            newX = x*0 - y*1 + pivot.x
            newY = x*1 + y*0 + pivot.y

            tmp.append(Point(newX, newY))
            if self._is_colision(newX,newY,1):
                return
        self.shape = tmp
        

    def _is_colision(self, x, y, flag):
        
        # if moving sideways or rotating
        if flag:    
            if x < 0 or x >= self.w or Point(x,y) in self.placed_blocks[int(y/BLOCK_SIZE)]:
                return True
        
        # if moving down
        else:           
            if y >= self.h or Point(x,y) in self.placed_blocks[int(y/BLOCK_SIZE)]:
                for shape in self.shape:
                    index = int(shape.y / BLOCK_SIZE)
                    self.placed_blocks[index].append(shape)
                self._gen_shape()
                self._clear_placed_line()
                return True
        
        return False


    def _clear_placed_line(self):   
        ind = []
        for i in range(self.board_h):
            if len(self.placed_blocks[i]) >= self.board_w:
                ind.append(i)

        multiplyer = len(ind)
        self.score += 100*multiplyer * multiplyer

        for i in ind:
            for j in range(i,0,-1):
                tmp = []
                for block in self.placed_blocks[j-1]:
                    tmp.append(Point(block.x, block.y + BLOCK_SIZE))
                self.placed_blocks[j] = tmp