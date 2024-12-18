import pygame
import cv2 as cv
import numpy as np
import random

import pygame.locals
from modules.ML_video import VRS
import sys
from modules.utilities import Button, Storage

pygame.init()

SCREEN_HEIGHT = 1080/2
SCREEN_WIDTH = 1920/2
BIRD_X = SCREEN_HEIGHT/2
BUILDING = pygame.image.load("./resources/game/building1.png")
BIRD_IMG = pygame.transform.scale(pygame.image.load("./resources/game/airplane.png"), (48,29))
PIPE_GAP = 150
PIPE_WIDTH = 70
PIPE_SPEED = -4
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
data = Storage()

class Bird:
    def __init__(self):
        self.x = BIRD_X
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.image = BIRD_IMG

    def update(self, x:int=BIRD_X, y:int=SCREEN_HEIGHT//2):
        self.x = x
        self.y = y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())

class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.passed = False

    def update(self):
        self.x += PIPE_SPEED - self.difficulty

    def draw(self):
        screen.blit(pygame.transform.scale(BUILDING, (PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)), (self.x, self.height + PIPE_GAP))
        screen.blit(pygame.transform.scale(pygame.transform.flip(BUILDING, 0, 1), (PIPE_WIDTH, self.height)), (self.x, 0))

    def get_upper_rect(self):
        return pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)

    def get_lower_rect(self):
        return pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)
    
    @property
    def difficulty(self):
        return data.score/10
    
def MainMenu():
    global data
    clock = pygame.time.Clock()
    running = True
    place_holder = ""
    high_score = f"High Score: {data.high_score}"
    
    bg_img = pygame.image.load("./resources/mainmenu/main_menu.jpg")
    new_game = Button(pygame.image.load("./resources/mainmenu/new_game.png"), ((SCREEN_WIDTH/2)+50, (SCREEN_HEIGHT/2)+50), scale=3, hover_img=pygame.image.load("./resources/mainmenu/new_game_highlighted.png"))
    quit_game = Button(pygame.image.load("./resources/mainmenu/quit_game.png"), ((SCREEN_WIDTH/2)-50 - (new_game.img.get_width()//3), (SCREEN_HEIGHT/2)+50), scale=3, hover_img=pygame.image.load("./resources/mainmenu/quit_game_highlighted.png"))
    highest_score_text = pygame.font.SysFont("Arial", 45)
    highest_score = highest_score_text.render(str(high_score), True, (255, 255, 255))
    Name_font = pygame.font.SysFont("Arial", 50)
    
    while running:
        pos = pygame.mouse.get_pos()
        
        new_game.hover(pos)
        quit_game.hover(pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                data.save()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    try:
                        place_holder = place_holder[:-1]
                    except IndexError:
                        pass
                elif event.key == pygame.K_RETURN:
                    if place_holder != "":
                        Game()
                else:
                    place_holder += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_game.IsPressed(pos):
                    if place_holder != "":
                        Game()
                if quit_game.IsPressed(pos):
                    running = False
                    data.save()
                    
        data.player = place_holder
        Name_text = Name_font.render(place_holder, True, (255,255,255))
        
        screen.blit(pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
                
        pygame.draw.rect(screen, (255,255,255), (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2 - 30, 500, 60) , 2, 10)
        screen.blit(Name_text, (SCREEN_WIDTH//2-245, SCREEN_HEIGHT//2 - 25))
        screen.blit(highest_score, (SCREEN_WIDTH//2-len(str(high_score))*12+10, SCREEN_HEIGHT//2 - 79))
        new_game.update(screen=screen)
        quit_game.update(screen=screen)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

def GameOver():
    global data
    clock = pygame.time.Clock()
    running = True
    
    new = Button(pygame.image.load("./resources/gameover/New.png"),((SCREEN_WIDTH/2)+50, (SCREEN_HEIGHT/2)+50) , scale=3, hover_img=pygame.image.load("./resources/gameover/New_highlight.png"))
    qui = Button(pygame.image.load("./resources/gameover/Quit.png"), ((SCREEN_WIDTH/2)-50 - (new.img.get_width()//3), (SCREEN_HEIGHT/2)+50), scale=3, hover_img=pygame.image.load("./resources/gameover/Quit_highlight.png"))
    score_font = pygame.font.SysFont("Arial", 40)
    score_text = score_font.render(str(data.score),True, (14, 165, 218))
    bg_img = pygame.image.load("./resources/gameover/gameover_bg.jpeg")
    font = pygame.font.SysFont("Arial", 80)
    text = font.render("Game Over", True, (255, 255, 255))
    
    while running:
        mouse_pos = pygame.mouse.get_pos()

        new.hover(mouse_pos=mouse_pos)
        qui.hover(mouse_pos=mouse_pos)
        
        screen.blit(pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data.save()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if new.IsPressed(mouse_pos=mouse_pos):
                    Game()
                if qui.IsPressed(mouse_pos=mouse_pos):
                    MainMenu()
        
        screen.blit(score_text, ((SCREEN_WIDTH/2)-(len(str(data.score))*20) + 10, (SCREEN_HEIGHT/2)-70))
        screen.blit(text, ((SCREEN_WIDTH/2)-(len("Game Over")*45/2) - 5, (SCREEN_HEIGHT/2)-40))
        new.update(screen=screen)
        qui.update(screen=screen)
        
        pygame.display.flip()
        clock.tick(60)
        
    

def Game():
    vr = VRS("./ML_algorithm/yolov11n-face.pt", scale=0.25)
    cap = cv.VideoCapture(0)
    global data
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = [Pipe(SCREEN_WIDTH + 200)]
    running = True
    data.reset()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                data.save()
                pygame.quit()
                sys.exit()
        suc, fram = cap.read()
        vr.predict(fram, img_flip=True, device="mps")
        img = cv.cvtColor(vr.img, cv.COLOR_BGR2RGB)
        pyimg = pygame.transform.smoothscale(pygame.image.frombuffer(img.tobytes(),(img.shape[1], img.shape[0]), "RGB"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(pyimg, (0,0))

        try:
            m_coords = vr.mid_coords[:1][0]
            
            bird.update(m_coords[0]*2, m_coords[1]*2)
            print(bird.x, bird.y)
        except:
            bird.update(bird.x, bird.y)

        for pipe in pipes:
            pipe.update()

            if bird.get_rect().colliderect(pipe.get_upper_rect()) or bird.get_rect().colliderect(pipe.get_lower_rect()):
                running = False

            if pipe.x + PIPE_WIDTH < bird.x and not pipe.passed:
                pipe.passed = True
                data.score += 1
                print(f"Score: {data.score}")

        if pipes[-1].x < SCREEN_WIDTH - 200:
            pipes.append(Pipe(SCREEN_WIDTH))


        pipes = [pipe for pipe in pipes if pipe.x + PIPE_WIDTH > 0]

        if bird.y > SCREEN_HEIGHT or bird.y < 0:
            running = False


        bird.draw()
        for pipe in pipes:
            pipe.draw()

        font = pygame.font.SysFont("Arial", 24)
        score_text = font.render(f"Score: {data.score}", True, (0,0,0))
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(FPS)
        
    data.record(data.score)
    print(data.data)
    cap.release()
    GameOver()
    

if __name__ == "__main__":
    MainMenu()