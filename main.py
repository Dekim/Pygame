import os
import sys
from typing import Optional
from random import choice, randint

import pygame
from PIL import ImageFilter, Image

settings = {
    'fps': 60,
    'screen_background': (11, 11, 11)
}

data = {
    'level': 1,
    'km': 0,
    'fireflies': 0,
    'stars': 0
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
        self.start = None
        self.end = None
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
    pygame.quit()
    sys.exit(0)


def blur_image(surf, radius):
    pil_string_image = pygame.image.tostring(surf, "RGB",False)
    pil_image = Image.frombuffer("RGB", surf.get_size(), pil_string_image)
    pil_blurred = pil_image.filter(ImageFilter.GaussianBlur(radius=radius))
    blurred_image = pygame.image.fromstring(pil_blurred.tobytes(), pil_blurred.size, pil_blurred.mode)
    return blurred_image.convert_alpha()


def start_menu(screen: pygame.Surface, clock: pygame.time.Clock, cursor: Cursor):
    menu = pygame.Surface((800, 600))
    menu.fill(settings['screen_background'])

    fairy_img = pygame.image.load('resource/image/player.png')
    fairy_img = pygame.transform.scale(fairy_img, (250, 400))

    play_btn_pressed = False
    exit_btn_pressed = False
    score_btn_pressed = False

    play_btn = Button("Играть", (180, 200), menu)
    play_btn.style['font-size'] = 25
    play_btn.style['border-width'] = 15
    play_btn.style['states']['normal']['color'] = (255, 255, 255)
    play_btn.style['states']['normal']['background'] = (9, 117, 96)
    play_btn.style['states']['normal']['border-color'] = (9, 117, 96)
    play_btn.style['states']['pressed']['color'] = (255, 255, 255)
    play_btn.style['states']['pressed']['background'] = (8, 106, 87)
    play_btn.style['states']['pressed']['border-color'] = (8, 106, 87)

    exit_btn = Button("Выход", (202, 350), menu)
    exit_btn.style['font-size'] = 15
    exit_btn.style['border-width'] = 8
    exit_btn.style['states']['normal']['color'] = (255, 255, 255)
    exit_btn.style['states']['normal']['background'] = (51, 115, 165)
    exit_btn.style['states']['normal']['border-color'] = (51, 115, 165)
    exit_btn.style['states']['pressed']['color'] = (255, 255, 255)
    exit_btn.style['states']['pressed']['background'] = (41, 92, 132)
    exit_btn.style['states']['pressed']['border-color'] = (41, 92, 132)

    score_table_btn = Button("Таблица рекордов", (555, 50), menu)
    score_table_btn.style['font-size'] = 12
    score_table_btn.style['states']['normal']['color'] = (255, 255, 255)
    score_table_btn.style['states']['normal']['background'] = settings['screen_background']
    score_table_btn.style['states']['normal']['border-color'] = settings['screen_background']
    score_table_btn.style['states']['pressed']['color'] = (230, 230, 230)
    score_table_btn.style['states']['pressed']['background'] = settings['screen_background']
    score_table_btn.style['states']['pressed']['border-color'] = settings['screen_background']

    level_label = Label(f"Уровень {data['level']}", 12)


    def draw_menu():
        nonlocal menu
        menu.fill(settings['screen_background'])

        menu.blit(fairy_img, (500, 125))
        menu.blit(level_label.text, (25, 25))

        # Отрисовка элементов
        play_btn.draw(play_btn_pressed)
        exit_btn.draw(exit_btn_pressed)
        score_table_btn.draw(score_btn_pressed)

        screen.blit(blur_image(menu, 10) if score_frame_being_drawn else menu, (0, 0))

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

        label = Label("Километров пройдено:", 12)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 125))

        label = Label(f"{data['km']} km", 24)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 150))

        label = Label("Собрано светлячков:", 12)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 200))

        label = Label(str(data['fireflies']), 24)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 225))

        label = Label("Звезды за побежденных врагов:", 12)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 275))
        label = Label(str(data['stars']), 24)
        tx, ty = label.get_size()
        frame.blit(label.text, (300 - tx / 2, 300))

        screen.blit(frame, (100, 100))


    draw_menu()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEMOTION:
                draw_menu()

                if score_frame_being_drawn:
                    draw_score()

                cursor.draw(*event.pos)

            if score_frame_being_drawn:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    close_score_frame_pressed = close_score_frame_btn.clicked(x - 100, y - 100)

                    draw_menu()
                    draw_score()
                    cursor.draw(*event.pos)
                if event.type == pygame.MOUSEBUTTONUP:
                    if close_score_frame_pressed:
                        close_score_frame_pressed = False
                        close_score_frame_btn = None
                        score_frame_being_drawn = False

                        draw_menu()
                        cursor.draw(*event.pos)
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    play_btn_pressed = play_btn.clicked(*event.pos)
                    exit_btn_pressed = exit_btn.clicked(*event.pos)
                    score_btn_pressed = score_table_btn.clicked(*event.pos)

                    draw_menu()
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

                        draw_menu()
                        draw_score()
                        cursor.draw(*event.pos)

                    if exit_btn_pressed:
                        terminate()

        pygame.display.flip()
        clock.tick(settings['fps'])


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
    for i in range(3):
        clouds_line = ''
        for _ in range(max_width + 1):
            clouds_line += choice(('~', '.'))
        mapTxt.insert(i, clouds_line)
    mapTxt.insert(3, ''.ljust(max_width + 1, 'X'))
    return mapTxt


player = None
tile_images: dict[str, pygame.Surface] = {
    'dirty': load_image('dirty.png'),
    'dirty2': load_image('dirty2.png'),
    'dirty3': load_image('dirty3.png'),
    'wall': load_image('cobblestone.png'),
    'grass': load_image('grass.png'),
    'grass2': load_image('grass2.png'),
    'tree': load_image('tree.png'),
    'forest': load_image('forest_bg.png'),
    'cloud': load_image('cloud.png'),
    'cloud2': load_image('cloud2.png'),
    'cloud3': load_image('cloud3.png')
}
tile_width = tile_height = 64
tiles_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
collide_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Firefly:
    def __init__(self, x, y, surf):
        self.x = x
        self.y = y
        self.vx = -5
        self.vy = -5
        self.surf = surf

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.y < 10 or self.y > tile_height - 10:
            self.vy = -self.vy
        if self.x < 10 or self.x > tile_width - 10:
            self.vx = -self.vx


    def draw(self):
        pygame.draw.circle(self.surf, (255, 255, 255, 255), (self.x, self.y), 5)



class Fireflies(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(tiles_group, all_sprites)
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(pygame.Surface((64, 64)))
        self.taken = False

        self.quantity = randint(1, 5)
        positions = [(randint(10, tile_width - 10), randint(10, tile_height - 10)) for _ in range(self.quantity)]
        self.fireflies = list()
        for pos in positions:
            self.fireflies.append(Firefly(*pos, self.image))

    def update(self):
        self.image.fill((0, 0, 0, 0))
        for firefly in self.fireflies:
            firefly.move()
            firefly.draw()


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
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)



class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x: int, pos_y: int):
        super().__init__(player_group, all_sprites)
        self.image = load_image('player.png', scale=(100, 150))
        self.image_left = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 15)
        self.speed = 5
        self.mask = pygame.mask.from_surface(self.image)

    def check_collide(self):
        for sprite in collide_sprites:
            if pygame.sprite.collide_mask(self, sprite):
                if isinstance(sprite, Fireflies):
                    sprite.taken = True
                    sprite.image.fill((0, 0, 0, 0))
                    data['fireflies'] += sprite.quantity
                    sprite.quantity = 0
                    collide_sprites.remove_internal(sprite)
                    return False
                return True
        return False


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '@':
                new_player = Player(x, y)
                pass
            elif level[y][x] == '*':
                Fireflies(x, y)
            elif level[y][x] in '|&':
                tile_name = {
                    '|': 'tree',
                    '&': 'forest'
                }[level[y][x]]
                img = tile_images[tile_name]

                Tile(tile_name, x + img.get_width() // tile_width, y - img.get_height() // tile_height + 1)
            elif level[y][x] == 'X':
                Tile(None, x, y)
            else:
                symbol = level[y][x]
                if symbol != '.':
                    Tile({
                        '~': choice(('cloud', 'cloud2', 'cloud3')),
                        '_': choice(('grass', 'grass2')),
                        '#': 'wall',
                        '+': 'dirty3',
                        '=': 'dirty2',
                        '-': 'dirty'
                    }[symbol], x, y)

    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def game():
    running = True

    player, cx, cy = generate_level(load_level(f"{data['level']}.txt"))
    bg = load_image('mountains.jpg')

    for sprite in all_sprites:
        if sprite not in player_group and sprite.image not in (tile_images['tree'], tile_images['forest'],
                                                               tile_images['cloud'], tile_images['cloud2'],
                                                               tile_images['cloud3']):
            collide_sprites.add(sprite)

    camera = Camera()

    player_img = player.image
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

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
        for sprite in all_sprites:
            camera.apply(sprite)
            if sprite not in player_group:
                if isinstance(sprite, Fireflies) and not sprite.taken:
                    sprite.update()
                screen.blit(sprite.image, sprite.rect)

        screen.blit(player_img, player.rect)
        screen.blit(Label(f"Светлячков: {data['fireflies']}", 12).text, (10, 10))

        pygame.display.flip()
        clock.tick(settings['fps'])


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Светлячки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()

    cursor = Cursor(screen)

    start_menu(screen, clock, cursor)
    game()

    pygame.quit()
