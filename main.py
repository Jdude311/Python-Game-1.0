import math
import numpy
import time
import pygame


class GameObject:
    def __init__(self, name, position, dimensions):
        self.name = str(name)
        self.x = position[0]
        self.y = position[1]
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def __str__(self):
        return self.name + " at position (" + str(self.x) + ", " + str(self.y) + ")\n"
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def checkCollision(self, entity_rect):
        if self.rect.collideRect(entity_rect):
            return True;
        else: 
            return False;


class GameObjectPlayer(GameObject):
    def __init__(self, name, position, dimensions):
        super().__init__(name, position, dimensions)
        self.angle = 0
        self.xsp = 0
        self.ysp = 0
        self.speed = 0

    def takeInput(self, input):
        angleSum = 0
        angleNumber = 0
        if input[pygame.K_d] or input[pygame.K_a] or input[pygame.K_s] or input[pygame.K_w]:
            self.speed = numpy.maximum(1 + self.speed * 0.001, 5)
            if input[pygame.K_a]:
                angleSum += math.pi
                angleNumber += 1
            if input[pygame.K_s]:
                angleSum += math.pi/2
                angleNumber += 1
            if input[pygame.K_w]:
                angleSum += 3*math.pi/2
                angleNumber += 1
            if input[pygame.K_d] and angleSum % (math.pi * 2) < math.pi:
                angleSum += 0
                angleNumber += 1
            elif input[pygame.K_d] and angleSum % (math.pi * 2) >= math.pi:
                angleSum += math.pi * 2
                angleNumber += 1
            self.angle = (angleSum / angleNumber)
        else:
            self.speed = numpy.minimum(self.speed*0.999 + 1 if self.speed != 0 else 0, 0)
        
        self.xsp = self.speed * math.cos(self.angle)
        self.ysp = self.speed * math.sin(self.angle)

    def move(self):        
        self.x += self.xsp
        self.y += self.ysp


class GameObjectBlock(GameObject):
    "Nonmoving object with position. Used for blocks."
    def __init__(self, name, position, dimensions):
        super().__init__(name, position, dimensions)


class GameObjectProjectile(GameObject):
    "This type of object has a speed, which contains information for x and y speed. It is a list."
    def __init__(self, name, position, dimensions, angle, speed):
        super().__init__(name, position, dimensions)
        self.speed = speed
        self.angle = angle
        self.xsp = math.cos(self.angle) * self.speed
        self.ysp = math.sin(self.angle) * self.speed

    def move(self):
        "Move the object. Must be called each frame."
        if self.x + self.width + self.xsp >= screen.get_size()[0] or self.x + self.xsp <= 0:
            self.xsp = -self.xsp
        else:
            self.xsp = self.xsp * 0.95
        if self.y + self.height + self.ysp >= screen.get_size()[1] or self.y + self.ysp <= 0:
            self.ysp = -self.ysp
        else:
            self.ysp = round((self.ysp + 2) * 0.95)  # Only gravity if not on ground
        # Move object
        self.x += self.xsp
        self.y += self.ysp
        # Set angle using methamphet--I mean, math
        self.angle = abs(-math.atan2(self.ysp, self.xsp) - math.pi)
        #print(round(math.degrees(self.angle)))


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
#screen = pygame.display.set_mode((300, 300), pygame.RESIZABLE)
screen = pygame.display.set_mode((640, 480), pygame.RESIZABLE)

entities = []
# Blocks
entities.append(GameObjectBlock("block", (0, 275), (100, 25)))

# Projectiles
entities.append(GameObjectProjectile("proj", (0, 300), (10, 10), math.pi/4, 50))

# Player
entities.append(GameObjectPlayer("player", (100, 100), (50,50)))


# Game loop
running = True;
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    # Clear Screen
    screen.fill("black")
    # Update object states
    for entity in entities:
        if callable(getattr(entity, "takeInput", None)):  # Take input
            entity.takeInput(keys)
        if callable(getattr(entity, "move", None)):  # Move objects
            entity.move()
        if callable(getattr(entity, "draw", None)):  # Draw objects
            entity.draw(screen)
    # Refresh Screen
    pygame.display.update()
    time.sleep(0.0166666667)

pygame.quit()
