# H19_project2_philiaa_philipth
Project 2 for philiaa (philiaa@mail.uio.no) and philipth (philipth@mail.uio.no)

## Run Code
Run with:
g++ --std=c++11

## Functions
All functions have been compiled and runned

## Problem 3

### Algorithm Analysis

| Task                   |ArrayList | LinkedList |
|------------------------|:--------:|:----------:|
| Get element i by index | O(1)     | O(n)       |
| Insert at front        | O(n)     | O(1)       |
| Append                 | O(1)     | O(n)       |
| Insert at middle       | O(n)     | O(n)       |
| Remove from front      | O(n)     | O(1)       |
| Remove from back       | O(n)     | O(n)       |
| Remove middle          | O(n)     | O(n)       |
| Print                  | O(n)     | O(n)       |

In all the tasks, whenever there is an O(n), it was because there was a loop.
So none of the tasks go past O(n), because there is no nested loops.
There is some difference in the actual expressions, but since we don't care about coefficients and lower scaling expressions,
we discard these.

## Problem 4

### Josephus Problem

If we use the last_man_standing function with inputs n=68 and k=7, we get that the last soldier to die,
would be number 68, the last person in the ring.
