import os
import sys
import csv
from typing import Optional
from random import choice
import pygame
from PIL import ImageFilter, Image

settings = {
    'fps': 60,
    'screen_background': (11, 11, 11)
}

data = {
    'level': 1,
    'tmp': 0,
    'fireflies': 0,
    'min_time': 5 * 60
}


class Cursor:
    def __init__(self, screen: pygame.Surface):
        self.img = pygame.image.load("resource/image/cursor.png")
        self.screen = screen
        screen.blit(self.img, (-40, 0))

    def draw(self, x: int, y: int) -> None:
        self.screen.blit(self.img, (x - 16, y - 16))


class Label:
    def __init__(self, content, size, sysfont=False, font='resource/font/t2ddr-font.ttf', color=(255, 255, 255)):
        if sysfont:
            font = pygame.font.SysFont(font, size)
        else:
            font = pygame.font.Font(font, size)
        self.text = font.render(content, True, color)

    def get_size(self):
        return self.text.get_size()


class Button:
    def __init__(self, text: str, pos: tuple[int, int], surface: pygame.Surface):
        self.text = text
        self.pos = pos
        self.screen = surface
        self.disabled = False
        self.start: tuple[int, int]
        self.end: tuple[int, int]
        self.style = {
            'font-size': 30,
            'border-width': 10,
            'states': {
                'normal': {
                    'color': (255, 255, 255),
                    'border-color': (255, 255, 255),
                    'background': (0, 0, 0)
                },
                'pressed': {
                    'color': (150, 150, 150),
                    'border-color': (150, 150, 150),
                    'background': (0, 0, 0)
                },
                'disabled': {
                    'color': (150, 150, 150),
                    'border-color': (150, 150, 150),
                    'background': (30, 30, 30)
                }
            }
        }

    def draw(self, pressed=False) -> None:
        if self.disabled:
            state = 'disabled'
        elif pressed:
            state = 'pressed'
        else:
            state = 'normal'

        label = Label(self.text, self.style['font-size'], color=self.style['states'][state]['color'])
        tx, ty = label.get_size()
        x, y = self.pos
        self.start = (x - 25, y - 5)
        self.end = (tx + 50, ty + 15)

        if self.style['states'][state]['background'] != "transparent":
            # Заливка
            pygame.draw.rect(self.screen, self.style['states'][state]['background'], (*self.start, *self.end), 0)

        if self.style['states'][state]['border-color'] != "transparent":
            # Рисуем рамку
            # Левая и правая границы
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (self.start[0] - self.style['border-width'], self.start[1] + self.style['border-width'],
                              self.style['border-width'], self.end[1] - self.style['border-width'] * 2))
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (self.start[0] + self.end[0], self.start[1] + self.style['border-width'],
                              self.style['border-width'], self.end[1] - self.style['border-width'] * 2))
            # Верхняя и нижняя
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (*self.start, self.end[0], self.style['border-width']))
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (self.start[0], self.start[1] + self.end[1] - self.style['border-width'],
                              self.end[0], self.style['border-width']))
            # Квадратики по углам
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (
                             self.start[0] - self.style['border-width'] / 2, self.start[1] + self.style['border-width'] / 2,
                             self.style['border-width'], self.style['border-width']))
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (
                             self.start[0] + self.end[0] - self.style['border-width'] / 2, self.start[1] + self.style['border-width'] / 2,
                             self.style['border-width'], self.style['border-width']))
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (
                             self.start[0] - self.style['border-width'] / 2, self.start[1] + self.end[1] - self.style['border-width'] / 2 - self.style['border-width'],
                             self.style['border-width'], self.style['border-width']))
            pygame.draw.rect(self.screen, self.style['states'][state]['border-color'],
                             (
                                 self.start[0] + self.end[0] - self.style['border-width'] / 2,
                                 self.start[1] + self.end[1] - self.style['border-width'] / 2 - self.style['border-width'],
                                 self.style['border-width'], self.style['border-width']))

        self.screen.blit(label.text, self.pos)

    def clicked(self, x, y) -> bool:
        if self.disabled:
            return False

        if all((x > self.start[0], x < self.end[0] + self.pos[0], y > self.start[1], y < self.end[1] + self.pos[1])):
            self.draw(True)
            return True

        return False


def terminate():
    with open('scores.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(['level', 'fireflies', 'min_time'])
        writer.writerow([data['level'], data['fireflies'], data['min_time']])

    pygame.quit()
    sys.exit(0)


def blur_image(surf, radius):
    pil_string_image = pygame.image.tostring(surf, "RGBA",False)
    pil_image = Image.frombuffer("RGBA", surf.get_size(), pil_string_image)
    pil_blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
    blurred_image = pygame.image.fromstring(pil_blurred.tobytes(), pil_blurred.size, pil_blurred.mode)
    return blurred_image.convert_alpha()


def start_menu(screen: pygame.Surface, clock: pygame.time.Clock, cursor: Cursor):
    screen.fill(settings['screen_background'])

    fairy_img = pygame.image.load('resource/image/player.png')
    fairy_img = pygame.transform.scale(fairy_img, (250, 400))

    play_btn_pressed = False
    exit_btn_pressed = False
    score_btn_pressed = False

    play_btn = Button("Играть", (180, 200), screen)
    play_btn.style['font-size'] = 25
    play_btn.style['border-width'] = 15
    play_btn.style['states']['normal']['color'] = (255, 255, 255)
    play_btn.style['states']['normal']['background'] = (9, 117, 96)
    play_btn.style['states']['normal']['border-color'] = (9, 117, 96)
    play_btn.style['states']['pressed']['color'] = (255, 255, 255)
    play_btn.style['states']['pressed']['background'] = (8, 106, 87)
    play_btn.style['states']['pressed']['border-color'] = (8, 106, 87)

    exit_btn = Button("Выход", (202, 350), screen)
    exit_btn.style['font-size'] = 15
    exit_btn.style['border-width'] = 8
    exit_btn.style['states']['normal']['color'] = (255, 255, 255)
    exit_btn.style['states']['normal']['background'] = (51, 115, 165)
    exit_btn.style['states']['normal']['border-color'] = (51, 115, 165)
    exit_btn.style['states']['pressed']['color'] = (255, 255, 255)
    exit_btn.style['states']['pressed']['background'] = (41, 92, 132)
    exit_btn.style['states']['pressed']['border-color'] = (41, 92, 132)

    score_table_btn = Button("Таблица рекордов", (555, 50), screen)
    score_table_btn.style['font-size'] = 12
    score_table_btn.style['states']['normal']['color'] = (255, 255, 255)
    score_table_btn.style['states']['normal']['background'] = settings['screen_background']
    score_table_btn.style['states']['normal']['border-color'] = settings['screen_background']
    score_table_btn.style['states']['pressed']['color'] = (230, 230, 230)
    score_table_btn.style['states']['pressed']['background'] = settings['screen_background']
    score_table_btn.style['states']['pressed']['border-color'] = settings['screen_background']

    level_label = Label(f"Уровень {data['level']}", 12)

    score_frame_being_drawn = False
    close_score_frame_btn = None
    close_score_frame_pressed = False

    def draw_score():
        nonlocal close_score_frame_btn
        frame = pygame.Surface((600, 400), pygame.SRCALPHA)
        frame.fill((0, 0, 0, 155))

        close_score_frame_btn = Button("X", (550, 25), frame)
        close_score_frame_btn.style['font-size'] = 15
        close_score_frame_btn.style['states']['normal']['background'] = "transparent"
        close_score_frame_btn.style['states']['pressed']['background'] = "transparent"
        close_score_frame_btn.style['states']['normal']['border-color'] = "transparent"
        close_score_frame_btn.style['states']['pressed']['border-color'] = "transparent"
        close_score_frame_btn.style['states']['pressed']['color'] = (255, 41, 73)
        close_score_frame_btn.draw(close_score_frame_pressed)

        label = Label("Таблица рекордов", 15)
        frame.blit(label.text, (150, 25))

        label = Label("Ваш рекорд", 25)
        frame.blit(label.text, (150, 75))

        label = Label("В самый лучший день вы", 15)
        tx, ty = label.get_size()
        frame.blit(label.text, (100, 200))

        label = Label(f"собрали {data['fireflies']} светлячков", 15)
        tx, ty = label.get_size()
        frame.blit(label.text, (100, 225))

        minutes = data['min_time'] // 60
        seconds = data['min_time'] - (minutes * 60)

        label = Label("за {:02}:{:02}".format(minutes, seconds), 15)
        tx, ty = label.get_size()
        frame.blit(label.text, (100, 250))

        screen.blit(frame, (100, 100))

    running = True
    last_cur_pos = (20, 20)

    blured = None
    while running:
        if score_frame_being_drawn:
            screen.blit(blured, (0, 0))
            draw_score()
        else:
            screen.fill(settings['screen_background'])
            play_btn.draw(play_btn_pressed)
            exit_btn.draw(exit_btn_pressed)
            score_table_btn.draw(score_btn_pressed)
            screen.blit(level_label.text, (10, 10))
            screen.blit(fairy_img, (500, 100))
            if blured is None:
                blured = blur_image(screen, 10)
        cursor.draw(*last_cur_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                last_cur_pos = event.pos

            if score_frame_being_drawn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    close_score_frame_pressed = close_score_frame_btn.clicked(x - 100, y - 100)
                    cursor.draw(*event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if close_score_frame_pressed:
                        close_score_frame_pressed = False
                        score_frame_being_drawn = False
                        cursor.draw(*event.pos)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_btn_pressed = play_btn.clicked(*event.pos)
                    exit_btn_pressed = exit_btn.clicked(*event.pos)
                    score_btn_pressed = score_table_btn.clicked(*event.pos)

                    cursor.draw(*event.pos)

                if event.type == pygame.MOUSEBUTTONUP:
                    if play_btn_pressed:
                        play_btn.draw()
                        cursor.draw(*event.pos)
                        play_btn_pressed = False
                        running = False

                    if score_btn_pressed:
                        score_btn_pressed = False
                        score_frame_being_drawn = True
                        score_table_btn.draw()

                        draw_score()
                        cursor.draw(*event.pos)

                    if exit_btn_pressed:
                        terminate()

        pygame.display.flip()
        clock.tick(settings['fps'])
    else:
        game(cursor)

def load_image(name, colorkey=None, scale:Optional[tuple[int, int]]=None, flip:Optional[tuple[bool, bool]]=None) -> pygame.Surface:
    fullname = os.path.join('resource/image', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    if flip is not None:
        image = pygame.transform.flip(image, *flip)

    return image


def load_level(filename):
    filename = "resource/level/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    mapTxt = list(map(lambda x: 'X' + x.ljust(max_width, '.') + 'X', level_map))
    mapTxt.insert(0, ''.ljust(max_width + 1, 'X'))
    return mapTxt


tile_images: dict[str, pygame.Surface] = {
    'dirt': load_image('dirt.png', scale=(64, 64)),
    'grass_dirt': load_image('grass_side_carried.png', scale=(64, 64)),
    'wall': load_image('cobblestone.png', scale=(64, 64)),
    'grass': load_image('tallgrass_carried.tga', scale=(64, 64)),
    'grass2': load_image('double_plant_grass_carried.png', scale=(64, 64)),
    'tree': load_image('log_oak.png', scale=(64, 64)),
    'leaves': load_image('leaves_oak_carried.tga', scale=(64, 64)),
    'sweet_berry_s1': load_image('sweet_berry_bush_stage1.png', scale=(64, 64)),
    'sweet_berry_s2': load_image('sweet_berry_bush_stage2.png', scale=(64, 64)),
    'flower': load_image('flower_cornflower.png', scale=(64, 64)),
}
tile_width = tile_height = 64
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
collide_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
snakes_group = pygame.sprite.Group()


class Firefly(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.x, self.y = tile_width * pos_x, tile_height * pos_y
        self.vx = -5
        self.vy = -5

        self.taken = False
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)

        img_front, img_back = pygame.Surface((64, 64), pygame.SRCALPHA), pygame.Surface((64, 64), pygame.SRCALPHA)
        pygame.draw.circle(img_front, (255, 255, 255, 255), (32, 32), 10)
        pygame.draw.circle(img_back, (255, 255, 255, 255), (32, 32), 15)
        img_back = blur_image(img_back, 10)

        self.image.blit(img_back, (0, 0))
        self.image.blit(img_front, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect().move(self.x, self.y)


    def move(self):
        last_x, last_y = self.x, self.y
        self.x += self.vx
        self.y += self.vy
        for sprite in collide_sprites:
            if pygame.sprite.collide_rect(self, sprite) and sprite != self:
                if self.rect.bottom - sprite.rect.bottom > 0:  # bottom side collided
                    self.vy = -self.vy
                elif sprite.rect.bottom - self.rect.top > 0:  # top side collided
                    self.vy = -self.vy
                if 0 < self.rect.right - sprite.rect.left < tile_width:  # left side collided
                    self.vx = -self.vx
                elif 8 > sprite.rect.right - self.rect.left:  # right side collided
                    self.vx = -self.vx
                self.x, self.y = last_x, last_y
                break


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type: Optional[str], pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)

        if tile_type is None:
            self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
            self.image.set_alpha(0)
            self.mask = pygame.mask.from_surface(pygame.Surface((64, 64)))
        else:
            self.image = tile_images[tile_type]
            self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, groups, sheet, columns, rows, x, y):
        super().__init__(*groups)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Snake(AnimatedSprite):
    def __init__(self, pos_x, pos_y):
        super().__init__((all_sprites, snakes_group), load_image("snake.png"), 7, 1, tile_width * pos_x, tile_height * pos_y)
        self.move_to_right = True
        self.stop = False
    
    def update(self):
        super().update()

        if not self.move_to_right:
            self.image = pygame.transform.flip(self.image, True, False)

        if self.cur_frame == 6:
            for player in player_group:
                if pygame.sprite.collide_mask(self, player):
                    player.health.take(10)                    
                    stop = True
                    break
            else:
                stop = False

            if not stop:
                for sprite in collide_sprites:
                    if pygame.sprite.collide_rect(self, sprite) and sprite != self:
                        if 0 < self.rect.right - sprite.rect.left < tile_width or self.rect.collidepoint(sprite.rect.midright):
                            self.move_to_right = not self.move_to_right
                        break

                if self.move_to_right:
                    self.rect.x += tile_width
                else:
                    self.rect.x -= tile_width


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png', scale=(100, 150))
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 15)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)
        self.health = Health(self)

    def check_collide(self):
        for sprite in collide_sprites:
            if isinstance(sprite, Snake):
                continue

            if pygame.sprite.collide_mask(self, sprite):
                if isinstance(sprite, Firefly):
                    sprite.taken = True
                    data['tmp'] += 1
                    self.health.add(10)
                    collide_sprites.remove_internal(sprite)
                    return False
                return True
        return False


class Health:
    def __init__(self, player: Player):
        self.player = player
        self.health = 100

    def _speed_control(func):
        def controller(self, *args):
            if self.health <= 10:
                self.player.speed = 1
            elif self.health <= 40:
                self.player.speed = 2
            elif self.health <= 70:
                self.player.speed = 3
            elif self.health <= 90:
                self.player.speed = 4
            elif self.health > 90:
                self.player.speed = 5
            func(self, *args)
        return controller

    @_speed_control
    def take(self, count):
        if self.health - count > 0:
            self.health -= count
        else:
            self.health = 0

    @_speed_control
    def add(self, count):
        if self.health + count < 100:
            self.health += count
        else:
            self.health = 100


fireflies_count = 0


def generate_level(level):
    global fireflies_count
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                new_player = Player(x, y)
                pass
            elif level[y][x] == 'X':
                Tile(None, x, y)
            elif level[y][x] == '*':
                Firefly(x, y)
                fireflies_count += 1
            elif level[y][x] == '~':
                Snake(x, y)
            else:
                symbol = level[y][x]
                if symbol != '.':
                    Tile({
                        '_': choice(('grass', 'grass2')),
                        '#': 'wall',
                        '+': 'grass_dirt',
                        '-': 'dirt',
                        '|': 'tree',
                        '/': 'leaves',
                        '=': 'sweet_berry_s1',
                        '!': 'sweet_berry_s2',
                        '1': 'flower'
                    }[symbol], x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if isinstance(obj, Firefly):
            obj.rect.x += self.dx
            obj.rect.x += obj.vx
            obj.rect.y += self.dy
            obj.rect.y += obj.vy
        else:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


player: Player

blacklist = (
    tile_images['tree'],
    tile_images['grass'],
    tile_images['grass2'],
    tile_images['leaves'],
    tile_images['sweet_berry_s1'],
    tile_images['sweet_berry_s2'],
    tile_images['flower']
)


def game(cursor):
    global fireflies_count, tiles_group, all_sprites, collide_sprites, player_group, snakes_group

    # Таймер для анимации змеи
    fps_time_delay = 100
    snake_anim_timer_event = pygame.USEREVENT + 1
    pygame.time.set_timer(snake_anim_timer_event, fps_time_delay)

    # Таймер игры
    game_time = 5 * 60  # На 1 игру дается 5 минут
    time_delay = 1000
    timer_event = pygame.USEREVENT + 2
    pygame.time.set_timer(timer_event, time_delay)

    blured = None
    game_ended = False
    game_over = False
    end_text = tuple()

    frame = pygame.Surface((600, 400), pygame.SRCALPHA)
    frame.fill((0, 0, 0, 155))

    home_btn = Button("Домой", (100, 300), frame)
    home_btn.style['font-size'] = 15
    home_btn.style['border-width'] = 8
    home_btn.style['states']['normal']['color'] = (255, 255, 255)
    home_btn.style['states']['normal']['background'] = (9, 117, 96)
    home_btn.style['states']['normal']['border-color'] = (9, 117, 96)
    home_btn.style['states']['pressed']['color'] = (255, 255, 255)
    home_btn.style['states']['pressed']['background'] = (8, 106, 87)
    home_btn.style['states']['pressed']['border-color'] = (8, 106, 87)
    home_btn_pressed = False

    exit_btn = Button("Выход", (400, 300), frame)
    exit_btn.style['font-size'] = 15
    exit_btn.style['border-width'] = 8
    exit_btn.style['states']['normal']['color'] = (255, 255, 255)
    exit_btn.style['states']['normal']['background'] = (51, 115, 165)
    exit_btn.style['states']['normal']['border-color'] = (51, 115, 165)
    exit_btn.style['states']['pressed']['color'] = (255, 255, 255)
    exit_btn.style['states']['pressed']['background'] = (41, 92, 132)
    exit_btn.style['states']['pressed']['border-color'] = (41, 92, 132)
    exit_btn_pressed = False

    def end_menu_draw():
        nonlocal blured
        if blured is None:
            blured = blur_image(screen, 10)
        screen.blit(blured, (0, 0))

        label = Label("Вы проиграли" if game_over else "Вы победили", 15)
        frame.blit(label.text, (300 - label.get_size()[0] // 2, 25))

        line_i = 0
        for i in range(100, 300, 25):
            if line_i < len(end_text):
                label = Label(end_text[line_i], 15)
                frame.blit(label.text, (100, i))
                line_i += 1
            else:
                break

        home_btn.draw(home_btn_pressed)
        exit_btn.draw(exit_btn_pressed)

        screen.blit(frame, (100, 100))

    running = True

    player, cx, cy = generate_level(load_level(f"{data['level']}.txt"))
    bg = load_image('mountains.jpg')

    for sprite in all_sprites:
        if sprite not in player_group and sprite.image not in blacklist:
            collide_sprites.add(sprite)

    camera = Camera()

    player_img = player.image
    last_cursor_pos = (20, 20)
    while running:
        if game_ended:
            end_menu_draw()
            cursor.draw(*last_cursor_pos)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == pygame.MOUSEMOTION:
                    last_cursor_pos = event.pos
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    x -= 100
                    y -= 100
                    home_btn_pressed = home_btn.clicked(x, y)
                    exit_btn_pressed = exit_btn.clicked(x, y)
                if event.type == pygame.MOUSEBUTTONUP:
                    if exit_btn_pressed:
                        terminate()
                    if home_btn_pressed:
                        running = False
        else:
            if player.health.health == 0:
                game_ended = True
                game_over = True
                end_text = ("Вас укусила змея",)
            elif game_time == 0:
                game_ended = True
                game_over = True
                end_text = (f"Вы не успели собрать {fireflies_count}", "светлячков за 5 минут")
            elif data['tmp'] == fireflies_count:
                game_ended = True
                game_time = abs(game_time - 5 * 60)
                minutes = game_time // 60
                seconds = game_time - (minutes * 60)
                tmp_text = [f"Вы собрали {fireflies_count} светлячков", "за {:02}:{:02}".format(minutes, seconds)]

                if data['level'] < 2:
                    data['level'] += 1
                if data['min_time'] > game_time:
                    tmp_text.insert(0, "НОВЫЙ РЕКОРД!!!")
                    data['fireflies'] = data['tmp']
                    data['min_time'] = game_time

                end_text = tuple(tmp_text)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                if event.type == snake_anim_timer_event:
                    snakes_group.update()
                if event.type == timer_event:
                    game_time -= 1

            last_x, last_y = player.rect.x, player.rect.y
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                player.rect.y -= player.speed
            if keys[pygame.K_s] or keys[pygame.K_DOWN]:
                player.rect.y += player.speed
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.rect.x -= player.speed
                player_img = player.image
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.rect.x += player.speed
                player_img = player.image_left
            if keys[pygame.KMOD_SHIFT]:
                print(True)

            if player.check_collide():
                player.rect.x = last_x
                player.rect.y = last_y

            screen.blit(bg, (0, 0))

            camera.update(player)
            draw_queues = [[], []]
            for sprite in all_sprites:
                camera.apply(sprite)
                if sprite not in player_group:
                    if isinstance(sprite, Firefly):
                        if sprite.taken:
                            continue
                        else:
                            sprite.move()
                            draw_queues[0].append(sprite)
                    elif isinstance(sprite, Snake):
                        draw_queues[1].append(sprite)
                    else:
                        screen.blit(sprite.image, sprite.rect)

            for draw_queue in draw_queues:
                for sprite in draw_queue:
                    screen.blit(sprite.image, sprite.rect)

            screen.blit(player_img, player.rect)
            screen.blit(Label(f"Здоровье +{player.health.health}", 12).text, (10, 10))
            screen.blit(Label(f"Светлячков: {data['tmp']}::{fireflies_count}", 12).text, (10, 32))

            minutes = game_time // 60
            seconds = game_time - (minutes * 60)
            screen.blit(Label("{:02}:{:02}".format(minutes, seconds), 12).text, (722, 10))

        pygame.display.flip()
        clock.tick(settings['fps'])
    else:
        fireflies_count = 0
        tiles_group = pygame.sprite.Group()
        all_sprites = pygame.sprite.Group()
        collide_sprites = pygame.sprite.Group()
        player_group = pygame.sprite.Group()
        snakes_group = pygame.sprite.Group()
        data['tmp'] = 0
        start_menu(screen, clock, cursor)


if __name__ == '__main__':
    if os.path.exists('scores.csv'):
        with open('scores.csv', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                if row[0] == 'level':  # skip header
                    continue

                data['level'] = int(row[0])
                data['fireflies'] = int(row[1])
                data['min_time'] = int(row[2])

    pygame.init()
    pygame.display.set_caption('Светлячки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    cursor = Cursor(screen)

    start_menu(screen, clock, cursor)

    pygame.quit()
