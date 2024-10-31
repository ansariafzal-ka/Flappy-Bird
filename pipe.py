import pygame
from constants import PIPE_GAP, SCROLL_SPEED

class Pipe(pygame.sprite.Sprite):
    
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/pipe.png")
        self.rect = self.image.get_rect()
        
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(PIPE_GAP / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(PIPE_GAP / 2)]
            
    def update(self):
        self.rect.x -= SCROLL_SPEED
        if self.rect.right < 0:
            self.kill()
            