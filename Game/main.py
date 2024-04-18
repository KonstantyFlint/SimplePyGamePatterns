import random

import pygame
import sys

from behavior.ai import ChasePlayer
from patterns.observer import Observer, KillEvent
from patterns.prototype import Spawner
from entity import Player, Monster, Projectile, entity_manager
from patterns.singleton import Singleton
from render import render_entity, render_game_info
from utils import get_sprite_and_rect

pygame.init()

screen_width = 1600
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Design Patterns")

clock = pygame.time.Clock()
FPS = 60

proto_bullet = Projectile(
    **get_sprite_and_rect(
        x=0,
        y=0,
        width=30,
        height=30,
        sprite_path="assets/plasma_ball.png",
    ),
    speed=30,
    register=False,
)

gun = Spawner(proto_bullet)

player = Player(
    **get_sprite_and_rect(
        x=screen_width // 2,
        y=screen_height // 2,
        width=100,
        height=100,
        sprite_path="assets/protagonist.png",
    ),
    speed=5,
    gun=gun,
)

proto_monster = Monster(
    **get_sprite_and_rect(
        x=0,
        y=0,
        width=100,
        height=100,
        sprite_path="assets/monster.png",
    ),
    speed=3,
    ai=ChasePlayer(),
    register=False,
)

proto_monster_2 = Monster(
    **get_sprite_and_rect(
        x=screen_width,
        y=0,
        width=150,
        height=150,
        sprite_path="assets/monster.png",
    ),
    speed=5,
    ai=ChasePlayer(),
    register=False,
)

monster_spawner = Spawner(proto_monster)
monster_spawner_2 = Spawner(proto_monster_2)

ALLOWED_EVENTS = [
    pygame.QUIT,
    pygame.MOUSEBUTTONDOWN,
]


def limit_input_event_types():
    pygame.event.set_blocked(None)
    pygame.event.set_allowed(ALLOWED_EVENTS)
    pygame.event.clear()


class _GameInfo(Singleton):

    def __init__(self):
        self.game_over = False
        self.kills = 0


game_info = _GameInfo()


class PlayerKilledObserver(Observer):

    def on_notify(self, event):
        if isinstance(event, KillEvent) and event.killed == player:
            game_info.game_over = True


class MonsterKilledObserver(Observer):

    def on_notify(self, event):
        if isinstance(event, KillEvent) and isinstance(event.killed, Monster):
            game_info.kills += 1


entity_manager.register_entity_observer(PlayerKilledObserver())
entity_manager.register_entity_observer(MonsterKilledObserver())

limit_input_event_types()


def should_run():
    return len(pygame.event.get(eventtype=pygame.QUIT)) == 0


while should_run():

    if not game_info.game_over and random.randint(0, 100) < 5:
        monster_spawner.spawn(y=random.randint(0, screen_height))
        monster_spawner_2.spawn(y=random.randint(0, screen_height))

    entity_manager.update()

    screen.fill((255, 255, 255))
    for entity in entity_manager:
        render_entity(entity, screen)

    render_game_info(game_info, screen)

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
sys.exit()
