def calculate_difference(n):
    if n > 17:
        return 2 * abs(n - 17)
    else:
        return 17 - n

# Test the function
number1 = int(input("Enter 1st number : "))
result = calculate_difference(number1)
print(f"The result for {number1} is {result}")

number2 = int(input("Enter 2nd number : "))
result = calculate_difference(number2)
print(f"The result for {number2} is {result}")