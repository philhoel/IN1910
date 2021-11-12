import numpy as np
from chaos_game import ChaosGame

def test_init_nGon():

    success = False

    try:
        testObj = ChaosGame(nGon=1)
    except TypeError:
        success = True
    assert success

def test_init_r():

    success = False

    try:
        testObj = ChaosGame(r='string')
    except TypeError:
        success = True
    assert success

def test_r_value():

    success = False

    try:
        testObj = ChaosGame(r=4)
    except ValueError:
        success = True
    assert success

def test_ngon_boundaries():

    testObj = ChaosGame()
    expected = 3
    computed = len(testObj.corners)
    success = (expected == computed)
    assert success



