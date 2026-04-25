import sys
import pygame
from random import *

class Drive:  # создаём класс
    def __init__(self, a, c, d): #конструктор, в нём  создаются свойства, вызывается при создании объекта
        self.image = pygame.image.load(a) # self.image - свойство
        self.rect = self.image.get_rect() # self.rect - свойство объекта, прямоугольник
        self.rect.x = c # self.x - свойство объекта
        self.rect.y = d #self.y - свойство объекта

    def move_car(self):  # метод движения машинки
        keys = pygame.key.get_pressed()
        if keys[pygame.K_A] == True:
            self.rect.x -= 35
        if keys[pygame.K_D]:
            self.rect.x += 35

    def draw_image(self): # метод отрисовки
        win.blit(self.image, (self.rect.x , self.rect.y))

    def move_objects(self):  # метод движения объектов
        self.rect.y += 15

background = Drive('background.png', 0, 0)  # создание объекта класса Drive
crystal = Drive(".png", 60, randint(-100,0))

window_size=(900, 760) # ширина / высота
win = pygame.display.set_mode(window_size)  # создание экрана
pygame.display.set_caption("Crystal Drive")  # заголовок окна
clock = pygame.time.Clock()  # для FPS (контроль скорости)

# главный игровой цикл (пока True - игра работает)
while True:
    clock.tick(60)  # 60 кадров в секунду
    background.draw_image()  # отрисовка фона

    for event in pygame.event.get():  # обработка событий
        if event.type == pygame.QUIT:  # если нажали на крестик - выйти из игры
            sys.exit()