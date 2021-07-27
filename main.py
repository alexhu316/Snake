import pygame
import random

FPS = 8
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
squares = [[7, 8]]  # the snake
num_fruits = 5
fruits = []  # the fruits
direction = 0  # 0 = UP, 1 = DOWN, 2 = LEFT, 3 = RIGHT
score = 0
valid_keys = [pygame.K_UP, pygame.K_w, pygame.K_DOWN, pygame.K_s, pygame.K_LEFT, pygame.K_a, pygame.K_RIGHT, pygame.K_d]
game_over = True

pygame.init()
window = pygame.display.set_mode((500, 600))
pygame.display.set_caption("Snake")


def draw_grid():
    window.fill(BLACK)

    # displays big 'SNAKE' title
    font = pygame.font.SysFont('Comic Sans MS', 70)
    text = font.render('Snake', True, WHITE, None)
    text_rect = text.get_rect()
    text_rect.center = (250, 65)
    window.blit(text, text_rect)

    # displays score
    font = pygame.font.SysFont('Comic Sans MS', 50)
    text = font.render(f"{score}", True, WHITE, None)
    text_rect = text.get_rect()
    text_rect.center = (440, 41)
    window.blit(text, text_rect)

    # Start button
    font = pygame.font.SysFont('Comic Sans MS', 20)
    text = font.render("Start", True, WHITE, None)
    text_rect = text.get_rect()
    text_rect.center = (60, 35)
    window.blit(text, text_rect)

    # gridlines
    for i in range(16):
        pygame.draw.line(window, WHITE, (25, 125 + 30 * i), (475, 125 + 30 * i), 2)
        pygame.draw.line(window, WHITE, (25 + 30 * i, 125), (25 + 30 * i, 575), 2)


def handle_graphics():
    """draws everything on a given frame"""
    draw_grid()
    for fruit in fruits:  # fruits
        pygame.draw.rect(window, RED, pygame.Rect(26 + 30 * fruit[0], 126 + 30 * fruit[1], 29, 29))
    for square in squares:  # snake
        pygame.draw.rect(window, WHITE, pygame.Rect(25 + 30 * square[0], 125 + 30 * square[1], 30, 30))
    if direction in [0, 1]:  # eyes looking in the direction the snake is moving
        pygame.draw.rect(window, GREY,
                         pygame.Rect(25 + 30 * squares[0][0], 125 + 25 * direction + 30 * squares[0][1], 5, 5))
        pygame.draw.rect(window, GREY,
                         pygame.Rect(51 + 30 * squares[0][0], 125 + 25 * direction + 30 * squares[0][1], 5, 5))
    else:
        pygame.draw.rect(window, GREY,
                         pygame.Rect(25 + 25 * (direction - 2) + 30 * squares[0][0], 125 + 30 * squares[0][1], 5, 5))
        pygame.draw.rect(window, GREY,
                         pygame.Rect(25 + 25 * (direction - 2) + 30 * squares[0][0], 151 + 30 * squares[0][1], 5, 5))
    if len(squares) > 1:  # body
        if squares[0][1] == squares[1][1]:
            if squares[0][0] == squares[1][0] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[0][0], 140 + 30 * squares[0][1]),
                                 (25 + 30 * squares[0][0], 140 + 30 * squares[0][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[0][0], 140 + 30 * squares[0][1]),
                                 (55 + 30 * squares[0][0], 140 + 30 * squares[0][1]), 10)
        else:
            if squares[0][1] == squares[1][1] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[0][0], 140 + 30 * squares[0][1]),
                                 (40 + 30 * squares[0][0], 125 + 30 * squares[0][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[0][0], 140 + 30 * squares[0][1]),
                                 (40 + 30 * squares[0][0], 155 + 30 * squares[0][1]), 10)
        if squares[-1][1] == squares[-2][1]:
            if squares[-1][0] == squares[-2][0] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]),
                                 (25 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]),
                                 (55 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]), 10)
        else:
            if squares[-1][1] == squares[-2][1] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]),
                                 (40 + 30 * squares[-1][0], 125 + 30 * squares[-1][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[-1][0], 140 + 30 * squares[-1][1]),
                                 (40 + 30 * squares[-1][0], 155 + 30 * squares[-1][1]), 10)
    for i in range(1, len(squares) - 1):  # body
        if squares[i - 1][1] == squares[i + 1][1]:
            pygame.draw.line(window, GREY, (25 + 30 * squares[i][0], 140 + 30 * squares[i][1]),
                             (55 + 30 * squares[i][0], 140 + 30 * squares[i][1]), 10)
        elif squares[i - 1][0] == squares[i + 1][0]:
            pygame.draw.line(window, GREY, (40 + 30 * squares[i][0], 125 + 30 * squares[i][1]),
                             (40 + 30 * squares[i][0], 155 + 30 * squares[i][1]), 10)
        else:
            pygame.draw.rect(window, GREY, pygame.Rect(36 + 30 * squares[i][0], 136 + 30 * squares[i][1], 10, 10))
            if squares[i][0] == squares[i - 1][0] + 1 or squares[i][0] == squares[i + 1][0] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[i][0], 140 + 30 * squares[i][1]),
                                 (25 + 30 * squares[i][0], 140 + 30 * squares[i][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[i][0], 140 + 30 * squares[i][1]),
                                 (55 + 30 * squares[i][0], 140 + 30 * squares[i][1]), 10)
            if squares[i][1] == squares[i - 1][1] + 1 or squares[i][1] == squares[i + 1][1] + 1:
                pygame.draw.line(window, GREY, (40 + 30 * squares[i][0], 140 + 30 * squares[i][1]),
                                 (40 + 30 * squares[i][0], 125 + 30 * squares[i][1]), 10)
            else:
                pygame.draw.line(window, GREY, (40 + 30 * squares[i][0], 140 + 30 * squares[i][1]),
                                 (40 + 30 * squares[i][0], 155 + 30 * squares[i][1]), 10)
    pygame.display.update()


def put_fruit():
    """picks locations for new fruit"""
    global fruits
    global num_fruits
    if len(fruits) == num_fruits:
        fruits = []
    matrix = []
    for i in range(15):
        for j in range(15):
            if [i, j] not in squares and [i, j] not in fruits:
                matrix.append([i, j])
    if len(matrix) > 0:
        fruits.append(random.choice(matrix))


def main():
    """runs the game"""
    run = True
    clock = pygame.time.Clock()
    key_presses = []

    while run:
        global squares
        global direction
        global game_over
        global score
        global valid_keys

        # queues up the direction of the first key pressed
        if len(key_presses) > 0:
            key = key_presses[0]
            if (key == pygame.K_UP or key == pygame.K_w) and (direction != 1 or len(squares) == 1):
                direction = 0
            elif (key == pygame.K_DOWN or key == pygame.K_s) and (direction != 0 or len(squares) == 1):
                direction = 1
            elif (key == pygame.K_LEFT or key == pygame.K_a) and (direction != 3 or len(squares) == 1):
                direction = 2
            elif (key == pygame.K_RIGHT or key == pygame.K_d) and (direction != 2 or len(squares) == 1):
                direction = 3
            key_presses = key_presses[1:]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # allows the program to stop after closing
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # gives effect to the start button
                mouse = pygame.mouse.get_pos()
                if 20 <= mouse[0] <= 100 and 20 <= mouse[1] <= 50:
                    squares = [[7, 9]]
                    for i in range(num_fruits):
                        put_fruit()
                    direction = 0
                    direction = 0
                    score = 0
                    game_over = False
            if event.type == pygame.KEYDOWN:  # queues (up to two) the most recent key press(es)
                if len(key_presses) < 3 and event.key in valid_keys:
                    key_presses.append(event.key)

        if not game_over:
            # moves the snake in its direction, eating fruit if there is one
            if direction == 0:
                squares.insert(0, [squares[0][0], squares[0][1] - 1])
            elif direction == 1:
                squares.insert(0, [squares[0][0], squares[0][1] + 1])
            elif direction == 2:
                squares.insert(0, [squares[0][0] - 1, squares[0][1]])
            elif direction == 3:
                squares.insert(0, [squares[0][0] + 1, squares[0][1]])
            if squares[0] in fruits:
                fruits.remove(squares[0])
                score += 1
                put_fruit()
            else:
                squares.pop()

            # checks for game over conditions
            if squares[0] in squares[1:]:
                game_over = True
            if 0 > min(squares[0][0], squares[0][1]) or 14 < max(squares[0][0], squares[0][1]):
                game_over = True
            if not game_over:
                handle_graphics()

        # movements come 8 times per second
        clock.tick(FPS)


# when the program is launched, this displays the grid and starts the main loop
handle_graphics()
pygame.display.update()
main()
