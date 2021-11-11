import math
import numpy
import time
import pygame


class GameObject:
    def __init__(self, name, position, dimensions):
        self.name = str(name)
        self.x = position[0]
        self.y = position[1]
        self.xsp = 0
        self.ysp = 0
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.collisionDirections = [0,0,0,0]  # up, down, left, right
    
    def __str__(self):
        return self.name + " at position (" + str(self.x) + ", " + str(self.y) + ")\n"
    
    def draw(self, screen):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, (255, 0, 0), self.rect)

    def checkCollision(self, entity_list):
        self.collisionDirections = [0,0,0,0]
        rect_next = self.rect.move(self.xsp, self.ysp)
        collisions = rect_next.collidelistall(entity_list)
        if len(collisions) > 0:
            for colliding_entity in collisions:
                if entity_list[colliding_entity].y <= self.y:
                    self.collisionDirections[0] = 1
                if entity_list[colliding_entity].y >= self.y:
                    self.collisionDirections[1] = 1
                if entity_list[colliding_entity].x >= self.x: 
                    self.collisionDirections[3] = 1
                if entity_list[colliding_entity].x <= self.x: 
                    self.collisionDirections[2] = 1



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
            self.speed = numpy.maximum(0.25 + self.speed * 0.01, 10)  # Maximum speed
            if input[pygame.K_a]:
                angleSum += math.pi
                angleNumber += 1
            if input[pygame.K_s]:
                angleSum += math.pi/2
                angleNumber += 1
            if input[pygame.K_w]:
                angleSum += 3*math.pi/2
                angleNumber += 1
            if input[pygame.K_d] and angleSum % (math.pi * 2) <= math.pi:
                angleSum += 0
                angleNumber += 1
            elif input[pygame.K_d] and angleSum % (math.pi * 2) >= math.pi:
                angleSum += math.pi * 2
                angleNumber += 1
        else:
            self.speed = numpy.minimum(self.speed*0.99 + 1 if self.speed != 0 else 0, 0)
        if angleNumber != 0:
            self.angle = (angleSum / angleNumber) 

        xsp_prelim = self.speed * math.cos(self.angle)
        ysp_prelim = self.speed * math.sin(self.angle)
        if numpy.sign(xsp_prelim) < 0 and self.collisionDirections[2] == 0:
            self.xsp = xsp_prelim
        elif numpy.sign(xsp_prelim) > 0 and self.collisionDirections[3] == 0:
            self.xsp = xsp_prelim
        else:
            self.xsp = 0

        if numpy.sign(ysp_prelim) < 0 and self.collisionDirections[0] == 0:
            self.ysp = ysp_prelim
        elif numpy.sign(ysp_prelim) > 0 and self.collisionDirections[1] == 0:
            self.ysp = ysp_prelim
        else:
            self.ysp = 0

    def move(self):
        self.rect = self.rect.move(self.xsp, self.ysp)
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

entities = {"player": [], "blocks": [], "projectiles": []}
# Blocks
entities["blocks"].append(GameObjectBlock("block", (0, 275), (100, 25)))

# Projectiles
entities["projectiles"].append(GameObjectProjectile("proj", (0, 300), (10, 10), math.pi/4, 50))

# Player
entities["player"].append(GameObjectPlayer("player", (100, 100), (50,50)))


# Game loop
running = True;
collision = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    keys = pygame.key.get_pressed()
    # Clear Screen
    screen.fill("black")
    # Update object states
    for block in entities["blocks"]:
        if callable(getattr(block, "draw", None)):  # Draw objects
            block.draw(screen)
    for projectile in entities["projectiles"]:
        if callable(getattr(projectile, "checkCollision", None)):  # Draw objects
            projectile.checkCollision(entities["blocks"])
            projectile.checkCollision(entities["player"])
        if callable(getattr(projectile, "move", None)):  # Draw objects
            projectile.move()
        if callable(getattr(projectile, "draw", None)):  # Draw objects
            projectile.draw(screen)
    for player in entities["player"]:
        if callable(getattr(player, "checkCollision", None)) and player.name == "player":  # Check player collisions
            #player.checkCollision((lambda : list(filter(lambda a : a != player, entities)))())  # Collision with not self
            player.checkCollision(entities["blocks"])
        if callable(getattr(player, "takeInput", None)):  # Take input
            player.takeInput(keys)
        if callable(getattr(player, "move", None)):  # Move objects
            player.move()
        if callable(getattr(player, "draw", None)):  # Draw objects
            player.draw(screen)
    # Refresh Screen
    pygame.display.update()
    time.sleep(0.0166666667)

pygame.quit()
# this is pretty f'in cool
