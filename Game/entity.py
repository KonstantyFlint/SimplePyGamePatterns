from collections import defaultdict
from typing import Dict, Tuple
from uuid import uuid4

from pygame import Rect, Surface

from behavior.action_binding import Binding
from behavior.ai import AI
from patterns.observer import Observable, KillEvent, Observer
from patterns.prototype import Prototype, Spawner
from patterns.singleton import Singleton
from utils import in_proximity


class _EntityManager(Singleton):
    def __init__(self):
        self._entities = {}
        self._entities_by_class = defaultdict(dict)
        self._register_queue = []
        self._unregister_queue = []
        self._observers = {}

    def update(self):
        self._perform_register()
        self._perform_update()
        self._perform_unregister()

    def register(self, entity: "Entity"):
        self._register_queue.append(entity)

    def unregister(self, entity: "Entity"):
        self._unregister_queue.append(entity)

    def register_entity_observer(self, observer: Observer, predicate=lambda e: True):
        for entity in self:
            if isinstance(entity, Observable) and predicate(entity):
                entity.add_observer(observer)
        self._observers[observer] = predicate

    def unregister_entity_observer(self, observer: Observer):
        for entity in self:
            if isinstance(entity, Observable):
                entity.remove_observer(observer)
        del self._observers[observer]

    def get_entities_map(self, klass=None) -> Dict[uuid4, "Entity"]:
        if klass is not None:
            return self._entities_by_class[klass]
        return self._entities

    def _perform_update(self):
        for entity in self._entities.values():
            entity.update()

    def _perform_register(self):
        for entity in self._register_queue:
            self._entities[entity.id] = entity
            self._entities_by_class[type(entity)][entity.id] = entity
            for (observer, predicate) in self._observers.items():
                if isinstance(entity, Observable) and predicate(entity):
                    entity.add_observer(observer)
        self._register_queue = []

    def _perform_unregister(self):
        for entity in self._unregister_queue:
            if entity.id in self._entities:
                del self._entities[entity.id]
                del self._entities_by_class[type(entity)][entity.id]
        self._unregister_queue = []

    def __iter__(self):
        yield from iter(self._entities.values())


entity_manager = _EntityManager()


class Entity:

    def __init__(self, rect: Rect, sprite: Surface, speed: int, register=True):
        self.rect = rect  # position and size
        self.sprite = sprite
        self.speed = speed
        self.id = uuid4()
        if register:
            entity_manager.register(self)

    def __del__(self):
        entity_manager.unregister(self)

    def update(self):
        pass

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    @property
    def width(self):
        return self.rect.width

    @width.setter
    def width(self, value):
        self.rect.width = value

    @property
    def height(self):
        return self.rect.height

    @height.setter
    def height(self, value):
        self.rect.height = value

    @property
    def center(self) -> Tuple[int, int]:
        return (
            self.x + self.width // 2,
            self.y + self.height // 2,
        )

    @center.setter
    def center(self, pos: Tuple[int, int]):
        (x_center, y_center) = pos
        self.x = x_center - self.width // 2
        self.y = y_center - self.height // 2


class PrototypeEntity(Entity, Prototype):
    keep_shallow = ("sprite",)
    ignore = ("id", "_observers")


class AIControlledEntity(Entity):

    def __init__(self, rect: Rect, sprite: Surface, speed: int, ai: AI, register: bool = True):
        super().__init__(rect, sprite, speed, register)
        self.ai = ai

    def update(self):
        for command in self.ai.get_commands(self):
            command.execute(self)
        super().update()


class KillerEntity(Entity, Observable):
    kill_class: Tuple[Entity, ...] = (),

    def __init__(self, rect: Rect, sprite: Surface, speed: int, register: bool = True):
        super().__init__(rect, sprite, speed, register)
        self._observers = set()

    def update(self):
        for klass in self.kill_class:
            for entity in entity_manager.get_entities_map(klass).values():
                if in_proximity(self, entity):
                    entity_manager.unregister(entity)
                    self.notify(KillEvent(self, entity))


class Player(Entity, Singleton):
    def __init__(self, rect: Rect, sprite: Surface, speed: int, gun: Spawner, binding: Binding = Binding()):
        super().__init__(rect, sprite, speed)
        self.gun = gun
        self.binding = binding

    def update(self):
        for command in self.binding.get_commands():
            command.execute(self)


class Monster(AIControlledEntity, PrototypeEntity, KillerEntity):
    kill_class = (Player,)

    def __init__(self, rect: Rect, sprite: Surface, speed: int, ai: AI, register: bool = True):
        super().__init__(rect, sprite, speed, ai, register)


class Projectile(PrototypeEntity, KillerEntity):
    kill_class = (Monster,)

    def __init__(
            self,
            rect: Rect,
            sprite: Surface,
            speed: int,
            dx_normalized: float = 0.0,
            dy_normalized: float = 0.0,
            lifetime: int = 60,
            register=True
    ):
        super().__init__(rect, sprite, speed, register)
        self.dx_normalized = dx_normalized
        self.dy_normalized = dy_normalized
        self.lifetime = lifetime

    def update(self):
        super().update()
        self.x += self.speed * self.dx_normalized
        self.y += self.speed * self.dy_normalized
        if self.lifetime <= 0:
            entity_manager.unregister(self)
        self.lifetime -= 1
