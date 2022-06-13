import pygame
import random
from enum import Enum
from collections import namedtuple

from torch import rand

pygame.init()
font = pygame.font.Font('../Assets/arial.ttf', 25)

Point = namedtuple('Point', 'x, y')

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


BLOCK_SIZE = 20
CLOCK_SPEED = 10


class Game:
    
    def __init__(self, width=640, height=480):
        self.window = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0

        self.direction = Direction.RIGHT
        self.head = Point(120,120)
        self.snake = [self.head,
                      Point(self.head.x-   BLOCK_SIZE, self.head.y), 
                      Point(self.head.x-(2*BLOCK_SIZE),self.head.y)]


        self.w = width
        self.h = height

        self.wall = []
        self.food = Point(0,0)
        self.place_food()
        self.run()


    def run(self):
        while self.running:
            self.clock.tick(CLOCK_SPEED)
            self.render()
            self.handle_events()
            self.update()
        pygame.quit()

    def update(self): 
        if self.is_collision():
            self.running = False
        self.move()

    def render(self):
        self.window.fill((0,0,0))

        for chunk in self.wall:
            pygame.draw.rect(self.window,(0,255,0),(chunk.x, chunk.y, BLOCK_SIZE, BLOCK_SIZE))
        for chunk in self.snake:
            pygame.draw.rect(self.window,(0,0,255),(chunk.x, chunk.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.window,(255,0,0),(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, (255,255,255))
        self.window.blit(text, [0, 0])
        
        pygame.display.update()
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

    def place_food(self):
        rx = random.randint(0,(self.w-BLOCK_SIZE)/BLOCK_SIZE)
        ry = random.randint(0,(self.h-BLOCK_SIZE)/BLOCK_SIZE)
        self.food = Point(rx * BLOCK_SIZE, ry * BLOCK_SIZE)

    def is_collision(self):
        if self.head.x > self.w - BLOCK_SIZE or self.head.y > self.h - BLOCK_SIZE or self.head.x < 0 or self.head.y < 0:
            return True
        if self.head in self.wall: 
            return True
        
        if self.head in self.snake[1:]:
            point = self.snake[1:].index(self.head)
            for i in range(len(self.snake) - point):
                out = self.snake.pop()
                if out not in self.wall:
                    self.wall.append(out)

        if self.food == self.head:
            self.snake.append(self.food)
            self.place_food()
            self.score+=1
        return False

    def move(self):
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        self.head = Point(x,y)

        self.snake.insert(0, self.head)
        self.snake.pop()



if __name__ == '__main__':
    g = Game()