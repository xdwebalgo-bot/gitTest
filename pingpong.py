import pygame
import sys

# ==========================================
# 1. INITIALIZATION AND SETUP
# ==========================================
pygame.init()

# Screen dimensions
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Procedural Ping Pong")

# Frame rate controller
clock = pygame.time.Clock()

# Colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ==========================================
# 2. GAME VARIABLES
# ==========================================

# --- Paddles ---
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 7

# Left paddle starting position and movement state
left_paddle_x = 30
left_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
left_paddle_dy = 0  # Change in Y (velocity)

# Right paddle starting position and movement state
right_paddle_x = WIDTH - 30 - PADDLE_WIDTH
right_paddle_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
right_paddle_dy = 0 # Change in Y (velocity)

# --- Ball ---
BALL_SIZE = 15
ball_x = WIDTH // 2 - BALL_SIZE // 2
ball_y = HEIGHT // 2 - BALL_SIZE // 2
ball_dx = 5  # Speed in the X direction
ball_dy = 5  # Speed in the Y direction

# --- Scores ---
left_score = 0
right_score = 0
# Font for displaying text (None uses default system font, 74 is the size)
font = pygame.font.Font(None, 74)

# ==========================================
# 3. MAIN GAME LOOP
# ==========================================
running = True
while running:
    
    # --------------------------------------
    # A. EVENT HANDLING (Keys and Clicks)
    # --------------------------------------
    for event in pygame.event.get():
        # Quit the game if the user closes the window
        if event.type == pygame.QUIT:
            running = False
            
        # Check if a key was pressed down
        if event.type == pygame.KEYDOWN:
            # Left player controls (W = Up, S = Down)
            if event.key == pygame.K_w:
                left_paddle_dy = -PADDLE_SPEED
            if event.key == pygame.K_s:
                left_paddle_dy = PADDLE_SPEED
                
            # Right player controls (Up Arrow, Down Arrow)
            if event.key == pygame.K_UP:
                right_paddle_dy = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                right_paddle_dy = PADDLE_SPEED
                
        # Check if a key was released
        if event.type == pygame.KEYUP:
            # Stop moving the left paddle if W or S is released
            if event.key == pygame.K_w or event.key == pygame.K_s:
                left_paddle_dy = 0
            # Stop moving the right paddle if Up or Down is released
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                right_paddle_dy = 0

    # --------------------------------------
    # B. GAME LOGIC (Updating positions)
    # --------------------------------------
    
    # 1. Move the paddles
    left_paddle_y += left_paddle_dy
    right_paddle_y += right_paddle_dy

    # 2. Prevent paddles from going off the screen
    if left_paddle_y < 0: 
        left_paddle_y = 0
    if left_paddle_y > HEIGHT - PADDLE_HEIGHT: 
        left_paddle_y = HEIGHT - PADDLE_HEIGHT
        
    if right_paddle_y < 0: 
        right_paddle_y = 0
    if right_paddle_y > HEIGHT - PADDLE_HEIGHT: 
        right_paddle_y = HEIGHT - PADDLE_HEIGHT

    # 3. Move the ball
    ball_x += ball_dx
    ball_y += ball_dy

    # 4. Ball collision with Top and Bottom walls
    # If the ball hits the top (0) or bottom (HEIGHT), reverse its Y direction
    if ball_y <= 0 or ball_y >= HEIGHT - BALL_SIZE:
        ball_dy *= -1 

    # 5. Ball collision with Paddles
    # We use Pygame's built-in Rect object to handle collision detection easily
    ball_rect = pygame.Rect(ball_x, ball_y, BALL_SIZE, BALL_SIZE)
    left_paddle_rect = pygame.Rect(left_paddle_x, left_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle_rect = pygame.Rect(right_paddle_x, right_paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT)

    # If the ball hits the left paddle and is moving left
    if ball_rect.colliderect(left_paddle_rect) and ball_dx < 0:
        ball_dx *= -1 # Reverse X direction (bounce)
        
    # If the ball hits the right paddle and is moving right
    if ball_rect.colliderect(right_paddle_rect) and ball_dx > 0:
        ball_dx *= -1 # Reverse X direction (bounce)

    # 6. Scoring mechanism
    # Ball goes off the left side
    if ball_x <= 0:
        right_score += 1
        # Reset ball to the center
        ball_x = WIDTH // 2 - BALL_SIZE // 2
        ball_y = HEIGHT // 2 - BALL_SIZE // 2
        ball_dx *= -1 # Serve the ball to the player who just scored
        
    # Ball goes off the right side
    elif ball_x >= WIDTH:
        left_score += 1
        # Reset ball to the center
        ball_x = WIDTH // 2 - BALL_SIZE // 2
        ball_y = HEIGHT // 2 - BALL_SIZE // 2
        ball_dx *= -1 # Serve the ball to the player who just scored

    # --------------------------------------
    # C. DRAWING (Rendering graphics)
    # --------------------------------------
    
    # 1. Clear the screen with a black background
    screen.fill(BLACK)

    # 2. Draw the center line (aaline stands for Anti-Aliased line)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # 3. Draw the paddles and the ball
    # Note: We reuse the rects we created during the collision step!
    pygame.draw.rect(screen, WHITE, left_paddle_rect)
    pygame.draw.rect(screen, WHITE, right_paddle_rect)
    pygame.draw.ellipse(screen, WHITE, ball_rect)

    # 4. Draw the scores
    left_text = font.render(str(left_score), True, WHITE)
    right_text = font.render(str(right_score), True, WHITE)
    
    # Blit (draw) the text surfaces onto the main screen
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

    # --------------------------------------
    # D. DISPLAY UPDATE
    # --------------------------------------
    # Update the full display surface to the screen
    pygame.display.flip()
    
    # Cap the frame rate at 60 Frames Per Second (FPS)
    clock.tick(60)

# ==========================================
# 4. CLEANUP
# ==========================================
pygame.quit()
sys.exit()