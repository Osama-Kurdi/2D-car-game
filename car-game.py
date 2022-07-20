
# 2D CAR GAME 

import os
import pygame
from pygame.math import Vector2
from math import radians, degrees, sin, copysign

pygame.init()


class Car:
    def __init__(self, x, y, car_length, max_acceleration, max_steering):
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.steering = 0
        self.acceleration = 0.0
        self.car_length = car_length
        self.angle = 0

        self.max_acceleration = max_acceleration
        self.max_steering = max_steering
        self.max_velocity = 20
        self.brake_deceleration = 10
        self.free_deceleration = 2

    def move(self, pressed, dt):
        if pressed[pygame.K_UP]:
            if self.velocity.x < 0:
                self.acceleration = self.brake_deceleration
            else:
                self.acceleration += 1 * dt
        elif pressed[pygame.K_DOWN]:
            if self.velocity.x > 0:
                self.acceleration = -self.brake_deceleration
            else:
                self.acceleration -= 1 * dt
        elif pressed[pygame.K_SPACE]:
            if abs(self.velocity.x) > dt * self.brake_deceleration:
                self.acceleration = -copysign(self.brake_deceleration, self.velocity.x)
            else:
                self.acceleration = -self.velocity.x / dt
        else:
            if abs(self.velocity.x) > dt * self.free_deceleration:
                self.acceleration = -copysign(self.free_deceleration, self.velocity.x)
            else:
                if dt != 0:
                    self.acceleration = -self.velocity.x / dt
        self.acceleration = max(-self.max_acceleration, min(self.acceleration, self.max_acceleration))

        if pressed[pygame.K_RIGHT]:
            self.steering -= 30 * dt
        elif pressed[pygame.K_LEFT]:
            self.steering += 30 * dt
        else:
            self.steering = 0
        self.steering = max(-self.max_steering, min(self.steering, self.max_steering))

    def update_car(self, dt):
        print(dt)
        self.velocity += (self.acceleration * dt, 0)
        if self.steering:
            turning_radius = self.car_length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        self.position += self.velocity.rotate(-self.angle) * dt
        self.angle += degrees(angular_velocity) * dt


class Game:
    def __init__(self):
        self.running = True
        self.ticks = 320
        self.current_lvl = 0
        self.clock = pygame.time.Clock()
        self.car = Car(10, 0, 3, 6, 30)
        self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.car_img = pygame.image.load('car.png').convert_alpha()
        self.font = pygame.font.SysFont("monospace", 15)

    def draw(self):
        self.display.fill((0, 0, 0))
        rotated = pygame.transform.rotate(self.car_img, self.car.angle)
        rect = rotated.get_rect()
        label = self.font.render("Made by MHD Usama Kurdi", 1, (255,255,0))
        self.display.blit(label, (100, 100))
        self.display.blit(rotated, self.car.position * 32 - (rect.width / 2, rect.height / 2))
        # self.car.check_collision(rect, self.cars[self.current_lvl])
        pygame.display.update()

    def run(self):
        while self.running:
            dt = self.clock.get_time() / 1000
            key = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
                    self.running = False
                    return

            self.car.update_car(dt)
            self.car.move(key, dt)
            self.draw()
            self.clock.tick(self.ticks)


if __name__ == '__main__':
    game = Game()
    game.run()
pygame.quit()
