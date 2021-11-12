import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from time import time

class DoublePendulum:

    def __init__(self, M1=1, L1=1, M2=1, L2=1, g=9.81):
        self.M1 = M1
        self.L1 = L1
        self.M2 = M2
        self.L2 = L2
        self.g = g
        self._t = None
        self._theta1 = None
        self._theta2 = None
        self._omega1 = None
        self._omega2 = None
        self._x1 = None
        self._z1 = None
        self._x2 = None
        self._z2 = None
        self._Potensial = None
        self._vx1 = None
        self._Vz1 = None
        self._vx2 = None
        self._vz2 = None
        self._Kinetic = None


    def __call__(self, t, y):
        """Returns a tuple on the form (omega1, theta1, omega2, theta2)"""
        M1 = self.M1
        L1 = self.L1
        M2 = self.M2
        L2 = self.L2
        g = self.g
        dw1 = (M2 * L1 * (y[1]**2)*np.sin(y[2] - y[0]) * np.cos(y[2] - y[0])
        + M2 * g * np.sin(y[2]) * np.cos(y[2]-y[0])
        + M2 * L2 * (y[3]**2)*np.sin(y[2]- y[0])
        -(M1 + M2) * g * np.sin(y[0]))
        #Next equation
        dt1 = (M1 + M2) * L1 - M2 * L1 * (np.cos(y[2] - y[0]))**2
        #Next equation
        dw2 = (-M2 * L2 * (y[3]**2) * np.sin(y[2]-y[0]) * np.cos(y[2]-y[0])
        + (M1 + M2) * g * np.sin(y[0]) * np.cos(y[2]-y[0])
        - (M1 + M2) * L1 * (y[1]**2) * np.sin(y[2]-y[0])
        - (M1 + M2)*g*np.sin(y[2]))
        #Next equation
        dt2 = (M1 + M2) * L2 - M2 * L2 * (np.cos(y[2] - y[0]))**2
        return (y[1], dw1/dt1, y[3], dw2/dt2)

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
        Initializes t, theta1, omega1, theta2, omega2, 
        x1, x2, z1, z2, Potensial, vx1, vz1, vx2, vz2 and Kinetic
        x and z is cartesian coordinates of the original coordinates
        z is chosen instead of y, to not be confused with y from solve_ivp
        """
        if angle == "deg":
            y0 = np.radians(y0)
        self.dt = dt

        n = int(T/dt)
        t = np.linspace(0, T, n)
        sol = solve_ivp(self, (0, T), y0, t_eval=t)
        self._t = sol.t
        self._theta1 = sol.y[0]
        self._theta2 = sol.y[2]
        self._omega1 = sol.y[1]
        self._omega2 = sol.y[3]
        self._x1 = self.L1*np.sin(self._theta1)
        self._z1 = -self.L1*np.cos(self._theta1)
        self._x2 = self._x1 + self.L2*np.sin(self._theta2)
        self._z2 = self.z1 - self.L2*np.cos(self._theta2)
        P1 = self.M1*self.g*(self._z1 + self.L1)
        P2 = self.M2*self.g*(self._z2 + self.L1 + self.L2)
        self._Potensial = P1 + P2
        self._vx1 = np.gradient(self._x1, self._t)
        self._vz1 = np.gradient(self._z1, self._t)
        self._vx2 = np.gradient(self._x2, self._t)
        self._vz2 = np.gradient(self._z2, self._t)
        K1 = 0.5*self.M1*(self._vx1**2 + self._vz1**2)
        K2 = 0.5*self.M2*(self._vx2**2 + self._vz2**2)
        self._Kinetic = K1 + K2
        

    
    @property
    def t(self):
        if self._t is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._t
    
    @property
    def theta1(self):
        if self._theta1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._theta1

    @property
    def omega1(self):
        if self._omega1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._omega1

    @property
    def theta2(self):
        if self._theta2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._theta2

    @property
    def omega2(self):
        if self._omega2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._omega2

    @property
    def x1(self):
        if self._x1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._x1
    
    @property
    def z1(self):
        if self._z1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._z1

    @property
    def x2(self):
        if self._x2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._x2
    
    @property
    def z2(self):
        if self._z2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._z2
    
    @property
    def Potensial(self):
        if self._Potensial is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._Potensial

    @property
    def vx1(self):
        if self._vx1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vx1
    
    @property
    def vz1(self):
        if self._vz1 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vz1
    
    @property
    def vx2(self):
        if self._vx2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vx2

    @property
    def vz2(self):
        if self._vz2 is None:
            print("Solve method was not called")
            raise AttributeError
        else:
            return self._vz2

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
                                        frames=range(len(self.x1)),
                                        repeat=None,
                                        interval=4,
                                        blit=True)

    def _next_frame(self, i):
        self.pendulums.set_data((0, self.x1[i], self.x2[i]),
                                (0, self.z1[i], self.z2[i]))
                    
        return self.pendulums, 

    def show_animation(self):
        plt.show()


    def save_animation(self, filename):
        self.animation.save(filename, fps=1000*self.dt)



def main():
    firstObject = DoublePendulum(L1=2.7, L2=2.7)
    firstObject.solve((0, 2, np.pi, 10), 10, 0.001)


    #plt.plot(firstObject.t, firstObject.theta1)
    plt.plot(firstObject.theta2, firstObject.omega2)
    plt.show()

    
    plt.plot(firstObject.t, firstObject.Potensial)
    plt.plot(firstObject.t, firstObject.Kinetic)
    plt.plot(firstObject.t, firstObject.Kinetic + firstObject.Potensial)
    plt.show()

    firstObject.createAnimation()
    firstObject.show_animation()

    

if __name__ == "__main__":

    main()