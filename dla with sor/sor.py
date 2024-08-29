import numpy as np
import matplotlib.pyplot as plt

def main():
    m, c, grow, n_particles, n_candidate, candidate, chance, particle_max, w, n = init()
    solve(n_particles, particle_max, c, candidate, n_candidate, grow, m, w, n, chance)

def init():
    m = 200
    c = generate_env(m)
    grow = np.zeros((m, m))
    n_particles = 0
    n_candidate = 0
    candidate = np.zeros((2, 0))
    chance = np.array([])
    particle_max = 10000
    w = 1.5
    n = 1
    x0, y0 = m // 2, m // 2
    grow, n_particles, candidate, n_candidate, c = add_particle(x0, y0, grow, n_candidate, n_particles, m, candidate, c)
    return m, c, grow, n_particles, n_candidate, candidate, chance, particle_max, w, n

def solve(n_particles, particle_max, c, candidate, n_candidate, grow, m, w, n, chance):
    fig, ax = plt.subplots(figsize=(8, 8))
    plt.ion()

    while n_particles <= particle_max:
        c = sor(c, w, m, grow)
        n_candidate = candidate.shape[1]
        chance = compute_probability(c, n_candidate, candidate, n, chance)
        random = np.random.rand(n_candidate)
        eaten_indices = np.where(chance > random)[0]
        
        elements_are_eaten = candidate[:, eaten_indices]
        chance = np.delete(chance, eaten_indices)
        candidate = np.delete(candidate, eaten_indices, axis=1)
        n_candidate -= len(eaten_indices)
        
        for element in elements_are_eaten.T:
            grow, n_particles, candidate, n_candidate, c = add_particle(int(element[0]), int(element[1]), grow, n_candidate, n_particles, m, candidate, c)
        
        ax.clear()
        ax.imshow(c, cmap='viridis')
        ax.imshow(grow, cmap='binary', alpha=0.3)
        ax.set_title(f'Particle: {n_particles}, Candidates: {n_candidate}')
        plt.pause(0.01)

    plt.ioff()
    plt.show()

def compute_probability(c, n_candidate, candidate, n, chance):
    if n_candidate != 0:
        probs = c[candidate[0].astype(int), candidate[1].astype(int)] ** n
        chance = probs / np.sum(probs)
    return chance

def sor(c, w, m, grow):
    for i in range(1, m-1):
        for j in range(1, m-1):
            if grow[i, j] == 1:
                continue
            c[i, j] = w/4 * (c[i+1, j] + c[i-1, j] + c[i, j+1] + c[i, j-1]) + (1-w) * c[i, j]
    return c

def add_particle(x, y, grow, n_candidate, n_particles, m, candidate, c):
    grow[x, y] = 1
    c[x, y] = 0
    n_particles += 1
    
    neighbors = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    for nx, ny in neighbors:
        if 0 <= nx < m and 0 <= ny < m and grow[nx, ny] == 0:
            candidate = np.column_stack((candidate, [nx, ny]))
            n_candidate += 1
    
    return grow, n_particles, candidate, n_candidate, c

def generate_env(m):
    r = m // 2
    x = np.zeros((m, m))
    c = np.arange(r-1, -1, -1)
    calc = m / 20
    
    for i in range(r):
        # x[c[i], :] = x[m-1-c[i], :] = -i/10
        # x[:, c[i]] = x[:, m-1-c[i]] = -i/10

        x[c[i], :] = x[m-1-c[i], :] = 1
        x[:, c[i]] = x[:, m-1-c[i]] = 1
    
    c = (x + calc) / 10
    return c

if __name__ == "__main__":
    main()