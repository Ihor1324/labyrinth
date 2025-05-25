from pygame import *  # Імпортуємо всі модулі з бібліотеки pygame
import pygame
from moviepy.editor import VideoFileClip
import numpy as np
import sys


pygame.init()
pygame.mixer.init()


def show_intro(screen, win_width, win_height):
    pygame.font.init()
    font_title = pygame.font.SysFont("arial", 50)
    font_text = pygame.font.SysFont("arial", 30)
    BLACK = (0, 0, 0)
    BLUE = (255, 255, 255)

    intro = True
    while intro:
        screen.fill(BLUE)

        title_text = font_title.render("Вітаємо в грі!", True, BLACK)
        rules = [
            "Правила гри:",
            "- Рухайтеся за допомогою стрілок.",
            "- Стріляй натиснувши на пробіл",
            "- Збирайте всі монети, як справжній мисливець за скарбами.",
            "- Уникайте привидів — вони не фанати дружби.",
            "- Знайдіть фініш, але тільки після збору монет!",
            "- Стіну фіналу відкриє тільки повна колекція зірок.",
            "",
            "Порада: я не раджу знищувати привидів.",
            "Натисніть ПРОБІЛ, щоб вирушити в пригоду..."
        ]

        screen.blit(title_text, (win_width // 2 - title_text.get_width() // 2, 50))
        for i, line in enumerate(rules):
            line_surface = font_text.render(line, True, BLACK)
            screen.blit(line_surface, (60, 150 + i * 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False

        pygame.display.flip()
        pygame.time.Clock().tick(60)



# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):  # Наслідуємо клас Sprite
    def __init__(self, player_image, player_x, player_y, size_x, size_y):  # Конструктор класу з параметрами
        sprite.Sprite.__init__(self)  # Ініціалізуємо батьківський клас

        self.image = transform.scale(image.load(player_image), (size_x, size_y))  # Завантажуємо зображення та змінюємо його розмір
        self.rect = self.image.get_rect()  # Отримуємо прямокутник для позиціювання
        self.rect.x = player_x  # Задаємо координату X
        self.rect.y = player_y  # Задаємо координату Y

    def reset(self):  # Метод для відображення спрайта на екрані
        window.blit(self.image, (self.rect.x, self.rect.y))  # Малюємо спрайт у заданій позиції

# клас головного гравця
class Player(GameSprite):  # Наслідуємо GameSprite
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):  # Конструктор з додатковими параметрами швидкості
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)  # Викликаємо конструктор батьківського класу
        self.x_speed = player_x_speed  # Горизонтальна швидкість
        self.y_speed = player_y_speed  # Вертикальна швидкість

    def update(self):  # Метод руху гравця з урахуванням зіткнень
        # Рух по X
        if packman.rect.x <= win_width - 80 and packman.x_speed > 0 or packman.rect.x >= 0 and packman.x_speed < 0:
            self.rect.x += self.x_speed  # Змінюємо координату X

        platforms_touched = sprite.spritecollide(self, barriers, False)  # Перевіряємо зіткнення з перешкодами
        if self.x_speed > 0:  # Рух праворуч
            for p in platforms_touched:
                self.rect.right = p.rect.left
        elif self.x_speed < 0:  # Рух ліворуч
            for p in platforms_touched:
                self.rect.left = p.rect.right

        # Рух по Y
        if packman.rect.y <= win_height - 80 and packman.y_speed > 0 or packman.rect.y >= 0 and packman.y_speed < 0:
            self.rect.y += self.y_speed  # Змінюємо координату Y

        platforms_touched = sprite.spritecollide(self, barriers, False)  # Знову перевіряємо зіткнення
        if self.y_speed > 0:  # Вниз
            for p in platforms_touched:
                self.rect.bottom = p.rect.top
        elif self.y_speed < 0:  # Вгору
            for p in platforms_touched:
                self.rect.top = p.rect.bottom


    def fire(self):  # Метод стрільби
        bullet = Bullet('bullet.png', self.rect.centerx + 10, self.rect.top + 10, 15, 20, 15)  # Створюємо кулю
        bullets.add(bullet)  # Додаємо її до групи куль

# Клас ворога, що рухається по горизонталі
class Enemy_h(GameSprite):
    side = "left"  # Початковий напрямок
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, x1, x2):  # Конструктор
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)  # Ініціалізуємо спрайт
        self.speed = player_speed  # Швидкість руху
        self.x1 = x1  # Ліва межа руху
        self.x2 = x2  # Права межа руху

    def update(self):  # Метод руху ворога
        if self.rect.x <= self.x1:  # Якщо дійшли до лівої межі
            self.side = "right"  # Змінюємо напрямок
        if self.rect.x >= self.x2:  # Якщо дійшли до правої межі
            self.side = "left"
        if self.side == "left":  # Рух вліво
            self.rect.x -= self.speed
        else:  # Рух вправо
            self.rect.x += self.speed

# Клас ворога, що рухається вертикально
class Enemy_v(GameSprite):
    side = "up"
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed, y1, y2):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.y1 = y1
        self.y2 = y2

    def update(self):
        if self.rect.y <= self.y1:
            self.side = "down"
        if self.rect.y >= self.y2:
            self.side = "up"
        if self.side == "up":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

# Клас кулі
class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        GameSprite.__init__(self, player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed

    def update(self):  # Рух кулі
        self.rect.x += self.speed  # Рух праворуч
        if self.rect.x > win_width + 10:  # Якщо за межами екрану
            self.kill()  # Видаляємо кулю


class star(GameSprite):
    pass

class decor(GameSprite):
    pass





# Розміри вікна
win_width = 1080
win_height = 720
window = display.set_mode((win_width, win_height))  # Створюємо вікно
display.set_caption("No Way Out")  # Заголовок
back = transform.scale(image.load("background.jpg"), (win_width, win_height))  # Фонове зображення

# Ініціалізація Pygame
pygame.init()

# Завантаження відео (перемога)
win_clip = VideoFileClip('thumb_video.mp4').subclip(0, 3.6)  # Відео для виграшу

# Завантаження відео (програш)
lose_clip = VideoFileClip('game _over.mp4').subclip(0, 3.6)  # Відео для програшу


barriers = sprite.Group()  # Група для перешкод
bullets = sprite.Group()   # Група для куль
monsters = sprite.Group()  # Група ворогів
coin = sprite.Group()      
coins = sprite.Group()


# Створення стін
#   x, y, width, height
#   'wall.png' — зображення стіни
#   x — координата по горизонталі (ліва межа)
#   y — координата по вертикалі (верхня межа)
#   width — ширина стіни
#   height — висота стіни (її товщина по вертикалі, якщо вона горизонтальна) 
w1 = GameSprite('wall.png', 0, 252, 126, 36)
w2 = GameSprite('wall.png', 0, 360, 126, 36)
w3 = GameSprite('wall.png', 90, 0, 36, 288)
w4 = GameSprite('wall.png', 90, 360, 36, 360)
w5 = GameSprite('wall.png', 198, 108, 36, 180)
w6 = GameSprite('wall.png', 90, 468, 144, 36)
w7 = GameSprite('wall.png', 198, 108, 144, 36)
w8 = GameSprite('wall.png', 198, 360, 144, 36)
w9 = GameSprite('wall.png', 198, 576, 144, 36)
w10 = GameSprite('wall.png', 306, 108, 36, 180)
w11 = GameSprite('wall.png', 306, 360, 36, 360)
w12 = GameSprite('wall.png', 306, 252, 144, 36)
w13 = GameSprite('wall.png', 414, 0, 36, 180)
w14 = GameSprite('wall.png', 414, 252, 36, 360)
w15 = GameSprite('wall.png', 414, 360, 252, 36)
w16 = GameSprite('wall.png', 414, 468, 144, 36)
w17 = GameSprite('wall.png', 414, 576, 144, 36)
w18 = GameSprite('wall.png', 522, 0, 36, 180)
w19 = GameSprite('wall.png', 522, 252, 36, 144)
w20 = GameSprite('wall.png', 522, 252, 144, 36)
w21 = GameSprite('wall.png', 630, 108, 36, 612)
w22 = GameSprite('wall.png', 630, 468, 252, 36)
w23 = GameSprite('wall.png', 738, 144, 144, 36)
w24 = GameSprite('wall.png', 738, 252, 144, 36)
w25 = GameSprite('wall.png', 738, 252, 36, 144)
w26 = GameSprite('wall.png', 846, 144, 36, 360)
w27 = GameSprite('wall.png', 738, 576, 342, 36)
w28 = GameSprite('wall.png', 954, 0, 36, 612)
w29 = GameSprite('wall.png', 90, 0, 900, 36)
w30 = GameSprite('wall.png', 90, 684, 990, 36)
w31 = GameSprite('wall.png', 954, 576, 36, 144)

barriers.add(w1)  # Додаємо стіни до групи
barriers.add(w2)
barriers.add(w3)
barriers.add(w4)
barriers.add(w5)
barriers.add(w6)
barriers.add(w7)
barriers.add(w8)
barriers.add(w9)
barriers.add(w10)
barriers.add(w11)
barriers.add(w12)
barriers.add(w13)
barriers.add(w14)
barriers.add(w15)
barriers.add(w16)
barriers.add(w17)
barriers.add(w18)
barriers.add(w19)
barriers.add(w20)
barriers.add(w21)
barriers.add(w22)
barriers.add(w23)
barriers.add(w24)
barriers.add(w25)
barriers.add(w26)
barriers.add(w27)
barriers.add(w28)
barriers.add(w29)
barriers.add(w30)
barriers.add(w31)

# Створення гравця та ворогів
packman = Player('mushroom.png', 5, 300, 50, 50, 0, 0)
monster1 = Enemy_v('ghost.png', 245, 145, 50, 50, 5, 145, 310)
monster2 = Enemy_v('ghost.png', 461, 37, 50, 50, 5, 40, 307)
monster3 = Enemy_h('ghost.png', 451, 515, 50, 50, 5, 451, 575)
monster4 = Enemy_h('ghost.png', 667, 190, 50, 50, 5, 667, 790)
coin1 = star('star.png', 245, 623, 50, 50)
coin2 = star('star.png', 461, 407, 50, 50)
coin3 = star('star.png', 785, 299, 50, 50)
prize = decor('coins.png', 562, 299, 60, 60)
final_sprite = GameSprite('pointer.png', 990, 620, 90, 56)

monsters.add(monster1)  # Додаємо ворогів до групи
monsters.add(monster2)
monsters.add(monster3)
monsters.add(monster4)
coin.add(coin1)
coin.add(coin2)
coin.add(coin3)
coins.add(prize)

finish = False  # Чи завершено гру
run = True  # Основний цикл гри

total_monsters = 4

coin_collected = 0
show_exit = False

show_intro(window, win_width, win_height)

background_music = pygame.mixer.Sound("background_music.wav")  # шлях до твого музичного файлу
background_music.set_volume(0.5)  # гучність (від 0.0 до 1.0)
background_music.play(-1)  # -1 означає безкінечне повторення

coin_sound = pygame.mixer.Sound("coin.wav")  # або "coin.ogg"
coin_sound.set_volume(0.5)  # гучність (від 0.0 до 1.0)

bullet_sound = pygame.mixer.Sound("bullet.wav")
bullet_sound.set_volume(0.5)  # гучність (від 0.0 до 1.0)

win_sound = pygame.mixer.Sound("win.wav")
win_sound.set_volume(0.4)  # гучність (від 0.0 до 1.0)

game_over_sound = pygame.mixer.Sound("game_over.wav")
game_over_sound.set_volume(0.4)  # гучність (від 0.0 до 1.0)

monster_killed = False


while run:  # Поки гра активна
    time.delay(30)  # Пауза 50 мс

    for e in event.get():  # Перебір подій
        if e.type == QUIT:  # Закрити гру
            run = False
        elif e.type == KEYDOWN:  # Якщо натиснута клавіша
            if e.key == K_LEFT:
                packman.x_speed = -5
            elif e.key == K_RIGHT:
                packman.x_speed = 5
            elif e.key == K_UP:
                packman.y_speed = -5
            elif e.key == K_DOWN:
                packman.y_speed = 5
            elif e.key == K_SPACE:
                packman.fire()  # Постріл
                bullet_sound.play()

        elif e.type == KEYUP:  # Відпускання клавіші
            if e.key == K_LEFT or e.key == K_RIGHT:
                packman.x_speed = 0
            if e.key == K_UP or e.key == K_DOWN:
                packman.y_speed = 0

    if not finish:  # Якщо гра не завершена
        window.blit(back, (0, 0))  # Фон
        packman.update()  # Оновлення гравця
        bullets.update()  # Оновлення куль

        for bullet in bullets:
            hit_monsters = sprite.spritecollide(bullet, monsters, True)
            if hit_monsters:
                bullet.kill()
                monster_killed = True  # Хоч один монстр був убитий


        packman.reset()  # Відображення гравця
        bullets.draw(window)  # Малювання всіх куль
        barriers.draw(window)  # Малювання перешкод
        final_sprite.reset()

        if coin_collected == 3 and not monster_killed and len(monsters) == total_monsters and w31 in barriers:
            barriers.remove(w31)
        


        sprite.groupcollide(monsters, bullets, True, True)  # Кулі знищують ворогів
        monsters.update()  # Оновлення ворогів
        monsters.draw(window)  # Малювання ворогів
        collected = sprite.spritecollide(packman, coin, True)
        if collected:
            coin_collected += len(collected)
            coin_sound.play()
            if coin_collected >= 3:
                show_exit = True
        coin.draw(window) # малюємо монету
        coins.draw(window) # малюємо монети в центрі
        sprite.groupcollide(bullets, barriers, True, False)  # Кулі зникають при ударі в стіну

        if sprite.spritecollide(packman, monsters, False):  # Перевірка зіткнення з ворогом
            finish = True  # Завершення гри

            # Відтворення відео програшу
            for frame in lose_clip.iter_frames(fps=30, dtype='uint8'):
                background_music.set_volume(0.0)  # гучність (від 0.0 до 1.0)
                game_over_sound.play()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                        exit()

                frame_surface = surfarray.make_surface(np.rot90(frame))  # перетворення кадру
                frame_surface = transform.scale(frame_surface, (win_width, win_height))  # маштабування під вікно
                window.blit(frame_surface, (0, 0))
                display.update()
                time.Clock().tick(30)
        

        if sprite.collide_rect(packman, final_sprite):
            finish = True

            # Відтворення відео перемоги
            for frame in win_clip.iter_frames(fps=30, dtype='uint8'):
                background_music.set_volume(0.0)  # гучність (від 0.0 до 1.0)
                game_over_sound.play()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        quit()
                        exit()

                frame_surface = surfarray.make_surface(np.rot90(frame))  # перетворення кадру
                frame_surface = transform.scale(frame_surface, (win_width, win_height))  # маштабування під вікно
                window.blit(frame_surface, (0, 0))
                display.update()
                time.Clock().tick(30)
    display.update()  # Оновлення екрану
