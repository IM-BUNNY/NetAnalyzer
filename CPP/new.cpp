#include <iostream>
#include <cstring>  // For strlen and strcpy

using namespace std;

class String {
private:
    char* str;  // Pointer to store the string
    int length; // To store the length of the string

public:
    // Default constructor (creates an uninitialized string of length 0)
    String() {
        length = 0;
        str = new char[1];
        str[0] = '\0';  // Empty string
        cout << "Default constructor is invoked" << endl;
    }

    // Parameterized constructor (creates a string initialized with a string constant)
    String(const char* s) {
        length = strlen(s);  // Get the length of the input string
        str = new char[length + 1];  // Allocate memory for the string
        strcpy(str, s);  // Copy the input string to str
        cout << "Parameterized constructor is invoked" << endl;
    }

    // Copy constructor (deep copy)
    String(const String& other) {
        length = other.length;
        str = new char[length + 1];  // Allocate memory for the new string
        strcpy(str, other.str);  // Copy the content of the other string
        cout << "Copy constructor is invoked" << endl;
    }

    // Destructor (deallocates the memory for the string)
    ~String() {
        delete[] str;
        cout << "Destructor is invoked" << endl;
    }

    // Function to concatenate two strings
    void concatenate(const String& other) {
        char* temp = new char[length + other.length + 1];  // Allocate memory for the concatenated string
        strcpy(temp, str);  // Copy the first string
        strcat(temp, other.str);  // Append the second string

        delete[] str;  // Free the old memory

        str = temp;  // Update the str pointer to the new concatenated string
        length += other.length;  // Update the length
    }

    // Function to copy one string to another
    void copy(const String& other) {
        delete[] str;  // Free the existing memory

        length = other.length;
        str = new char[length + 1];  // Allocate new memory
        strcpy(str, other.str);  // Copy the content of the other string
    }

    // Function to display the string
    void display() const {
        cout << str << endl;
    }
};

int main() {
    char input1[100], input2[100];

    // Get user input for the first string
    cout << "Enter the first string: ";
    cin.getline(input1, 100);
    String s1(input1);

    cout << "s1: ";
    s1.display();  // Display the first string

    // Get user input for the second string
    cout << "Enter the second string: ";
    cin.getline(input2, 100);
    String s2(input2);

    cout << "s2: ";
    s2.display();  // Display the second string

    // Concatenate two strings
    s1.concatenate(s2);
    cout << "s1 after concatenation with s2: ";
    s1.display();

    // Copy one string to another
    String s3;
    s3.copy(s2);
    cout << "s3 after copying from s2: ";
    s3.display();

    return 0;
}
