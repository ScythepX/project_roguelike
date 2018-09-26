class Tile:

    def __init__(self, id: int = 0, rotation: int = 0, state: int = 0, data: bytes = b''):
        self.id = id
        self.rotation = rotation
        self.state = state
        self.data = data