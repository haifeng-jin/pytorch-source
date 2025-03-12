# Ops explained

Let's take a look at this code example.

```py
import torch

a = torch.randn(2, 1)
b = torch.randn(2, 1)
c = a.add(b)
```

It just adds two tensors together.
`a` is a `DoubleTensor` instance inherited methods from `_TensorBase` and `torch._C.DoubleTensorBase`.
The `add` method is defined in the `torch._C.DoubleTensorBase`.
As we know, `torch._C` is a C++ extension.
It is defined in `TensorMethods.cpp`, which is auto generated using template `TensorMethods.cwrap`.
If you track it down, you will find the actual definition of the `add` function is in [`THTensorMath.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THTensorMath.h).

This is for the CPU implementation.
What about the GPUs? How does it do the hardware abstractions?
