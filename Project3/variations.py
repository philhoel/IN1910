import numpy as np
import matplotlib.pyplot as plt
import numba
import time
import argparse
import cProfile
from chaos_game import ChaosGame
from fern import AffineTransform
import sys
from matplotlib.animation import FuncAnimation

#############################
"""Written by Philip Hoel"""
############################

class Variations:

    """
    Transforms the plane, so the initial fractals gets another shape
    """

    def __init__(self, x=None, y=None, arr=None, colors='black', scale=False, turn='y'):
        try:
            if x is None and y is None:
                self.x = arr[:,0]
                self.y = arr[:,1]
            else:
                self.x = x
                self.y = y
        except TypeError:
            print("No values or wrong types given")
            print("Read documentation")
            raise TypeError

        if isinstance(colors, type('string')):
            self.colors = colors
        elif isinstance(colors, np.ndarray):
            self.colors = colors
        else:
            print("colors must be of type 'string' or an np.ndarray with 'float' values")
            raise TypeError

        if scale == True:

            if np.max(abs(self.x)) > np.max(abs(self.y)):
                self.x = self.x / np.max(abs(self.x))
                self.y = self.y / np.max(abs(self.x))
            else:
                self.x = self.x / np.max(abs(self.y))
                self.y = self.y / np.max(abs(self.y))

        self.r = np.sqrt(self.x**2 + self.y**2)
        self.theta = np.arctan2(self.y, self.x)
        self.phi = np.arctan2(self.x, self.y)


        if turn == 'y':
            self.y = -self.y

        elif turn == 'x':
            self.x = -self.x

        else:
            pass

    

    def linear(self):
        self.u = self.x
        self.v = self.y
        return self.u, self.v

    def sinusoidal(self):
        self.u, self.v = np.sin(self.x), np.sin(self.y)
        return self.u, self.v

    def spherical(self):
        self.u, self.v = 1/self.r**2 * self.x, 1/self.r**2 * self.y
        return self.u, self.v

    def swirl(self):
        self.u, self.v = self.x*np.sin(self.r**2) - self.y*np.cos(self.r**2), self.x*np.cos(self.r**2) + self.y*np.sin(self.r**2)
        return self.u, self.v

    def polar(self):
        self.u, self.v = self.theta/np.pi, self.r - 1
        return self.u, self.v

    def handkerchief(self):
        self.u, self.v = self.r*np.sin(self.theta + self.r), self.r*np.cos(self.theta - self.r)
        return self.u, self.v

    def heart(self):
        self.u, self.v = self.r * np.sin(self.theta*self.r), -self.r*np.cos(self.theta*self.r)
        return self.u, self.v

    def disc(self):
        self.u, self.v = self.theta/np.pi * np.sin(np.pi*self.r), self.theta/np.pi * np.cos(np.pi*self.r)
        return self.u, self.v

    def diamond(self):
        self.u, self.v = np.sin(self.theta)*np.cos(self.r), np.cos(self.theta)*np.sin(self.r)
        return self.u, self.v

    def exponential(self):
        self.u, self.u = np.exp(self.x - 1)*np.cos(np.pi*self.y), np.exp(self.x - 1)*np.sin(np.pi*self.y)
        return self.u, self.v

    def cross(self):
        squareroot = np.sqrt(1/(self.x**2 + self.y**2)**2)
        self.u, self.v = squareroot*self.x, squareroot*self.y
        return self.u, self.v

    
    def blend(self, weightDict):

        """
        Takes a dictionary with percentageweight: function

        Makes a linear combination of all the functions in the dictionary

        Parameters:

            weightDict - Dictionary with info. 
                         Strucure     weight : function
        """

        temp = 0
        temp2 = 0

        for key in weightDict:
            self.u, self.v = eval('self.'+weightDict[key])
            temp += self.u*key
            temp2 += self.v*key

        self.u, self.v = temp, temp2

        return self.u, self.v

    def gradual_transform(self, f, plot=True):

        """
        A gradual transform from linear to another plane

        Parameters:

            f - function to transform to

            plot - Wether to plot or not
        """

        plot_list = []
        trans, form = eval('self.'+f)()
        x, y = self.linear()

        for i in range(1, 5):
            u = (i/4)*x + (1-(i/4))*trans
            v = (i/4)*y + (1-(i/4))*form
            plot_list.append(u)
            plot_list.append(v)

        if plot == False:

            return plot_list

        plt.subplot(2, 2, 1)
        plt.scatter(plot_list[0], -plot_list[1], s=0.1, c=self.colors)
        plt.axis('equal')
        plt.axis('off')
        plt.subplot(2, 2, 2)
        plt.scatter(plot_list[2], -plot_list[3], s=0.1, c=self.colors)
        plt.axis('equal')
        plt.axis('off')
        plt.subplot(2, 2, 3)
        plt.scatter(plot_list[4], -plot_list[5], s=0.1, c=self.colors)
        plt.axis('equal')
        plt.axis('off')
        plt.subplot(2, 2, 4)
        plt.scatter(plot_list[6], -plot_list[7], s=0.1, c=self.colors)
        plt.axis('equal')
        plt.axis('off')
        plt.show()

    def plot(self, cmap):

        plt.scatter(self.u, -self.v, c=self.colors, cmap=cmap, s=0.1)
        plt.axis('equal')
        plt.axis('off')
        plt.show()


# ------------------------------ OUTSIDE CLASS --------------------------------- #

def nGon(f, steps=10000, r=1/3, nGon=4):

    """
    Creates an n-gon with colors
    Uses the class ChaosGame from chaos_game.py

    parameters:

        f - function to transform the plane

        steps - Number of points. Default to 10 000

        r - A number to required for calucation. Needs to be less than one

        nGon - Number of corners of the n-gon. Needs to be bigger than 3
    """
    new_obj = ChaosGame(r=1/3, nGon=4)
    X, C = new_obj.get_color_array(steps)

    var = Variations(arr=X, colors=C, turn='y')
    f(var)
    var.plot(cmap='jet')


def fern(f, steps=10000, plot=True):

    """
    Creates a plot of the Barnsley Fern.
    Uses the class AffineTransform from fern.py

    Parameters:

        f - function to transform the plane

        steps - Number of points. Defaults to 10 000

        plot - Whether to plot or not. If set to False, returns array
    """
    f1 = AffineTransform(0, 0, 0, 0.16, 0, 0)
    f2 = AffineTransform(0.85, 0.04, -0.04, 0.85, 0, 1.6)
    f3 = AffineTransform(0.20, -0.26, 0.23, 0.22, 0, 1.60)
    f4 = AffineTransform(-0.15, 0.28, 0.26, 0.24, 0, 0.44)

    def func(X, functions):
        probability = [0.01, 0.85, 0.07, 0.07]
        p_cumulative = np.cumsum(probability)
        r = np.random.random()
        for j, p in enumerate(p_cumulative):
            if r < p:
                return functions[j](X)


    X = np.zeros((steps, 2))
    functions = [f1, f2, f3, f4]
    for i in range(1, steps):
        X[i] = func(X[i-1], functions)

    new_obj = Variations(arr=X, colors='green', scale=True)

    if plot == False:
        
        return new_obj

    f(new_obj)
    new_obj.plot('jet')

def meshgrid_plot(blend_dict):

    N = 60
    grid_values = np.linspace(-1, 1, N)
    x = np.ones(N*N)
    y = np.ones(N*N)
    for i in range(N):
        index = i*N
        x[index:index+N] *= grid_values[i]
        y[index:index+N] *= grid_values

    test_obj = Variations(x, y, colors='black')

    #Creating different standard plots
    x_linear, y_linear = test_obj.linear()
    x_swirl, y_swirl = test_obj.swirl()
    x_handkerchief, y_handkerchief = test_obj.handkerchief()
    x_disc, y_disc = test_obj.disc()

    #Plotting meshgrid in subplot
    plt.subplot(2, 2, 1)
    plt.scatter(x_linear, y_linear, s=0.1)
    plt.axis('equal')
    plt.axis('off')
    plt.title('Linear')
    plt.subplot(2, 2, 2)
    plt.scatter(x_swirl, y_swirl, s=0.1)
    plt.axis('equal')
    plt.axis('off')
    plt.title('Swirl')
    plt.subplot(2, 2, 3)
    plt.scatter(x_handkerchief, y_handkerchief, s=0.1)
    plt.axis('equal')
    plt.axis('off')
    plt.title('Handkerchief')
    plt.subplot(2, 2, 4)
    plt.scatter(x_disc, y_disc, s=0.1)
    plt.axis('equal')
    plt.axis('off')
    plt.title('Disc')
    plt.show()

    # Plotting blend method
    test_obj.blend(new_dict)
    test_obj.plot('jet')

if __name__ == "__main__":

    
    #var_obj is chaos game
    #new_obj is fern
    

    # Dictionary for blend method
    new_dict = {0.3: 'swirl()', 0.3:'linear()', 0.2: 'disc()', 0.2: 'polar()'}

    # Plotting meshgrid
    meshgrid_plot(new_dict)
    
    # Creating and plotting chaos game
    test_obj = ChaosGame(r=1/3, nGon=4)
    X, C = test_obj.get_color_array(100000)
    var_obj = Variations(arr=X, colors=C)
    var_obj.gradual_transform('swirl')
    var_obj.gradual_transform('polar')
    var_obj.blend(new_dict)
    var_obj.plot('jet')

    #Testing fern
    new_obj = fern(Variations.linear, 10000, plot=False)
    new_obj.gradual_transform('swirl')
    

    # Testing functions outside of class
    nGon(Variations.linear, 10000)
    nGon(Variations.swirl, 10000)
    nGon(Variations.handkerchief, 10000)
    nGon(Variations.disc, 10000)

    fern(Variations.linear, 10000)
    fern(Variations.swirl, 10000)
    fern(Variations.handkerchief, 10000)
    fern(Variations.disc, 10000)