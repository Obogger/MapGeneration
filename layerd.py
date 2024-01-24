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

def polish_map(saved_grids): 
    polished_grid = []
    extra_index = 0
    for row in saved_grids[0]:
        for _ in range(8):
            polished_grid.append([])
            for pixel in row:
                for _ in range(8):
                    polished_grid[extra_index].append(pixel)
            extra_index += 1
    extra_index = 0
    extra_extra_index = 0
    for row in saved_grids[1]:
        for _ in range(4):
            extra_extra_index = 0
            for pixel in range(len(row)-1):
                for _ in range(4):
                    polished_grid[extra_index][extra_extra_index] += 0.5 * row[pixel]
                    extra_extra_index += 1
            extra_index += 1
    extra_index = 0
    extra_extra_index = 0
    for row in saved_grids[2]:
        for _ in range(2):
            extra_extra_index = 0
            for pixel in range(len(row)-1):
                for _ in range(2):
                    polished_grid[extra_index][extra_extra_index] += 0.25 * row[pixel]
                    extra_extra_index += 1
            extra_index += 1
    vintegrette = 25
    vintegrette_clone = 25
    vintegrette_clone_clone = 25
    for i in range(len(polished_grid)):
        if i < vintegrette:
            polished_grid[i] = [(x + (vintegrette_clone * 50 / (i +1))) for x in polished_grid[i]]
        if i + vintegrette >= len(polished_grid):
            polished_grid[i] = [(x + (vintegrette_clone * 50 / vintegrette)) for x in polished_grid[i]]
            vintegrette -= 1
        vintegrette_clone_clone = 25
        for j in range(len(polished_grid[i])):
            vintegrettex = 25
            if j < vintegrettex:
                polished_grid[i][j] += (vintegrette_clone * 50) / (j + 1)
            if j + vintegrettex >= len(polished_grid[i]):
                if vintegrette_clone_clone == 0:
                    vintegrette_clone_clone = 1
                polished_grid[i][j]  += (vintegrette_clone * 50) / vintegrette_clone_clone
                vintegrette_clone_clone -= 1
            polished_grid[i][j] += 0.125 * saved_grids[3][i][j]
            polished_grid[i][j] = polished_grid[i][j] / (1+0.5+0.25+0.125)
    return polished_grid

def water_clamp(pixel, water_level):
    if pixel > water_level:
        pixel = 255
    else:
        pass
    return pixel
    
def move_camera(deltax, deltay):
    pass
    return deltax, deltay

def run(grid):
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Anonymous-Pro-B", 30)
    background_color = [(255,255,255),(50,20,150), (0,0,0)]
    color_index = 0
    resolution = 0.5
    GRID_SIZES = [int(100 * resolution), int(200 * resolution), int(400 * resolution), int(800 * resolution)]
    saved_grids = [0,0,0,0]
    grid_size = GRID_SIZES[0]
    water_level = 125


    map_index = 0
    PIXEL_SIZE = 4
    running = True
    camera_offset_x = 0
    camera_offset_y = 0
    deltax = 0
    deltay = 0
    SPEED = 100

    while running:
        dt = clock.tick()/1000
        is_iterating_sharp = False
        is_iterating_smooth = False
        screen.fill(background_color[color_index])
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        text_surface = font.render(str(), False, (0, 0, 0))
        """
        Space: Iterate Sharp
        WASD: Move map
        O: zoom out
        I: zoom in
        M: Change color of background
        F: Itareate smooth
        R: Reset current grid
        J: Save current_grid and start next
        P: Reset to small gridsize again
        """
        camera_offset_y += deltay *dt
        camera_offset_x += deltax * dt
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    deltay += SPEED
                if event.key == pygame.K_s:
                    deltay -= SPEED
                if event.key == pygame.K_d:
                    deltax -= SPEED
                if event.key == pygame.K_a:
                    deltax += SPEED
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    is_iterating_sharp = True
                if event.key == pygame.K_m:
                    if color_index < len(background_color) - 1:
                        color_index += 1
                    else:
                        color_index = 0
                if event.key == pygame.K_f:
                    is_iterating_smooth = True
                if event.key == pygame.K_r:
                    grid = make_grid(grid_size)
                if event.key == pygame.K_w:
                    deltay -= SPEED
                if event.key == pygame.K_s:
                    deltay += SPEED
                if event.key == pygame.K_a:
                    deltax -= SPEED
                if event.key == pygame.K_o:
                    if PIXEL_SIZE == 1:
                        pass
                    else:
                        PIXEL_SIZE -= 1
                if event.key == pygame.K_i:
                    PIXEL_SIZE += 1
                if event.key == pygame.K_d:
                    deltax += SPEED
                if event.key == pygame.K_j:
                    match map_index:
                        case 0:
                            saved_grids[0] = grid.copy()
                            grid_size = GRID_SIZES[1]
                            map_index = 1
                            grid = make_grid(grid_size)

                        case 1:
                            saved_grids[1] = grid.copy()
                            grid_size = GRID_SIZES[2]
                            map_index = 2
                            grid = make_grid(grid_size)
                        case 2:
                            saved_grids[2] = grid.copy()
                            grid_size = GRID_SIZES[3]
                            map_index = 3
                            grid = make_grid(grid_size)
                        case 3:
                            saved_grids[3] = grid.copy()
                            grid = polish_map(saved_grids)
                if event.key == pygame.K_p:
                    map_index = 0
                    grid_size = GRID_SIZES[0]
                    grid = make_grid(grid_size)
                

        for row_index in range(len(grid)):
            if PIXEL_SIZE * row_index + camera_offset_y > 720:
                break
            if PIXEL_SIZE * row_index + camera_offset_y < 0:
                pass
            else:   
                for pixel_index in range(len(grid[row_index])):
                    if PIXEL_SIZE * pixel_index + camera_offset_x > 1280:
                        break
                    if PIXEL_SIZE * pixel_index + camera_offset_x < 0:
                        pass
                    else:
                        cell_surface = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
                        #cell_surface.set_alpha(water_clamp(grid[row_index][pixel_index], water_level))
                        if grid[row_index][pixel_index] >= water_level:
                            if grid[row_index][pixel_index] > 255 * 3:
                                cell_surface.fill((255 / 3,255 / 3,150))
                            else:
                                cell_surface.fill((grid[row_index][pixel_index]/3,grid[row_index][pixel_index]/3,150))

                        else:
                            cell_surface.fill((grid[row_index][pixel_index],150,grid[row_index][pixel_index]))
                        screen.blit(cell_surface, (0 + PIXEL_SIZE*pixel_index + camera_offset_x, 0 + PIXEL_SIZE * row_index + camera_offset_y))

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
