#include<iostream>
using namespace std;

class exec
{
    private :
        int x,y ;

        public:
        void get(int a,int b)
        {
            x=a;
            y=b;
        }
        void divide()
        {
            try 
            {
            if (x != 0 && y != 0) 
            {
                int z = x / y;
                cout << "Result: " << z ;
            } 
            else 
            {
                throw y;
            }
        }
        catch (int a) 
        {
            cout << "ERROR: Cannot divide by ZERO." ;
        }
        catch(...)
        {
            // handle all the other exceptions 
        }
    }
};
int main()
{
    int a, b;
    cout << "Enter first number: ";
    cin >> a;
    cout << "Enter second number: ";
    cin >> b;

    exec div;
    div.get(a, b);
    div.divide();

    return 0;
}