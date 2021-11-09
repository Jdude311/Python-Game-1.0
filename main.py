import math
import time
import pygame


class GameObject:
    def __init__(self, name, position):
        self.name = str(name)
        self.x = position[0]
        self.y = position[1]

    def __str__(self):
        return self.name + " at position (" + str(self.x) + ", " + str(self.y) + ")\n"

class GameObjectPlayer(GameObject):
    def __init__(self, name, position):
        super().__init__(name, position)
        self.width = 25
        self.height = 25

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.width, self.height))


class GameObjectBlock(GameObject):
    "Nonmoving object with position. Used for blocks."
    def __init__(self, name, position):
        super().__init__(name, position)


class GameObjectProjectile(GameObject):
    "This type of object has a speed, which contains information for x and y speed. It is a list."
    def __init__(self, name, position, dimensions, angle, speed):
        super().__init__(name, position)
        self.speed = speed
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.angle = angle
        self.xsp = math.cos(self.angle) * self.speed
        self.ysp = math.sin(self.angle) * self.speed

    def move(self):
        "Move the object. Must be called each frame."
        if self.x + self.width + self.xsp >= screen.get_size()[0] or self.x + self.xsp <= 0:
            self.xsp = -self.xsp
        else:
            self.xsp = self.xsp * 0.98
        if self.y + self.height + self.ysp >= screen.get_size()[1] or self.y + self.ysp <= 0:
            self.ysp = -self.ysp
        else:
            self.ysp = round((self.ysp + 2) * 0.98)  # Only gravity if not on ground
        self.x += self.xsp
        self.y += self.ysp
        self.angle = abs(-math.atan2(self.ysp, self.xsp) - math.pi)
        print(round(math.degrees(self.angle)))

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


class GameObjectProjectileBullet(GameObjectProjectile):
    "Special class for bullets."
    def __init__(self, name, position, dimensions, angle, speed):
        super().__init__(name, position, dimensions, angle, speed)
        self.sprite = pygame.image.load("bullet.png").convert()
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))

    def draw(self, screen):
        screen.blit(self.sprite, self.sprite.get_rect(center=(100,100)))


# Set up game
pygame.init()
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
block1 = GameObjectBlock("joe", (1, 2))
projectile1 = GameObjectProjectile("proj", (0, 300), (10, 10), math.pi/4, 50)
bullet1 = GameObjectProjectileBullet("bullet", (0,300), (10, 10), math.pi/4, 50)
pygame.display.update()

# Game loop
running = True;
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    projectile1.move()
    projectile1.draw(screen)
    bullet1.move()
    bullet1.draw(screen)
    pygame.display.update()
    time.sleep(0.0166666667)

pygame.quit()
