import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Interactive Christmas Card")

# Colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 128, 0)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Koch Snowflake function
def koch_snowflake(order, scale=100):
    def divide_segment(p1, p2):
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        p3 = (p1[0] + dx / 3, p1[1] + dy / 3)
        p4 = (p1[0] + dx * 2 / 3, p1[1] + dy / 3 * 2)
        px, py = (
            p3[0] + dx / 3 * math.cos(math.pi / 3) - dy / 3 * math.sin(math.pi / 3),
            p3[1] + dx / 3 * math.sin(math.pi / 3) + dy / 3 * math.cos(math.pi / 3),
        )
        p5 = (px, py)
        return [p1, p3, p5, p4, p2]

    def recurse(points, level):
        if level == 0:
            return points
        new_points = []
        for i in range(len(points) - 1):
            new_points.extend(divide_segment(points[i], points[i + 1])[:-1])
        new_points.append(points[-1])
        return recurse(new_points, level - 1)

    points = [
        (0, -scale),
        (-scale * math.sin(math.pi / 3), scale / 2),
        (scale * math.sin(math.pi / 3), scale / 2),
        (0, -scale),
    ]
    return recurse(points, order)

# Snowflake class
class Snowflake:
    def __init__(self, x, y, color, order):
        self.x = x
        self.y = y
        self.color = color
        self.order = order
        self.scale = random.randint(10, 40)
        self.points = koch_snowflake(order, scale=self.scale)
        self.speed = random.uniform(1, 3)
        self.angle = random.uniform(0, 360)  # Initial angle of rotation
        self.rotation_speed = random.uniform(-2, 2)  # Speed of rotation (positive or negative)

    def draw(self, surface):
        # Rotate the snowflake points around the center
        rotated_points = []
        for p in self.points:
            px = p[0] * math.cos(math.radians(self.angle)) - p[1] * math.sin(math.radians(self.angle))
            py = p[0] * math.sin(math.radians(self.angle)) + p[1] * math.cos(math.radians(self.angle))
            rotated_points.append((self.x + px, self.y + py))

        # Draw the rotated snowflake
        pygame.draw.lines(surface, self.color, False, rotated_points, 1)

    def update(self):
        # Update the snowflake's position and angle
        self.y += self.speed
        self.angle += self.rotation_speed  # Rotate the snowflake
        if self.y > HEIGHT:
            self.y = -100
            self.x = random.randint(0, WIDTH)
            self.scale = random.randint(30, 100)
            self.points = koch_snowflake(self.order, scale=self.scale)
            self.speed = random.uniform(1, 3)
            self.rotation_speed = random.uniform(-2, 2)  # New rotation speed

# Draw red-green colored text
def draw_christmas_text(surface, text, x, y):
    font = pygame.font.Font(None, 50)  # Define the font and size
    colors = [RED, DARK_GREEN]  # Alternating colors (red and green)

    # Loop through each letter and render it with alternating colors
    for i, letter in enumerate(text):
        color = colors[i % 2]  # Alternate between red and green
        letter_surface = font.render(letter, True, color)  # Render the letter
        letter_rect = letter_surface.get_rect()
        letter_rect.topleft = (x, y)  # Position the letter
        surface.blit(letter_surface, letter_rect)  # Draw the letter on the screen
        x += letter_rect.width  # Update x for the next letter


# Draw a Christmas tree
def draw_christmas_tree(surface):
    # Tree foliage (stacked triangles)
    tree_top = [(WIDTH // 2, HEIGHT - 240), (WIDTH // 2 - 50, HEIGHT - 180), (WIDTH // 2 + 50, HEIGHT - 180)]
    tree_middle = [(WIDTH // 2, HEIGHT - 200), (WIDTH // 2 - 70, HEIGHT - 120), (WIDTH // 2 + 70, HEIGHT - 120)]
    tree_bottom = [(WIDTH // 2, HEIGHT - 180), (WIDTH // 2 - 100, HEIGHT - 40), (WIDTH // 2 + 100, HEIGHT - 40)]

    # Draw the tree triangles
    pygame.draw.polygon(surface, GREEN, tree_top)
    pygame.draw.polygon(surface, GREEN, tree_middle)
    pygame.draw.polygon(surface, GREEN, tree_bottom)

    # Tree Trunk
    trunk_rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 40, 40, 40)
    pygame.draw.rect(surface, BROWN, trunk_rect)

    # Draw the star at the top of the tree
    star_color = (255, 223, 0)  # Yellow
    star_points = [
        (WIDTH // 2, HEIGHT - 263),  # Top point
        (WIDTH // 2 - 10, HEIGHT - 248),  # Left inner
        (WIDTH // 2 - 25, HEIGHT - 245),  # Left outer
        (WIDTH // 2 - 15, HEIGHT - 230),  # Bottom left
        (WIDTH // 2 - 20, HEIGHT - 210),  # Bottom inner left
        (WIDTH // 2, HEIGHT - 220),  # Center bottom
        (WIDTH // 2 + 20, HEIGHT - 210),  # Bottom inner right
        (WIDTH // 2 + 15, HEIGHT - 230),  # Bottom right
        (WIDTH // 2 + 25, HEIGHT - 245),  # Right outer
        (WIDTH // 2 + 10, HEIGHT - 248)   # Right inner
    ]
    pygame.draw.polygon(surface, star_color, star_points)


    # Add red ornaments
    ornament_color = RED
    ornaments = [
        (WIDTH // 2 - 20, HEIGHT - 195),
        (WIDTH // 2 + 20, HEIGHT - 195),
        (WIDTH // 2 - 35, HEIGHT - 140),
        (WIDTH // 2 + 35, HEIGHT - 140),
        (WIDTH // 2 - 50, HEIGHT - 80),
        (WIDTH // 2 + 50, HEIGHT - 80),
        (WIDTH // 2, HEIGHT - 120),
        (WIDTH // 2, HEIGHT - 60)
    ]
    for ornament in ornaments:
        pygame.draw.circle(surface, ornament_color, ornament, 5)


# Create a list of snowflakes
snowflakes = [
    Snowflake(
        random.randint(0, WIDTH),
        random.randint(-HEIGHT, 0),
        random.choice([RED, GREEN]),
        random.randint(2, 5),
    )
    for _ in range(20)
]

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the Christmas tree
    draw_christmas_tree(screen)

    # Draw the "Merry Christmas X" text
    draw_christmas_text(screen, "Merry Christmas X!", WIDTH // 2-160, 200)  # Adjust x, y for position

    # Update and draw each snowflake
    for snowflake in snowflakes:
        snowflake.update()
        snowflake.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
