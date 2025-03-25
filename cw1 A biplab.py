import pygame
import sys
import heapq

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Algorithm - BIPLAB TWATI")

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

# Heuristic function: Euclidean distance
def heuristic(node1, node2):
    x1, y1 = node_coords[node1]
    x2, y2 = node_coords[node2]
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5  # Euclidean distance

# A* algorithm
def a_star_search(graph, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))  # (priority, node)
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    f_score = {node: float('inf') for node in graph}
    f_score[start] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]

        for neighbor, weight in graph[current].items():
            tentative_g_score = g_score[current] + weight

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))

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
shortest_path, total_cost = a_star_search(graph, start_node, end_node)
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
