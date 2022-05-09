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
THRUST = 0.4

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
        self.image = pygame.transform.scale(self.image, (45, 150))  # Scale

        # Create the rect
        self.rect = self.image.get_rect()

        # Set the coords off the screen
        self.rect.center = self.random_coords()

        # Set the initial xvelocity
        self.dx = -3

    def update(self, score=0):
        """Change the x coordinate by its dx"""
        self.rect.x += self.dx

        # Recycle the obstacle by setting its position back off the screen
        if self.rect.x <= 0:
            self.rect.center = self.random_coords()
            score += 1

    def random_coords(self):
        """Returns a random set of coordinates off the screen to the right"""
        return [
            random.randrange(WIDTH + 100, WIDTH + 300),
            random.randrange(0, HEIGHT)
        ]

    def speed_up(self):
        """Speed up the movement of the obstacles after a certain score is reached"""
        self.dx -= 0.5



def main():
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

    # Create obstacles with random height and add to group
    for i in range(3):
        obstacle = Obstacle()
        obstacle_group.add(obstacle)
        time.sleep(1)

    # ----- LOCAL VARIABLES
    done = False
    clock = pygame.time.Clock()
    space_bar_pressed = False
    score = 0

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

        # ----- RENDER
        screen.fill(BLACK)
        player_group.draw(screen)
        obstacle_group.draw(screen)

        # ----- UPDATE DISPLAY
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()