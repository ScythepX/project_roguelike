from abc import ABCMeta
from typing import List

import pygame as pg

from ..common.resources import ResourceManager


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
    def __init__(self, resource: dict):
        super().__init__()
        self.rmanager = ResourceManager(resource['pack'], resource['id'])
        tex_path = self.rmanager.get_resource(resource['filename'])
        self._texture = pg.image.load(tex_path.name)

    def draw(self, screen):
        if not self.is_enabled:
            return
        coords = self.object.get_component(Transform).coords
        sprite = self._texture
        screen.blit(sprite, coords)


class Script(Component):
    def __init__(self, resource: dict):
        super().__init__()
        self.rmanager = ResourceManager(resource['pack'], resource['id'])
        script_path = self.rmanager.get_resource(resource['filename'])
        # self._script =

    def on_key_down(self, key):
        print(key)
        pass

    def on_key_up(self, key):
        print(key)
        pass


class SoundSource(Component):
    def __init__(self, resource: List):
        pass
