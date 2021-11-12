#include <iostream>
#include <cmath>
#include <cstdlib>
#include <string>
#include <stdexcept>
#include <exception>
#include <vector>


//-------------------------- STRUCT Node ---------------------------------

struct Node {
    int storage;
    Node* next;
    Node* prev;

    Node(int n) {
        storage = n;
        next = nullptr;
        prev = nullptr;
    }

    Node(int n, Node* N, Node* P) {
        storage = n;
        next = N;
        prev = P;
    }
};

//-------------------------- CLASS CircLinkedList -------------------------------

class CircLinkedList {
    private:
        Node* head;
        int size = 0;

    public:

        CircLinkedList() {
            head = nullptr;
        }

        CircLinkedList(int n) {
            
            head = nullptr;

            for (int i = 0; i <= n; i++) {
                append(i);
            }
        }

        CircLinkedList(int i, int n) {
            head = nullptr;

            while (i <= n) {
                append(i);
                i++;
            }
        }

        ~CircLinkedList() {
            int i = 0;
            Node* current;
            Node* next_node;

            current = head;

            while (i < size) {
                next_node = current->next;
                delete current;
                current = next_node;
                i += 1;
            }
        }

        // Overloading operator
        int& operator[] (int index) {
            if (size == 0) {
                throw std::range_error("List is empty");
            }
            if (index > size-1) {
                index = index % size;
            }
            Node* current;
            current = head;
            for (int i = 0; i < index; i++) {
                current = current->next;
            }
            return current->storage;
        }

        // Member function: length()
        // Return the length of the list
        int length(void) {
            return size;
        }

        // Member function: append()
        // Adds an element to the back of the list
        void append(int n) {
            if (head == nullptr) {
                head = new Node(n, head, head);
                size += 1;
                return;
            }

            int i = 0;
            Node* current;
            Node* tmp;
            current = head;
            while (i < size-1) {
                current = current->next;
                i += 1;
            }

            tmp = new Node(n, head, current);
            current->next = tmp;
            head->prev = tmp;
            size += 1;
        }

        // Member function: stack_front
        // Appends to the front of the list
        void stack_front(int n) {
            if (head == nullptr) {
                head = new Node(n, head, head);
                size += 1;
                return;
            }
            
            Node* current;
            Node* tmp;
            current = head;
            tmp = head;
            for (int i = 0; i < size-1; i++) {
                current = current->next;
            }


            head = new Node(n, tmp, current);
            size += 1;
            
        }

        // Member function: insert()
        // Inserts an element at specified index
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
            } 
            else if (index == 0) {
                stack_front(val);
            } else {
                throw std::range_error("IndexError: Index out of range");
            }
        }

        // Member function: remove()
        // Removes an element at specified index
        void remove(int index) {
            if (index == 0) {
                Node* current;
                current = head;
                head = current->next;
                head->prev = current->prev;
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
                throw std::range_error("IndexError: Index out of range");
            }
        }


        int pop(int index) {
            int pop_value;
            if (index == 0) {
                Node* current;
                current = head;
                head = current->next;
                head->prev = current->prev;
                pop_value = current->storage;
                delete current;

                size -= 1;

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
                index = index%size;
                pop(index);
                //throw std::range_error("IndexError: Index out of range");
            }
        }

        int pop(void) {
            int pop_value;
            pop_value = pop(size-1);

            return pop_value;
        }

        void print(void) {
            Node* current = head;
            int i = 0;
            std::cout << "[ ";
            while (i < size-1) {
                std::cout << current->storage;
                std::cout << ", ";
                current = current->next;
                i += 1;
            }

            std::cout << current->storage << " ]" << std::endl;
        }


        
        std::vector<int> josephus_sequence(int k) {
            int i = 0;
            std::vector<int> dead_soldiers;
            int popped_soldiers;
            Node* current;
            Node* temp;
            current = head;
            for (int j = 0; j < k-1; j++) {
                current = current->next;
            }
            while (size != 0) {
                Node* tmp;
                dead_soldiers.push_back(current->storage);
                tmp = current->next;
                temp = current->prev;
                tmp->prev = temp;
                temp->next = tmp;
                tmp = current;
                while (i < k) {
                    current = current->next;
                    i++;
                }
                delete tmp;
                size -= 1;
                i = 0;
            }

            return dead_soldiers;
        }
};

// -------------------------- OUTSIDE CLASS ---------------------------------------

int last_man_standing(int n, int k) {
    CircLinkedList new_obj(1, n);
    std::vector<int> dead_soldiers = new_obj.josephus_sequence(k);
    return dead_soldiers[dead_soldiers.size()-1];
}

// -------------------------- MAIN -------------------------------------------

int main() {

    std::cout << std::endl;

    // Initiation
    CircLinkedList example;

    std::cout << "Testing append()" << std::endl;
    std::cout << "----------------" << std::endl;
    std::cout << std::endl;
    
    // Function call
    example.append(1);
    example.append(2);
    example.append(3);
    example.append(4);
    example.append(5);
    example.append(6);
    example.append(7);
    example.append(8);
    example.print();

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing insert(0, 0)" << std::endl;
    std::cout << "--------------------" << std::endl;
    std::cout << std::endl;

    // Function call
    example.insert(0,0);
    example.print();

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing remove(0)" << std::endl;
    std::cout << "-----------------" << std::endl;
    std::cout << std::endl;

    // Function call
    example.remove(0);
    example.print();


    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing pop()" << std::endl;
    std::cout << "-----------------" << std::endl;
    std::cout << std::endl;

    // Function call
    example.pop();
    example.print();

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing length()" << std::endl;
    std::cout << "-----------------" << std::endl;
    std::cout << std::endl;

    // Function call
    std::cout << example.length() << std::endl;

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing operator" << std::endl;
    std::cout << "-----------------" << std::endl;
    std::cout << std::endl;

    // Function call
    std::cout << example[4] << std::endl;

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing Overloaded constructor" << std::endl;
    std::cout << "------------------------------" << std::endl;
    std::cout << std::endl;

    // Initiation
    CircLinkedList example_2(7);
    example_2.print();

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing Josephus sequence" << std::endl;
    std::cout << "------------------------------" << std::endl;
    std::cout << std::endl;

    // Initiation
    std::vector<int> new_vector;
    CircLinkedList josephus(1, 68);
    //josephus.print();
    //std::cout << josephus.length() << std::endl;
    
    new_vector = josephus.josephus_sequence(7);
    for (int i = 0; i < new_vector.size(); i++) {
        std::cout << i+1 << ". dead: " << new_vector[i] << std::endl;
    }
    

    std::cout << std::endl;
    std::cout << "----------------------------------" << std::endl;
    std::cout << std::endl;
    std::cout << "Testing last_man_standing" << std::endl;
    std::cout << "------------------------------" << std::endl;
    std::cout << std::endl;

    std::cout << last_man_standing(68, 7) << std::endl;

    return 0;
}