import numpy as np
import matplotlib.pyplot as plt
import numba
import time
import argparse
import cProfile
import sys

#################################################
""" 
Written by Philip Hoel
A program for plotting Sierpinski Triangles
"""
#################################################


# ------------------------------------------ CLASS Triangle ----------------------------------------------- #

class Triangle:
    
    def __init__(self, gonSize, corners):
        self.gonSize = gonSize
        self.corners = corners

    def random_points(self):
        """
        Chooses random weights, which sums up to 1
        Creates a linear combo of the three vectors created
        Returns the linear combo
        """
        j = 0
        y = np.random.dirichlet(np.ones(self.gonSize), size=1)
        X = np.zeros(self.corners.shape)
        LinearCombo = np.zeros((1,2))

        for i in y[0]:
            X[j] = i*self.corners[j]
            LinearCombo += X[j]
            j += 1

        return LinearCombo

    def iteration(self, iter, plot=True, runtime=False):
        """

        Method: iteration

        Parameters:

            iter - Number of points/iterations

            plot - To plot arrays or return arrays

            runtime - print out runtime of iterations and plotting

        Method calls random_points() method to get a start value
        Loops through array and uses the formula Xi+1 = (Xi + Cj) / 2
        Here Cj is a random choosen corner
        Method skips the first 5 values and then starts to add values to an array
        If plot=True, then the method plots the array with the plt.scatter()

        """
        X = self.random_points()

        for i in range(5):
            X = (X + self.corners[np.random.randint(0, self.gonSize)])/2
        
        X_array = np.zeros((iter, 2))

        x = time.time()
        for i in range(iter):
            X = (X + self.corners[np.random.randint(0, self.gonSize)])/2
            X_array[i] = X
        y = time.time()
        
        if plot == True:

            x1 = time.time()
            plt.scatter(*zip(*X_array), c='black', s=0.1, marker='.')
            x2 = time.time()
            plt.title('Colorless - Sierpinski Triangle')
            plt.axis('equal')
            plt.axis('off')
            plt.show()

            if runtime == True:
                print(f"Runtime for {iter} iterations (Calculations): ",y-x)
                print(f"Runtime for {iter} iterations (Plotting): ",x2-x1)
                print(f"Runtime for {iter} iterations (Total): ",(y-x) + (x2-x1))

        else:

            if runtime == True:
                print(f"Runtime for {iter} iterations (Calculations): ",y-x)
                print(f"Runtime for {iter} iterations (Plotting): ",x2-x1)
                print(f"Runtime for {iter} iterations (Total): ",(y-x) + (x2-x1))

            return X_array
    
    def color_iteration(self, iter, plot=True, runtime=False):

        """

        Method: color_iteration

        Parameters:

            iter - Number of points/iterations

            plot - To plot arrays or return arrays

            runtime - print out runtime of iterations and plotting

        Method calls random_points() method to get a start value
        Loops through array and uses the formula Xi+1 = (Xi + Cj) / 2
        Here Cj is a random choosen corner, where each corner has a color added to a color list
        Method skips the first 5 values and then starts to add values to an array
        If plot=True, then the method plots the array with the plt.scatter(), with c=color_list

        """
        
        X = self.random_points()

        for i in range(5):
            X = (X + self.corners[np.random.randint(0, self.gonSize)])/2

        X_array = np.zeros((iter, 2))
        color_array = np.zeros(iter)
        color_list = []

        x = time.time()

        for i in range(iter):
            rand_index = np.random.randint(0, self.gonSize)
            X = (X + self.corners[rand_index])/2
            X_array[i] = X
            color_array[i] = rand_index

            if rand_index == 0:
                color_list.append('red')

            elif rand_index == 1:
                color_list.append('blue')

            elif rand_index == 2:
                color_list.append('green')

        y = time.time()

        if plot == True:
            x1 = time.time()
            plt.scatter(*zip(*X_array), c=color_list, s=0.1, marker='.')
            x2 = time.time()
            plt.title('Color List - Sierpinski Triangle')
            plt.axis('equal')
            plt.axis('off')
            plt.show()

            if runtime == True:
                print("Runtime for {} iterations (Calculations): {}".format(iter, y-x))
                print("Runtime for {} iterations (Plotting): {}".format(iter, x2-x1))
                print("Runtime for {} iterations (Total): {}".format(iter, (y-x) + (x2-x1)))

        else:

            if runtime == True:
                print("Runtime for {} iterations (Calculations): {}".format(iter, y-x))
                print("Runtime for {} iterations (Plotting): {}".format(iter, x2-x1))
                print("Runtime for {} iterations (Total): {}".format(iter, (y-x) + (x2-x1)))

            return X_array, color_array

    def alternative_color(self, iter, plot=True, runtime=False):

        """
        Method: alternative_color

        Parameters:

            iter - Number of points/iterations

            plot - To plot arrays or return arrays

            runtime - print out runtime of iterations and plotting
        
        Method calls random_points() method to get a start value
        Loops through array and uses the formula Xi+1 = (Xi + Cj) / 2
        Here Cj is a random choosen corner.
        Method skips the first 5 values and then starts to add values to an array
        If plot=True, then the method plots the array with the plt.scatter()
        Calculates a RGB color array, which is plotted with the plt.scatter()

        """

        C = np.zeros((iter, 3))
        r_1 = np.array([1, 0, 0])
        r_2 = np.array([0, 1, 0])
        r_3 = np.array([0, 0, 1])
        r_j = [r_1, r_2, r_3]

        X = self.random_points()

        for i in range(5):
            X = (X + self.corners[np.random.randint(0, self.gonSize)])/2

        X_array = np.zeros((iter, 2))

        x = time.time()

        for i in range(1, iter):
            rand_index = np.random.randint(0, self.gonSize)
            X = (X + self.corners[rand_index])/2
            X_array[i-1] = X
            C[i] = (C[i-1] + r_j[rand_index])/2

        y = time.time()

        if plot == True:
            x1 = time.time()
            plt.scatter(*zip(*X_array), c=C, s=0.1, marker='.')
            x2 = time.time()
            plt.title('RGB Color Array - Sierpinski Triangle')
            plt.axis('equal')
            plt.axis('off')
            plt.show()

            if runtime == True:
                print("Runtime for {} iterations (Calculations): {}".format(iter, y-x))
                print("Runtime for {} iterations (Plotting): {}".format(iter, x2-x1))
                print("Runtime for {} iterations (Total): {}".format(iter, (y-x) + (x2-x1)))

        else:

            if runtime == True:
                print("Runtime for {} iterations (Calculations): {}".format(iter, y-x))
                print("Runtime for {} iterations (Plotting): {}".format(iter, x2-x1))
                print("Runtime for {} iterations (Total): {}".format(iter, (y-x) + (x2-x1)))

            return X_array, color_array

    def plot_bouderies(self):
        """

        Plots the boundaries of the n-gon

        """

        plt.scatter(*zip(*self.corners))
        plt.show()

# -------------------------------------------- OUTSIDE CLASS ------------------------------------------------ #



if __name__ == "__main__":
    n = 3
    c0 = np.array([0,0])
    c1 = np.array([1,0])
    c2 = np.array([0.5,0.866])

    parser = argparse.ArgumentParser(
        description="Sierpinksi script"
    )

    parser.add_argument('Function', help='Which function to use', type=int)
    parser.add_argument('Iterations', help='How many points to plot', type=int)
    parser.add_argument('--Runtime', help='Wheather to print runtime or not', type=bool)
    args = parser.parse_args()

    corners = np.array([c0, c1, c2])
    new_obj = Triangle(3, corners)

    if args.Function == 1:
        new_obj.iteration(args.Iterations, runtime=args.Runtime)
    elif args.Function == 2:
        new_obj.color_iteration(args.Iterations, runtime=args.Runtime)
    elif args.Function == 3:
        new_obj.alternative_color(args.Iterations, runtime=args.Runtime)
    else:
        print()
        print("Please choose between function 1 - 3")
        print()
        print("Function 1: iterations")
        print()
        print("Function 2: color_iteration")
        print()
        print("Function 3: alternative_color")
        print()
        print("Please see docstrings for more information")
        print()
        sys.exit()