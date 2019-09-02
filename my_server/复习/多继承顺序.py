class Grapa:
    def show(self):
        print("grapa")

class A(Grapa):
    def show(self):
        super().show()
        print("A")

class B(Grapa):
    def show(self):
        super().show()
        print("B")

class C(A, B):
    def show(self):
        super().show()


c = C()
c.show()
print(C.mro())