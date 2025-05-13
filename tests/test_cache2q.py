import unittest

from cache2q import Cache2Q


class Test2Q(unittest.TestCase):
    def test_sanity(self):
        # recent 2
        # recent_evict 4
        # frequent 2
        cache = Cache2Q[int, int](8)

        cache.set(1, 1)
        cache.set(2, 2)
        cache.set(3, 3)
        # [3, 2] [1] []

        self.assertEqual(1, cache.get(1))
        # 1 become frequent
        # [3, 2] [] [1]

        cache.set(4, 4)
        cache.set(5, 5)
        cache.set(6, 6)
        cache.set(7, 7)
        cache.set(8, 8)
        # [8, 7] [6, 5, 4, 3] [1]
        self.assertIsNone(cache.get(2))

        self.assertEqual(7, cache.get(7))
        # touching recent don't move it
        # [8, 7] [6, 5, 4, 3] [1]

        cache.set(9, 9)
        # [9, 8] [7, 6, 5, 4] [1]
        self.assertIsNone(cache.get(3))

        self.assertEqual(5, cache.get(5))
        self.assertEqual(6, cache.get(6))
        # 5, 6 become frequent
        # [9, 8] [7, 4] [5, 6]

        self.assertIsNone(cache.get(1))
