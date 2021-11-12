# H19_project3_philipth
Project 3 for philipth (philipth@mail.uio.no)

## Assignment 1  
triangle.py uses argparse library  
run: python triangle.py number iterations --Runtime true  
number: Choose functions between 1, 2, and 3  
iterations: number of points to use  
--Runtime: Optional parameter to print runtime  

## Assignment 2
chaos_game.py test_chaos_game.py  
run: python chaos_game.py  
run: pytest  
Will simply run through 6 different chaos game plots  

## Assignment 3
fern.py uses argparse library  
run: python fern.py iterations --Runtime --cProfile  
iterations: number of points to use  
--Runtime: Optional parameter to print runtime  
--cProfile: Optional parameter to run cProfile  

## Assignment 4
variations.py  
run: python variations.py  

For problem c) to d) in assignment 4, I was a little confused about what the assignment asked for, so I instead made two different functions.  
The first one (blend) takes in a dictionary with procentage (key) and method to use (value) and creates a linear combination of these. It does not  
make a uniform difference, because that must be specified in the dictionary.  
The second one (gradual_transform) takes in a method and gradually plots from that method to linear.  

## Problems encountered
Did encounter some issues with fern. For some reason I could not figure out, it does not plot the transforms correctly other than linear and swirl.
