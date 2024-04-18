from typing import List

from patterns.command import MoveRight, MoveLeft, MoveUp, MoveDown, DoNothing, Command


class AI:

    def get_commands(self, ai_entity):
        raise NotImplementedError()


class ChasePlayer(AI):

    def get_commands(self, ai_entity) -> List[Command]:

        from entity import Player, entity_manager
        player_list = list(entity_manager.get_entities_map(Player).values())
        if len(player_list) == 0:
            return [DoNothing()]

        player = player_list[0]
        dx = player.x - ai_entity.x
        dy = player.y - ai_entity.y

        if abs(dx) > abs(dy):
            if dx > 0:
                return [MoveRight()]
            else:
                return [MoveLeft()]
        else:
            if dy > 0:
                return [MoveDown()]
            else:
                return [MoveUp()]
