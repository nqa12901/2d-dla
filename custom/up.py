import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.animation as animation

# PARAMETERS INITIALIZATIONS:
N = 4000  # Number of Particles in Aggregate
bias = 0  # Central tendency of random walkers (increase to speed up simulation)

# Random Number Generator Seed
seed = int(time.time())
random.seed(seed)

# OTHER INITIALIZATIONS:
diameter = 1.0  # Particle Diameter
r_step = 0.5 * diameter  # Step size
r_bind = 1 * diameter  # Distance to bind particle

# Particle Array
x = np.zeros((N, 3))

# OTHER CONSTANTS:
PI = 4.0 * math.atan(1.0)

# Spatial Hashing Initialization
grid_size = 2 * r_bind
hash_grid = defaultdict(list)

def grid_hash(tx, ty):
    return (int(tx // grid_size), int(ty // grid_size))

def bindcheck(ind, tx, ty):
    bound = False
    gx, gy = grid_hash(tx, ty)
    neighbors = [(gx+i, gy+j) for i in range(-1, 2) for j in range(-1, 2)]
    for cell in neighbors:
        for i in hash_grid[cell]:
            dx = tx - x[i, 0]
            dy = ty - x[i, 1]
            dr = math.sqrt(dx * dx + dy * dy)  # Distance between particles
            if dr < r_bind:
                R = random.random()
                if P(ind, tx, ty) > R:
                    # Bind the particle
                    x[ind, 0] = tx
                    x[ind, 1] = ty
                    x[ind, 2] = counts
                    bound = True
    return bound

def P(ind, tx, ty):
    return 0.1  # Sticking probability

def main():
    start = time.time()  # Counting steps (as a measure of time)
    n0 = 100  # Number of initial particles
    global counts
    counts = 0

    # Create Distribution of Initial Particles:
    for i in range(n0):
        x[i, 0] = i - 50
        x[i, 1] = 0
        hash_grid[grid_hash(x[i, 0], x[i, 1])].append(i)

    tymax = 10

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(4, 4))
    scatter = ax.scatter(x[:, 0], x[:, 1], s=1)
    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # DLA Start:
    for i in range(n0, N):

        # Initialize Particle i:
        tx = 100 * random.random() - 50
        ty = random.choice([tymax, -tymax])
        bound = False

        # Simulate Brownian Motion Until Particle is Bound:
        while not bound:
            # Random Walk:
            theta = 2 * PI * random.random()
            tx += r_step * math.cos(theta)
            ty += r_step * math.sin(theta) - bias * 0.1
            counts += 1
            if tx < -50 or tx > 50 or ty > 50:
                # Reinitialize Particle
                tx = 100 * random.random() - 50
                ty = random.choice([tymax, -tymax])
                bound = False
            bound = bindcheck(i, tx, ty)

        if bound:
            hash_grid[grid_hash(tx, ty)].append(i)
            if abs(ty) > tymax: 
                tymax = abs(ty) + 5

        print(f"Particle {i}: Bound at ({tx}, {ty})")

        # Update the scatter plot and title
        scatter.set_offsets(x[:, :2])
        ax.set_title(f'Diffusion Limited Aggregation\nParticles Added: {i+1}')
        fig.canvas.draw_idle()
        plt.pause(0.01)

    print(f"Number of Steps Taken: {counts}")
    end = time.time()
    processing_time = end - start
    print(f"Processing Time: {processing_time}")

    # Keep the plot open
    plt.ioff()
    plt.show()

    artists.append(scatter)

    # Gọi hàm để lưu video
    save_animation()

if __name__ == "__main__":
    main()
