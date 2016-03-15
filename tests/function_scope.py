def f(x, y):
    def i():
        print(x + y)
    return i
a = f(1, 2)
b = f(3, 4)
a()
b()