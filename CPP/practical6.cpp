#include <iostream>
using namespace std;

// Forward declaration of Distance2 class
class Distance2;

// Distance1 class stores distance in miles
class Distance1 {
private:
    double miles;

public:
    Distance1(double m = 0) : miles(m) {}  // Constructor to initialize miles

    // Friend function declaration for adding Distance1 and Distance2
    friend Distance1 addDistances(const Distance1& d1, const Distance2& d2);

    // Function to display the distance in miles
    void display() const {
        cout << miles << " miles" << endl;
    }
};

// Distance2 class stores distance in kilometers and meters
class Distance2 {
private:
    int km;
    int m;

public:
    Distance2(int kilometers = 0, int meters = 0) : km(kilometers), m(meters) {
        // If meters are 1000 or more, convert them to kilometers
        if (m >= 1000) {
            km += m / 1000;
            m = m % 1000;
        }
    }

    // Friend function declaration for adding Distance1 and Distance2
    friend Distance1 addDistances(const Distance1& d1, const Distance2& d2);

    // Function to display the distance in kilometers and meters
    void display() const {
        cout << km << " kilometers and " << m << " meters" << endl;
    }
};

// Friend function to add Distance1 and Distance2
Distance1 addDistances(const Distance1& d1, const Distance2& d2) {
    // 1 mile = 1.60934 kilometers
    double total_km = d2.km + d2.m / 1000.0;
    double km_to_miles = total_km / 1.60934;  // Convert kilometers to miles
    double total_miles = d1.miles + km_to_miles;

    return Distance1(total_miles);  // Return the result as a Distance1 object
}

int main() {
    // Create Distance1 object (distance in miles)
    Distance1 d1(5);  // 5 miles

    // Create Distance2 object (distance in kilometers and meters)
    Distance2 d2(3, 500);  // 3 kilometers and 500 meters

    // Display the distances
    cout << "Distance1: ";
    d1.display();
    cout << "Distance2: ";
    d2.display();

    // Add distances
    Distance1 result = addDistances(d1, d2);

    // Display the result in miles
    cout << "Result after adding: ";
    result.display();

    return 0;
}
