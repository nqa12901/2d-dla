import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# Define the city's geography (2D grid)
grid_size = 100
elevation_map = np.random.rand(grid_size, grid_size)  # random elevation map
water_bodies = np.zeros((grid_size, grid_size))  # initialize water bodies
water_bodies[20:40, 20:40] = 1  # add a lake in the middle

# Define the city's population and growth rate
population = 1000
growth_rate = 0.02

# Define the road network
road_network = np.zeros((grid_size, grid_size))  # initialize road network
road_network[grid_size//2, grid_size//2] = 1  # start with a single road in the CBD

# Define the DLA algorithm parameters
diffusion_rate = 0.5
aggregation_rate = 0.2

# Simulate the city's growth for 50 years
for year in range(50):
    # Calculate population density
    population_density = population / (grid_size ** 2)

    # Apply the DLA algorithm
    for i in range(grid_size):
        for j in range(grid_size):
            if road_network[i, j] == 1:
                # Diffusion: move to a neighboring cell with probability diffusion_rate
                if np.random.rand() < diffusion_rate:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    direction = np.random.choice(directions)
                    new_i, new_j = i + direction[0], j + direction[1]
                    if (0 <= new_i < grid_size) and (0 <= new_j < grid_size):
                        road_network[new_i, new_j] = 1

                # Aggregation: add a new road with probability aggregation_rate
                if np.random.rand() < aggregation_rate:
                    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    direction = np.random.choice(directions)
                    new_i, new_j = i + direction[0], j + direction[1]
                    if (0 <= new_i < grid_size) and (0 <= new_j < grid_size):
                        if road_network[new_i, new_j] == 0:
                            road_network[new_i, new_j] = 1

    # Update population and road network
    population *= (1 + growth_rate)
    road_network = road_network.astype(int)

# Visualize the road network as a graph
G = nx.Graph()
for i in range(grid_size):
    for j in range(grid_size):
        if road_network[i, j] == 1:
            G.add_node((i, j))
            for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                new_i, new_j = i + direction[0], j + direction[1]
                if (0 <= new_i < grid_size) and (0 <= new_j < grid_size):
                    if road_network[new_i, new_j] == 1:
                        G.add_edge((i, j), (new_i, new_j))

nx.draw(G, node_size=5, node_color='blue', edge_color='gray')
plt.show()