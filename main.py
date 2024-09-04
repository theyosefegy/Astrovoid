import pygame
from constants import *
from Sprites.Player import Player
from Sprites.Asteroid import Asteroid
from Abstract.asteroidfield import AsteroidField
from Sprites.Shot import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, FONT_SIZE)
    score = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shotsGroup = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shotsGroup, drawable, updatable)
    Player.containers = (updatable, drawable)
    
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        for asteroid in asteroids:
            for shot in shotsGroup:
                if(shot.isInCollide(other_circle=asteroid)):
                    asteroid.split()
                    shot.kill()
                    score += 10

            if player.isInCollide(asteroid):
                player.killPlayer()


        for obj in updatable:
            obj.update(dt)

        for shot in shotsGroup:
            shot.update(dt)


        for obj in drawable:
            obj.draw(screen)

        # ".render()" Creates a new Surface object, which means we will need to use the ".blit()" function
        score_text = font.render(f"Score: {score}", True, "white")
        lives_text = font.render(f"Lives: {player.lives}", True, "white")
         # This will copy the text from the surface it was created and paste it in the "Screen" Surface.
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()
        screen.fill("black")

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
