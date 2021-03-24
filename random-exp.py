# Add background image and music

import pygame
from pygame.locals import *
import random
import time
import os

SIZE = 40
FPS = 144
SCREEN_WIGHT = 720
SCREEN_HEIGHT = 1280
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = random.randint(1,17)*SIZE
        self.y = random.randint(1,31)*SIZE

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()

    def move(self):
        self.x = random.randint(1,17)*SIZE
        self.y = random.randint(1,31)*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.update()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        pygame.display.set_caption("Codebasics Snake And Apple Game")
        self.surface = pygame.display.set_mode((SCREEN_WIGHT, SCREEN_HEIGHT))
        
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        
        self.running = True
        self.pause = False
        
        self.tick = pygame.time.Clock().tick
        
    def text_screen(text, colour, size, text_x, text_y):
        font = pygame.font.SysFont(None, size)
        screen_text = font.render(text, True, colour)
        self.surface.blit(screen_text, [text_x,text_y])
    
    def welcome(self):
        self.render_background()
        # self.text_screen("Welcome to Snakes", (225,0,0), 80, 100, 250)
        font = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont('arial', 40)
        wish_welcome = "Welcome to Snakes"
        str_cmd = "Press Space Bar To Play"
        screentext_wish_welcome = font.render(wish_welcome, True, (225,0,0))
        screentext_str_cmd = font2.render(str_cmd, True, (255,225,225))
        self.surface.blit(screentext_wish_welcome, [200,700])
        self.surface.blit(screentext_str_cmd, [100,250])
        pygame.display.update()
        
       # Getting user Key Command
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                
                if event.key == pygame.K_9:
                    self.running = False
                
                if event.key == pygame.K_SPACE:
                     self.render_background()
                     self.play_background_music()
                     self.snake.walk()
                     self.apple.draw()
                     self.display_score()
                     self.play()
                     pygame.display.update()
    
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)
        
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        return False
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        bg = pygame.transform.scale(bg, (SCREEN_WIGHT, SCREEN_HEIGHT))
        self.surface.blit(bg, (0,0))
    
    def wish_bye(self):
        window = pygame.image.load("resources/bye.jpg")
        font = pygame.font.SysFont('arial', 90)
        window = pygame.transform.scale(window, (225, 110))
        bye = font.render(f"Bye!",True,(255,0,0))
        self.surface.blit(window,(270,520))
        self.surface.blit(bye, (300,520))
        pygame.display.update()
    
    def play(self):
        self.welcome()
        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                self.pause = True
                raise "Collision Occurred"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(200,200,200))
        self.surface.blit(score,(50,10))

    def game_over(self):
        self.render_background()
        pygame.mixer.music.pause()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type = KEYDOWN:
                if event.key == K_RETURN:
                    pygame.mixer.music.unpause()
                    self.pause = False
                    self.welcomes()
                    
                elif event.keys == K_9:
                    self.running = False
        
    def run(self):
        while self.running:
            if(not os.path.exists("hiscore.txt")):
                with open("hiscore.txt", "w") as f:
                    f.write("0")
                    
            with open("hiscore.txt", "r") as f:
                hiscore = int(f.read())
            
            if not self.pause:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_9:
                        	pygame.mixer.music.pause()
                        	self.wish_bye()
                        	pygame.time.wait(500)
                        	self.running = False
                            
                        if event.key == K_4:
                            self.snake.move_left()
                                
                        if event.key == K_6:
                            self.snake.move_right()
                                
                        if event.key == K_2:
                           	self.snake.move_up()

                        if event.key == K_8:
                            self.snake.move_down()
                            
                        #elif event.type == QUIT:
                        #	running = False
                            
                self.welcome()
            else:
                self.game_over()
            self.tick(FPS)
            #try:

#                if not pause:
#                    self.play()

#            except Exception as e:
#                self.show_game_over()
#                pause = True
#                self.re
        #    self.clock.tick(self.fps)

if __name__ == '__main__':
    game = Game()
    game.run()
    
