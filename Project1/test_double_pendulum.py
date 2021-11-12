from double_pendulum import DoublePendulum
import numpy as np

def test_double_pendulum():
    example = DoublePendulum(L1=2.7, L2=2.7)
    expected = 0.0244977116
    computed = example(0, (np.pi/2, 0.1, np.pi/4, 0.2))[1]
    tol = 1e-10
    success = abs(expected - computed) < tol
    assert success

def test_pendulum_solve():
    """
    Tests weather the length of the pendulum stays the same.
    Creates an object, iterates through the array and tests R == L
    with a tolerance and adds a True value to a test array. 
    If all values in test array are True, no assertion error.
    Tests weather omega and theta arrays are filled with zeros
    if y0 = (0,0)
    Tests if time array still stays the same if y0 = (0,0)
    """
    Object = DoublePendulum(2)
    Object2 = DoublePendulum(2)
    Object.solve((np.pi, 1, np.pi/2, 2), 3, 0.001)
    Object2.solve((0,0,0,0), 3, 0.001)
    tol = 1e-14
    testArray = []
    testArray2 = []
    success2 = 0
    success3 = 0
    r = np.sqrt(Object.x1**2 + Object.z1**2)
    for i in r:
        if abs(i - Object.L1) < tol:
            testArray.append(True)
    success = all(testArray)

    for i in range(len(Object2.t)):
        success2 += Object2.theta1[i]
        success3 += Object2.omega1[i]
        if Object2.t[i] == Object.t[i]:
            testArray2.append(True)
    success4 = all(testArray2)
        
    assert success, "R^2 is not equal to L^2"
    assert success2 == 0, "theta does not stay zero"
    assert success3 == 0, "omega does not stay zero"
    assert success4, "time array is not the same"

def test_double_pendulum_properties():
    """
    Test weather AttributeError is raised when solve method is not called
    """

    success = False
    Object = DoublePendulum(2)
    
    try:
        Object.t
    except AttributeError:
        success = True
    assert success

    try:
        Object.theta1
    except AttributeError:
        success = True
    assert success

    try:
        Object.omega1
    except AttributeError:
        success = True
    assert success

    