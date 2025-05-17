import heapq
import numpy as np
import time

import pygame

################################## Dijkstra setup ##############################################
maze_width = maze_height = 50

locations = np.zeros((maze_width, maze_height))
locations[np.random.rand(maze_width, maze_height) > 0.8] = 1

start_location = (0, 0)
locations[start_location] = 0

visited_locations = []
unvisited_locations = []

nodes = {(x, y): [] for x in range(maze_width) for y in range(maze_height)}

# // Setup for cords
previous = {cords: None for cords in nodes.keys()}
visited = {cords: False for cords in nodes.keys()}
distances = {cords: float("inf") for cords in nodes.keys()}
distances[start_location] = 0

# // Create priority queue and add starting location
queue = []
heapq.heappush(queue, (0, start_location))

# // remove the rocks from possible locations
rocks = []
for node_cords, neighbours in nodes.items():
    row = locations[node_cords[0]]
    if row[node_cords[1]] == 1:
        rocks.append(node_cords)

for location in rocks:
    del nodes[location]

# // find neighbours for all locations
for node_cords, _ in nodes.items():
    neighbours = []

    # // left
    if node_cords[0] > 0:
        neighbouring_node = (node_cords[0] - 1, node_cords[1])
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    # // right
    if node_cords[0] < maze_width - 1:
        neighbouring_node = (node_cords[0] + 1, node_cords[1])
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    # // up
    if node_cords[1] > 0:
        neighbouring_node = (node_cords[0], node_cords[1] - 1)
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    # // down
    if node_cords[1] < maze_height - 1:
        neighbouring_node = (node_cords[0], node_cords[1] + 1)
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    nodes[node_cords] = neighbours

################################## Pygame setup ##############################################
pygame.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
screen.fill("white")
block_size_x, block_size_y = (screen_width//maze_width, screen_height//maze_height)

# // Initialize grid
# // draw empty locations and rocks
for y in range(0, screen_height, block_size_y):
    for x in range(0, screen_width, block_size_x):
        rect = pygame.Rect(x, y, block_size_x, block_size_y)

        position = (x//block_size_x, y//block_size_y)
        if position not in rocks:
            pygame.draw.rect(screen, (255, 255, 255), rect, )
        else:
            pygame.draw.rect(screen, (0, 0, 0), rect,)

# // Color starting location
rect = pygame.Rect(0, 0, block_size_x, block_size_y)
pygame.draw.rect(screen, (255, 0, 0), rect)

# // Update grid lines, so they don't get overlapped by the blocks
for begin_location in range(0, screen_height, block_size_y):
    pygame.draw.line(screen, (0, 0, 0), (0, begin_location), (screen_width, begin_location))
    pygame.draw.line(screen, (0, 0, 0), (begin_location, 0), (begin_location, screen_height))
pygame.display.update()

found = False
clicked_tile = None

# // Wait for user to select end location and mark its position
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        # // Find position of mouse click and calculate the position on the grid
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            mouse_x = mouse_pos[0]
            mouse_y = mouse_pos[1]

            # // In the case that the clicked tile is not a rock, mark that tile with a golden squar
            clicked_tile = (mouse_x // block_size_x, mouse_y // block_size_y)
            if clicked_tile not in rocks:
                found = True
                rect = pygame.Rect(clicked_tile[0] * block_size_x, clicked_tile[1] * block_size_y, block_size_x, block_size_y)
                pygame.draw.rect(screen, (255, 215, 0), rect)
                pygame.display.update()
                break

    if found:
        end_location = clicked_tile
        break


################################## main loop ##############################################
while queue:
    removed_distance, removed_location = queue.pop(0)
    visited[removed_location] = True

    # // check which neighbours to visit
    for neighbour in nodes[removed_location]:
        if visited[neighbour]:
            continue
        else:
            rect = pygame.Rect(block_size_x * neighbour[0], block_size_y * neighbour[1], block_size_x, block_size_y)
            pygame.draw.rect(screen, (0, 255, 0), rect)

        # // if a better path is found, update the dictionairies keeping track of the shortest path/distance
        new_distance = removed_distance + 1
        if new_distance < distances[neighbour]:
            distances[neighbour] = new_distance
            previous[neighbour] = removed_location
            heapq.heappush(queue, (new_distance, neighbour))

    # // Mark location as visited in pygame
    rect = pygame.Rect(block_size_x * removed_location[0], block_size_y * removed_location[1], block_size_x, block_size_y)
    pygame.draw.rect(screen, (255, 0, 0), rect)

    # // Update grid lines, so they don't get overlapped by the blocks
    for begin_location in range(0, screen_height, block_size_y):
        pygame.draw.line(screen, (0, 0, 0), (0, begin_location), (screen_width, begin_location))
        pygame.draw.line(screen, (0, 0, 0), (begin_location, 0), (begin_location, screen_height))
    pygame.display.update()
    time.sleep(0.01)


################################## show shortest path ##############################################
# // Find the shortest path by going in reverse order from the end location
previous_location = previous[end_location]
shortest_path = [end_location, previous_location]

while previous_location != (0, 0):
    previous_location = previous[previous_location]
    shortest_path.append(previous_location)

# // Reverse order from end -> start to start -> end
shortest_path.reverse()

rect = pygame.Rect(clicked_tile[0] * block_size_x, clicked_tile[1] * block_size_y, block_size_x, block_size_y)
pygame.draw.rect(screen, (255, 215, 0), rect)
pygame.display.update()

# // Fill the path in green on the screen
for tile_location in shortest_path:
    rect = pygame.Rect(block_size_x * tile_location[0], block_size_y * tile_location[1], block_size_x, block_size_y)
    pygame.draw.rect(screen, (0, 255, 0), rect)
    pygame.display.update()

    time.sleep(0.1)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
