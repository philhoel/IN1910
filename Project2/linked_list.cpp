#include <iostream>
#include <string>
#include <cmath>
#include <stdexcept>
#include <exception>
#include <cstdlib>
#include <vector>

using namespace std;


// Doubly Linked List

//-------------------------STRUCT Node ----------------------------------

struct Node {
    int storage;
    Node *next;
    Node *prev;

    // Struct constructor
    Node(int n) {
        storage = n;
        next = nullptr;
        prev = nullptr;
    }

    // Struct constructor
    Node(int n, Node* N, Node* P) {
        storage = n;
        next = N;
        prev = P;
    }
};

//------------------------- CLASS LinkedList ----------------------------

class LinkedList {
    private:
        int size = 0;
        Node* head;
        //Node* tail;

    public:

        // Constructor
        LinkedList() {
            head = nullptr;
            //tail = nullptr;
        }


        // Overloaded constructor
        // Makes it possible to initiate list with given values
        LinkedList(vector<int> input_vec) {
            head = nullptr;

            for (int i = 0; i <= input_vec.size(); i++) {
                append(input_vec[i]);
            }
        }


        // Destructor
        ~LinkedList() {
            Node* current;
            Node* next_node;

            current = head;

            while (current != nullptr) {
                next_node = current->next;
                delete current;
                current = next_node;
            }
        }

        // Overload [] operator
        int& operator[] (int index) {
            if ((index < 0) or (index >= size)) {
                throw range_error("IndexError: Index out of range");
            }
            Node* current;
            current = head;
            for (int i = 0; i < index; i++) {
                current = current->next;
            }
            return current->storage;
        }

        // Return length of list
        int length(void) {
            return size;
        }

        // Member fuction: append
        // Adds an element at the end of the list
        void append(int n) {
            if (head == nullptr) {
                head = new Node(n, nullptr, nullptr);
                size += 1;
                return;
            }

            Node* current;
            current = head;
            while (current->next != nullptr) {
                current = current->next;
            }

            current->next = new Node(n, nullptr, current);
            size += 1;
        }

        // Member function: stack_front
        // Appends to the front of the list
        void stack_front(int n) {
            if (head == nullptr) {
                head = new Node(n, nullptr, nullptr);
                size += 1;
                return;
            }

            Node* current;
            current = head;
            head = new Node(n, current, nullptr);
            current->prev = head;

            size += 1;
            
        }

        // Member function: insert
        // Adds an element at specified index
        void insert(int val, int index) {
            if (index == size-1) {
                append(val);

            } else if ((index > 0) and (index < size-1)) {
                Node* current;
                Node* tmp;
                current = head;

                for (int i = 0; i < index; i++) {
                current = current->next;
                }

                current = current->prev;
                
                tmp = new Node(val, current->next, current);
                current->next = tmp;
                current = tmp->next;
                current->prev = tmp;

                size += 1;

            } else if (index == 0) {
                stack_front(val);

            } else {
                throw range_error("IndexError: Index out of range");
            }
        }

        // Member function: remove
        // Removes an element at specified index
        void remove(int index) {
            if (index == 0) {
                Node* current;
                current = head;
                head = current->next;
                head->prev = nullptr;
                delete current;

                size -= 1;

            } else if ((index > 0) and (index <= size-1)) {
                Node* current;
                Node* tmp;
                Node* temp;
                current = head;
                for (int i = 0; i < index; i++) {
                    current = current->next;
                }
                tmp = current->prev;
                temp = current->next;
                tmp->next = temp;
                temp->prev = tmp;
                delete current;

                size -= 1;

            } else {
                throw range_error("IndexError: Index out of range");
            }
        }

        // Member function: pop
        // Removes an element at specified index and returns the value
        int pop(int index) {
            int pop_value;
            if (index == 0) {
                Node* current;
                current = head;
                head = current->next;
                head->prev = nullptr;
                pop_value = current->storage;
                delete current;

                return pop_value;

            } else if ((index > 0) and (index <= size-1)) {
                Node* current;
                Node* tmp;
                Node* temp;
                current = head;
                for (int i = 0; i < index; i++) {
                    current = current->next;
                }
                tmp = current->prev;
                temp = current->next;
                tmp->next = temp;
                temp->prev = tmp;
                pop_value = current->storage;
                delete current;

                size -= 1;

                return pop_value;
            } else {
                throw range_error("IndexError: Index out of range");
            }
        }

        // Member function: Overloaded pop
        // Removes the last element and returns the value
        int pop(void) {
            int pop_value;
            pop_value = pop(size-1);

            return pop_value;
        }

        // Member function: print
        // Prints out list nicely
        void print(void) {
            Node* current = head;
            cout << "[ ";
            while (current->next != nullptr) {
                cout << current->storage;
                cout << ", ";
                current = current->next;
            }

            cout << current->storage << " ]" << endl;
        }

};

// ------------------------ MAIN -----------------------------------------

int main() {

    LinkedList example;

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing append()" << endl;
    cout << "----------------" << endl;
    cout << endl;


    example.append(1);
    example.append(2);
    example.append(3);
    example.append(4);
    example.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing length()" << endl;
    cout << "----------------" << endl;
    cout << endl;


    cout << example.length() << endl;

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing insert(2, 2)" << endl;
    cout << "--------------------" << endl;
    cout << endl;

    example.insert(2, 2);
    example.insert(2, 0);
    example.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing remove(0)" << endl;
    cout << "-----------------" << endl;
    cout << endl;

    example.remove(0);
    example.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing pop(2)" << endl;
    cout << "--------------" << endl;
    cout << endl;

    example.pop(2);
    example.print();

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing operator" << endl;
    cout << "----------------" << endl;
    cout << endl;

    for (int i = 0; i < example.length(); i++) {
        cout << example[i] << endl;
    }

    cout << endl;
    cout << "----------------------------------" << endl;
    cout << endl;
    cout << "Testing Overloaded constructor" << endl;
    cout << "------------------------------" << endl;
    cout << endl;

    //vector<int> new_vec{1, 2, 3, 4, 5, 6};
    LinkedList example_2({1, 2, 3, 4, 5, 6});
    example_2.print();

    return 0;
}