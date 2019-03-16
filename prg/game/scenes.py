import json

from .objects import GameObject
from ..game import components


class SceneManager:
    def __init__(self):
        self._scene = Scene()

    def load_scene(self, name):
        with open(f'res/scenes/{name}.rgscene', 'r') as f:
            j = json.loads(f.read())
        scene = Scene(j['name'])
        for obj in j['objects']:
            go = GameObject(obj['name'])
            for component in obj['components']:
                if hasattr(components, component):
                    cmp = getattr(components, component, None)
                    args = obj['components'][component]
                    go.add_component(cmp(**args))
            scene.objects.append(go)
        self._scene = scene

    def do_update(self):
        for obj in self._scene.objects:
            obj.do_update()

    def on_key_pressed(self, key):
        for obj in self._scene.objects:
            obj.on_key_pressed(key)

    def on_key_released(self, key):
        for obj in self._scene.objects:
            obj.on_key_released(key)

    def on_mouse_down(self, pos):
        pass

    def on_mouse_up(self, pos):
        pass

    def on_mouse_move(self, pos):
        pass

    def draw(self, screen):
        objects = sorted(self._scene.objects, key=lambda x: x.get_z())
        for obj in objects:
            obj.draw(screen)


class Scene:
    def __init__(self, name='Scene'):
        self.name = name
        self.objects = []

    def __repr__(self):
        return f'Scene[{self.name}]'
