import torch

a = torch.randn(2, 1)
b = torch.randn(2, 1)
c = a.add(b)

print(a)
print(a.add)
print(b)
print(c)
