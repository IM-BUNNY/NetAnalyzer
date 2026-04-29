def in_range_or_not(number):
    return abs(number - 1000) <= 100 or abs(number - 2000) <= 100
num = int(input("Enter a number: "))
result = in_range_or_not(num)
if result:
    print(f"The number {num} is within 100 of 1000 or 2000.")
else:
    print(f"The number {num} is not within 100 of 1000 or 2000.")
    print("")
