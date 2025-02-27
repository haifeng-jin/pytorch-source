import torch
from torch.autograd.functions import Variable

a = torch.randn(2, 1)
a = Variable(a)
b = torch.randn(2, 1)
b = Variable(b)
c = a.mul(b)

print(a)
print(b)
print(c)

c.backward(torch.randn(2, 1))

print(a.grad)
print(b.grad)
