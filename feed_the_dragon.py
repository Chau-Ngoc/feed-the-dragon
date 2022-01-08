import pygame, random


def regenerate_coin():
    coin_rect.x = WINDOW_WIDTH + COIN_BUFFER_DISTANCE
    coin_rect.y = random.randint(100, WINDOW_HEIGHT - 32)


# set game properties
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = (20, 20, 20)
TEXT_COLOR = "#009DAE"
LINE_COLOR = "#3E8E7E"
FONT_SIZE = 40
FPS = 80
PLAYER_STARTING_LIVES = 5
PLAYER_VELOCITY = 10
COIN_STARTING_VELOCITY = 5
COIN_ACCELERATION = 0.5
COIN_BUFFER_DISTANCE = 100

score = 0
lives = PLAYER_STARTING_LIVES
coin_velocity = COIN_STARTING_VELOCITY

# initialize pygame
pygame.init()

# create the main display surface
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Feed The Dragon")


# ------------------------------ PREPARE GAME ASSETS ------------------------------
# load the images
dragon_image = pygame.image.load(
    "./feed_the_dragon_assets/dragon_right.png"
)  # -> Surface
dragon_rect = dragon_image.get_rect()  # -> Rect
dragon_rect.left = 30
dragon_rect.centery = WINDOW_HEIGHT // 2

coin_image = pygame.image.load("./feed_the_dragon_assets/coin.png")  # -> Surface
coin_rect = coin_image.get_rect()  # -> Rect
coin_rect.x = WINDOW_WIDTH + COIN_BUFFER_DISTANCE
coin_rect.y = random.randint(100, WINDOW_HEIGHT - 32)

# load the text
font = pygame.font.Font(
    "./feed_the_dragon_assets/FastHand-lgBMV.ttf", FONT_SIZE
)  # -> Font

# set in-game text
score_text = font.render(f"Score: {score}", True, TEXT_COLOR)  # -> Surface
score_text_rect = score_text.get_rect()  # -> Rect
score_text_rect.left = 10
score_text_rect.centery = 50

game_title = font.render("Feed The Dragon", True, TEXT_COLOR)  # -> Surface
game_title_rect = game_title.get_rect()  # -> Rect
game_title_rect.centerx = WINDOW_WIDTH // 2
game_title_rect.centery = 50

lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)  # -> Surface
lives_text_rect = lives_text.get_rect()  # -> Rect
lives_text_rect.right = WINDOW_WIDTH - 10
lives_text_rect.centery = 50

gameover_text = font.render("Gameover", True, TEXT_COLOR)  # -> Surface
gameover_rect = gameover_text.get_rect()  # -> Rect
gameover_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

continue_text = font.render("Press 'Enter' to continue", True, TEXT_COLOR)  # -> Surface
continue_rect = continue_text.get_rect()  # -> Rect
continue_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)

# load sound and background music
coin_eaten_sound = pygame.mixer.Sound("./feed_the_dragon_assets/coin_sound.wav")
coin_eaten_sound.set_volume(0.2)

miss_sound = pygame.mixer.Sound("./feed_the_dragon_assets/miss_sound.wav")
miss_sound.set_volume(0.1)

pygame.mixer.music.load("./feed_the_dragon_assets/ftd_background_music.wav")

# set the window icon
pygame.display.set_icon(dragon_image)

# create clock to control fps
clock = pygame.time.Clock()


# ------------------------------ THE MAIN GAME LOOP ------------------------------
pygame.mixer.music.play(-1)
running = True
while running:
    if pygame.event.get(pygame.QUIT):
        running = False

    # fill the background with black
    display_surface.fill(BACKGROUND_COLOR)

    # draw a line
    pygame.draw.line(
        display_surface, LINE_COLOR, (10, 100), (WINDOW_WIDTH - 10, 100), width=4
    )

    # blit the images onto the display surface at the given rect coordinate
    display_surface.blit(dragon_image, dragon_rect)
    display_surface.blit(coin_image, coin_rect)

    # blit the text_surface at the text_rect coordinate
    display_surface.blit(game_title, game_title_rect)
    display_surface.blit(score_text, score_text_rect)
    display_surface.blit(lives_text, lives_text_rect)

    # move coin
    coin_rect.x -= coin_velocity
    if coin_rect.x < 0:
        regenerate_coin()
        lives -= 1
        miss_sound.play()

    if dragon_rect.colliderect(coin_rect):
        regenerate_coin()
        score += 1
        coin_velocity += COIN_ACCELERATION
        coin_eaten_sound.play()

    # update the HUD
    lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
    score_text = font.render(f"Score: {score}", True, TEXT_COLOR)

    # if player's lives have been depleted, it is gameover
    if lives == 0:
        display_surface.fill(BACKGROUND_COLOR)
        display_surface.blit(gameover_text, gameover_rect)
        display_surface.blit(continue_text, continue_rect)

        regenerate_coin()

        pygame.display.update()
        pygame.mixer.music.stop()

        # pause the game and ask if player wants to continue playing or quit
        is_paused = True
        while is_paused:
            for event in pygame.event.get():

                # check for key pressed to reset the game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        score = 0
                        lives = PLAYER_STARTING_LIVES
                        coin_velocity = COIN_STARTING_VELOCITY
                        dragon_rect.y = WINDOW_HEIGHT // 2
                        pygame.mixer.music.play(-1)
                        is_paused = False

                # check if player wants to quit the game
                elif event.type == pygame.QUIT:
                    is_paused = False
                    running = False

    # move the dragon
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and dragon_rect.top > 100:
        dragon_rect.y -= PLAYER_VELOCITY
    elif keys[pygame.K_DOWN] and dragon_rect.bottom < WINDOW_HEIGHT:
        dragon_rect.y += PLAYER_VELOCITY

    # update the display
    pygame.display.update()

    # tick the clock at 60fps
    clock.tick(FPS)


# ------------------------------ QUIT THE GAME ------------------------------
pygame.quit()
