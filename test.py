class C:
     def foo(self):
         print(self.__class__)


class D:
     def foo(self):
         print(self.__class__)

c = C()
d = D()
c.foo()
d.foo()

c.foo = d.foo
c.foo()
