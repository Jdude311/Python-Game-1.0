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
        if self.x + self.width + self.xsp >= 300 or self.x + self.xsp <= 0:
            self.xsp = -self.xsp
        if self.y + self.height + self.ysp >= 300 or self.y + self.ysp <= 0:
            self.ysp = -self.ysp
        self.x += self.xsp
        self.y += self.ysp
        self.angle = abs(-math.atan2(self.ysp, self.xsp) - math.pi)
        print(round(math.degrees(self.angle)))

        self.xsp = self.xsp * 0.9
        self.ysp = (self.ysp) * 0.9



    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))


# Set up game
pygame.init()

surface = pygame.display.set_mode((300, 300))
block1 = GameObjectBlock("joe", (1, 2))
projectile1 = GameObjectProjectile("bullet", (150, 150), (10, 10), math.pi/3, 5)
pygame.draw.circle(surface, (255, 0, 0), (30, 30), 10)
pygame.display.update()

# Game loop
while True:
    surface.fill("black")
    projectile1.move()
    projectile1.draw(surface)
    pygame.display.update()
    time.sleep(0.0166666667)
