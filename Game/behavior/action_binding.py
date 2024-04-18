from typing import Dict, List

import pygame

from patterns.command import MoveUp, MoveDown, MoveLeft, MoveRight, ShootAtCursor, Command

default_key_binding = {
    pygame.K_w: MoveUp(),
    pygame.K_s: MoveDown(),
    pygame.K_a: MoveLeft(),
    pygame.K_d: MoveRight(),
}

default_mouse_binding = {
    pygame.BUTTON_LEFT: ShootAtCursor(),
}


class Binding:

    def __init__(self, key_binding: Dict[int, Command] = None, mouse_binding: Dict[int, Command] = None):
        if key_binding is None:
            key_binding = default_key_binding
        if mouse_binding is None:
            mouse_binding = default_mouse_binding
        self.key_binding = key_binding
        self.mouse_binding = mouse_binding

    def get_commands(self) -> List[Command]:
        pressed_keyboard_buttons = pygame.key.get_pressed()
        pressed_mouse_buttons = {
            event.button for event in pygame.event.get(eventtype=pygame.MOUSEBUTTONDOWN)
        }

        commands = []
        for (key, command) in self.key_binding.items():
            if pressed_keyboard_buttons[key]:
                commands.append(command)
        for (button, command) in self.mouse_binding.items():
            if button in pressed_mouse_buttons:
                commands.append(command)

        return commands
