from abc import ABCMeta
from typing import List
from ..common.resources import ResourceManager
import pygame as pg


class Component(metaclass=ABCMeta):
    def __init__(self):
        self.enabled = True
        self.object = None

    def __repr__(self):
        return f'{self.__class__.__name__} component of {self.object}'

    @property
    def is_enabled(self):
        return self.enabled and self.object is not None


class Transform(Component):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.x = x
        self.y = y

    @property
    def coords(self):
        return self.x, self.y


class Sprite(Component):
    def __init__(self, resource: List):
        super().__init__()
        self.rmanager = ResourceManager(resource[0], resource[1])
        tex_path = self.rmanager.get_resource(resource[2])
        self._texture = pg.image.load(tex_path.name)

    def draw(self, screen):
        if not self.is_enabled:
            return
        coords = self.object.get_component(Transform).coords
        sprite = self._texture
        screen.blit(sprite, coords)