#include <iostream>
#include <typeinfo> // For typeid
using namespace std;

// Base class Shape
class Shape {
public:
    virtual void display() const = 0; 
    virtual ~Shape() {}
};

// Derived class Circle
class Circle : public Shape {
public:
    void display() const override 
    {
        cout << "This is a Circle." << endl;
    }
};

class Rectangle : public Shape {
public:
    void display() const override 
    {
        cout << "This is a Rectangle." << endl;
    }
};

int main() {

    Circle c1;
    Rectangle r1;


    Shape* shapes[2];
    shapes[0] = &c1;
    shapes[1] = &r1;


    for (int i = 0; i < 2; ++i) 
    {
        cout << "Shape " << i + 1 << ": ";
        if (dynamic_cast<Circle*>(shapes[i])) 
        {
            cout << "Type is Circle" << endl;
        } 
        else if (dynamic_cast<Rectangle*>(shapes[i])) 
        {
            cout << "Type is Rectangle" << endl;
        }
        shapes[i]->display();
    }

    return 0;
}
