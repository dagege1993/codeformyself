class Parent(object):
    x = 3


class ChildA(Parent):
    pass


class ChildB(Parent):
    pass


print(Parent.x, ChildA.x, ChildB.x)
ChildA.x = 2
print(Parent.x, ChildA.x, ChildB.x)
Parent.x = 1
print(Parent.x, ChildA.x, ChildB.x)
