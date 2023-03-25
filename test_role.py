import unittest
from roles import Roles

# Manually create mock functions
def mock_function(*args, **kwargs):
    pass

# Replace the actual imported functions in the Roles class with the mock functions
Roles.map['primary']['test'] = mock_function
Roles.map['secondary']['test'] = mock_function
Roles.map['secondary']['fireflies'] = mock_function
Roles.map['secondary']['colourwave'] = mock_function
Roles.map['secondary']['trail'] = mock_function
Roles.map['secondary']['rainbow'] = mock_function

class TestRoles(unittest.TestCase):

    def test_get_webmap(self):
        expected_webmap = [
            {"label": "Test Secondary",
             "id": "secondary",
             "value": "test"}
        ]
        self.assertEqual(Roles.get_webmap(), expected_webmap)

    def test_default_primary(self):
        self.assertEqual(Roles.default_primary().__name__, "dummy_role")

    def test_default_secondary(self):
        self.assertEqual(Roles.default_secondary().__name__, "dummy_role")

    def test_primary_map(self):
        expected_map = {
            'test': mock_function,
            'none': mock_function
        }
        self.assertEqual(set(Roles.primary_map().keys()), set(expected_map.keys()))

    def test_secondary_map(self):
        expected_map = {
            'test': mock_function,
            'fireflies': mock_function,
            'colourwave': mock_function,
            'trail': mock_function,
            'rainbow': mock_function,
            'none': mock_function
        }
        self.assertEqual(set(Roles.secondary_map().keys()), set(expected_map.keys()))

# Run the tests
if __name__ == '__main__':
    unittest.main()
