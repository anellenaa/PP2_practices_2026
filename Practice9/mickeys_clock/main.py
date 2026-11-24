import os
import pygame
from clock import MickeyClock

BASE = os.path.dirname(os.path.abspath(__file__))


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Mickey's Clock")
    clock_obj = pygame.time.Clock()

    center = (300, 320)
    mickey = MickeyClock(center, os.path.join(BASE, "images", "mickey_hand.png"))

    running = True
    while running:
        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Drawing: white background and clock face
        screen.fill((255, 255, 255))
        pygame.draw.circle(screen, (0, 0, 0), center, 260, 4)
        for i in range(12):  # 12 hour marks around the circle
            v = pygame.math.Vector2(0, -245).rotate(i * 30)
            pygame.draw.circle(screen, (0, 0, 0), (center[0] + v.x, center[1] + v.y), 6)

        # Hands (time is read from the system clock, so it is always in sync)
        mickey.draw(screen)

        # 3. Show the frame
        pygame.display.flip()
        clock_obj.tick(30)  # limit to 30 frames per second

    pygame.quit()


if __name__ == "__main__":
    main()