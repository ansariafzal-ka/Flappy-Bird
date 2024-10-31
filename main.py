import pygame
from pygame.locals import *
from constants import *
from bird import Bird
from pipe import Pipe
from button import Button
import random

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

bg = pygame.image.load('img/bg.png')
ground_img = pygame.image.load("img/ground.png")
ground_scroll = 0

bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(60, int(SCREEN_HEIGHT / 2))
bird_group.add(flappy)

game_over = False
last_pipe = pygame.time.get_ticks()

pass_pipe = False
score = 0

button_img = pygame.image.load("img/restart.png")


font = pygame.font.SysFont("Bauhaus 93", 50)
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color)
    screen.blit(img, (x, y))
    
    
def reset_game():
    global score
    pipe_group.empty()
    flappy.rect.x = 60
    flappy.rect.y = int(SCREEN_HEIGHT / 2)
    score = 0
    
button = Button(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2 - 60, button_img)

run = True
while run:
    clock.tick(FPS)
    
    screen.blit(bg, (0, 0))
    
    pipe_group.draw(screen)
    
    bird_group.draw(screen)
    bird_group.update(game_over)
    
    
    screen.blit(ground_img, (ground_scroll, 461))
    
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right and pass_pipe is False:
            pass_pipe = True
        if pass_pipe is True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
                
                
    draw_text(str(score), font, WHITE, int(SCREEN_WIDTH / 2), 15)
    
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        game_over = True

    if flappy.rect.bottom >= 461:
        game_over = True
        flappy.flying = False
        
    if not game_over and flappy.flying is True:
        
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > PIPE_FREQUENCY:
            pipe_height = random.randint(-60, 60)
            top_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, -1)
            btm_pipe = Pipe(SCREEN_WIDTH, int(SCREEN_HEIGHT / 2) + pipe_height, 1)
            pipe_group.add(top_pipe)
            pipe_group.add(btm_pipe)
            last_pipe = time_now
            
        ground_scroll -= SCROLL_SPEED
        if abs(ground_scroll) > 21:
            ground_scroll = 0
        pipe_group.update()
        
    if game_over is True:
        if button.draw(screen) is True:
            game_over = False
            reset_game()

    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not flappy.flying and not game_over:
            flappy.flying = True
            
    pygame.display.update()
            
pygame.quit()
