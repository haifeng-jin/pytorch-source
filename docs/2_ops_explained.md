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

In the

```cpp
      THPTensor* result = _result_guard.get();
      _th_result.release();
      
      THTensor_(add)(LIBRARY_STATE ((THPTensor*)result)->cdata, ((THPTensor*)self)->cdata, THPUtils_(unpackReal)(PyTuple_GET_ITEM(args, 0)));Py_INCREF(result);
      return (PyObject*)(result);
```

If you track it down, you will find the actual definition of the `add` function is in [`THTensorMath.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THTensorMath.h).


## GPU implementation

Above is the CPU implementation.
The GPU implementation can be found in [`THCTensorMathPairwise.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/THC/generic/THCTensorMathPairwise.h) similarly.

It launches the following kernel in [`THCApply.cuh`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/THC/THCApply.cuh) to handle the add operation.

```cuda
__global__ void
kernelPointwiseApply2(TensorInfo<Ta, IndexType> a,
                      TensorInfo<Tb, IndexType> b,
                      IndexType totalElements,
                      Op op) {
  // Iterate over the elements assigned to the current thread.
  for (IndexType linearIndex = blockIdx.x * blockDim.x + threadIdx.x;
       linearIndex < totalElements;
       linearIndex += gridDim.x * blockDim.x) {
    // Convert `linearIndex` into an offset of `a`
    const IndexType aOffset =
      IndexToOffset<Ta, IndexType, ADims>::get(linearIndex, a);

    // Convert `linearIndex` into an offset of `b`
    const IndexType bOffset =
      IndexToOffset<Tb, IndexType, BDims>::get(linearIndex, b);

    // Performing the actual op.
    op(&a.data[aOffset], &b.data[bOffset]);
  }
}
```

## Hardware abstraction

The hardware abstraction is on a very high level, which means there are more hardware specific code.
The abstraction is on the backend level.
The user choose different backend (CPU/GPU), the PyTorch will then use `TH` or `THC` accordingly.
There are totally separate implementation of the `Tensor`, `Storage` classes, and their ops.

## Type abstraction

The type abstraction is done on a super low level, which means the code are pretty generic and less amount of type-specific code.
All these kernels, and ops `add`, `sub`, etc., are all type-agnostic.
You can find them under the `generic` directory under each C/C++/CUDA project.

## The Tensor ops today
