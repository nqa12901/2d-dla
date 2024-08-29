import numpy as np
import random
import math
import time
import matplotlib.pyplot as plt
from collections import defaultdict
from IPython.display import display, clear_output

def grid_hash(tx, ty, grid_size):
    return (int(tx // grid_size), int(ty // grid_size))

def bindcheck(ind, tx, ty, x, r_bind, hash_grid, grid_size):
    bound = False
    gx, gy = grid_hash(tx, ty, grid_size)
    neighbors = [(gx+i, gy+j) for i in range(-1, 2) for j in range(-1, 2)]
    for cell in neighbors:
        for i in hash_grid[cell]:
            dx = tx - x[i, 0]
            dy = ty - x[i, 1]
            r2 = dx * dx + dy * dy
            if r2 <= r_bind * r_bind:
                bound = True
                break
        if bound:
            break
    return bound

def P(ind, tx, ty):
    return 1  # Sticking probability

def dla_algorithm(N=1000, bias=0, diameter=1.0, r_step=None, r_bind=None):
    if r_step is None:
        r_step = 0.5 * diameter
    if r_bind is None:
        r_bind = 1 * diameter

    x = np.zeros((N, 3))
    seed = int(time.time())
    random.seed(seed)
    
    grid_size = 2 * r_bind
    hash_grid = defaultdict(list)

    PI = 4.0 * math.atan(1.0)
    
    plt.ion()
    fig, ax = plt.subplots(figsize=(8, 8))
    scatter = ax.scatter(x[:, 0], x[:, 1], s=1)
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    n0 = 1  # Number of initial particles
    counts = 0
    for i in range(n0):
        x[i, 0] = 0
        x[i, 1] = 0
        hash_grid[grid_hash(0, 0, grid_size)].append(i)
    
    maxx, maxy = 0, 0
    rmax = 2.0 * r_step

    for i in range(n0, N):
        display(num_particles_slider, bias_slider, diameter_slider, r_step_slider, r_bind_slider, start_button)
        rmax = math.sqrt(maxx * maxx + maxy * maxy)
        r_spawn = rmax + 2.0 * diameter
        r_kill = r_spawn + 2.0 * diameter

        theta = 2 * PI * random.random()
        tx = r_spawn * math.cos(theta)
        ty = r_spawn * math.sin(theta)
        r = math.sqrt(tx * tx + ty * ty)
        bound = False

        while not bound:
            theta = 2 * PI * random.random()
            tx += r_step * math.cos(theta) - bias * tx / r
            ty += r_step * math.sin(theta) - bias * ty / r
            r = math.sqrt(tx * tx + ty * ty)
            counts += 1
            if r > r_kill:
                theta = 2 * PI * random.random()
                tx = r_spawn * math.cos(theta)
                ty = r_spawn * math.sin(theta)
                r = math.sqrt(tx * tx + ty * ty)
                bound = False
            bound = bindcheck(i, tx, ty, x, r_bind, hash_grid, grid_size)

        if bound:
            hash_grid[grid_hash(tx, ty, grid_size)].append(i)
            x[i, 0] = tx
            x[i, 1] = ty

        if x[i, 0] > maxx:
            maxx = x[i, 0]
        if x[i, 1] > maxy:
            maxy = x[i, 1]

        scatter.set_offsets(x[:, :2])
        ax.set_title(f'Diffusion Limited Aggregation\nParticles Added: {i+1}')
        
        clear_output(wait=True)
        display(fig)
        plt.pause(0.01)

    plt.ioff()
    plt.show()

# Run the algorithm
num_particles_slider = widgets.IntSlider(
    value=1000,
    min=100,
    max=10000,
    step=100,
    description='Num Particles:',
    continuous_update=False
)

bias_slider = widgets.FloatSlider(
    value=0,
    min=-1,
    max=1,
    step=0.01,
    description='Bias:',
    continuous_update=False
)

diameter_slider = widgets.FloatSlider(
    value=1.0,
    min=0.1,
    max=10.0,
    step=0.1,
    description='Diameter:',
    continuous_update=False
)

r_step_slider = widgets.FloatSlider(
    value=0.5,
    min=0.1,
    max=10.0,
    step=0.1,
    description='Step Size:',
    continuous_update=False
)

r_bind_slider = widgets.FloatSlider(
    value=1.0,
    min=0.1,
    max=10.0,
    step=0.1,
    description='Bind Distance:',
    continuous_update=False
)

start_button = widgets.Button(description="Start")

# Hàm để gọi khi nút start được bấm
def on_start_button_clicked(b):
    display(num_particles_slider, bias_slider, diameter_slider, r_step_slider, r_bind_slider, start_button)
    num_particles = num_particles_slider.value
    bias = bias_slider.value
    diameter = diameter_slider.value
    r_step = r_step_slider.value
    r_bind = r_bind_slider.value  
    dla_algorithm(N=num_particles, bias=bias, diameter=diameter, r_step=r_step, r_bind=r_bind)
    

# Kết nối hàm với sự kiện click của nút start
start_button.on_click(on_start_button_clicked)

# Hiển thị GUI
display(num_particles_slider, bias_slider, diameter_slider, r_step_slider, r_bind_slider, start_button)