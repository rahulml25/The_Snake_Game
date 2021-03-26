 
# Add background image and music

import pygame
from pygame.locals import *
import random
import time
import os

SIZE = 40
FPS = 144
BACKGROUND_COLOR = (110, 110, 5)
wight = 720
height = 840

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(1,((wight/SIZE)-1))*SIZE
        self.y = random.randint(1,((height/SIZE)-1))*SIZE

class Snake:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.image = pygame.image.load("resources/block.jpg").convert()
        self.direction = 'stay'

        self.length = 1
        self.x = [40]
        self.y = [40]
        
        self.score = self.length - 1
        self.highscore = self.open_hiscore()
        
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
        if self.direction == 'stay':
            self.x[0] = SIZE
            self.y[0] = SIZE

        self.draw()

    def open_hiscore(self):
        if (not os.path.exists('resources/highscore.txt')):
            with open('resources/highscore.txt', 'w') as f:
                f.write(f'{self.score}')
        
        with open('resources/highscore.txt') as f:
            return int(f.read())
    
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

        pygame.display.flip()

    def showhi(self):
        font = pygame.font.SysFont(None, 90)
        he = font.render(f"{self.highscore}",True,(255,0,0))
        self.parent_screen.blit(he,(70,300))
        
    
    def increase_length(self):
        self.length += 1
        self.score += 10
        self.x.append(-1)
        self.y.append(-1)

    def update_highscore(self):
        self.highscore = self.score

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        pygame.display.set_caption("Codebasics Snake And Apple Game")
        self.surface = pygame.display.set_mode((wight, height))
        
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        
        self.welcome()
        
    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play(-1, 0)

    def show_text(self, text, font, text_size, colour, position):
        text = pygame.font.SysFont(font, text_size).render(text, True, colour)
        self.surface.blit(text, position)
        self.screen_update()
    
    def frames(self, FPS):
        pygame.time.Clock().tick(FPS)
    
    def play_sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("resources/crash.mp3")
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound("resources/ding.mp3")

        pygame.mixer.Sound.play(sound)
    
    def screen_update(self):
        pygame.display.flip()
    
    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        bg = pygame.transform.scale(bg, (wight, height)).convert_alpha()
        self.surface.blit(bg, (0,0))
        self.screen_update()

    def entry_text(self):
        self.show_text(f'Welcome to Snakes', None, 90, (255,0,0),(70,300))
        self.show_text(f'Press Enter to Play Game', 'arial', 35, (255,255,255), (160,800))

    def welcome(self):
        start = False
        # self.surface.fill((246, 205, 230))
        self.render_background()
        self.entry_text()
        pygame.display.flip()
        while not start:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.play_background_music()
                        self.run()
                        start = True
                    if event.key == K_0:
                        start = True

    def play(self):
        self.surface.fill((0,0,0))
        self.render_background()
        self.display_score()
        # self.snake.showhi()
        self.snake.walk()
        self.apple.draw()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()
        
        if self.snake.x[0]<= 0 or self.snake.y[0]<0:
            self.play_sound('crash')
            raise "Collision Occurred"
        
        if self.snake.x[0]>= wight or self.snake.y[0]>height:
            self.play_sound('crash')
            raise "Collision Occurred"
        
        if self.snake.score>= self.snake.highscore:
            self.snake.update_highscore()
            with open('resources/highscore.txt', 'w') as f:
                f.write(str(self.snake.highscore))
        
        # snake colliding with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                raise "Collision Occurred"
        
    def display_score(self):
        self.show_text(f"Score: {self.snake.score}  Highscore: {self.snake.highscore}", 'arial', 30, (200,200,200), (50,10))
    
    def show_gameover(self):
        self.show_text('Game is over!', None, 80, (255,0,0), (50,300))
        self.show_text('To play again press Enter', 'arial', 30, (255,255,255), (50,400))
        self.show_text('To exit press 0', 'arial', 30, (255,255,255), (50,450))
        self.show_text(f'Your Score: {self.snake.score}', 'arial', 30, (255,255,255), (50,700))
        self.show_text(f'High Score: {self.snake.highscore}', 'arial', 30, (255,255,255), (480,700))

    def game_over(self):
        self.render_background()
        pygame.mixer.music.pause()
        self.show_gameover()
        pygame.display.flip()
    
    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_0:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if event.key == K_SPACE:
                        running = False
                        pygame.mixer.music.stop()
                        self.welcome()


                    if not pause:
                        if event.key == K_4:
                            self.snake.move_left()

                        if event.key == K_6:
                            self.snake.move_right()

                        if event.key == K_2:
                            self.snake.move_up()

                        if event.key == K_8:
                            self.snake.move_down()

                        if event.key == K_7:
                            self.snake.increase_length()
                            pygame.display.flip()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()

            # time.sleep(.1)
            self.frames(FPS)

if __name__ == '__main__':
    Game()
