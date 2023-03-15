import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle dimensions and speed
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 10
AI_PADDLE_SPEED = 4  # Moderate difficulty level

# Ball dimensions and speed
BALL_SIZE = 20
BALL_SPEED = 5

# Ball color and speed change
ball_color = [255, 255, 255]
color_step = 8.5
speed_step = 0.5
bounce_count = 0
max_bounces = 30

# Scores
score_a = 0
score_b = 0

# Define paddles and ball
paddle_a = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - 30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

def ai_move(paddle, ball, speed):
    if paddle.centery < ball.centery and paddle.bottom < HEIGHT:
        paddle.y += speed
    elif paddle.centery > ball.centery and paddle.top > 0:
        paddle.y -= speed

def bounce_angle(paddle):
    relative_intersect_y = paddle.centery - ball.centery
    normalized_intersect_y = relative_intersect_y / (PADDLE_HEIGHT / 2)
    bounce_angle = normalized_intersect_y * 5
    min_angle = 1
    if -min_angle < bounce_angle < min_angle:
        bounce_angle = min_angle if bounce_angle >= 0 else -min_angle
    return bounce_angle

def draw_scores():
    font_size = 72
    font = pygame.font.SysFont("Menlo", font_size)

    score_text_a = font.render(str(score_a), True, WHITE)
    score_text_b = font.render(str(score_b), True, WHITE)

    screen.blit(score_text_a, (WIDTH // 4, 10))
    screen.blit(score_text_b, (WIDTH * 3 // 4 - score_text_b.get_width(), 10))

def reset_ball():
    global bounce_count, ball_color, ball_dx, ball_dy
    
    # Reset ball to the center and its color to white
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_color = [255, 255, 255]
    bounce_count = 0

    # Reset ball speed
    ball_dx = BALL_SPEED if ball.left < 0 else -BALL_SPEED
    ball_dy = BALL_SPEED


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move paddle A (controlled by the computer)
    ai_move(paddle_a, ball, AI_PADDLE_SPEED)

    # Move paddle B
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
        paddle_b.y += PADDLE_SPEED

    # Update ball position
    ball.x += ball_dx
    ball.y += ball_dy

    # Ball collision with paddles
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_dx = -ball_dx
        ball_dy = -int(bounce_angle(paddle_a if ball.colliderect(paddle_a) else paddle_b))

        # Increase the ball's redness and speed
        if bounce_count < max_bounces:
            ball_color[1] -= color_step
            ball_color[2] -= color_step
            ball_dx += speed_step if ball_dx > 0 else -speed_step
            ball_dy += speed_step if ball_dy > 0 else -speed_step
            bounce_count += 1

    # Ball collision with top and bottom walls
    if ball.top <= 0:
        ball_dy = abs(ball_dy)
        ball.y = 0
    elif ball.bottom >= HEIGHT:
        ball_dy = -abs(ball_dy)
        ball.y = HEIGHT - BALL_SIZE

    # Ball collision with left and right walls (scoring)
    if ball.left <= 0:
        score_b += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_a += 1
        reset_ball()

        

    # Draw the game elements
    screen.fill(BLACK)
    draw_scores()
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, ball_color, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Update the display
    pygame.display.flip()
    pygame.time.delay(16)
