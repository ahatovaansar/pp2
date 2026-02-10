#1
class A:
    def show(self):
        print("Class A")

class B:
    def display(self):
        print("Class B")

class C(A, B):
    pass

obj = C()
obj.show()
obj.display()
