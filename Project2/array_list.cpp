#include <iostream>
#include <cstdlib>
#include <string>
#include <exception>
#include <stdexcept>
#include <cmath>
#include <vector>

using namespace std;

//----------------------------------------- CLASS ArrayList -----------------------------------

class ArrayList {
    private:
        // Creating an array pointer
        int *data;
        // Setting the true size
        int capacity;

        // Increasing capacity
        // f(n) = 5n +3
        // O(n)
        void capacity_increase(void) {
            capacity *= 2;
            int *tmp;
            tmp = new int[capacity];
            for (int i = 0; i < size; i++) {
                tmp[i] = data[i];
            }

            delete[] data;
            data = tmp;
            
        }

        // Decreases capacity
        void capacity_decrease(int capacity_input) {
            capacity = capacity_input;
            int *tmp;
            tmp = new int[capacity];
            for (int i = 0; i < size; i++) {
                tmp[i] = data[i];
            }

            delete[] data;
            data = tmp;
        }

        // Shrinks array to fit size
        void shrink_to_fit(void) {
            int i = 0;
            while (i < capacity) {
                if (size < pow(2, i)) {
                    capacity_decrease(pow(2, i));
                    break;
                }

                i += 1;
            }
        }

    public:
        // Setting the public size
        int size;

        // Constructor
        ArrayList() {
            size = 0;
            capacity = 10000;

            // Dynamically allocated array
            data = new int[capacity];
        }

        // Overloading the constructor. Makes it possible
        // to create array with given values
        // array({number, number, number...})
        ArrayList(vector<int> input_vec) {
            size = input_vec.size();
            capacity = 10000;
            data = new int[capacity];
            for (int i = 0; i < size; i++) {
                data[i] = input_vec[i];
            }
        }

        // Destructor
        ~ArrayList() {

            // Deallocating memory - Deleting allocated memory
            // to not get memory leaks
            delete[] data;
        }

        int& get_capacity(void) {
            return capacity;
        }

        // Overloading the [] operator, makes it possible to
        // call element of array using [index]
        int& operator[] (int i) {
            if ((0 <= size) and (i < size)) {
                return data[i];
            } else {
                throw range_error("IndexError");
            }
        }

        // Another way to get element at a certain index
        int& get(int i) {
            if ((0 <= i) and (i < size)) {
                return data[i];
            }
        }

        // Member function: length
        // Returns the number of elements in the array
        int length(void) {
            return size;
        }

        // Member function: append
        // Appends an element to the end of the array
        void append(int n) {
            if (size >= capacity) {
                capacity_increase();
            }

            data[size] = n;
            size += 1;
        }

        // Member function: insert
        // Inserts an element at specified index
        void insert(int val, int index) {
            if (size >= capacity) {
                capacity_increase();
            }
            if ((0 <= index) and (index <= size)) {
                int *tmp;
                tmp = new int[size+1];
                for (int i = 0; i <= size; i++) {
                    if (i < index) {
                        tmp[i] = data[i];
                    } 
                    else if (i == index) {
                        tmp[index] = val;
                    } else {
                        tmp[i] = data[i-1];
                    }
                }

                for (int i = 0; i <= size; i++) {
                    data[i] = tmp[i];
                }

                delete[] tmp;
                size += 1;
            } else {
                throw range_error("Index out of range");
            }
        }

        // Member function: remove
        // Removes an element from the list at specified index
        void remove(int index) {
            if ((0 <= index) and (index < size)) {
                int i = 0;
                int *tmp;
                tmp = new int[size-1];
                while (i < size-1) {
                    if (i < index) {
                        tmp[i] = data[i];
                    }
                    else  {
                        tmp[i] = data[i+1];
                    }

                    i += 1;
                }

                for (int i = 0; i < size-1; i++) {
                    data[i] = tmp[i];
                }

                delete[] tmp;
                size -= 1;

            } else {
                throw range_error("Index out of range");
            }

            double capacity_check = 0.25*capacity;
            
            if (size <= capacity_check) {
                shrink_to_fit();
            }
            
        }

        // Member function: pop
        // calls remove and removes element at given index
        // return that element
        int pop(int index) {
            int tmp_var;
            tmp_var = data[index];
            remove(index);

            return tmp_var;
        }

        // Member function: Overloaded pop
        // calls remove and removes last element in array
        // returns the last element
        int pop(void) {
            int tmp_var;
            tmp_var = data[size-1];
            remove(size-1);

            return tmp_var;
        }

        // Member function: print
        // Prints out the whole array within square brackets
        void print(void) {
            cout << "[ ";
            for (int i = 0; i < size-1; i++) {
                cout << data[i];
                cout << ", ";
            }
            cout << data[size-1] << " ]" << endl;
        }
};

// ------------------------ OUTSIDE CLASS --------------------------------

// Checks if an integer n is prime or not
bool is_prime(int n) {
    int check = 1;
    for (int i = 2; i < n; i++) {
        check *= (n%i);
    }
    if (check != 0) {
        return true;
    } else {
        return false;
    }
}

// ---------------------------- MAIN ----------------------------------------

int main(void) {

    // Testing primes
    int i = 3;
    int j = 0;
    ArrayList primes;
    while (j <= 10) {
        if (is_prime(i)) {
            primes.append(i);
            j += 1;
        }

        i += 1;
    }

    cout << endl;
    cout << "Testing primes" << endl;
    cout << "--------------" << endl;
    cout << endl;
    primes.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing initiation with vector" << endl;
    cout << "------------------------------" << endl;
    cout << endl;


    // Testing initiation with vector
    ArrayList new_list({1, 2, 3, 4, 5});
    new_list.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing insert(2, 2)" << endl;
    cout << "--------------------" << endl;
    cout << endl;

    // Testing insert member function
    new_list.print();
    new_list.insert(2, 2);
    new_list.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing remove(2)" << endl;
    cout << "--------------------" << endl;
    cout << endl;


    // Testing remove member function
    new_list.print();
    new_list.remove(2);
    new_list.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing pop(2)" << endl;
    cout << "--------------" << endl;
    cout << endl;

    // Testing pop member function
    new_list.print();
    new_list.pop(2);
    new_list.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing pop()" << endl;
    cout << "-------------" << endl;
    cout << endl;

    // Testing pop(void) member function
    new_list.print();
    new_list.pop();
    new_list.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing operator" << endl;
    cout << "----------------" << endl;
    cout << endl;

    cout << new_list[2] << endl;

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing length()" << endl;
    cout << "----------------" << endl;
    cout << endl;

    cout << new_list.length() << endl;

    return 0;
}