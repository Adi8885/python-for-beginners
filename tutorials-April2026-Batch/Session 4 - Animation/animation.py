"""
Simple Boids Simulation
Watch emergent flocking behavior!
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

class Boid:
    def __init__(self, x, y):
        self.position = np.array([x, y], dtype=float)
        self.velocity = np.random.rand(2) * 2 - 1 # Random direction
        self.max_speed = 2
    
    def update(self, boids):
        # Rule 1: Separation
        separation = self.separate(boids)
    
        # Rule 2: Alignment
        alignment = self.align(boids)
    
        # Rule 3: Cohesion
        cohesion = self.cohere(boids)
    
        # Combine rules
        self.velocity += separation * 1.5
        self.velocity += alignment * 1.0
        self.velocity += cohesion * 1.0
    
        # Limit speed
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = (self.velocity / speed) * self.max_speed
    
        # Move
        self.position += self.velocity
    
        # Wrap around screen
        self.position = self.position % 100
    
    def separate(self, boids):
        """Rule 1: Avoid crowding"""
        steer = np.array([0.0, 0.0])
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if distance < 5 and distance > 0:
                diff = self.position - boid.position
                steer += diff / distance
        return steer
    
    def align(self, boids):
        """Rule 2: Match velocity"""
        avg_velocity = np.array([0.0, 0.0])
        count = 0
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if distance < 15:
                avg_velocity += boid.velocity
                count += 1
        if count > 0:
            avg_velocity /= count
            return avg_velocity - self.velocity
        return avg_velocity
    
    def cohere(self, boids):
        """Rule 3: Move towards center"""
        center = np.array([0.0, 0.0])
        count = 0
        for boid in boids:
            distance = np.linalg.norm(self.position - boid.position)
            if distance < 20:
             center += boid.position
             count += 1
        if count > 0:
            center /= count
            return (center - self.position) * 0.01
        return center

# Create flock
num_boids = 50
boids = [Boid(np.random.rand() * 100, np.random.rand() * 100)
 for _ in range(num_boids)]

# Animate
fig, ax = plt.subplots(figsize=(8, 8))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect('equal')
scatter = ax.scatter([], [], c='blue', s=30)

def animate(frame):
    # Update all boids
    for boid in boids:
       boid.update(boids)

    # Get positions
    positions = np.array([boid.position for boid in boids])
    scatter.set_offsets(positions)
    
    ax.set_title(f'Boids Simulation - Frame {frame}', fontsize=14)
    return scatter,

anim = FuncAnimation(fig, animate, frames=200, interval=50, blit=True)
plt.show()
print("Watch the boids self-organize into flocks!")
print("No leader. Just 3 simple rules. Magic! ✨")