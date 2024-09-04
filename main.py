import pygame
from constants import *
from Player import Player
from Asteroid import Asteroid
from asteroidfield import AsteroidField
from Shot import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

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

            if (player.isInCollide(asteroid)):
                print("Game Over!")
                return
            
        screen.fill("black")    
        for obj in updatable:
            obj.update(dt)

        for shot in shotsGroup:
            shot.update(dt)


        for obj in drawable:
            obj.draw(screen)

        pygame.display.flip()
        screen.fill("black")

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000


if __name__ == "__main__":
    main()
