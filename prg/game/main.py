import sys
from collections import defaultdict

import pygame

from .scenes import SceneManager


class Game:
    def __init__(self, caption='', width=800, height=600, fps=60):
        self.frame_rate = fps
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = defaultdict(list)
        self.keyup_handlers = defaultdict(list)
        self.mouse_handlers = []
        self.manager = SceneManager()
        self.manager.load_scene('main')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self.manager.on_key_pressed(event.key)
            elif event.type == pygame.KEYUP:
                self.manager.on_key_released(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.manager.on_mouse_down(event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                self.manager.on_mouse_up(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.manager.on_mouse_move(event.pos)

    def run(self):
        while True:
            self.handle_events()
            self.manager.do_update()
            self.manager.draw(self.surface)
            pygame.display.update()
            self.clock.tick(self.frame_rate)
