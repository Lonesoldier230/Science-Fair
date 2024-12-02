from typing import Any
import pygame
import numpy as np

class Button():
    def __init__(self, img, pos:tuple,scale:float=1) -> None:
        self.img = img
        self.position = tuple(map(int, pos))
        self.resize = pygame.transform.scale(img, (img.get_width()//scale, img.get_height()//scale))
        
    def update(self, screen):
        screen.blit(self.resize, self.position)
    
    def IsPressed(self, mouse_pos:tuple):
        mouse_pos = list(map(int, mouse_pos))
        if mouse_pos[0] in range(self.position[0], self.position[0]+self.resize.get_width()) and mouse_pos[1] in range(self.position[1], self.position[1]+self.resize.get_height()):
            return True
        return False
    
class Storage():
    def __init__(self) -> None:
        try:
            self.data = np.load("./storage/data.npy")
        except:
            self.data = False
        self.h_score = 0
        self.score = 0
        self.player = ""
    
    def record(self, score:int):
        if type(self.data) == bool:
            if self.data == False:
                self.data = np.array([[self.player, score]])
        else:
            self.data = np.append(self.data, [[self.player, self.score]], axis=0)
            
    def save(self):
        np.save("./storage/data.npy", self.data)
        
    def reset(self):
        self.score = 0
            
    @property
    def high_score(self):
        try:
            self.h_score = np.max(np.uint32(self.data[:,1]))
        except:
            pass
        return self.h_score