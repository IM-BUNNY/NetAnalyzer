#include <iostream>
#include <stdexcept>
using namespace std;

class Cfather {
private:
    int age;

public:
    Cfather() {}

    Cfather(int a) {
        try {
            if (a < 0) {
                throw a;
            }
            age = a;
            cout << "Valid father age!\n";
        } catch (const invalid_argument& e) {
            cout << "Invalid age for father! Age cannot be negative.";
        }
    }

    int getAge() const {
        return age;
    }
};

class Cson : public Cfather {
private:
    int sage;

public:
    Cson() {}

    Cson(int sAge, int fAge) : Cfather(fAge) {
        try {
            if (sAge < 0)
            {
                throw sAge;
            }
            if (sAge >= fAge) 
            {
                throw runtime_error("Son's age cannot be greater than or equal to Father's age!");
            }
            sage = sAge;
            cout << "Valid son age!\n";
        } 
        catch (int a) 
        {
            cout<<"Invalid age for son! Age cannot be negative.";
        } 
        catch (const runtime_error& e) 
        {
            cout << e.what();
        }
    }
};

int main() {
    int fage, sage;

    cout << "Enter the age of father: ";
    cin >> fage;

    cout << "Enter the age of son: ";
    cin >> sage;

    Cfather f(fage);
    Cson s(sage, fage);

    return 0;
}
