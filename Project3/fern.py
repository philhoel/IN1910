import numpy as np
import matplotlib.pyplot as plt
from numba import jit
import time
import argparse
import cProfile

#############################
"""
Written by Philip Hoel
A program for plotting
Iterated Function Systems
"""
############################

class AffineTransform:

    def __init__(self, a=0, b=0, c=0, d=0, e=0, f=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
        self.f = f

        self.matrix = np.array([[self.a, self.b], [self.c, self.d]])
        

        self.vector = np.array([self.e, self.f])

    

    def __call__(self, vec=None, x=0, y=0):

        """
        Magic method: __call__

        Parameters:

            vec - x and y values as array or tuple

            x - x value

            y - y value

        
        Takes in the values of the variables in the function
        Calculates the Affine Transform
        """

        
        if isinstance(vec, np.ndarray):
            new_vec = self.matrix.dot(vec) + self.vector

        elif isinstance(vec, tuple):
            temp_vec = np.array([vec[0], vec[1]])
            new_vec = self.matrix.dot(temp_vec) + self.vector

        elif vec is None:
            temp_vec = np.array([x, y])
            new_vec = self.matrix.dot(temp_vec) + self.vector

        else:
            print("Vec must be an ndarray or tuple, or x and y must have float/int values")
            print(type(vec))
            raise TypeError
        
        
        return new_vec



def func(X, functions):

    """
    Chooses a function through cumulative probability
    Takes in an array and a list of functions
    """

    probability = [0.01, 0.85, 0.07, 0.07]
    p_cumulative = np.cumsum(probability)
    r = np.random.random()
    for j, p in enumerate(p_cumulative):
        if r < p:
            return functions[j](X)


def main(iter, runtime=False):

    """

    Main function

    Parameters:

        iter - Number of iterations

        runtime - Whether or not to print runtime


    Creates the functions proposed by Barnsley Fern
    Loops through an array of points
    Plots the array with scatter plot
    Calculates runtime of loops and plots

    """

    f1 = AffineTransform(0, 0, 0, 0.16, 0, 0)
    f2 = AffineTransform(0.85, 0.04, -0.04, 0.85, 0, 1.6)
    f3 = AffineTransform(0.20, -0.26, 0.23, 0.22, 0, 1.60)
    f4 = AffineTransform(-0.15, 0.28, 0.26, 0.24, 0, 0.44)

    functions = [f1, f2, f3, f4]

    X = np.zeros((iter, 2))

    x1 = time.time()
    for i in range(1, iter):
        X[i] = func(X[i-1], functions)
    x2 = time.time()
    
    
    x = time.time()
    plt.scatter(*zip(*X), s=0.1, marker='.', c='green')
    y = time.time()
    plt.title('Barnsley Fern - IFS')
    plt.axis('equal')
    plt.axis('off')
    plt.savefig('barnsley_fern.png')

    
    if args.Runtime == True:
        print(f"Runtime for {iter} iterations (Calculation): {x2-x1}")
        print(f"Runtime for {iter} iterations (Plotting): {y-x}")
        print(f"Runtime for {iter} iterations (Total): {(x2-x1) + (y-x)}")
    
    
    plt.show()


if __name__ == '__main__':

    
    parser = argparse.ArgumentParser(
        description="Barnsley Fern script"
    )

    parser.add_argument('Iterations', help='How many points to plot', type=int)
    parser.add_argument('--Runtime', help='Wheather to print runtime or not', type=bool)
    parser.add_argument('--cProfile', help='Wheather to run cProfile or not', type=bool)
    args = parser.parse_args()

    if args.cProfile == True:

        cProfile.run('main(args.Iterations)')

    else:

        main(args.Iterations, args.Runtime)
    


