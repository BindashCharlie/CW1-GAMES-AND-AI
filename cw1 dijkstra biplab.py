import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra's Algorithm - BIPLAB TWATI")

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

# Dijkstra's Algorithm
def dijkstra(graph, start, target):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (cost, node)
    came_from = {}
    shortest_distances = {node: float('inf') for node in graph}
    shortest_distances[start] = 0

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == target:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            path.reverse()
            return path, shortest_distances[target]

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < shortest_distances[neighbor]:
                shortest_distances[neighbor] = distance
                came_from[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    return None, float('inf')

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
shortest_path, total_cost = dijkstra(graph, start_node, end_node)
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
