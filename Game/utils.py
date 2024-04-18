from typing import Optional

import pygame


def in_proximity(a: "Entity", b: "Entity", distance: Optional[float] = None):
    if distance is None:
        distance = (a.width + a.height + b.width + b.height) / 4
    a_x, a_y = a.center
    b_x, b_y = b.center
    dx = b_x - a_x
    dy = b_y - a_y
    return (dx * dx + dy * dy) <= (distance * distance)


def get_sprite_and_rect(x: int, y: int, width: int, height: int, sprite_path: str):
    sprite = pygame.image.load(sprite_path)
    sprite = pygame.transform.scale(sprite, (width, height))
    rect = sprite.get_rect(center=(x, y))

    return {
        "sprite": sprite,
        "rect": rect,
    }
