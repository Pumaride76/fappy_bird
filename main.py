import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 400, 600
BIRD_WIDTH, BIRD_HEIGHT = 34, 24
PIPE_WIDTH, PIPE_HEIGHT = 52, 320
GAP_SIZE = 150
PIPE_SPEED = 3
GRAVITY = 0.6
FLAP_STRENGTH = -10
FRAME_RATE = 30
PIPE_COLOR = (0, 255, 0)  # Green color for the pipes

# Set up display
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images
bird_img = pygame.transform.scale(pygame.image.load('pig.jpg'), (BIRD_WIDTH, BIRD_HEIGHT))  # Replace with your bird image path

# Load sound
flap_sound = pygame.mixer.Sound('jump.mp3')  # Replace with your sound file path

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = HEIGHT // 2
        self.velocity = 0
        self.rect = pygame.Rect(self.x, self.y, BIRD_WIDTH, BIRD_HEIGHT)

    def flap(self):
        self.velocity = FLAP_STRENGTH
        flap_sound.play()  # Play sound when flap is called

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.rect.topleft = (self.x, self.y)

    def draw(self):
        win.blit(bird_img, (self.x, self.y))

# Pipe class (now using colored rectangles)
class Pipe:
    def __init__(self):
        self.x = WIDTH
        self.height = random.randint(50, HEIGHT - GAP_SIZE - 50)
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + GAP_SIZE, PIPE_WIDTH, HEIGHT - self.height - GAP_SIZE)

    def move(self):
        self.x -= PIPE_SPEED
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw top rectangle
        pygame.draw.rect(win, PIPE_COLOR, self.top_rect)
        # Draw bottom rectangle
        pygame.draw.rect(win, PIPE_COLOR, self.bottom_rect)

def main():
    def reset_game():
        nonlocal bird, pipes, score, game_over
        bird = Bird()
        pipes = [Pipe()]
        score = 0
        game_over = False

    bird = Bird()
    pipes = [Pipe()]
    score = 0
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 36)
    run = True
    game_over = False

    while run:
        clock.tick(FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.flap()
                if event.key == pygame.K_r and game_over:
                    reset_game()
                if event.key == pygame.K_q:
                    run = False

        if not game_over:
            bird.update()

            # Add a new pipe when the last pipe is halfway across the screen
            if pipes[-1].x < WIDTH // 2:
                pipes.append(Pipe())

            for pipe in pipes:
                pipe.move()
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

            # Collision detection
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top_rect) or bird.rect.colliderect(pipe.bottom_rect):
                    game_over = True

            # Check if the bird hits the ground or goes above the screen
            if bird.y + BIRD_HEIGHT > HEIGHT or bird.y < 0:
                game_over = True

        # Draw everything
        win.fill((255, 255, 255))  # Fill the screen with white
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        win.blit(score_text, (10, 10))

        if game_over:
            game_over_text = font.render('Game Over', True, (255, 0, 0))
            win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            final_score_text = font.render(f'Your Score: {score}', True, (0, 0, 0))
            win.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() // 2))
            restart_text = font.render('Press R to Restart or Q to Quit', True, (0, 0, 0))
            win.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + game_over_text.get_height() + final_score_text.get_height()))

        pygame.display.update()

    pygame.quit()
    print(f"Game Over! Your score: {score}")

if __name__ == "__main__":
    main()
