import pygame
from ball import Ball

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Moving Ball")
    clock = pygame.time.Clock()
    ball = Ball(WIDTH, HEIGHT)

    running = True
    while running:
        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:   # one key press = one step
                if event.key == pygame.K_UP:
                    ball.move(0, -Ball.STEP)     # y grows downward, so up is negative
                elif event.key == pygame.K_DOWN:
                    ball.move(0, Ball.STEP)
                elif event.key == pygame.K_LEFT:
                    ball.move(-Ball.STEP, 0)
                elif event.key == pygame.K_RIGHT:
                    ball.move(Ball.STEP, 0)

        # 2. Drawing
        screen.fill(WHITE)
        ball.draw(screen)

        # 3. Show the frame
        pygame.display.flip()
        clock.tick(60)   # frame rate control: max 60 FPS

    pygame.quit()


if __name__ == "__main__":
    main()