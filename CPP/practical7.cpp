#include <iostream>
#include <queue>  // Standard library queue
using namespace std;

class Queue {
private:
    queue<int> q;  // Use standard library queue to store integers

public:
    // Overload the '+' operator as a member function to insert an element into the queue
    Queue& operator+(int value) {
        q.push(value);  // Insert element at the end of the queue
        return *this;   // Return the current queue object for chaining
    }

    // Overload the '-' operator as a member function to remove an element from the queue
    Queue& operator-(int) {
        if (!q.empty()) {
            q.pop();  // Remove element from the front of the queue
        } else {
            cout << "Queue is empty. Cannot remove an element!" << endl;
        }
        return *this;  // Return the current queue object for chaining
    }

    // Function to display the elements in the queue
    void display() const {
        queue<int> temp = q;  // Create a temporary queue to display the elements
        cout << "Queue: ";
        while (!temp.empty()) {
            cout << temp.front() << " ";
            temp.pop();
        }
        cout << endl;
    }
};

int main() {
    Queue q;

    // Insert elements into the queue using '+' operator
    q + 10;
    q + 20;
    q + 30;
    q.display();  // Display queue: 10 20 30

    // Remove an element from the queue using '-' operator
    q - 0;
    q.display();  // Display queue: 20 30

    return 0;
}
