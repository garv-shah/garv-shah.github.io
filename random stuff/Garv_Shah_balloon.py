import random
import sys
import pygame

# pygame 2.1.2 (SDL 2.0.18, Python 3.10.0)

pygame.init()


# start class definitions
class Projectile(object):
    def __init__(self, x, y, vel):
        self.x = x
        self.y = y
        self.vel = vel

    def draw(self, window):
        pygame.draw.rect(window, (138, 138, 138), (self.x, self.y, 15, 15))


class Canon(object):
    def __init__(self, x, y, vel, width, height):
        self.x = x
        self.y = y
        self.vel = vel
        self.width = width
        self.height = height

    def draw(self, window):
        pygame.draw.rect(window,
                         (0, 0, 0),
                         (self.x,
                          self.y,
                          self.width,
                          self.height))

        pygame.draw.rect(window,
                         (0, 0, 0),
                         (self.x - (self.width / 3),
                          self.y + (self.height / 3),
                          self.width / 2,
                          self.height / 3))


class Balloon(object):
    def __init__(self, x, y, vel, radius):
        self.x = x
        self.y = y
        self.vel = vel
        self.radius = radius

    def draw(self, window):
        pygame.draw.circle(window, (132, 148, 68), (self.x, self.y), self.radius)
        pygame.draw.circle(window, (174, 195, 94), (self.x, self.y), self.radius - 5)
# end class definitions


# global variables
screen_width = 750
screen_height = 500
clock = pygame.time.Clock()
bullet_cooldown = 0
bullets = []
missed_bullets = 0
canon = Canon(625, 250, 6, 100, 50)
balloon = Balloon(50, 250, 2, screen_width / 30)
balloon_direction = random.choice((-1, 1))
balloon_cooldown = 0
game_over = False

# pygame setup
win = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Balloon Game")

# main game loop
while True:
    # creates time delay to have a more controlled fps
    clock.tick(60)

    for event in pygame.event.get():

        # if pygame event is quit, close game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # stores keys pressed
    keys = pygame.key.get_pressed()

    if game_over:
        pygame.font.init()
        largeFont = pygame.font.SysFont('Comic Sans MS', 50)
        lastScore = largeFont.render('You Win!', True, (80, 80, 80))
        currentScore = largeFont.render(f'You Missed {missed_bullets} Bullets', True, (80, 80, 80))
        win.blit(lastScore, (screen_width / 2 - lastScore.get_width() / 2, screen_height * 1/3))
        win.blit(currentScore, (screen_width / 2 - currentScore.get_width() / 2, screen_height * 1/2))
        pygame.display.update()
    else:
        # white background fill
        win.fill((255, 255, 255))

        # handles cannon movement, ensuring it does not go off the screen
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and canon.y > 0:
            canon.y -= canon.vel

        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and canon.y < screen_height - canon.height:
            canon.y += canon.vel

        # create bullets within cooldown period if space is clicked
        if keys[pygame.K_SPACE]:
            if bullet_cooldown == 0:
                bullets.append(Projectile(canon.x - (canon.width / 3), canon.y + (canon.height / 3), 20))
                bullet_cooldown = 40

        # Draw and move bullets
        for bullet in bullets:
            if screen_width > bullet.x > 0:
                bullet.x -= bullet.vel
                bullet.draw(win)

                # calculate if bullets have collision with balloon
                bullet_rect = pygame.Rect(bullet.x, bullet.y, 15, 15)
                pygame.draw.rect(win, (138, 138, 138), bullet_rect)

                collide = bullet_rect.colliderect(pygame.Rect(balloon.x, balloon.y, balloon.radius, balloon.radius))

                if collide:
                    game_over = True

                    # create a faded grey box over the screen for the end title
                    grey_box = pygame.Surface((screen_width, screen_height))
                    grey_box.set_alpha(128)
                    grey_box.fill((128, 128, 128))
                    win.blit(grey_box, (0, 0))
            else:
                # delete bullet if it hits end of screen and increment missed bullet counter
                bullets.pop(bullets.index(bullet))
                missed_bullets += 1

        # decrement bullet cooldown
        if bullet_cooldown > 0:
            bullet_cooldown -= 1

        if balloon_cooldown > 0:
            balloon_cooldown -= 1
        else:
            balloon_direction = random.choice((-1, 1))
            balloon_cooldown = 50

        if not (screen_height - balloon.radius > balloon.y > balloon.radius):
            balloon_direction *= -1

        balloon.y += balloon.vel * balloon_direction
        balloon.draw(win)

        canon.draw(win)
        pygame.display.update()
