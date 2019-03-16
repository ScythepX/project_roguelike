from typing import Union, List, Type

from .components import Sprite, Component, Script


class GameObject:
    def __init__(self, name='GameObject', components: Union[None, List[Component]] = None):
        self._components = components if components else []
        self.name = name

    def __repr__(self):
        return f'GameObject[{self.name}]'

    def get_component(self, cmp: Type[Component]):
        for component in self._components:
            if isinstance(component, cmp):
                return component

    def add_component(self, cmp: Component):
        if not self.get_component(cmp.__class__):
            cmp.object = self
            self._components += [cmp]
        else:
            ValueError("Component of such type already exists in this object")

    def do_update(self):
        pass

    def get_z(self) -> int:
        return 0

    def draw(self, screen):
        sprite = self.get_component(Sprite)
        if sprite:
            sprite.draw(screen)

    def on_key_pressed(self, key):
        script = self.get_component(Script)
        if script:
            script.on_key_down(key)

    def on_key_released(self, key):
        script = self.get_component(Script)
        if script:
            script.on_key_up(key)
