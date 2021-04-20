'''

Author: Rahul Mondal
Language: Python
Last Updated: 27th March, 2021

User Keys:
    
    1. Press SPACE to start the Game
    2. Press 0 or ESCAPE QUIT to Quit the Game
    3. Press 2 or Key Up to move the Snake 🐍 Upwards
    4. Press 8 or Key Up to move the Snake 🐍 Downwards
    5. Press 4 or Key Left to move The Snake 🐍 Left
    6. Press 6 or Key Right to move the Snake 🐍 Right
    7. There is two cheat code which is hidden *** 😜

What's new:
    
    1. You can enable child mode for children 😊
    2. There is a special mode for my friend Kaushik.
       (His requirement was not to die if Snake 🐍 collided with itself 😂)
    3. There is a new cheat code which is hidden*** 😜

'''

# Importing Modules
import pygame
from pygame.locals import *
from time import sleep
import random
import os

# Window size
Width = 720 # Screen Width
Height = 1280 # Screen Height

# Game Variables
SIZE = 40
FPS = 144

# Colours
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
blue = (170,220,250)
semi_white = (200,200,200)
light_pink = (246, 205, 230)

"Changeable Game Files"
'⏹️Game '
# Background
bgi_path = 'resources/images/background/'

bgi = 'bgi.jpg'
bgi2 = 'remaining/flr.jpg'

# Music Files
musics_path = 'resources/musics/'

bgm = 'bg_music.mp3'
ding_m = 'ding.mp3'
crash_m = 'crash.mp3'
scr_bgm = 'ratsasan.mp3'
scary_m = 'scary.mp3'
gameover_m = 'gameover.mp3'

# Scary images
scr_img_path = 'resources/images/scr_imgs/'

scr_img = 'scr.jpg'
scr_img2 = 'scr2.jpg'
mimi = 'remaining/mimi.jpg'

# HighScore text File
hiscr_path = 'resources/text_file/'

hiscr = 'highscore.txt'

# Sounds
sound_effects_path = 'resources/musics/sound_effects/'

s1 = 's1.mp3'
s2 = 's2.mp3'
s3 = 's3.mp3'
s4 = 's4.mp3'
s5 = 's5.mp3'
s6 = 's6.mp3'
s7 = 's7.mp3'

# Game modes
kaushik_mode = False
child_mode = False

def random_int(type):
    return random.randint(1,int((type/SIZE)-1))*SIZE

class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        food_path = 'resources/images/food/'
        apple_img = 'cut_head.jpg'
        img = pygame.image.load(food_path+apple_img)
        self.image = pygame.transform.scale(img, (SIZE, SIZE)).convert_alpha()
        
        self.x = random_int(wight)
        self.y = random_int(height)

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random_int(wight)
        self.y = random_int(height)

    # It is a cheat code Function
    def near_snake(self, snake_x, snake_y, snake_direction):
        
        if snake_x - (SIZE*3) != 0 and snake_direction == 'left':
            self.x = snake_x - (SIZE*2)
            self.y = snake_y
        
        elif snake_x + (SIZE*3) != Widht and snake_direction == 'right':
            self.x = snake_x + (SIZE*2)
            self.y = snake_y
        
        elif snake_y - (SIZE*3) != 0 and snake_direction == 'up':
            self.x = snake_x
            self.y = snake_y - (SIZE*2)
        
        elif snake_y + (SIZE*3) != Height and snake_direction == 'down':
            self.x = snake_x
            self.y = snake_y + (SIZE*2)
            
        self.draw()

# Game Snake 🐍 object
class Snake:      
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        
        # Loading Files
        self.load_heads()
        self.load_body()
        
        # Defining starting direction of Snake 🐍
        self.direction = None
        # Defining Snake 🐍 length
        self.length = 1
        
        # Making list for Snake 🐍 body and position
        self.x = [40] # List for 'X' axis
        self.y = [40] # List for 'Y' axis
        
        # Exciting random position for Snake 🐍 object
        self.x[0] = random_int(wight)
        self.y[0] = random_int(height)
        
        # Importing Snake 🐍 Head with the below function
        self.initial_head()
        
        # Defining Game starting Score & High Score
        self.score = 0
        self.highscore = self.open_hiscore()
        
    def load_heads(self):
        head_path = 'resources/images/snake/all_heads/'
        head_l = 'head_L.jpg'
        head_r = 'head_R.jpg'
        head_u = 'head_U.jpg'
        head_d = 'head_D.jpg'
        
        heads_names = [head_l,head_r,head_u,head_d]
        heads = []
        
        # Loading Heads
        for head in heads_names:
            head_file = pygame.image.load(head_path+head)
            resized_head = pygame.transform.scale(head_file, (SIZE, SIZE)).convert_alpha()
            heads.append(resized_head)
        
        # Types of Snake 🐍 Heads 
        self.h_L = heads[0]
        self.h_R = heads[1]
        self.h_U = heads[2]
        self.h_D = heads[3]

    def load_body(self):
        # Importing Snake 🐍 body
        body_path = 'resources/images/snake/body/'
        body = 'body.jpg'
        self.body = pygame.image.load(body_path+s_body).convert()

    # Defining for Snake 🐍 Game starting Head type
    def initial_head(self):
        # Starting Head if Snake 🐍 is at Left side
        if self.x[0] >= (wight/2):
            return self.h_L  
        # Starting Head if Snake 🐍 is at Right side
        if self.x[0] <= (wight/2):
            return self.h_R

    # Defining Function to move Snake 🐍 Left direction
    def move_left(self):
        self.direction = 'left'
        if child_mode:
            self.x[0] -= SIZE
        self.rotate_head()

    # Defining Function to move Snake 🐍 Right direction
    def move_right(self):
        self.direction = 'right'
        if child_mode:
            self.x[0] += SIZE
        self.rotate_head()

    # Defining Function to move Snake 🐍 Up direction
    def move_up(self):
        self.direction = 'up'
        if child_mode:
           self.y[0] -= SIZE
        self.rotate_head()

    # Defining Function to move Snake 🐍 Down direction
    def move_down(self):
        self.direction = 'down'
        if child_mode:
            self.y[0] += SIZE
        self.rotate_head()

    # Defining Function to rotate Snake 🐍 Head
    def rotate_head(self):
        # Defining condition to display Head turned to the Left direction
        if self.direction == 'left':
            self.head = self.h_L
            
        # Defining condition to display Head turned to the Right direction
        elif self.direction == 'right':
            self.head = self.h_R
            
        # Defining condition to display Head turned to the Up direction
        elif self.direction == 'up':
            self.head = self.h_U
            
        # Defining condition to display Head turned to the Down direction
        elif self.direction == 'down':
            self.head = self.h_D
        
    # Defining Function to move the Snake 🐍 Head & body in a certain direction
    def walk(self):
        # Updating the body In stages
        for i in range(self.length-1,0,-1):
            if not child_mode:
                    self.x[i] = self.x[i-1]
                    self.y[i] = self.y[i-1]
            else:
                if self.direction == 'left':
                    self.x[i] = self.x[i-1] + SIZE
                    self.y[i] = self.y[i-1]
                    
                if self.direction == 'right':
                    self.x[i] = self.x[i-1] - SIZE
                    self.y[i] = self.y[i-1]

                if self.direction == 'up':
                    self.x[i] = self.x[i-1]
                    self.y[i] = self.y[i-1] + SIZE
                    
                if self.direction == 'down':
                    self.x[i] = self.x[i-1]
                    self.y[i] = self.y[i-1] - SIZE

        if not child_mode:
            # Updating the Snake 🐍 running direction
            if self.direction == 'left':
                self.x[0] -= SIZE # Running to the Left direction

            if self.direction == 'right':
                self.x[0] += SIZE # Running to the Right direction

            if self.direction == 'up':
                self.y[0] -= SIZE # Running Upward

            if self.direction == 'down':
                self.y[0] += SIZE # Running Downward

        self.draw() # After moving in a certain direction it draws the Snake 🐍

    # Opening High Score file to note it
    def open_hiscore(self):
        # Exciting the 'highscore.txt' text file if it doesn't exists
        if (not os.path.exists(f'{hiscr_path}{hiscr}')):
            with open(f'{hiscr_path}{hiscr}', 'w') as f:
                f.write(f'{self.score}')
        
        # Reading the 'highscore.txt' text file and returning the High Score as an Integer
        with open(f'{hiscr_path}{hiscr}') as f:
            return int(f.read()) # Returning the High Score
    
    # Drawing the Snake 🐍 Head & it's body
    def draw(self):        # Drawing Snake 🐍 body if the length is greater than One (head only)
        if self.length >= 1:
            # Running while loop to draw the full body
            for i in range(1,self.length):
                self.parent_screen.blit(self.body, (self.x[i], self.y[i]))
        # Drawing Snake 🐍 Head
        self.parent_screen.blit(self.head, (self.x[0],self.y[0]))
        pygame.display.update()
    
    # Definition to increase the Snake 🐍 length & the score also
    def increase_length(self):
        self.length += 1 # Increasing Snake 🐍 length with One new body part
        self.score += 10 # Increasing Gamer'Score with 10 points
        self.x.append(-1) # Appending a random value in the Snake 🐍 list of 'X' axis
        self.y.append(-1) # Appending a random value in the Snake 🐍 list of 'Y' axis

    # Updating The High Score with the Score if the Score is greater than the High Score
    def update_highscore(self):
        self.highscore = self.score
        with open(f'{hiscr_path}{hiscr}', 'w') as f:
                f.write(str(self.highscore))

# Defining Game Object
class Game:
    # Initial variables for Game Object
    def __init__(self):
        pygame.init() # Initialising pygame
        pygame.mixer.init() # Initialising pygame music runner

        self.surface = pygame.display.set_mode((Width, Height)) # Exciting display to Show the game to the user
        pygame.display.set_caption("Snake And Apple Game by Rahul") # Naming The Game window
        
        self.load_bgIs()
        self.setObjects()

        self.sond = None
        self.random_sound()
        
        self.welcome() # Automatically calling welcome Function to wish the user Welcome and to get command to stat the game or exit it
        
    def load_bgIs(self):
        self.bgIs = []
        bgFs = [bgi,bgi2]
        for i in bgFs:
            f = pygame.image.load(f"{bgi_path}{i}") # Loading background image
            ir = pygame.transform.scale(f, (wight, height)).convert_alpha() # Resizing the background image
            self.bgIs.append(ir)
    
    # Defining Function to play the background music
    def play_background_music(self):
        pygame.mixer.music.load(f'{musics_path}{bgm}') # Loading the background music
        pygame.mixer.music.play(-1,0) # Playbacking the background music
        pygame.mixer.Sound.play(self.sond)

    def random_sound(self):
        soundL = [s1,s2,s3,s4,s5,s6,s7]
        n = random.randint(0,6)
        self.sond = pygame.mixer.Sound(f"{sound_effects_path}{soundL[n]}")

    # Defining Function to show text on the display. The font type, text size, font color and the position to show the text is changeable here
    def show_text(self, text, font_style, text_size, colour, position):
        text = pygame.font.SysFont(font_style, text_size).render(text, True, colour)
        self.surface.blit(text, position)
        self.update_screen()
    
    # Defining Function to manage the Game FPS (Frames per Second)
    def frames(self, fps):
        pygame.time.Clock().tick(fps)
    
    # Defining Function to play a sound if the Apple 🍎 is eaten or the Snake 🐍 is collided
    def play_sound(self, sound_name):
        # Condition to play the 'crash.mp3' Sound file
        if sound_name == "crash":
            sound = pygame.mixer.Sound(f"{musics_path}{crash_m}") #resources/crash.mp3")
        
        # Condition to play the 'ding.mp3' Sound file
        elif sound_name == 'ding':
            sound = pygame.mixer.Sound(f"{musics_path}{ding_m}")

        pygame.mixer.Sound.play(sound) # Playing the Sound
    
    # Defining Function to update the Screen
    def update_screen(self):
        pygame.display.update()
    
    # Defining Function to replace the Snake 🐍 & Apple 🍎 on a random position again after Game is over
    def setObjects(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    # Defining Function to check if the Snake 🐍 is collided with own body or ate the Apple 🍎
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        else:
            return False

    # Defining Function to render the background image
    def render_background(self, bgT):
        if bgT=='light_pink':
            self.surface.fill(light_pink)
        
        elif 'bgi' in bgT:
            background_image = self.bgIs[0]
            if bgT=='bgi2':
                background_image = self.bgIs[1]
                print(str(self.bgIs[1]))
            self.surface.blit(background_image, (0,0))
            Xl = (wight/2)-100
            Yu = int((height/2)*1.5)+100

            #self.surface.blit(pygame.transform.scale(pygame.image.load(bgi_path+bgi), (200, 50)).convert_alpha(), (Xl,Yu))
        self.update_screen()

    # Defining Function to welcome the user and to make the person known the entry and Escape command
    def entry_text(self):
        # Wishing Welcome
        self.show_text(f'Welcome to Snakes', None, 90, red,(70,300))
        # Entry command
        self.show_text(f'Press Space to Play Game', 'arial', 35, white, (160,800))

    # Defining Function to check if the Snake 🐍 is gone out of the Window
    def is_snake_out(self):
        # Out than 'X' or 'Y' axis
        if self.snake.x[0]<= 0 or self.snake.y[0]<=0:
            self.play_sound('crash') # Playing 'crash.mp3' Sound which notifies that the Snake is out than 'X'or 'Y' axis
            raise "Collision Occurred" # Calling Exception and 'Game over'
        
        # Out than the screen Height or width
        if self.snake.x[0]>=wight or self.snake.y[0]>=height:
            self.play_sound('crash') # Playing 'crash.mp3' Sound which notifies that the Snake is out than the screen Height or width
            raise "Collision Occurred" # Calling Exception and 'Game over'
        
    
    # Defining Welcome Function to show the starting and to run the game forward
    def welcome(self):
        start = False # Variable to initially start the Game
        snd = pygame.mixer.Sound(f'{sound_effects_path}{s6}')
        pygame.mixer.Sound.play(snd)
        self.render_background('bgi') # Rendering background
        self.entry_text() # Showing texts in the entry point
        # Running While loop
        while not start:
            # Getting user pressed keys
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.play_background_music()
                    start = True
                    self.run() # Starting the Game
                # Conditioning the KEYDOWN user pressed key type
                if event.type == KEYDOWN:
                    # Defining action after SPACE key is pressed
                    if event.key == K_SPACE:
                        self.play_background_music()
                        self.run() # Starting the Game
                        start = True # Stopping the efficacy of the starting keys
                    if event.key == K_0 or event.key == K_ESCAPE:
                        start = True # Not starting the game, the reality is QUIT-ing the Game! 😅

                elif event.type == QUIT:
                    start = True # Not starting the game, the reality is QUIT-ing the Game! 😅
    
    # Defining the Play Function to make the game playable
    def play(self):
        self.render_background('bgi2') # Rendering the background
        self.display_score() # Displaying Score and High Score
        if child_mode:
            self.snake.draw()
        
        self.snake.walk() # Making the Snake running
        self.apple.draw() # Drawing the Apple 🍎
        self.update_screen() # Updating the screen surface

        self.is_snake_out() # Checking if the Snake 🐍 is out of the Window
        
        # Snake 🐍 eating apple condition
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding") # Playing Sound the notifies the Snake 🐍 has eaten the Apple 🍎
            self.snake.increase_length() # Increasing the Snake 🐍 Length & the Game point with 10 numbers
            self.apple.move() # Moving the Apple 🍎 on a random position
            self.update_screen()
        
        # Condition to Update the High Score and Note it
        if self.snake.score>= self.snake.highscore:
            self.snake.update_highscore() # Updating High Score
        
        if not kaushik_mode:
            # Running 'for loop' to check if Snake 🐍 has collided with itself
            for i in range(3, self.snake.length):
                if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                    self.play_sound('crash') # Playing 'crash.mp3' Sound which notifies that the Snake is Collided with itself
                    raise "Collision Occurred" # Calling Exception and 'Game over'
        
        
    # Defining Function to displace User Game Score & High Score
    def display_score(self):
        self.show_text(f"Score: {self.snake.score}", 'arial', 30, blue, (30,10))
        self.show_text(f"Highscore: {self.snake.highscore}", 'arial', 30, blue, (495,10))
    
    # Defining Function to display Game is over, user commands, Score and High Score after the 'Game over'
    def show_gameover(self):
        self.ang_mimi()
        if not child_mode:
            pass
           # self.show_scary()
            
        # Showing 'Game is over'
        self.show_text('Game is over!', None, 80, red, (50,300))
        if child_mode:
            # Showing 'Game is over'
            self.show_text('Game is over!', None, 80, blue, (50,300))
        # Showing User commands
        self.show_text('To play again press Enter', 'arial', 30, white, (50,400))
        self.show_text('To exit press 0', 'arial', 30, white, (50,450))
        
        #self.show_text(f'New High Score: {self.snake.highscore}', 'arial', 30, white, (260,700))
        # Showing User Score
        self.show_text(f'Your Score: {self.snake.score}', 'arial', 30, white, (50,700))
        # Showing User High Score
        self.show_text(f'High Score: {self.snake.highscore}', 'arial', 30, white, (460,700))
        self.update_screen()

    def ang_mimi(self):
        image = pygame.image.load(f'{scr_img_path}{mimi}')
        image = pygame.transform.scale(image,(wight, height))
        self.surface.blit(image, (0,0))

    def show_scary(self):
        pygame.mixer.music.load(f'{musics_path}{scr_bgm}')
        pygame.mixer.music.play()
        sleep(5)
        pygame.mixer.music.load(f'{musics_path}{scary_m}')
        pygame.mixer.music.play()
        sleep(1)
        image = pygame.image.load(f'{scr_img_path}{scr_img}')

        if random.randint(0,1) == 1:
            image = pygame.image.load(f'{scr_img_path}{scr_img2}')

        image = pygame.transform.scale(image,(wight, height))
        self.surface.blit(image, (0,0))
        self.update_screen()
        sleep(3)

    # Defining Function to show 'Game is over'
    def game_over(self):
        #self.render_background() # Rendering background
        pygame.mixer.music.pause() # Pausing the background music
        self.random_sound()
        pygame.mixer.Sound.play(self.sond)
        
        self.surface.fill(red)
        sleep(3)
        self.show_gameover() # Displaying Game over
    
    # Defining Function to run the Game
    def run(self):
        running = True # Initial Veriable to run the Game
        pause = False # Initial Veriable to pause the Game if 'Game is over'

        while running:
            touched = False
            # Running 'for loop' to get the User key commands
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    touched = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    touched = False
                if touched:
                    poss = pygame.mouse.get_pos()
                    X, Y = poss[0], poss[1]
                    Xl = (wight/2)-100
                    Xr = Xl + 200
                    Yu = int((height/2)*1.5)+100
                    Yd = Yu + 50
                   # if not (Y < Yu or Y > Yd):
                    if X <= Xl and (Y >= Yu-75 and Y <= Yd+75):
                            self.snake.move_left()
                    elif X >= Xr and (Y >= Yu-75 and Y <= Yd+75):
                            self.snake.move_right()
                    else:
                        if Y <= Yu:
                            self.snake.move_up()
                        elif Y >= Yd:
                            self.snake.move_down()
                if pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mixer.music.unpause()
                        pause = False
                        self.random_sound()
                        self.play_background_music()

                # Conditioning the KEYDOWN user pressed key type
                if event.type == KEYDOWN:
                    # Defining keys actions
                    if event.key == K_0 or event.key == K_ESCAPE:
                        running = False # Existing the Game
                    
                    if pause:
                        # User key to 'Run the Game' again after 'Game is over'
                        if event.key == K_RETURN:
                            pygame.mixer.music.unpause()
                            pause = False
                            self.random_sound()
                            self.play_background_music()
                    

                    # User keys when 'Game is Running'
                    if not pause:
                        if event.key == K_4 or event.key == K_LEFT:
                            self.snake.move_left() # Moveing the Snake 🐍 to the Left direction

                        if event.key == K_6 or event.key == K_RIGHT:
                            self.snake.move_right() # Moveing the Snake 🐍 to the Right direction
                        # Restarting the Game
                        if event.key == K_1:
                            self.reset()
                            
                        if device == 'phone':
                            if event.key == K_2 or event.key == K_UP:
                                self.snake.move_up() # Moveing the Snake 🐍 Upward

                            if event.key == K_8 or event.key == K_DOWN:
                                self.snake.move_down() # Moveing the Snake 🐍 Downward
                        
                        elif device == 'comp':
                        
                            if event.key == K_8 or event.key == K_UP:
                                self.snake.move_up() # Moveing the Snake 🐍 Upward

                            if event.key == K_2 or event.key == K_DOWN:
                                self.snake.move_down() # Moveing the Snake 🐍 Downward
                        
                        if not child_mode:
                            if event.key == K_9 or event.key == K_q:
                                self.apple.near_snake(self.snake.x[0], self.snake.y[0], self.snake.direction)
                            # Cheat code to increase the Snake 🐍 length & User Score
                            if event.key == K_7:
                                self.snake.increase_length() # increasing the Game Score as cheating

                # User key to QUIT the Game
                elif event.type == QUIT:
                    running = False
            try:

                # Running the Game If 'Game is not over'
                if not pause:
                    self.play() # Starts playing the Game

            # Defining Exception to
            except Exception as e:
                print(e)
                self.game_over() # Showing 'Game over'
                pause = True # Pausing the Game
                self.reset() # Replaces the Snake 🐍 & Apple 🍎 on a random position again after Game is over

            # time.sleep(.1)
            self.frames(FPS) # Managing Game FPS (Frames per Second)


'''

The Cheat codes:
    1. Press 7 to increase Your Score and the Snake 🐍 length
    2. Press q or 9 to import the Apple 🍎 near the Snake 🐍
    

'''

# Condition not to Execute the bellow codes in another programme if the Game file is imported in other programme
if __name__ == '__main__':
    Game() # Calling Game Class which automatically Displays the Game
