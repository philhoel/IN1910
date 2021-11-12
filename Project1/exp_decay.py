from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt


class ExponentialDecay:
    """
    A class for setting up and solve ODEs of the form 'du/dt = -a * u'.

    Attributes
    ----------
    a : (int, float)
        A constant that is used in the ODE.
    """
    def __init__(self, a):
        self.a = a

    def __call__(self, t, u):
        """Computes the RHS of 'du/dt = -a * u'."""
        return -self.a * u

    def solve(self, u0, T, dt):
        """
        Solves the ODE in the call method using the initial value
        'u0 = u(0)' on the time interval (0, T] with step size dt.
        Uses the solve_ivp function from the scipy.integrate module,
        which is a part of the SciPy library.

        Parameters
        ----------
        u0 : (int, float)
            The initial value.
        T : (int, float)
            The end point of the interval.
        dt : (int, float)
            The step size.

        Returns
        -------
        A tuple (t_, u_), where t_ is an array containing the time points,
        and u_ is an array containing the associated solution points.
        """
        n = np.ceil(T/dt)
        t = np.linspace(0, T, n)
        sol = solve_ivp(self, (0, T), (u0,), t_eval=t)
        return sol.t, sol.y[0]

if __name__ == "__main__":
    # Example code
    decay_model = ExponentialDecay(1)
    t, u = decay_model.solve(1, 10, 0.01)

    plt.plot(t, u)
    plt.show()
