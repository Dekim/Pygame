import sys
import pygame
from PIL import ImageFilter, Image

settings = {
    'fps': 60,
    'screen_background': (11, 11, 11)
}

data = {
    'level': 0,
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


def game():
    running = True

    fairy_img = pygame.image.load('resource/image/player.png')
    fairy_img = pygame.transform.scale(fairy_img, (100, 150))
    fairy_img_right = fairy_img
    fairy_img_left = pygame.transform.flip(fairy_img, True, False)
    fairy_img = fairy_img_right


    fairy_x, fairy_y = 250, 125
    fairy_speed = 5

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()


        if keys[pygame.K_w]:
            fairy_y -= fairy_speed
        if keys[pygame.K_s]:
            fairy_y += fairy_speed
        if keys[pygame.K_a]:
            fairy_x -= fairy_speed
            fairy_img = fairy_img_right
        if keys[pygame.K_d]:
            fairy_x += fairy_speed
            fairy_img = fairy_img_left


        # fairy_x = max(0, min(fairy_x, 800 - fairy_img.get_width()))
        # fairy_y = max(0, min(fairy_y, 600 - fairy_img.get_height()))

        screen.fill(settings['screen_background'])
        screen.blit(fairy_img, (fairy_x, fairy_y))
        pygame.display.flip()
        clock.tick(settings['fps'])


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Светлячки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    pygame.mouse.set_visible(False)

    clock = pygame.time.Clock()
    screen.fill(settings['screen_background'])

    cursor = Cursor(screen)

    start_menu(screen, clock, cursor)
    game()

    pygame.quit()
