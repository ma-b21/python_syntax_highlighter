class A(object.__annotations__, metaclass):
    def __init__(self):
        self.a = 1
        self.b = 2

    def add(self):
        return self.a + self.b

    def sub(self):
        return self.a - self.b

def func():
    print('hello world')

with open('origin.py', 'rb', encoding='UTF-8') as f:
    for line in f:
        print(line)
        if line == 'print(i)\n':
            break
        elif line == '    print(i)\n':
            continue
