import math
import time
import pygame


class GameObject:
    def __init__(self, name, x, y):
        self.name = str(name)
        self.x = int(x)
        self.y = int(y)

    def __str__(self):
        return self.name + " at position (" + str(self.x) + ", " + str(self.y) + ")\n"


class GameObjectBlock(GameObject):
    "Nonmoving object with position. Used for blocks."
    def __init__(self, name, x, y):
        super().__init__(name, x, y)


class GameObjectProjectile(GameObject):
    "This type of object has a speed, which contains information for x and y speed. It is a list."
    def __init__(self, name, x, y, width, height, angle, speed):
        super().__init__(name, x, y)
        self.speed = speed
        self.width = width
        self.height = height
        self.angle = math.radians(angle)

    def move(self):
        "Move the object. Must be called each frame."
        xsp = math.cos(self.angle) * self.speed
        ysp = math.sin(self.angle) * self.speed
        if self.x + self.width + xsp >= 300:
            self.angle += 2*(math.pi/2 - self.angle)
        elif self.x + xsp <= 0:
            self.angle += 2*(math.pi/2 - self.angle)
        if self.y + self.height + ysp >= 300:
            self.angle += 2*(2*math.pi - self.angle)
        elif self.y + ysp <= 0:
            self.angle += 2*(2*math.pi - self.angle)
        xsp = math.cos(self.angle) * self.speed
        ysp = math.sin(self.angle) * self.speed
        self.x += xsp
        self.y += ysp

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, 10, 10))


# Set up game
pygame.init()

surface = pygame.display.set_mode((300, 300))
block1 = GameObjectBlock("joe", 1, 2)
projectile1 = GameObjectProjectile("bullet", 150, 150, 10, 10, 60, 10)
pygame.draw.circle(surface, (255, 0, 0), (30, 30), 10)
pygame.display.update()

# Game loop
while True:
    surface.fill("black")
    projectile1.move()
    projectile1.draw(surface)
    pygame.display.update()
    time.sleep(0.0166666667)
