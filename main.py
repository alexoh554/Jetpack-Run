import pygame
import random
import time

# ----- CONSTANTS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
SKY_BLUE = (95, 165, 228)
WIDTH = 800
HEIGHT = 600
TITLE = "Joypack Jetride"
GRAVITY = 0.2
THRUST = 0.7

score = 0

class Player(pygame.sprite.Sprite):
    """This class is the jetpack man that the player controls"""

    # Methods
    def __init__(self):
        """Constructor"""
        super().__init__()

        # Create the image
        self.image = pygame.image.load("./assets/running_man.png")
        self.image = pygame.transform.scale(self.image, (60, 110)) # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        # Position/Speed vectors (x and dx are constant 0)
        self.rect.x = 50
        self.rect.y = HEIGHT - self.rect.height
        self.dy = 0

    def update(self):
        """Move the player"""
        # Gravity
        self.calc_grav()

        # Move up/down
        self.rect.y += self.dy

        # Check for contact

        # Update sprite based on player's vertical movement/status

    def calc_grav(self):
        """Calculate gravity and update the speed vector"""
        # Add the gravity unit to the dy
        self.dy += GRAVITY

        # Check if player on ground
        if self.rect.y >= HEIGHT - self.rect.height and self.dy >= 0:
            self.dy = 0
            self.rect.y = HEIGHT - self.rect.height

        # Check if player on ceiling
        if self.rect.y <= 0:
            self.dy = 1
            self.rect.y = 0

    def fly(self):
        """Called when the user hits the space bar. The player moves up at constant acceleration"""
        self.dy -= THRUST

class Obstacle(pygame.sprite.Sprite):
    """Class is obstacles that a player faces on the screen"""
    def __init__(self):
        """
        :param height: height of the knife in px
        """
        super().__init__()

        # Create the image
        self.image = pygame.image.load("./assets/knife.png")
        self.image = pygame.transform.scale(self.image, (70, 150))  # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        # Set the coords off the screen
        self.rect.center = self.random_coords()
        self.rect.x = random.randrange(WIDTH, WIDTH*2)

        # Set the initial xvelocity
        self.dx = -5

    def update(self):
        """Change the x coordinate by its dx"""
        self.rect.x += self.dx

        # Recycle the obstacle by setting its position back off the screen
        if self.rect.x <= 0:
            self.rect.center = self.random_coords()

        if score % 200 == 0 and score != 0:
            self.speed_up()

    def random_coords(self):
        """Returns a random set of coordinates off the screen to the right"""
        return [
            random.randrange(WIDTH + 10, WIDTH + 300),
            random.randrange(0, HEIGHT)
        ]

    def speed_up(self):
        """Speed up the obstacles when the function is called"""
        self.dx -= 0.5



def game_loop():
    pygame.init()

    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # Create sprite groups
    player_group = pygame.sprite.Group()
    obstacle_group = pygame.sprite.Group()

    # Create player and add to group
    player = Player()
    player_group.add(player)

    # Create obstacles and add to group
    for i in range(4):
        obstacle = Obstacle()
        obstacle_group.add(obstacle)



    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    space_bar_pressed = False
    score = 0
    time_until_score = 0
    GAME_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 20)

    # ----- MAIN LOOP
    while not done:
        # -- Event Handler
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # Check for user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space_bar_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    space_bar_pressed = False

        # Make the player fly if the space key is pressed
        if space_bar_pressed:
            player.fly()

        # ----- LOGIC
        player_group.update()
        obstacle_group.update()

        # If a player group collides with an obstacle group end the game
        collided_player = pygame.sprite.spritecollide(player, obstacle_group, dokill=True)
        if len(collided_player) > 0:
            done = True
            return score

        # Update the score every time_until_score iterations of the while loop
        if time_until_score == 6:
            score += 1
            time_until_score = 0

            # Every time the score reaches a certain amount, speed up the obstacles
            if score % 200 == 0:
                obstacle_group.update()
        time_until_score += 1

        # ----- RENDER
        screen.fill(BLACK)
        player_group.draw(screen)
        obstacle_group.draw(screen)

        # Display the score on the top left of the screen
        score_surf = GAME_FONT.render(f"SCORE:{score}", True, WHITE)
        screen.blit(score_surf, (0, 0))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)


    pygame.quit()

def end_game_loop() -> bool:
    """Returns True if user wants to play again"""
    # ----- SCREEN PROPERTIES
    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption(TITLE)

    # ----- LOCAL VARIABLES
    done = False
    GAME_OVER_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 50)
    SCORE_FONT = pygame.font.Font("./assets/ARCADE_N.TTF", 30)
    clock = pygame.time.Clock()

    # ----- MAIN LOOP
    while not done:
        # ----- EVENT HANDLER
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                # Check for user input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        # ----- LOGIC



        # ------ RENDER
        # Display game over text
        game_over_surf = GAME_OVER_FONT.render("GAME OVER", True, WHITE)
        screen.blit(game_over_surf, (WIDTH / 2 - 200, HEIGHT / 2))

        # Display the user's score
        score_surf = SCORE_FONT.render(f"YOUR SCORE:{score}", True, WHITE)
        screen.blit(score_surf, (WIDTH/2 - 200, HEIGHT / 2 - 100))

        # Display user instructions
        instructions_surf = SCORE_FONT.render("Press SPACE to play again", True, WHITE)
        screen.blit(instructions_surf, (50, HEIGHT / 2 + 100))

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)


def main():
    game_loop()
    time.sleep(0.5)
    while end_game_loop():
        game_loop()
        time.sleep(0.5)

if __name__ == "__main__":
    main()