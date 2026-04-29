#include <iostream>

class A {
public:
    void show() {
        std::cout << "Class A" << std::endl;
    }
};

class B : public A {
public:
    void show() {
        std::cout << "Class B" << std::endl;
    }
};

class C : public A {
public:
    void show() {
        std::cout << "Class C" << std::endl;
    }
};

class D : public B, public C {
};

int main() {
    D obj;
    // obj.show(); // Error: ambiguous call to show()
    obj.B::show(); // Specify which show() to call
    obj.C::show(); // Specify which show() to call
    return 0;
}
