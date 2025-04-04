import pygame
import random
import math

pygame.init()

# definire constante

FPS = 60

WIDTH, HEIGHT = 800, 800
ROWS = 4
COLS = 4

RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

OUTLINE_COLOR = (50, 129, 168)
OUTLINE_THICKNESS = 8
BACKGROUND_COLOR = (50, 60, 168)
FONT_COLOR = (169, 149, 50)

# crearea unui pygame window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - GAME")

FONT = pygame.font.SysFont('Arial', 60, bold = True)
MOVE_VEL = 20

class Tile:
    # culorile pentru fiecare bloc din jocul original 2048
    COLORS = [
        (237, 229, 218),
        (238, 225, 201),
        (243, 178, 122),
        (246, 150, 101),
        (247, 124, 95),
        (247, 95, 59),
        (237, 208, 115),
        (237, 204, 99),
        (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = col * RECT_HEIGHT

    def culoare(self):
        # pentru blocul de culoare 2 vrem sa obtinem indexul 0 din COLORS, pentru blocul de culoare 4 vrem indexul 1 etc.
        # blocurile sunt puteri ale lui 2 deci putem folosi un logaritm in baza 2
        index_color = int(math.log2(self.value)) - 1
        color = self.COLORS[index_color]
        return color

    def desenare(self, screen):
        color = self.culoare()
        pygame.draw.rect(screen, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        screen.blit(
            text, (self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                   self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
                   ),
        )

    def set_pozitie(self):
        pass

    def mutare(self, delta):
        pass


def desenare_grid(screen):
    # delimiteaza patratelele ecranului
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(screen, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for cols in range(1, COLS):
        x = cols * RECT_WIDTH
        pygame.draw.line(screen, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(screen, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def desenare(screen, tiles):
    screen.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.desenare(screen)

    desenare_grid(screen)

    pygame.display.update()

def generare_random(tiles):
    row = None
    col = None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        if f"{row}{col}" not in tiles:
            break

    return row, col

def generare_blocuri():
    # vom folosi un dictionar pentru a putea indentifica foarte rapid blocul dupa linie si coloana
    tiles = {}
    for _ in range(2):
        row, col = generare_random(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(screen):
    clock = pygame.time.Clock()
    run_loop = True

    # vom folosi un dictionar pentru a putea indentifica foarte rapid blocul dupa linie si coloana
    tiles = generare_blocuri()

    while run_loop:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
                break

        desenare(screen, tiles)

    pygame.quit()


if __name__ == "__main__":
    main(SCREEN)




