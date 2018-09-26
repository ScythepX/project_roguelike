import struct


map_header_struct = struct.Struct('6c4L')  # b'rgmap1'; WIDTH, HEIGHT, SPAWN_X, SPAWN_Y: int
# TODO: Add TITLE: char(50) to header


def _line_struct(width: int) -> struct.Struct:
    """ Generates Struct for line of tiles """
    return struct.Struct(f'{width}iii')  # {witdth} ID: int; Rotation: int; State: int


class Tile:

    def __init__(self, id: int = 0, rotation: int = 0, state: int = 0, data: bytes = b''):
        self.id = id
        self.rotation = rotation
        self.state = state
        self.data = data

    def __repr__(self):
        return f'Tile[{self.id}]'


class Map:

    def __init__(self, tiles=None, title: str = '', spawn_x: int = 0, spawn_y: int = 0):
        self.tiles = tiles if tiles else []
        self.title = title
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y

    def load_from_file(self, filename: str):
        with open(filename, 'rb') as f:
            header = f.read(40)
            *head, width, height, self.spawn_x, self.spawn_y = map_header_struct.unpack(header)
            if not b''.join(head) == b'rgmap1':
                raise ValueError('File has invalid format')
            for _ in range(height):
                line = f.read(struct.calcsize(f'{width}i'))  # TODO: Use _line_struct
                ids = struct.unpack(f'{width}i', line)  # TODO: Use _line_struct, add other fields
                self.tiles += [*ids]

    def save_to_file(self, filename: str):
        with open(filename, 'wb') as f:
            width = len(self.tiles)
            height = len(self.tiles[0])
            header = map_header_struct.pack(b'r', b'g', b'm', b'a', b'p', b'1', width, height, self.spawn_x,
                                            self.spawn_y)
            f.write(header)

            for row in self.tiles:
                line = map(lambda x: x.id, row)
                f.write(struct.pack(f'{len(row)}i', *line))  # TODO: Use _line_struct, add other fields


line1 = [Tile(i) for i in range(5)]
line2 = [Tile(i) for i in range(10, 15)]
m = Map()
m.tiles = [line1, line2]
print('Before:')
print(m.tiles)
m.save_to_file('test')
m = Map()
m.load_from_file('test')
print('After:')
print(m.tiles)
__import__('os').remove('test')
