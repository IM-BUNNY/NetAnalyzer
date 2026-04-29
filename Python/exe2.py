def my_atoi(s: str) -> int:
    s = s.strip()
    if not s:
        return 0

    sign = 1
    i = 0
    result = 0

    if s[0] in ['-', '+']:
        if s[0] == '-':
            sign = -1
        i += 1

    while i < len(s):
        if s[i].isdigit():
            result = result * 10 + (ord(s[i]) - ord('0'))
        
        i += 1

    return sign * result

print(my_atoi("31e3"))