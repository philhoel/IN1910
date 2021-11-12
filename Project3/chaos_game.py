import numpy as np
import matplotlib.pyplot as plt
import numba
import time
import argparse
import cProfile

#######################################
"""
Written by Philip Hoel
A program for a generalized chaos game
"""
######################################


# --------------------------------------------- CLASS ChaosGame ---------------------------------------------- #

class ChaosGame:

    """ Class for creating n-gons through chaos game """

    # --------------------- Private ------------------------------- #

    def __init__(self, r=0.5, nGon=3):

        """
        Init

        Parameters:

            r:
                - number used in calculation
                - must be type float
                - must be less than 1

            nGon:
                - number of boundary points
                - must be more than 2
                - must be int

        
        """
        if isinstance(r, float) and 0 < r and r < 1:
            self.r = r
        
        elif isinstance(r, (float, int)) and r >= 1:
            print("r must be of type 'float' in the interval (0, 1)")
            raise ValueError
        else:
            print("r must be of type 'float' in the interval (0, 1)")
            raise TypeError

        if isinstance(nGon, int) and nGon >= 3:
            self.nGon = nGon
        else:
            print("nGon must be of type 'int' and >= 1")
            raise TypeError

        self.corners = self._generate_ngon()

    def _generate_ngon(self):

        """Calculates n-gon position"""

        angle = 2*np.pi/self.nGon
        theta = []
        theta_i = 0 
        for i in range(self.nGon):
            theta.append(theta_i)
            theta_i += angle

        corners = np.zeros((self.nGon, 2))
        for i in range(self.nGon):
            corners[i] = (np.sin(theta[i]), np.cos(theta[i]))

        return corners

    def _starting_point(self):

        """Calculates starting values"""

        j = 0
        y = np.random.dirichlet(np.ones(self.nGon), size=1)
        X = np.zeros(self.corners.shape)
        LinearCombo = np.zeros((1,2))
        for i in y[0]:
            X[j] = i*self.corners[j]
            LinearCombo += X[j]
            j += 1

        return LinearCombo

    def _compute_color(self, steps, discard=5):

        """
        Calculates both points for array and color values

        Parameters:

            steps - number of points

            discard - number of points to skip

        """

        X = self._starting_point()
        for j in range(discard):
            X = self.r * X + (1 - self.r) * self.corners[np.random.randint(0, self.nGon)]

        X_array = np.zeros((steps, 2))
        C = np.zeros(steps)
        for k in range(1, steps):
            C_index = np.random.randint(0, self.nGon)
            X = self.r * X + (1 - self.r) * self.corners[C_index]
            X_array[k] = X
            C[k] = (C[k-1] + C_index)/2

        return X_array, C


    # ---------------------------------- Public ------------------------------ #

    def iterate(self, steps, discard=5):

        """
        Calulates points for array, without colors

        Parameters:

            steps - number of points

            discard - number of points to skip

        """
        X = self._starting_point()
        for i in range(discard):
            X = self.r * X + (1 - self.r) * self.corners[np.random.randint(0, self.nGon)]

        X_array = np.zeros((steps, 2))
        corner_index = np.zeros(steps)
        for i in range(steps):
            C_index = np.random.randint(0, self.nGon)
            X = self.r * X + (1 - self.r) * self.corners[C_index]
            X_array[i] = X
            corner_index[i] = C_index

        return X_array, corner_index

    def plot(self, color=False, cmap='jet', steps=10000, title='n-gon'):

        """
        Plots array

        Parameters:

            color - Whether to plot with color or not

            cmap - Type of color mapping

            steps - number of points

            title - title for plot
        """
        
        if color:
            X_array, C = self._compute_color(steps)
            plt.scatter(*zip(*X_array), s=0.1, marker='.', c=C, cmap=cmap)
            plt.title(title)
            plt.axis('equal')
            plt.axis('off')
            
            
        else:
            X_array, corner_index = self.iterate(steps, 5)
            plt.scatter(*zip(*X_array), s=0.1, marker='.', cmap=cmap)
            plt.title(title)
            plt.axis('equal')
            plt.axis('off')

    
    def show(self, color=False, cmap='jet', steps=10000, title='n-gon'):

        """
        Plots array

        Parameters:

            color - Whether to plot with color or not

            cmap - Type of color mapping

            steps - number of points

            title - title for plot
        """
        
        self.plot(color, cmap, steps, title)
        plt.show()

    def savepng(self, outfile, color=False, cmap='jet', steps=10000, title='n-gon'):

        """
        Saves plot

        Parameters:

            outfile - name of saved file

            color - Whether to plot with color or not

            cmap - Type of color mapping

            steps - number of points

            title - title for plot
        """

        self.plot(color, cmap, steps, title)
        plt.savefig(outfile, dpi=300, transparent=True)
        plt.clf()
    
    
    def get_color_array(self, steps):

        """
        Returns point array and color array for further use of arrays

        Parameters:

            steps - number of points
        """
        X_array, C = self._compute_color(steps)

        return X_array, C

    def plot_ngon(self):

        """
        Plots boundariy points for n-gon
        """
        plt.scatter(*zip(*self.corners))
        plt.show()


def main():

    final_obj1 = ChaosGame(r=1/2, nGon=3)
    final_obj2 = ChaosGame(r=1/3, nGon=4)
    final_obj3 = ChaosGame(r=1/3, nGon=5)
    final_obj4 = ChaosGame(r=3/8, nGon=5)
    final_obj5 = ChaosGame(r=1/3, nGon=6)
    final_obj1.savepng('chaos1.png', True, 'jet', 100000, 'Triangle')
    final_obj2.savepng('chaos2.png', True, 'jet', 100000, 'Square')
    final_obj3.savepng('chaos3.png', True, 'jet', 100000, 'Pentagon')
    final_obj4.savepng('chaos4.png', True, 'jet', 100000, 'Pentagon 2')
    final_obj5.savepng('chaos5.png', True, 'jet', 100000, 'Hexagon')


if __name__ == '__main__':

    
    
    test_obj = ChaosGame(1/2, 3)
    test_obj.show(True, 'jet', 100000, title='Triangle')

    for i in range(3, 8):
        test = ChaosGame(1/3, i)
        test.show(True, 'jet', 100000, title=f'{i}-gon')
    
    

    #main()

    
    
