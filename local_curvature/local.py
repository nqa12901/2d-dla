import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt
from collections import defaultdict

# PARAMETERS INITIALIZATIONS:
N = 2000  # Number of Particles in Aggregate
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
    A = 10.0  # Parameter for probability function
    B = 0.50  # Parameter for probability function
    L = 5.0 * diameter  # Sample Cell size
    C = 0.01  # Min bound on probability p

    n = 0  # Particle count inside cell
    for i in range(ind):
        if abs(x[i, 0] - tx) < L and abs(x[i, 1] - ty) < L:
            n += 1  # Count particles within surrounding L x L cell

    n0 = ((L - 1) / 2) / L  # Particle count for straight line of particles
    nl = n / (L * L)
    p = A * (nl - n0) * B  # Evaluate p

    if p < C:
        p = C  # Ensure p >= C

    return p

def main():
    start = time.time()  # Counting steps (as a measure of time)
    n0 = 1  # Number of initial particles
    global counts
    counts = 0

    # Create Distribution of Initial Particles:
    for i in range(n0):
        x[i, 0] = 0
        x[i, 1] = 0
        hash_grid[grid_hash(0, 0)].append(i)
    maxx, maxy = 0, 0
    rmax = 2.0 * r_step

    # Set up the plot
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter(x[:, 0], x[:, 1], s=1)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # DLA Start:
    for i in range(n0, N):
        rmax = math.sqrt(maxx * maxx + maxy * maxy)
        r_spawn = rmax + 2.0 * diameter
        r_kill = r_spawn + 2.0 * diameter

        # Initialize Particle i:
        theta = 2 * PI * random.random()
        tx = r_spawn * math.cos(theta)
        ty = r_spawn * math.sin(theta)
        r = math.sqrt(tx * tx + ty * ty)
        bound = False

        # Simulate Brownian Motion Until Particle is Bound:
        while not bound:
            # Random Walk:
            theta = 2 * PI * random.random()
            tx += r_step * math.cos(theta) - bias * tx / r
            ty += r_step * math.sin(theta) - bias * ty / r
            r = math.sqrt(tx * tx + ty * ty)
            counts += 1
            if r > r_kill:
                # Reinitialize Particle
                theta = 2 * PI * random.random()
                tx = r_spawn * math.cos(theta)
                ty = r_spawn * math.sin(theta)
                r = math.sqrt(tx * tx + ty * ty)
                bound = False
            bound = bindcheck(i, tx, ty)

        if bound:
            hash_grid[grid_hash(tx, ty)].append(i)

        if x[i, 0] > maxx:
            maxx = x[i, 0]
        if x[i, 1] > maxy:
            maxy = x[i, 1]
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

if __name__ == "__main__":
    main()
