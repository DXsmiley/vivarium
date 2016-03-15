def r(i):
    if i <= 0:
        return 1
    return r(i - 1) + r(i - 2)

print(r(int(input())))