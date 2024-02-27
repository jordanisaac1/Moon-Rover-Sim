import pygame
import heapq
import random

# Initialize pygame
pygame.init()
clock = pygame.time.Clock()

VISION_RANGE = 4
# Constants
WIDTH, HEIGHT = 900, 900
GRID_SIZE = 60
CELL_SIZE = WIDTH // GRID_SIZE
START = (2, 2)

ROVER_COLOR = (0, 0, 128)

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Rover Navigation")

def generate_random_goal():
    """
    Generates a random goal that is not the same as the start position.
    
    :return: A random goal position.
    """
    goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    while goal == START:
        goal = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    return goal
        
GOAL = generate_random_goal()

def generate_random_obstacles(density):
    """
    Generates random obstacles based on the given density.
    
    :param density: Fraction of grid cells that should be obstacles.
    :return: List of obstacle coordinates.
    """
    num_obstacles = int(GRID_SIZE * GRID_SIZE * density)
    obstacles = []
    while len(obstacles) < num_obstacles:
        x = random.randint(0, GRID_SIZE - 1)
        y = random.randint(0, GRID_SIZE - 1)
        if (x, y) not in obstacles and (x, y) != START and (x, y) != GOAL:
            obstacles.append((x, y))
    return obstacles

OBSTACLES = generate_random_obstacles(0.00)


def octal_distance(a, b):
    dx = abs(a[0] - b[0])
    dy = abs(a[1] - b[1])
    return min(dx, dy) * 1.5 + abs(dx - dy)

def visible_obstacles(position):
    """Return the list of obstacles that are within the VISION_RANGE of the given position."""
    visible = []
    for obstacle in OBSTACLES:
        if abs(position[0] - obstacle[0]) <= VISION_RANGE and abs(position[1] - obstacle[1]) <= VISION_RANGE:
            visible.append(obstacle)
    return visible


def astar_search(start, goal):
    # open_set will contain nodes to visit, sorted by their heuristic (f_score)
    open_set = [(0, start)]  # Initialize with starting position

    local_obstacles = visible_obstacles(start)
    
    # A dictionary to remember which node led to the current node
    came_from = {}
    
    # Dictionary to store the cost to get to each node
    g_score = {node: float("inf") for row in range(GRID_SIZE) for node in [(row, col) for col in range(GRID_SIZE)]}
    g_score[start] = 0  # The cost to get to the start is zero
    
    # Dictionary to store the heuristic value for each node (cost to get there + estimated cost to goal)
    f_score = {node: float("inf") for row in range(GRID_SIZE) for node in [(row, col) for col in range(GRID_SIZE)]}
    f_score[start] = octal_distance(start, goal)  # Initial heuristic value
    
    while open_set:
        _, current = heapq.heappop(open_set)  # Get the node with the lowest heuristic
        
        # If we've reached the goal, we're done!
        if current == goal:
            return reconstruct_path(came_from, current)

        # Define possible moves, including diagonals
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        # Check each possible move
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Diagonal moves cost more
            move_cost = 1.5 if dx != 0 and dy != 0 else 1

            # Check if the move is valid (within bounds and not into an obstacle)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in local_obstacles:
                
                # Calculate the new tentative cost to get to the neighbor
                tentative_g_score = g_score[current] + move_cost
                
                # If this path to neighbor is better (shorter) than previously known paths, update!
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + octal_distance(neighbor, goal)
                    
                    # If neighbor is not yet to be visited, add it to open_set
                    if neighbor not in [item[1] for item in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    # If we exit the loop without returning, there's no path to the goal
    return []



def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def draw_grid():
    for i in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (i, 0), (i, HEIGHT))
        pygame.draw.line(screen, GRAY, (0, i), (WIDTH, i))


def main():
    run = True
    rover_position = START
    stuck = False  # Flag to indicate if the rover is stuck
    move_counter = 0  # Add this
    move_frequency = 10  # Add this
    vision_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)


    drawing = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
        # Detect mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button pressed
                    drawing = True
                    x, y = event.pos
                    cell_y, cell_x = x // CELL_SIZE, y // CELL_SIZE  # Swap these here
                    if (cell_x, cell_y) not in [START, GOAL]:
                        if (cell_x, cell_y) in OBSTACLES:
                            OBSTACLES.remove((cell_x, cell_y))
                        else:
                            OBSTACLES.append((cell_x, cell_y))
                        
        # Detect mouse motion
            if event.type == pygame.MOUSEMOTION and drawing:
                x, y = event.pos
                cell_y, cell_x = x // CELL_SIZE, y // CELL_SIZE  # Swap these here too
                if (cell_x, cell_y) not in [START, GOAL, *OBSTACLES]:
                    OBSTACLES.append((cell_x, cell_y))
                
        # Detect mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button released
                    drawing = False


        screen.fill(WHITE)
        draw_grid()

        vision_surface.fill((0, 0, 0, 0))
        pygame.draw.circle(vision_surface, (100, 100, 100, 128), 
                           (rover_position[1] * CELL_SIZE + CELL_SIZE // 2, 
                            rover_position[0] * CELL_SIZE + CELL_SIZE // 2), 
                           VISION_RANGE * CELL_SIZE)
        
        screen.blit(vision_surface, (0, 0))

        move_counter += 2

        # Draw obstacles
        for obstacle in OBSTACLES:
            pygame.draw.rect(screen, RED, (obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if not stuck:
            # Decide on the next move in real-time
            if rover_position != GOAL and move_counter % move_frequency == 0:  # Modified this line
                path = astar_search(rover_position, GOAL)
                if not path:  # Rover can't find a way
                    stuck = True
                elif len(path) > 1:  # if there's a valid path, and it's not just the rover's current position
                    rover_position = path[1]  # move to the next step

        if stuck:
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render("Rover is stuck", True, (0, 0, 255))
            text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(text_surface, text_rect)
            pygame.display.flip()
            pygame.time.wait(3000)  # Show the message for 3 seconds
            run = False



        pygame.draw.rect(screen, ROVER_COLOR, (rover_position[1] * CELL_SIZE, rover_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        # Draw start and goal
        pygame.draw.rect(screen, GREEN, (START[1] * CELL_SIZE, START[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, GREEN, (GOAL[1] * CELL_SIZE, GOAL[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()

        clock.tick(30)  # Wait for 200 milliseconds for slower movement
        pygame.display.flip()

    pygame.quit()



if __name__ == "__main__":
    main()
