import unittest
from ..map import *
from os import remove
from os.path import exists


class WorkWithFiles(unittest.TestCase):
    def setUp(self):
        with open('invalid', 'wb') as f:
            f.write(b'i am not rgmap file')

    def tearDown(self):
        if exists('test'):
            remove('test')
        remove('invalid')

    def test_save_load(self):
        line1 = [Tile(i) for i in range(5)]
        line2 = [Tile(i) for i in range(10, 15)]
        old_ids = [i for i in map(lambda x: x.id, line1 + line2)]
        m = Map()
        m.tiles = [line1, line2]

        m.save_to_file('test')
        self.assertEqual(True, exists('test'))

        m = Map()
        m.load_from_file('test')
        new_tiles = [*m.tiles[0], *m.tiles[1]]
        new_ids = [i for i in map(lambda x: x.id, new_tiles)]
        self.assertEqual(old_ids, new_ids)

    def test_load_invalid_format(self):
        m = Map()
        with self.assertRaises(ValueError):
            m.load_from_file('invalid')


if __name__ == '__main__':
    unittest.main()
