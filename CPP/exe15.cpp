#include <iostream>
#include <fstream>
#include <string>

const int MAX_CONTACTS = 100; // Maximum number of contacts

class PhoneBook {
private:
    std::string names[MAX_CONTACTS];
    std::string numbers[MAX_CONTACTS];
    int contactCount;

public:
    PhoneBook() : contactCount(0) {}

    // Load contacts from a file
    void loadContacts(const std::string& filename) {
        std::ifstream file(filename);
        std::string line;
        while (std::getline(file, line) && contactCount < MAX_CONTACTS) {
            size_t pos = line.find(':');
            if (pos != std::string::npos) {
                names[contactCount] = line.substr(0, pos);
                numbers[contactCount] = line.substr(pos + 1);
                contactCount++;
            }
        }
        file.close();
    }

    // Save contacts to a file
    void saveContacts(const std::string& filename) {
        std::ofstream file(filename);
        for (int i = 0; i < contactCount; i++) {
            file << names[i] << ": " << numbers[i] << std::endl;
        }
        file.close();
    }

    // Get telephone number by name
    std::string getNumber(const std::string& name) {
        for (int i = 0; i < contactCount; i++) {
            if (names[i] == name) {
                return numbers[i];
            }
        }
        return "Contact not found.";
    }

    // Get name by telephone number
    std::string getName(const std::string& number) {
        for (int i = 0; i < contactCount; i++) {
            if (numbers[i] == number) {
                return names[i];
            }
        }
        return "Number not found.";
    }

    // Update telephone number
    void updateNumber(const std::string& name, const std::string& newNumber) {
        for (int i = 0; i < contactCount; i++) {
            if (names[i] == name) {
                numbers[i] = newNumber;
                std::cout << "Number updated." << std::endl;
                return;
            }
        }
        std::cout << "Contact not found." << std::endl;
    }
};

void showMenu() {
    std::cout << "\nPhone Book Menu:" << std::endl;
    std::cout << "1. Get telephone number by name" << std::endl;
    std::cout << "2. Get name by telephone number" << std::endl;
    std::cout << "3. Update telephone number" << std::endl;
    std::cout << "4. Exit" << std::endl;
}

int main() {
    PhoneBook phoneBook;
    phoneBook.loadContacts("phonebook.txt");

    int choice;

    do {
        showMenu();
        std::cout << "Enter your choice: ";
        std::cin >> choice;
        std::cin.ignore(); // Clear newline character from input buffer

        switch (choice) {
            case 1: {
                std::string name;
                std::cout << "Enter name: ";
                std::getline(std::cin, name);
                std::cout << "Telephone number: " << phoneBook.getNumber(name) << std::endl;
                break;
            }
            case 2: {
                std::string number;
                std::cout << "Enter telephone number: ";
                std::getline(std::cin, number);
                std::cout << "Name: " << phoneBook.getName(number) << std::endl;
                break;
            }
            case 3: {
                std::string name, newNumber;
                std::cout << "Enter name: ";
                std::getline(std::cin, name);
                std::cout << "Enter new telephone number: ";
                std::getline(std::cin, newNumber);
                phoneBook.updateNumber(name, newNumber);
                phoneBook.saveContacts("phonebook.txt"); // Save changes to file
                break;
            }
            case 4:
                std::cout << "Exiting..." << std::endl;
                break;
            default:
                std::cout << "Invalid choice. Please try again." << std::endl;
        }
    } while (choice != 4);

    return 0;
}