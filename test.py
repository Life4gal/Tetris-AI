class A:
	...


class B(A):
	...


b = A()
print(type(b))

b.__class__ = B
print(type(b))
