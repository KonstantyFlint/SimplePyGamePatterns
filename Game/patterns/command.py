from math import sqrt

import pygame


class Command:

    def execute(self, entity):
        raise NotImplementedError()


class DoNothing(Command):

    def execute(self, entity):
        pass


class MoveRight(Command):

    def execute(self, entity):
        entity.x += entity.speed


class MoveLeft(Command):

    def execute(self, entity):
        entity.x -= entity.speed


class MoveUp(Command):

    def execute(self, entity):
        entity.y -= entity.speed


class MoveDown(Command):

    def execute(self, entity):
        entity.y += entity.speed


class ShootAtCursor(Command):

    def execute(self, entity):
        gun = getattr(entity, "gun")
        if gun is None:
            return
        (target_x, target_y) = pygame.mouse.get_pos()
        (x_center, y_center) = entity.center
        dx = target_x - x_center
        dy = target_y - y_center
        distance = sqrt(dx * dx + dy * dy)
        if distance == 0:
            distance = 1
        dx_normalized = dx / distance
        dy_normalized = dy / distance
        gun.spawn(
            center=entity.center,
            dx_normalized=dx_normalized,
            dy_normalized=dy_normalized,
        )
