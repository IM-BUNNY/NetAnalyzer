#include <iostream>
using namespace std;

class Cfather {
private:
    int age;
public:
    Cfather() {}

    Cfather(int a) 
    {
        try 
        {
            if (a <= 0) 
            {
                int err = 1;
                throw err;
            }
            age = a;
        } 
        catch (int errorCode) 
        {
            if (errorCode == 1) 
            {
                cout<< "Error: Father's age cannot be negative or zero!\n";
            }
        }
    }

    int getAge() const 
    {
        return age;
    }
};

class Cson : public Cfather 
{
private:
    int sage;
public:
    Cson() {}

    Cson(int sAge, int fAge) : Cfather(fAge) 
    {
        try {
            if (sAge <= 0) 
            {
                int errorCode = 2; 
                throw errorCode;
            }
            if (sAge >= fAge) 
            {
                int errorCode = 3; 
                throw errorCode;
            }
            sage = sAge;
        } 
        catch (int errorCode) 
        {
            if (errorCode == 2) 
            {
                cout << "Error: Son's age cannot be negative or zero!" ;
            } else if (errorCode == 3) 
            {
                cout << "Error: Son's age cannot be greater than or equal to Father's age!" ;
            }
        }
    }
};

int main() 
{
    int fage, sage;

    cout << "Enter the age of father: ";
    cin >> fage;
    cout << "Enter the age of son: ";
    cin >> sage;

    Cson son(sage, fage); 
    return 0;
}
