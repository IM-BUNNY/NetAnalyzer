/* #include <iostream>
using namespace std;

template <typename T>
void change(T &x, T &y) 
{
    T a;
    a = x;
    x = y;
    y = a;
    cout << "After swapping: " << x << " " << y << endl;
}

int main()
{
    int s;
    int p, q;
    float a, b;
    char x, y;

    cout << "Enter the data you want to swap:" << endl;
    cout << "1. Swap integers\n";
    cout << "2. Swap floating values\n";
    cout << "3. Swap characters\n";
    cin >> s;

    switch (s)
    {
    case 1:
        cout << "Enter the first integer value: ";
        cin >> p;
        cout << "Enter the second integer value: ";
        cin >> q;
        cout << "Entered values: " << p << " " << q << endl;
        change(p, q);
        break;

    case 2:
        cout << "Enter the first floating value: ";
        cin >> a;
        cout << "Enter the second floating value: ";
        cin >> b;
        cout << "Entered values: " << a << " " << b << endl;
        change(a, b);
        break;

    case 3:
        cout << "Enter the first character: ";
        cin >> x;
        cout << "Enter the second character: ";
        cin >> y;
        cout << "Entered characters: " << x << " " << y << endl;
        change(x, y);
        break;

    default:
        cout << "Invalid option!" << endl;
    }

    return 0;
} */
#include <iostream>
#include <string>
using namespace std;

template <typename T>
class Swapper {
private:
    T x, y;

public:

    Swapper(T x, T y) : x(x), y(y) {}


    void change()
    {
        T temp = x;
        x = y;
        y = temp;
        cout << "After swapping: " << x << " " << y << endl;
    }

    void displayOriginal()
    {
        cout << "Entered values: " << x << " " << y << endl;
    }
};

int main()
{
    string dataType;

    cout << "Enter the data type you want to swap (int, float, char): ";
    cin >> dataType;

    if (dataType == "int") {
        int p, q;
        cout << "Enter the first integer value: ";
        cin >> p;
        cout << "Enter the second integer value: ";
        cin >> q;
        Swapper<int> swapper(p, q);
        swapper.displayOriginal();
        swapper.change();
    }
    else if (dataType == "float") {
        float a, b;
        cout << "Enter the first floating value: ";
        cin >> a;
        cout << "Enter the second floating value: ";
        cin >> b;
        Swapper<float> swapper(a, b);
        swapper.displayOriginal();
        swapper.change();
    }
    else if (dataType == "char") {
        char x, y;
        cout << "Enter the first character: ";
        cin >> x;
        cout << "Enter the second character: ";
        cin >> y;
        Swapper<char> swapper(x, y);
        swapper.displayOriginal();
        swapper.change();
    }
    else {
        cout << "Invalid data type entered!" << endl;
    }

    return 0;
}

