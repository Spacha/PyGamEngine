"""
Run tests from the root:
    cd PyGamEngine
    pytest

You can auto-discover and run all tests with this command:

    py.test

Documentation: https://docs.pytest.org/en/latest/
"""

from Tanks import Tanks
from GameEngine.Core import Game

def test_init():
    game = Game((100,100), 60.0)
    game.init()
    assert True