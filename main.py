import random
import pygame
import pymunk

"""Started June 14 2025
from Pymunk Basics by Ear of Corn Programming


"""


pygame.init()
W, H = 800, 700
DISPLAY = pygame.display.set_mode((W, H))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
SPACE.gravity = (0, 1000)

def clear_surface(h, w, fill=None):
    if fill is None:
        return pygame.Surface((h, w), pygame.SRCALPHA)
    else:
        s = pygame.Surface((h, w))
        s.fill(fill)
        return s

def flip(x, y, null=False):
    if not null:
        return x, H - y
    else:
        return x, y

bodies = pygame.sprite.Group()
joints = pygame.sprite.Group()


class BodySprite(pygame.sprite.Sprite):
    body_num = 0
    def __init__(self, x, y, mass=0, collision_type=0, color=(255, 0, 0), category=pymunk.Body.DYNAMIC):
        super().__init__(bodies)
        self.color = color

        self.m = mass
        self.body = pymunk.Body(self.m, body_type=category)
        self.body.position = self.x, self.y = flip(x, y)

        self.shape = pymunk.Circle(self.body, 10)  # pymunk.Poly(self.body, [(-1, 1), (1, 1), (1, -1), (-1, -1)])
        self.shape.density = 1
        # BodySprite.body_num += 1
        # self.shape.collision_type = collision_type  # BodySprite.body_num

    def update(self):
        self.x, self.y = self.body.position


    def draw(self, s):
        pass


class Ball(BodySprite):
    def __init__(self, x, y, r, collision_type=0, group=0, color=(255, 0, 0)):
        super().__init__(x, y, 5, collision_type, color=color)
        # self.body.velocity = random.uniform(-500, 500), random.uniform(-500, 500)

        self.radius = r
        self.h, self.w = self.radius * 2, self.radius * 2

        self.shape = pymunk.Circle(self.body, self.radius)
        # print(self.body)
        self.shape.density = 1  # when shape inits, density must be manually set
        self.shape.elasticity = 1

        self.shape.collision_type = collision_type  # shape.collsiion_type is *separate* from init
        self.shape.filter = pymunk.ShapeFilter(group=group)

    def draw(self, s):
        # if self.shape.collision_type == 2:
        #     self.color = (0, 0, 255)
        # else:
        #     self.color = (255, 0, 0)
        pygame.draw.circle(s, self.color, (self.x, self.y), self.radius)

    # def tagged(self, arbiter, space, data):
    #     self.shape.collision_type = 2
    #     # return True


class Platform(BodySprite):
    def __init__(self, x1, y1, x2, y2, color=(0, 0, 0), group=0):
        super().__init__(x1, y1, color=color, category=pymunk.Body.STATIC)
        print(self.body)

        self.x1, self.y1 = x1, y1
        self.x2, self.y2 = x2, y2
        self.start, self.end = 0, 0

        self.shape = pymunk.Segment(self.body, (0, 0), (600, 0), 5)
        self.shape.elasticity = 1
        self.shape.density = 1
        self.shape.filter = pymunk.ShapeFilter(group=group)
        # SPACE.add(self.body, self.shape)
    def update(self):
        self.start = flip(self.x1, self.y1)
        self.end = flip(self.x2, self.y2)

    def draw(self, s):
        pygame.draw.line(s, self.color, self.start, self.end, 5)


def collide(arbiter, space, data):
    print('hello')
    return True

# floor = Floor(0, 700, 800, 100)
# ball1 = Ball(200, 600, 10, 1)
# ball2 = Ball(500, 600, 10, 2)
class Rope(pygame.sprite.Sprite):
    def __init__(self, body, attachment):
        super().__init__(joints)
        self.body1 = body
        if isinstance(attachment, pymunk.Body):
            self.body2 = attachment

        elif isinstance(attachment, tuple):
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = flip(*attachment)
        self.joint = pymunk.PinJoint(self.body1, self.body2)

        self.start = self.body1.position
        self.end = self.body2.position

    def update(self):
        self.start = self.body1.position
        self.end = self.body2.position

    def draw(self, s):
        pygame.draw.line(s, (0, 0, 0), self.start, self.end, 3)



def main():
    # balls = [Ball(random.randint(0, W), random.randint(0, H), 10, i + 3) for i in range(200)]
    # balls.append(Ball(400, 400, 10, 2, ))
    #
    ball1 = Ball(150, 600, 10, color=(255, 0, 0), group=1)
    ball2 = Ball(300, 600, 10, color=(0, 255, 0), group=1)
    ball3 = Ball(450, 600, 10, color=(0, 0, 255), group=1)
    platform1 = Platform(0, 400, W, 400, (0, 0, 0), group=1)
    platform2 = Platform(0, 100, W, 100, (128, 64, 0), group=2)

    # rope1 = Rope(ball1.body, (300, 550))
    # rope2 = Rope(ball1.body, ball2.body)

    for sprite in bodies:
        print(sprite.body, sprite.shape)
        SPACE.add(sprite.body, sprite.shape)
    for sprite in joints:
        SPACE.add(sprite.joint)
    #
    #
    # handlers = [SPACE.add_collision_handler(2, i + 3) for i in range(200)]
    # for i, handler in enumerate(handlers):
    #     handler.separate = balls[i].tagged


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        bodies.update()
        joints.update()

        # images, blitting
        DISPLAY.fill('white')

        for body in bodies:
            # print(body)
            body.draw(DISPLAY)
        for joint in joints:
            joint.draw(DISPLAY)

        pygame.display.update()
        CLOCK.tick(60)
        SPACE.step(1/60)


main()
pygame.quit()
