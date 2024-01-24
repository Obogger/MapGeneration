import pygame
import random

pygame.init()
pygame.font.init()


def make_grid(size):
    grid = [[random.randint(0,1) for collum in range(size)] for row in range(size)]
    return grid

def surrounding_area_population(grid, row_index, pixel_index):
    count = 0
    if grid[row_index][pixel_index - 1]:
        count += 1
    if grid[row_index - 1][pixel_index]:
        count += 1
    if grid[row_index - 1][pixel_index - 1]:
        count += 1

    pixel_index = -1 if pixel_index == len(grid[row_index]) - 1 else pixel_index
    if grid[row_index][pixel_index + 1]:
        count += 1
    if grid[row_index-1][pixel_index + 1]:
        count += 1


    row_index = -1 if row_index == len(grid) - 1 else row_index
    if grid[row_index + 1][pixel_index]:
        count += 1
    if grid[row_index + 1][pixel_index - 1]:
        count += 1

    if grid[row_index + 1][pixel_index + 1]:
        count += 1

    
    return count

def run(grid):
    grid_size = 100
    PIXEL_SIZE = 7
    is_iterating = False
    running = True
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Anonymous-Pro-B", 30)

    while running:
        is_iterating = False
        screen.fill("purple")
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        text_surface = font.render(str(), False, (0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_iterating = True
                if event.key == pygame.K_r:
                    grid = make_grid(grid_size)
        for row_index in range(len(grid)):
            for pixel_index in range(len(grid[row_index])):
                if grid[row_index][pixel_index] == 1:
                    cell = pygame.Rect((0 + PIXEL_SIZE*pixel_index, 0 + PIXEL_SIZE * row_index), (PIXEL_SIZE,PIXEL_SIZE))
                    pygame.draw.rect(screen, "black", cell)
                else:
                    pass

        if is_iterating:
            for row_index in range(len(grid)):
                for pixel_index in range(len(grid[row_index])):
                    level = surrounding_area_population(grid, row_index, pixel_index)
                    if level >= 5:
                        grid[row_index][pixel_index] = 1
                    elif level <= 3:
                        grid[row_index][pixel_index] = 0
                    #print(level)
        # flip() the display to put your work on screen
        pygame.display.flip()

        #clock.tick(60)  # limits FPS to 60

run(make_grid(100))

pygame.quit()
