import pygame
import sys
from itertools import permutations

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brute Force Algorithm- BIPLAB TWATI")

# Color scheme
BACKGROUND = (245, 245, 220)
NODE_COLOR = (70, 130, 180)
EDGE_COLOR = (105, 105, 105)
PATH_COLOR = (220, 20, 60)

# Graph configuration
graph = {
    'X': {'Y': 3, 'Z': 8},
    'Y': {'X': 2, 'Z': 4, 'W': 6},
    'Z': {'X': 5, 'Y': 3, 'W': 2},
    'W': {'Y': 4, 'Z': 5}
}

# Node coordinates for visualization
node_coords = {
    'X': (150, 300),
    'Y': (350, 150),
    'Z': (350, 450),
    'W': (650, 300)
}

def brute_force_search(graph, start, target):
    nodes = list(graph.keys())
    nodes.remove(start)
    nodes.remove(target)
    
    shortest_path = None
    min_cost = float('inf')
    
    for permutation in permutations(nodes):
        current_path = [start] + list(permutation) + [target]
        total_cost = 0
        
        try:
            for i in range(len(current_path)-1):
                total_cost += graph[current_path[i]][current_path[i+1]]
        except KeyError:
            continue
        
        if total_cost < min_cost:
            min_cost = total_cost
            shortest_path = current_path
            
    return shortest_path, min_cost

def draw_interface():
    screen.fill(BACKGROUND)
    
    # Draw edges with weights
    drawn_edges = set()
    for node, connections in graph.items():
        for neighbor, weight in connections.items():
            if (node, neighbor) not in drawn_edges and (neighbor, node) not in drawn_edges:
                pygame.draw.line(screen, EDGE_COLOR, 
                               node_coords[node], node_coords[neighbor], 2)
                
                # Calculate weight label position
                mid_x = (node_coords[node][0] + node_coords[neighbor][0]) // 2
                mid_y = (node_coords[node][1] + node_coords[neighbor][1]) // 2
                font = pygame.font.Font(None, 28)
                text = font.render(str(weight), True, EDGE_COLOR)
                screen.blit(text, (mid_x + 5, mid_y - 15))
                
                drawn_edges.add((node, neighbor))
    
    # Draw nodes
    for node, pos in node_coords.items():
        pygame.draw.circle(screen, NODE_COLOR, pos, 25)
        label = pygame.font.Font(None, 40).render(node, True, (255, 255, 255))
        screen.blit(label, (pos[0]-10, pos[1]-12))
    
    # Highlight optimal path
    if shortest_path:
        for i in range(len(shortest_path)-1):
            start = node_coords[shortest_path[i]]
            end = node_coords[shortest_path[i+1]]
            pygame.draw.line(screen, PATH_COLOR, start, end, 6)
    
    pygame.display.flip()

# Calculate path
start_node = 'X'
end_node = 'W'
shortest_path, total_cost = brute_force_search(graph, start_node, end_node)
print(f"Optimal Path: {' → '.join(shortest_path)}")
print(f"Total Cost: {total_cost}")

# Visualization loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    draw_interface()

pygame.quit()
sys.exit()