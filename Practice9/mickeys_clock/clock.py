import datetime
import pygame


class MickeyClock:
    """A clock whose hands are Mickey Mouse's hands."""

    def __init__(self, center, image_path):
        self.center = center
        # The image shows a hand pointing UP; the pivot is the image center
        right = pygame.image.load(image_path).convert_alpha()
        # Left hand = mirrored right hand (horizontal flip)
        left = pygame.transform.flip(right, True, False)
        self.right_hand = right   # minutes hand
        self.left_hand = left     # seconds hand

    def get_time(self):
        """Return (minutes, seconds) of the current system time."""
        now = datetime.datetime.now()
        # min(..., 59) guards against a leap second (second == 60)
        return now.minute, min(now.second, 59)

    def _draw_hand(self, screen, image, angle):
        # pygame rotates COUNTER-clockwise, a clock moves clockwise -> minus sign
        rotated = pygame.transform.rotate(image, -angle)
        # Rotation changes the image size, so re-center it on the clock center
        rect = rotated.get_rect(center=self.center)
        screen.blit(rotated, rect)

    def draw(self, screen):
        minutes, seconds = self.get_time()
        minute_angle = minutes * 6 + seconds * 0.1   # 360 / 60 = 6 degrees per minute
        second_angle = seconds * 6                   # 6 degrees per second
        self._draw_hand(screen, self.right_hand, minute_angle)
        self._draw_hand(screen, self.left_hand, second_angle)

        # Digital time (mm:ss) for clarity
        font = pygame.font.SysFont("arial", 32)
        text = font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        screen.blit(text, text.get_rect(center=(self.center[0], 40)))