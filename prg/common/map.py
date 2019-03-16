import struct
from copy import copy
from typing import List, Tuple

rgmap_header = b'rgmap1'
map_header_struct = struct.Struct('4i50s')  # b'rgmap1'; WIDTH, HEIGHT, SPAWN_X, SPAWN_Y: int


def _line_struct(height: int) -> struct.Struct:
    """ Generates Struct for line of tiles """
    return struct.Struct(f'{height*3}i')  # {height} ID: int; Rotation: int; State: int


def _split_fields(fields: Tuple[int]) -> List[List[int]]:
    arrs = []
    fields = copy(fields)
    size = 3
    while len(fields) > size:
        pice = fields[:size]
        arrs.append(pice)
        fields = fields[size:]
    arrs.append(fields)
    return arrs


class Tile:

    def __init__(self, id: int = 0, rotation: int = 0, state: int = 0, data: bytes = b''):
        self.id = id
        self._load_resources()
        self.rotation = rotation
        self.state = state
        self.data = data

    def _load_resources(self):
        # self.rm = ResourceManager('tiles', self.id)
        pass

    def __repr__(self):
        return f'Tile[{self.id}]'


class Map:

    def __init__(self, tiles: List[List[Tile]] = None, title: str = '', spawn_x: int = 0, spawn_y: int = 0):
        self.tiles = tiles if tiles else []
        self.title = title
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def load_from_file(self, filename: str):
        with open(filename, 'rb') as f:
            header = f.read(len(rgmap_header) + map_header_struct.size)
            if not header[:len(rgmap_header)] == rgmap_header:
                raise ValueError('File has invalid format')
            buffer = map_header_struct.unpack(header[len(rgmap_header):])
            width, height, self.spawn_x, self.spawn_y, title = buffer
            self.title = title.decode().strip('\x00')
            for _ in range(width):
                line = f.read(_line_struct(height).size)
                fields = _split_fields(_line_struct(height).unpack(line))

                self.tiles.append([i for i in map(lambda x: Tile(*x), fields)])

    def save_to_file(self, filename: str):
        with open(filename, 'wb') as f:
            width = len(self.tiles)
            height = len(self.tiles[0])
            f.write(rgmap_header)
            header = map_header_struct.pack(width, height, self.spawn_x,
                                            self.spawn_y, bytes(self.title, encoding='utf8'))
            f.write(header)

            for row in self.tiles:
                line = []
                for i in row:
                    line += [i.id, i.rotation, i.state]
                f.write(_line_struct(len(row)).pack(*line))
