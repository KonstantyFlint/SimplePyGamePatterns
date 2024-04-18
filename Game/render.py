import pygame
from pygame import Surface

from entity import Entity


def render_entity(character: Entity, screen: Surface):
    return screen.blit(character.sprite, character.rect)


def render_game_info(game_info, screen: Surface):
    if game_info.game_over:
        font = pygame.font.Font(None, 100)
        game_over_text = font.render("SKILL ISSUE", True, (0, 0, 255))
        text_rect = game_over_text.get_rect()
        text_rect.center = (screen.get_rect().width // 2, screen.get_rect().height // 2)
        screen.blit(game_over_text, text_rect)
    font = pygame.font.Font(None, 100)
    game_over_text = font.render(str(game_info.kills), True, (0, 0, 255))
    text_rect = game_over_text.get_rect()
    text_rect.center = (screen.get_rect().width - 200, 100)
    screen.blit(game_over_text, text_rect)
