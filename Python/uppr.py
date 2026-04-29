def to_uppercase(i):
    result = ""
    for char in i:
        if 'a' <= char <= 'z': 
            result += chr(ord(char) - 32) 
        else:
            result += char  
    return result

# Example usage
i = "hello world!"
print("Original String:", i)
print("Uppercase String:", to_uppercase(i))