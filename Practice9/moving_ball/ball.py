import pygame


class Ball:
    RADIUS = 25          # ball size is 50x50
    STEP = 20            # pixels moved per key press
    COLOR = (255, 0, 0)  # red

    def __init__(self, screen_width, screen_height):
        self.sw = screen_width
        self.sh = screen_height
        self.x = screen_width // 2    # x, y is the CENTER of the ball
        self.y = screen_height // 2

    def move(self, dx, dy):
        """Move the ball, but only if it stays fully inside the screen."""
        new_x = self.x + dx
        new_y = self.y + dy
        if (new_x - self.RADIUS >= 0 and new_x + self.RADIUS <= self.sw and
                new_y - self.RADIUS >= 0 and new_y + self.RADIUS <= self.sh):
            self.x, self.y = new_x, new_y
        # otherwise the input is simply ignored

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS)