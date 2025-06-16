import random
import pygame
import pymunk

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


class BodySprite(pygame.sprite.Sprite):
    body_num = 0
    def __init__(self, x, y, mass, collision_type, color=(255, 0, 0), category=pymunk.Body.DYNAMIC):
        super().__init__(bodies)
        self.color = color

        self.m = mass
        self.body = pymunk.Body(self.m, 100, category)
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
    def __init__(self, x, y, r, collision_type=0, color=(255, 0, 0)):
        super().__init__(x, y, 5, collision_type, color=color)
        # self.body.velocity = random.uniform(-500, 500), random.uniform(-500, 500)

        self.radius = r
        self.h, self.w = self.radius * 2, self.radius * 2

        self.shape = pymunk.Circle(self.body, self.radius)
        # print(self.body)
        self.shape.density = 1  # when shape inits, density must be manually set
        self.shape.elasticity = 1

        self.shape.collision_type = collision_type  # shape.collsiion_type is *separate* from init

    def draw(self, s):
        if self.shape.collision_type == 2:
            self.color = (0, 0, 255)
        else:
            self.color = (255, 0, 0)
        pygame.draw.circle(s, self.color, (self.x, self.y), self.radius)

    def tagged(self, arbiter, space, data):
        self.shape.collision_type = 2
        # return True


class Floor(BodySprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, category=pymunk.Body.STATIC)

        self.x1, self.y1 = self.start = x1, y1
        self.x2, self.y2 = self.end = x2, y2
        print(self.start, self.end)

        self.shape = pymunk.Segment(self.body, self.start, self.end, 5)
        self.shape.elasticity = 1

    def draw(self, s):
        pygame.draw.line(s, self.color, self.start, self.end, 5)

def collide(arbiter, space, data):
    print('hello')
    return True

# floor = Floor(0, 700, 800, 100)
# ball1 = Ball(200, 600, 10, 1)
# ball2 = Ball(500, 600, 10, 2)
class Rope:
    def __init__(self, body, attachment):
        self.body1 = body
        if isinstance(attachment, pymunk.Body):
            print('body', attachment)
            self.body2 = attachment

        elif isinstance(attachment, tuple):
            print('coords', attachment)
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = flip(*attachment)
        joint = pymunk.PinJoint(self.body1, self.body2)
        SPACE.add(joint)

        self.start = self.body1.position
        self.end = self.body2.position

    def update(self):
        self.start = self.body1.position
        self.end = self.body2.position

    def draw(self, s):
        print(self.start, self.end)
        pygame.draw.line(s, (0, 0, 0), self.start, self.end, 3)



def main():
    # balls = [Ball(random.randint(0, W), random.randint(0, H), 10, i + 3) for i in range(200)]
    # balls.append(Ball(400, 400, 10, 2, ))
    #
    ball1 = Ball(300, 600, 10,)
    ball2 = Ball(200, 150, 10, )
    rope1 = Rope(ball1.body, (300, 550))
    rope2 = Rope(ball1.body, ball2.body)

    for sprite in bodies:
        SPACE.add(sprite.body, sprite.shape)
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
        rope1.update()
        rope2.update()
        # print(bodies)

        DISPLAY.fill('white')

        for body in bodies:
            body.draw(DISPLAY)
        rope1.draw(DISPLAY)
        rope2.draw(DISPLAY)

        # x, y = body.position
        # pygame.draw.circle(DISPLAY, 'red', (round(x), int(y)), 10)
        # DISPLAY.blit(ball1.image, (ball1.x, ball1.y), )


        pygame.display.update()
        CLOCK.tick(60)
        SPACE.step(1/60)


main()
pygame.quit()
