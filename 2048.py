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

def desenare_grid(screen):
    # delimiteaza patratelele ecranului
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(screen, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for cols in range(1, COLS):
        x = cols * RECT_WIDTH
        pygame.draw.line(screen, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(screen, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

def desenare(screen):
    screen.fill(BACKGROUND_COLOR)

    desenare_grid(screen)

    pygame.display.update()



def main(screen):
    clock = pygame.time.Clock()
    run_loop = True

    while run_loop:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_loop = False
                break

        desenare(screen)

    pygame.quit()


if __name__ == "__main__":
    main(SCREEN)




