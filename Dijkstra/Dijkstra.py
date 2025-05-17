import numpy as np
import heapq

width = 10
height = 10
locations = np.zeros((width, height))

locations[np.random.rand(width, height) > 0.8] = 1
locations[(0,0)] = 0

visited_locations = []
unvisited_locations = []
start_location = (0, 0)

nodes = {(x, y): [] for x in range(width) for y in range(height)}

# // remove "1" from possible locations to visit
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
    if node_cords[0] < width - 1:
        neighbouring_node = (node_cords[0] + 1, node_cords[1])
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    # // up
    if node_cords[1] > 0:
        neighbouring_node = (node_cords[0], node_cords[1] - 1)
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    # // down
    if node_cords[1] < height - 1:
        neighbouring_node = (node_cords[0], node_cords[1] + 1)
        if neighbouring_node in nodes.keys():
            neighbours.append(neighbouring_node)

    nodes[node_cords] = neighbours

# // Setup for cords
previous = {cords: None for cords in nodes.keys()}
visited = {cords: False for cords in nodes.keys()}
distances = {cords: float("inf") for cords in nodes.keys()}
distances[start_location] = 0

# // Create priority queue and add starting location
queue = []
heapq.heappush(queue, (0, start_location))

# // Start main loop, keep going until queue is empty
while queue:
    removed_distance, removed_location = queue.pop(0)
    visited[removed_location] = True

    # // check which neighbours to visit
    for neighbour in nodes[removed_location]:
        if visited[neighbour]:
            continue

        # // if a better path is found, update the dictionairies keeping track of the shortest path/distance
        new_distance = removed_distance + 1
        if new_distance < distances[neighbour]:
            distances[neighbour] = new_distance
            previous[neighbour] = removed_location
            heapq.heappush(queue, (new_distance, neighbour))

print(distances[(width - 1, height -1)])