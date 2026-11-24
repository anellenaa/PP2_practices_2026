import os
import pygame
from player import MusicPlayer

BASE = os.path.dirname(os.path.abspath(__file__))


def fmt(sec):
    """Format seconds as m:ss."""
    sec = int(sec)
    return f"{sec // 60}:{sec % 60:02d}"


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 300))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)
    small = pygame.font.SysFont("arial", 20)

    player = MusicPlayer(os.path.join(BASE, "music"))

    running = True
    while running:
        # 1. Events: keyboard controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next()
                elif event.key == pygame.K_b:
                    player.previous()
                elif event.key == pygame.K_q:
                    running = False

        # 2. Logic: move on automatically when a track ends
        player.check_end()

        # 3. Drawing
        screen.fill((30, 30, 40))
        status = "Playing" if player.playing else "Stopped"
        title = f"Track {player.index + 1}/{len(player.playlist)}: {player.name()}"
        screen.blit(font.render(title, True, (255, 255, 255)), (30, 30))
        screen.blit(font.render(status, True, (120, 220, 120) if player.playing else (220, 120, 120)), (30, 75))

        # Progress bar: gray background + blue filled part
        pos = player.position()
        ratio = min(pos / player.length, 1) if player.length else 0
        pygame.draw.rect(screen, (80, 80, 90), (30, 140, 540, 20))
        pygame.draw.rect(screen, (90, 170, 255), (30, 140, int(540 * ratio), 20))
        screen.blit(small.render(f"{fmt(pos)} / {fmt(player.length)}", True, (255, 255, 255)), (30, 170))

        screen.blit(small.render("P=Play  S=Stop  N=Next  B=Back  Q=Quit", True, (200, 200, 200)), (30, 250))

        # 4. Show the frame
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    main()