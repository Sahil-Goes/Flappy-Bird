import pygame
import time
import os
import random
pygame.font.init()
pygame.init()
pygame.mixer.init()

#Load game sounds
pygame.mixer.music.load(os.path.join("music","background.wav"))
pygame.mixer.music.play(-1)  # Loop Background music
jump_sound = pygame.mixer.Sound(os.path.join("music","jump.wav"))

WIN_WIDTH = 500
WIN_HEIGHT = 800

#Loading Images
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird3.png")))
             ]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bg.png")))

TITLE_IMG = pygame.image.load(os.path.join("imgs", "title.png"))
TITLE_IMG = pygame.transform.scale(TITLE_IMG, (400, 120))  # adjust size as needed


STAT_FONT = pygame.font.SysFont("comicsans", 50)


#Bird class controls its position, movement and animation
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25    #How much bird will tilt
    ROT_VEL = 20         #Speed of rotation while falling
    ANIMATION_TIME = 5   #How fast bird will flap its wings

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5        # Jump upward (-ve since pygame uses - as up and + as down)
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        #vertical displacement
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        #terminal velocity: to keep bird movement within a broundary
        if d >= 16:
            d = 16

        if d < 0:
            d -= 2

        self.y = self.y + d

        #to ADJUST TILT: up when going up, down when falling
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    #function to display Flappy Bird images
    def draw(self,win):
        self. img_count += 1

        #cycle through bird animation frames
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS [0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # If bird is diving, keep wings in mid-flap position
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5
    def __init__(self,x):
        self.x = x
        self.height = 0
        
        #To track where pipe gap will appear on screen
        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):
        self.height = random.randrange(50,450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        
        return False
    
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
    
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        #Ground Movement: Using a 2 block method
        #If one block is off screen it repeats after other in a cycle

        if self.x1 + self.WIDTH < 0:        #If block 1 is off screen
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:        #Ifblock 2 is off screen
            self.x2 = self.x1 + self.WIDTH

    def draw(self,win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))

    #shadow effect
    shadow = STAT_FONT.render("Score: " + str(score), 1, (0,0,0))
    win.blit(shadow, (WIN_WIDTH - 10 - text.get_width() + 2, 12))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    base.draw(win)
    bird.draw(win)
    pygame.display.update()


def show_start_screen(win):
    instruction_font = pygame.font.SysFont("comicsans", 30)
    start_sound = pygame.mixer.Sound(os.path.join("music","gamestart.wav"))

    clock = pygame.time.Clock()
    blink_interval = 500
    last_blink = pygame.time.get_ticks()
    show_instruction = True

    waiting = True
    while waiting:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_sound.play()
                    waiting = False
                    
        now = pygame.time.get_ticks()
        if now - last_blink > blink_interval:
            show_instruction = not show_instruction
            last_blink = now

        win.blit(BG_IMG, (0, 0))
        win.blit(TITLE_IMG, (WIN_WIDTH / 2 - TITLE_IMG.get_width() / 2, 175))

        if show_instruction:
            instr_text = instruction_font.render("Press SPACE to Start", 1, (255, 255, 255))
            win.blit(instr_text, (WIN_WIDTH / 2 - instr_text.get_width() / 2, 400))

        pygame.display.update()



def show_game_over(win, score):
    game_over_font = pygame.font.SysFont("comicsans", 70)
    restart_font = pygame.font.SysFont("comicsans", 30)

    gameover_sound = pygame.mixer.Sound(os.path.join("music","gameover.wav"))
    gameover_sound.play()

    text = game_over_font.render("Game Over", 1, (255, 0, 0))
    score_text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))

    waiting = True
    clock = pygame.time.Clock()
    blink_interval = 500  # ms
    last_blink = pygame.time.get_ticks()
    show_restart = True

    while waiting:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                    return

        now = pygame.time.get_ticks()
        if now - last_blink > blink_interval:
            show_restart = not show_restart
            last_blink = now

        win.blit(BG_IMG, (0, 0))
        win.blit(text, (WIN_WIDTH / 2 - text.get_width() / 2, 200))
        win.blit(score_text, (WIN_WIDTH / 2 - score_text.get_width() / 2, 300))

        if show_restart:
            restart_text = restart_font.render("Press R to Restart", 1, (255, 255, 255))
            win.blit(restart_text, (WIN_WIDTH / 2 - restart_text.get_width() / 2, 400))

        pygame.display.update()


#Main Game Loop
def main():
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    show_start_screen(win)

    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0
    run = True
    game_active = False  # Bird won't move until first spacebar press

    while run:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_active:
                        game_active = True  # Starts game on first space
                    bird.jump()
                    jump_sound.play()

        if game_active:
            bird.move()

            add_pipe = False
            rem = []
            for pipe in pipes:
                if pipe.collide(bird):
                    run = False  # Ends game on collision

                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    rem.append(pipe)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(600))

            for r in rem:
                pipes.remove(r)

            # Bird hit ground or flew off top
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                run = False  

            base.move()
        draw_window(win, bird, pipes, base, score)

    # Game over screen
    show_game_over(win, score)

main()        