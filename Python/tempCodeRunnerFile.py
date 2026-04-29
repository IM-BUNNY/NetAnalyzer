def my_atoi(s: str) -> int:
    s = s.strip()
    if not s:
        return 0

    sign = 1
    i = 0
    result = 0

    # check sign
    if s[0] in ['-', '+']:
        if s[0] == '-':
            sign = -1
        i += 1

    # process all characters
    while i < len(s):
        if s[i].isdigit():  # only handle digits
            result = result * 10 + (ord(s[i]) - ord('0'))
        # if it's not a digit, just skip it
        i += 1

    return sign * result

print(my_atoi("31e2r3r4r21"))