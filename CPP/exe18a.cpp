#include <iostream>
#include <string>
#include <cctype>
using namespace std;

class Employee 
{
private:
    string name;
    int age;
    double salary;

public:
    void enterData() {
        int err = 0;  

        try 
        {
            cout << "Enter name: ";
            getline(cin, name);

            for (char c : name) {
                if (isdigit(c)) {
                    err = 1;  
                    throw err;
                }
            }

            cout << "Enter age: ";
            cin >> age;
            if (age < 18 || age > 60) {
                err = 2;
                throw err;
            }

            cout << "Enter salary: ";
            cin >> salary;
            cin.ignore();
        }
        catch (int a) 
        {
            if (a == 1) {
                cout<< "Error: Name should not contain numeric characters.";
            } else if (a == 2) {
                cout<< "Error: Age must be between 18 and 60.";
            }
        }
        catch(...)
        {

        }
    }

    void displayData() const {
        cout << "\nEmployee Details:\n";
        cout << "Name: " << name << "\n";
        cout << "Age: " << age << "\n";
        cout << "Salary: " << salary << "\n";
    }
};

int main() {
    Employee emp;
    emp.enterData();
    emp.displayData();
    return 0;
}
