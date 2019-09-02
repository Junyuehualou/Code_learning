class Stu:
    def __init__(self, name: str):
        self.name = name

    def run(self):
        print(self.name + "跑步ing")



s1 = Stu("jack")    # __init__(s1, name: str)
s2 = Stu("may")     # __init__(s2, name: str)

s1.run()        # s1.run(s1)
s2.run()        # s2.run(s2)