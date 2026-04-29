import sys
import pygame
import random
import sqlite3

class Drive:
    def __init__(self, a, c, d):
        self.image = pygame.image.load(a)
        self.rect = self.image.get_rect()
        self.rect.x = c
        self.rect.y = d

    def move_car(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= 35
        if keys[pygame.K_d]:
            self.rect.x += 35

    def draw_image(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def move_down(self):
        self.rect.y += 20

# ЗАГРУЗКА ОБЪЕКТОВ
pygame.init()  # Включаем pygame (окно, картинки, клавиши)
pygame.mixer.init()  # Включаем звуки и музыку

# звуки
pygame.mixer.music.load("music_game.mp3")
game_over_sound = pygame.mixer.Sound("sound_game_over.mp3")
crystal_sound = pygame.mixer.Sound("crystal_sound.mp3")
car_sound = pygame.mixer.Sound("car_sound.mp3")

# настройка громкости
pygame.mixer.music.set_volume(0.5)  # фоновая музыка на 50%
game_over_sound.set_volume(0.8)  # авария на 80%
crystal_sound.set_volume(0.8)  # сбор кристаллов на 80%
car_sound.set_volume(0.3)  # двигатель на 30%

# картинки
bg1 = Drive('road.png', 0, 0)
bg2 = Drive('road.png', 0, -760)
car = Drive('c_car.png', 400, 650)
crystal = Drive('crystal.png', 0, 0)
obstacle = Drive('obstacle.png', 0, 0)
canister = Drive('canister.png', 0, 0)
menu_img = pygame.image.load('road.png')  # для меню

# окно
window_size=(900, 760) # ширина / высота
win = pygame.display.set_mode(window_size)  # создание экрана
pygame.display.set_caption("Crystal Drive")  # заголовок окна
clock = pygame.time.Clock()  # для FPS (контроль скорости)

# переменные
score = 0  # общий счёт на главном экране
fuel = 100  # топливо
crystals = []
obstacles = []
canisters = []
game_over = False

# бд для рекорда
conn = sqlite3.connect("my_score.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS records (score INT)")
conn.commit()
c.execute("SELECT MAX(score) FROM records")
best = c.fetchone()[0]
if best is None:
    best = 0

pygame.mixer.music.play(-1)  # зацикливаем музыку

# ГЛАВНЫЙ ЦИКЛ
while True:
    #  ГЛАВНОЕ МЕНЮ
    menu = True
    button = pygame.Rect(370, 350, 160, 50)
    font = pygame.font.Font(None, 50)
    text = font.render("ИГРАТЬ", True, (255, 255, 255))
    record_font = pygame.font.Font(None, 70)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    menu = False

        win.blit(menu_img, (0, 0))
        pygame.draw.rect(win, (128, 0, 255), button)
        win.blit(text, (385, 360))
        record_text = record_font.render(f"МОЙ РЕКОРД: {best}", True, (255, 255, 255))
        win.blit(record_text, (270, 150))
        pygame.display.flip()
        clock.tick(60)

    #  СБРОС ПЕРЕД ИГРОЙ
    score = 0
    fuel = 100
    car.rect.x = 400
    crystals = []
    obstacles = []
    canisters = []
    game_over = False
    ct = ob = cn = 0

    #  ИГРА
    while True:
        clock.tick(60)

        # движение фона
        bg1.rect.y += 3
        bg2.rect.y += 3
        if bg1.rect.y >= 760:
            bg1.rect.y = bg2.rect.y - 760
        if bg2.rect.y >= 760:
            bg2.rect.y = bg1.rect.y - 760

        # звук двигателя
        if not game_over and fuel > 0:
            car_sound.play(-1)
        else:
            car_sound.stop()

        # движение машинки
        car.move_car()
        if car.rect.x < 50:
            car.rect.x = 50
        if car.rect.x > 850:
            car.rect.x = 850

        # бензин
        if not game_over:
            fuel -= 0.2
            if fuel <= 0:
                game_over = True
                game_over_sound.play()
                car_sound.stop()

        # спавн объектов
        if not game_over:
            ct += 1
            if ct > 25:
                ct = 0
                crystals.append(Drive('crystal.png', random.randint(20, 840), -50))

            ob += 1
            if ob > 50:
                ob = 0
                obstacles.append(Drive('obstacle.png', random.randint(20, 840), -50))

            cn += 1
            if cn > 100:
                cn = 0
                canisters.append(Drive('canister.png', random.randint(20, 840), -50))

        # движение объектов
        for i in crystals: i.move_down()
        for j in obstacles: j.move_down()
        for k in canisters: k.move_down()

        # удаление
        crystals = [i for i in crystals if i.rect.y < 760]
        obstacles = [j for j in obstacles if j.rect.y < 760]
        canisters = [k for k in canisters if k.rect.y < 760]

        # столкновения
        car_rect = car.rect

        for i in crystals[:]:
            if car_rect.colliderect(i.rect):
                crystals.remove(i)
                score += 1
                crystal_sound.play()

        for j in obstacles[:]:
            if car_rect.colliderect(j.rect):
                game_over = True
                game_over_sound.play()
                car_sound.stop()

        for k in canisters[:]:
            if car_rect.colliderect(k.rect):
                canisters.remove(k)
                fuel += 20
                if fuel > 100: fuel = 100

        # отрисовка
        bg1.draw_image()
        bg2.draw_image()
        for i in crystals: i.draw_image()
        for j in obstacles: j.draw_image()
        for k in canisters: k.draw_image()
        car.draw_image()

        # текст
        f = pygame.font.Font(None, 40)
        win.blit(f.render(f"СЧЁТ: {score}", 1, (255, 255, 255)), (10, 10))
        win.blit(f.render(f"БЕНЗИН: {int(fuel)}", 1, (0, 255, 0)), (10, 50))

        # GAME OVER - выход в меню
        if game_over:
            go_text = pygame.font.Font(None, 70).render("GAME OVER", True, (255, 0, 0))
            win.blit(go_text, (385, 350))
            pygame.display.flip()
            pygame.time.wait(1000)  # ждём секунду
            break  # выходим из игры в меню

        # сохраняем рекорд
        if score > best:
            best = score
            c.execute("INSERT INTO records VALUES (?)", (score,))
            conn.commit()

        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()