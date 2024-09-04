import pygame
from constants import *
from Abstract.CircleShape import CircleShape
from Sprites.Shot import *
import sys

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0

        self.acceleration = 2
        self.velocity = pygame.Vector2(0, 0)
        self.friction = 0.98  # Friction to slow down the player


        self.timer = 0
        self.lives = 3
        self.invincible = False
        self.respawn_time = 2  # 2 seconds of invincibility after respawn
        self.last_respawn = None

    def draw(self, screen):
        # If the player is invincible, you can draw them with a different color or effect
        color = "white" if not self.invincible else "grey"
        pygame.draw.polygon(screen, color, self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)

        # Rotation
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        # Shooting
        if keys[pygame.K_SPACE]:
            self.shoot()

        if self.timer > 0:
            self.timer -= dt


        # Update the player's position based on velocity
        self.position += self.velocity * dt

        self.velocity *= self.friction

        # Check invincibility timer
        if self.invincible:
            if pygame.time.get_ticks() - self.last_respawn >= self.respawn_time * 1000:
                self.invincible = False  # End invincibility after respawn time

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.velocity += forward * PLAYER_SPEED * dt * self.acceleration

    def shoot(self):
        if self.timer > 0:
            return
        new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        new_shot.velocity += pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.timer = PLAYER_SHOOT_COOLDOWN

    def killPlayer(self):
        self.kill()
        self.lives -= 1

        if self.lives > 0:
            # Initiate respawn process
            self.respawn()
        
        if self.lives <= 0:
            sys.exit(0)

    def respawn(self):
        # Reset position, mark as invincible, and set respawn time
        self.position = pygame.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.invincible = True
        self.last_respawn = pygame.time.get_ticks()

        # Optionally, re-add the player sprite to the groups it belongs to
        self.add(Player.containers)


    