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
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (50, 60, 168)
FONT_COLOR = (169, 149, 50)

# crearea unui pygame window
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048 - GAME")

FONT = pygame.font.SysFont("comicsans", 60, bold = True)
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
        self.y = row * RECT_HEIGHT

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

    def set_pozitie(self, ceil = False):
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def mutare(self, delta):
        self.x += delta[0]
        self.y += delta[1]


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

def mutare_blocuri(screen, tiles, clock, direction):
    update = True
    blocks = set()

    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = (
            lambda  tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        )
        ceil = True

    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = (
            lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        )
        ceil = False

    while update:
        clock.tick(FPS)
        update = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue
            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.mutare(delta)
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                if merge_check(tile, next_tile):
                    tile.mutare(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.mutare(delta)
            else:
                continue

            tile.set_pozitie(ceil)
            update = True
        update_blocuri(screen, tiles, sorted_tiles)

    return end_miscare(tiles)

def end_miscare(tiles):
    if len(tiles) == 16:
        return "Ai pierdut"

    row, col = generare_random(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2,4]), row, col)
    return "Continua"


def update_blocuri(screen, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    desenare(screen, tiles)

def generare_blocuri():
    # vom folosi un dictionar pentru a putea indentifica foarte rapid blocul dupa linie si coloana
    tiles = {}
    for _ in range(2):
        row, col = generare_random(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

def desenare_butoane(screen, rect, text, font, culoareButon, culoareText):
    # desenarea propriu zisa a butonului
    pygame.draw.rect(screen, culoareButon, rect, border_radius=10)

    text_render = font.render(text, True, culoareText)

    # calculeaza pozitia centrata a textului
    text_x = rect.x + (rect.width - text_render.get_width()) // 2
    text_y = rect.y + (rect.height - text_render.get_height()) // 2

    # afiseaza textul
    screen.blit(text_render, (text_x, text_y))

def butoane_meniu(screen, start_rect, quit_rect):
    screen.fill((30, 30, 30))

    # desenez butonul pentru Start Game
    desenare_butoane(screen, start_rect, "Start Game", FONT, (0, 200, 0), (255, 255, 255))

    # desenez butonul pentru Quit
    desenare_butoane(screen, quit_rect, "Quit", FONT, (200, 0, 0), (255, 255, 255))

    pygame.display.update()

def meniu(screen):
    clock = pygame.time.Clock()
    start_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 110, 350, 100)
    quit_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 30, 350, 100)

    in_meniu = True

    while in_meniu:
        clock.tick(FPS)
        butoane_meniu(screen, start_rect, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    in_meniu = False
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mutare_blocuri(screen, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    mutare_blocuri(screen, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    mutare_blocuri(screen, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    mutare_blocuri(screen, tiles, clock, "down")

        desenare(screen, tiles)

    pygame.quit()


if __name__ == "__main__":
    meniu(SCREEN)
    main(SCREEN)




