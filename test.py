from main import *
import unittest
from unittest.mock import Mock


class Test(unittest.TestCase):

    def test_calculate_velocities(self):
        mock = Mock()
        configure()
        mock.side_effect = calculate_velocities(start_date="2020-09-10", end_date="2020-09-17")
        self.assertEqual(mock(), 2.0527590165)
        self.assertEqual(mock(), 43.4342292687)
        self.assertEqual(mock(), 11.803780829033162)
        self.assertEqual(mock(), 9.9115941689)


if __name__ == '__main__':
    unittest.main()