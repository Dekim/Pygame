import sys
import pygame


class Button:
    def __init__(self, text: str, pos: tuple[int, int], surface: pygame.Surface):
        self.text = text
        self.pos = pos
        self.screen = surface
        self.start = None
        self.end = None

    def draw(self):
        font = pygame.font.SysFont("Times New Roman", 30)
        text = font.render(self.text, True, (255, 255, 255))
        tx, ty = text.get_size()
        x, y = self.pos
        self.start = (x - 25, y - (50 - ty) / 2)
        self.end = (tx + 50, 50)
        pygame.draw.rect(self.screen, (255, 255, 255), (*self.start, *self.end), 3)
        self.screen.blit(text, self.pos)

    def clicked(self, x, y):
        return all((x > self.start[0], x < self.end[0] + self.pos[0], y > self.start[1], y < self.end[1] + self.pos[1]))


def scope_draw(screen: pygame.Surface):
    # TODO
    # Получение данных из файла
    font = pygame.font.SysFont("Times New Roman", 30)
    text = font.render("Таблица рекордов", True, (255, 255, 255))
    screen.blit(text, (550, 100))


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Светлячки')
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)

    running = True
    x_pos = 0
    fps = 60
    clock = pygame.time.Clock()
    screen.fill((11, 11, 11))

    play_btn = Button("Играть", (200, 200), screen)
    exit_btn = Button("Выход", (202, 300), screen)
    play_btn.draw()
    exit_btn.draw()
    scope_draw(screen)

    cursor = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(cursor, (133, 200, 0, 200), (20, 20), 20, 0)
    screen.blit(cursor, (-40, 0))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                x, y = event.pos
                screen.fill((11, 11, 11))

                # Отрисовка элементов
                play_btn.draw()
                exit_btn.draw()
                scope_draw(screen)

                screen.blit(cursor, (x - 20, y - 20))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if exit_btn.clicked(*event.pos):
                    sys.exit(0)

        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
