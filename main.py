from symbol import return_stmt

import pygame
import pymunk

pygame.init()
DISPLAY = pygame.display.set_mode((800, 700))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
SPACE.gravity = (0, 1000)

body = pymunk.Body(5)
body.position = 200, 10
shape = pymunk.Circle(body, 10)
shape.density = 1
shape.elasticity = 1
SPACE.add(body, shape)

body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
shape2 = pymunk.Segment(body2, (0, 400), (800, 600), 5)
shape2.elasticity = 1
SPACE.add(body2, shape2)

def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        DISPLAY.fill('white')

        x, y = body.position
        pygame.draw.circle(DISPLAY, 'red', (round(x), int(y)), 10)
        pygame.draw.line(DISPLAY, (0, 0, 0), (0, 400), (800, 600), 5)

        pygame.display.update()
        CLOCK.tick(60)
        SPACE.step(1/60)


main()
pygame.quit()
