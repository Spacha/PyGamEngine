"""
You can auto-discover and run all tests with this command:

    py.test

Documentation: https://docs.pytest.org/en/latest/
"""

from Tanks import Tanks

def test_loop():
    game = Tanks()
    assert game.loop() is None