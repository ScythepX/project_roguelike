import zipfile
import json
from os.path import isdir, isfile, exists
from tempfile import NamedTemporaryFile
BASE_DIR = 'res'


class ResourceError(RuntimeError):
    """Exception for resource parsing errors"""
    pass


class ResourceNotFoundError(ResourceError, FileNotFoundError):
    pass


class ResourceManager:
    """
    Resource manager class if for loading game resources, such as Tiles and Items
    Usage: rm = ResourceManager('tiles', 123)
           fs_sound = rm.get_resource('footstep')
    """
    def __init__(self, pack: str, id: int, create=False):
        self.pack_path = f'{BASE_DIR}/{pack}'
        if not (exists(self.pack_path) and isdir(self.pack_path)):
            raise ResourceNotFoundError(f'"{self.pack_path}" was not found')
        self.id_path = f'{self.pack_path}/{id}'
        if isfile(self.id_path):
            self.zip = zipfile.PyZipFile(self.id_path)
        elif isdir(self.id_path):
            self.zip = None
        else:
            raise ResourceNotFoundError(f'"{self.id_path}" was not found')
        self.item_id = id
        self._parse_info()

    def _parse_info(self):
        try:
            with open(self.id_path + '/' + 'main', 'r') as f:
                d = json.loads(f.read())
        except json.JSONDecodeError:
            raise ResourceError('Basic resource information can not be decoded')
        self.name = d.get('name', 'Unnamed Resource Item')
        self.description = d.get('description', 'No Description provided for this item')
        self.available_resources = d.get('res_list', [])

    def get_resource(self, name='main') -> NamedTemporaryFile:
        if self.zip is not None:
            try:
                with self.zip.open(name) as f:
                    tmpfile = NamedTemporaryFile()
                    tmpfile.write(f.read())
                    tmpfile.seek(0)
                    return tmpfile
            except KeyError:
                raise ResourceNotFoundError(f'No item named {name} in this res pack')
        else:
            try:
                with open(self.id_path + '/' + name, 'rb') as f:
                    tmpfile = NamedTemporaryFile()
                    tmpfile.write(f.read())
                    tmpfile.seek(0)
                    return tmpfile
            except FileNotFoundError:
                raise ResourceNotFoundError(f'No item named {name} in this res pack')
