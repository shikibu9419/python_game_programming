import types

class Person():
    def __init__(self, name):
        self.name = name

    def hi(self):
        pass

def ouch(self):
    print("I am {}".format(self.name))

def main():
    """ main routine """
    p0 = Person("John")
    p1 = Person("Alex")
    p2 = Person("Peter")

    p1.hi = types.MethodType(ouch, p1)
    p2.hi = types.MethodType(lambda self: print("I AM %s" % self.name), p2)

    for p in (p0, p1, p2):
        p.hi()

if __name__ == '__main__':
    main()
