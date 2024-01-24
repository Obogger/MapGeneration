#1# Victory Royale
import pygame
import random
from operator import add

pygame.init()
pygame.font.init()

def make_grid(size : int) -> list:
    """Creates a list containing  random values either 0 or 255 organazied in 
    rows containing list[size][size] = [[255,0,0,0,255,255,255,0...], [0,0,0,0,255,255,255,0]...]"""
    grid = [[random.randint(0,1) * 255 for collum in range(size)] for row in range(size)]
    return grid

def binary_surrounding_population(
        grid : list, row_index : int, pixel_index : int) -> int:
    """Cheks to see if the surrounding 8 cells are lit or unlit and returns the 
    amount of lit cells"""

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

def alpha_shade_surrouning_population(grid, row_index, pixel_index):
    count = 0
    count += grid[row_index][pixel_index - 1]
    count += grid[row_index - 1][pixel_index]
    count += grid[row_index - 1][pixel_index - 1]

    pixel_index = -1 if pixel_index == len(grid[row_index]) - 1 else pixel_index
    count += grid[row_index][pixel_index + 1]
    count += grid[row_index-1][pixel_index + 1]


    row_index = -1 if row_index == len(grid) - 1 else row_index
    count += grid[row_index + 1][pixel_index]
    count += grid[row_index + 1][pixel_index - 1]

    count += grid[row_index + 1][pixel_index + 1]

    count = count / 8

    
    return count

def polish_map(small_grid, medium_grid, large_grid): 
    polished_grid = []
    extra_index = 0
    for row in small_grid:
        for _ in range(4):
            polished_grid.append([])
            for pixel in row:
                for _ in range(4):
                    #print(2)
                    polished_grid[extra_index].append(pixel)
            extra_index += 1
    extra_index = 0
    extra_extra_index = 0
    for row in medium_grid:
        for _ in range(2):
            extra_extra_index = 0
            for pixel in range(len(row)-1):
                for _ in range(2):
                    #print(2)
                    polished_grid[extra_index][extra_extra_index] += 0.5 * row[pixel]
                    extra_extra_index += 1
            extra_index += 1
    #print (polished_grid[0])
    vintegrette = 25
    vintegrette_clone = 25
    for i in range(len(polished_grid)):
        if i < vintegrette:
            polished_grid[i] = [(x + (vintegrette_clone * 50 / (i +1))) for x in polished_grid[i]]
        if i + vintegrette >= len(polished_grid):
            polished_grid[i] = [(x + (vintegrette_clone * 50 / vintegrette)) for x in polished_grid[i]]
            vintegrette -= 1
        for j in range(len(polished_grid[i])):
            vintegrettex = 25
            if j < vintegrettex:
                polished_grid[i][j] += (vintegrette_clone * 50) / (j + 1)
            if j + vintegrettex >= len(polished_grid[i]):
                polished_grid[i][j]  += (vintegrette_clone * 50) / vintegrettex
                vintegrettex -= 1
            polished_grid[i][j] += 0.25 * large_grid[i][j]
            polished_grid[i][j] = polished_grid[i][j] / (1+0.5+0.25)
    return polished_grid

def water_clamp(pixel, water_level):
    if pixel > water_level:
        pixel = 255
    else:
        pass
    return pixel
    


def run(grid):
    print(grid[0])
    resolution = 1
    SMALL_GRID_SIZE = int(100 * resolution)
    MEDIUM_GRID_SIZE = int(200 * resolution)
    LARGE_GRID_SIZE = int(400 * resolution)
    grid_size = SMALL_GRID_SIZE
    water_level = 125


    map_index = 0
    PIXEL_SIZE = 2
    running = True
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Anonymous-Pro-B", 30)

    while running:
        is_iterating_sharp = False
        is_iterating_smooth = False
        screen.fill((255,255,255))
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        text_surface = font.render(str(), False, (0, 0, 0))
        """
        Space: Iterate Sharp
        W: Itareate smooth
        R: Reset current grid
        J: Save current_grid and start next
        P: Reset to small gridsize again
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_iterating_sharp = True
                if event.key == pygame.K_w:
                    is_iterating_smooth = True
                if event.key == pygame.K_r:
                    grid = make_grid(grid_size)
                if event.key == pygame.K_j:
                    match map_index:
                        case 0:
                            small_grid = grid.copy()
                            grid_size = MEDIUM_GRID_SIZE
                            map_index = 1
                            grid = make_grid(grid_size)

                        case 1:
                            medium_grid = grid.copy()
                            grid_size = LARGE_GRID_SIZE
                            map_index = 2
                            grid = make_grid(grid_size)
                        case 2:
                            large_grid = grid.copy()
                            grid = polish_map(small_grid, medium_grid, large_grid)
                if event.key == pygame.K_p:
                    map_index = 0
                    grid_size = SMALL_GRID_SIZE
                    grid = make_grid(grid_size)
                

        for row_index in range(len(grid)):
            for pixel_index in range(len(grid[row_index])):
                cell_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
                cell_surface.set_alpha(water_clamp(grid[row_index][pixel_index], water_level))
                if grid[row_index][pixel_index] >= water_level:
                    cell_surface.fill((50,20,150))
                else:
                    cell_surface.fill((50,150,20))
                screen.blit(cell_surface, (0 + PIXEL_SIZE*pixel_index, 0 + PIXEL_SIZE * row_index))

        if is_iterating_sharp:
            for row_index in range(len(grid)):
                for pixel_index in range(len(grid[row_index])):
                    level = binary_surrounding_population(grid, row_index, pixel_index)
                    if level >= 5:
                        grid[row_index][pixel_index] = 255
                    elif level <= 3:
                        grid[row_index][pixel_index] = 0
        if is_iterating_smooth:
            for row_index in range(len(grid)):
                for pixel_index in range(len(grid[row_index])):
                    level = alpha_shade_surrouning_population(grid, row_index, pixel_index)
                    grid[row_index][pixel_index] = level
        # flip() the display to put your work on screen
        pygame.display.flip()

        #clock.tick(60)  # limits FPS to 60

run(make_grid(10))

pygame.quit()
