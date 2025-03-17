# Autograd

Autograd is the feature to automatically compute the gradients when we call `.backward()`.

Here is a code example:

```py
import torch
from torch.autograd.functions import Variable

a = torch.randn(2, 1)
a = Variable(a)
b = torch.randn(2, 1)
b = Variable(b)
c = a.add(b)
# When calling .backward, it has to be a single value tensor, or pass in the grads.
c.backward(torch.randn(2, 1))

print(a.grad)
print(b.grad)
```

The related code is under [`torch/autograd`](https://github.com/haifeng-jin/pytorch-source/tree/master/torch/autograd).

The most important classes here are [`Variable`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/autograd/variable.py#L3) and [`Function`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/autograd/function.py#L4).
These two classes together records the compute graph during all the ops.

A `Variable` records its `creator`, which is the `Function`, which corresponds to an op that produced this `Variable`.
It also stores the actual tensor and the grad.

All the ops used are wrapped as a `Function`, which records the output tensor IDs and the `Functions` that produces the input tensors.

In this way, the entire compute graph can be traced back from any point.

There is also an important concept called `Leaf`, which is an empty `Function`, which produces `Variables` directly as the users initialize them instead of as the result of any op. It marks as a stop for backpropagation.

The logic for running the backpropagation is in [`ExecutionEngine.run_backward()`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/autograd/engine.py#L39). It parses the compute graph backwards and compute all the grads by calling `Function._do_backward()`.

## Autograd today

The `Variable` class and the `Tensor` class got merged.
Here is the [proposal](https://github.com/pytorch/pytorch/issues/13638) for the change.
The change only affect Python APIs, the C++ implementations remained separate.
Now, all tensors can have grads.
It uses `torch.Tensor.requires_grad` to indicate if a grad should be automatically computed.

Also, the autograd implementation got moved from Python to C++, for faster execution.
