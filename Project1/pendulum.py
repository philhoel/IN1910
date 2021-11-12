import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Pendulum:
    """Class for creating a model of a pendulum"""

    def __init__(self, L=1, M=1, g=9.81):
        """
        Initilazing class
        On default L=1, M=1, g=9.81
        Rest of variables are created as None, to be used later.
        """
        self.L = L
        self.M = M
        self.g = g
        self._t = None
        self._theta = None
        self._omega = None
        self._x = None
        self._z = None
        self._Potensial = None
        self._vx = None
        self._vy = None
        self._Kinetic = None

    def __call__(self, t, y):
        
        """
        Computes the RHS of the ODEs '(d theta)/dt = omega'
        and '(d omega)/dt = -(g/L)*sin(theta)', and returns
        them as a tuple in the order given.
        """
        return (y[1], -(self.g/self.L)*np.sin(y[0]))

    def solve(self, y0, T, dt, angle="rad"):
        
        """
        Solves the coupled ODEs in the call method
        using the initial values 'y0[0] = theta(0)' and
        'y0[1] = omega(0)' on the time interval (0, T] with step size dt.
        Parameters
        ----------
        y0 : tuple
            The initial values, y0[0]=theta(0) and y0[1]=omega(0).
        T : (int, float)
            The end point of the interval.
        dt : (int, float)
            The step size.
        angles : string
            Keyword argument is set to 'rad', assuming input is in radians.
            If set to 'deg', it converts the input from degrees to radians.

        Initializes t, theta, omega, x, z, Potensial, vx, vz and Kinetic
        x and z is cartesian coordinates of the original polar coordinates
        z is chosen instead of y, to not be confused with y from solve_ivp
        """
        if angle == "deg":
            #Fiks degrees funksjon
            #y0
            #TypeError: can't multiply sequence by non-int of type 'float'
            #y0[0]
            #TypeError: 'tuple' object does not support item assignment
            y0 = y0 * (180/np.pi)

        self.dt = dt
        n = int(T/dt)
        print(type(n))
        t = np.linspace(0, T, n)
        sol = solve_ivp(self, (0, T), y0, t_eval=t)
        self._t = sol.t
        self._theta = sol.y[0]
        self._omega = sol.y[1]
        self._x = self.L*np.sin(sol.y[0])
        self._z = -self.L*np.cos(sol.y[0])
        self._Potensial = self.M*self.g*(self._z + self.L)
        self._vx = np.gradient(self.L*np.cos(sol.y[0]), sol.t)
        self._vz = np.gradient(self.L*np.sin(sol.y[0]), sol.t)
        self._Kinetic = 0.5*self.M*(self._vx**2 + self.z**2)

    #Finn en løsning på å ikke ha så mange properties
    @property
    def t(self):
        if self._t is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._t

    @property
    def theta(self):
        if self._theta is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._theta
    
    @property
    def omega(self):
        if self._omega is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._omega

    @property
    def x(self):
        if self._x is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._x

    @property
    def z(self):
        if self._z is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._z

    @property
    def Potensial(self):
        if self._Potensial is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._Potensial
    
    @property
    def vx(self):
        if self._vx is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vx
    
    @property
    def vy(self):
        if self._vy is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vy

    @property
    def Kinetic(self):
        if self._Kinetic is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._Kinetic

    def createAnimation(self):

        fig = plt.figure()

        #plt.axis('equal')
        plt.axis('off')
        plt.axis((-8, 8, -8, 8))

        self.pendulums, = plt.plot([], [], 'o-')
        self.animation = FuncAnimation(fig, self._next_frame,
                                        frames=range(len(self.x)),
                                        repeat=None,
                                        interval=1000*self.dt,
                                        blit=True)

    def _next_frame(self, i):
        self.pendulums.set_data((0, self.x[i]),
                                (0, self.z[i]))
                                
                    
        return self.pendulums, 

    def show_animation(self):
        plt.show()


    def save_animation(self, filename):
        self.animation.save(filename, fps=60)

class DampenedPendulum(Pendulum):
    """
    Class for modelling a Dampened pendulum.
    Inherits from Pendulum class.
    """

    def __init__(self, B, L=1, M=1, g=9.81):
        Pendulum.__init__(self, L, M, g)
        self.B = B

    def __call__(self, t, y):
        return (y[1], -(self.g/self.L)*np.sin(y[0]) - (self.B/self.M)*y[1])

    


def main():

    firstObject = Pendulum(2.7)
    firstObject.solve((np.pi/2, 2), 10, 0.001)

    secondObject = DampenedPendulum(0.3, L=2.7)
    secondObject.solve((np.pi/2, 2), 10, 0.001)


    plt.plot(firstObject.t, firstObject.theta)
    plt.title("Pendulum motion: Theta(t)")
    plt.show()

    """
    plt.plot(firstObject.x, firstObject.z)
    plt.title("Pendulum motion: X and Y coordinates")
    plt.show()
    plt.plot(firstObject.t, firstObject._Potensial)
    plt.title("Potensial energy")
    plt.show()
    plt.plot(firstObject.t, firstObject.Kinetic)
    plt.title("Kinetic energy")
    plt.show()
    plt.plot(firstObject.t, firstObject._Potensial + firstObject.Kinetic)
    plt.title("Total energy")
    plt.show()

    plt.plot(secondObject.t, secondObject.theta)
    plt.title("Pendulum motion: Theta(t)")
    plt.show()
    plt.plot(secondObject.x, secondObject.z)
    plt.title("Pendulum motion: X and Y coordinates")
    plt.show()
    plt.plot(secondObject.t, secondObject._Potensial)
    plt.title("Potensial energy")
    plt.show()
    plt.plot(secondObject.t, secondObject.Kinetic)
    plt.title("Kinetic energy")
    plt.show()
    plt.plot(secondObject.t, secondObject._Potensial + secondObject.Kinetic)
    plt.title("Total energy")
    plt.show()

    #firstObject.createAnimation()
    #firstObject.show_animation()

    #secondObject.createAnimation()
    #secondObject.show_animation()

    """

if __name__ == "__main__":

    main()
