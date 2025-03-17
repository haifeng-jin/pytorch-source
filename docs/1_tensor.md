# Tensor

Tensor is just a view of the storage.
The storage manages the actual memory allocation of the tensor.

Here are the core classes:
* The Python classes: [`torch/Tensor.py`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/Tensor.py), [`torch/Storage.py`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/Storage.py).
* The C++ wrappers: [`torch/csrc/generic/Tensor.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/csrc/generic/Tensor.h), [`torch/csrc/generic/Storage.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/csrc/generic/Storage.h)
* The actual C implementation: [`torch/lib/TH/generic/THTensor.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THTensor.h), [`torch/lib/TH/generic/THStorage.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THStorage.h).

As you can see, a lot of them are under the `generic` directory, which means the implementations are type-agnostic.
They can be applied to integers as well as floats.

The Python and C++ wrappers are just wrappers. What matters is the C implementations.

## The Tensor class

Here are the actual code of the core classes with my comments.

```C
typedef struct THTensor
{
    long *size; // A list of integers. The shape of the tensor.

    // A list of integers.
    // The increments needed on each dimension to get the next element.
    // Similar to the `step` argument of `range()` in Python.
    // Mainly used to provide a different view of the same storage.
    long *stride; 

    int nDimension; // Length of the shape list.

    THStorage *storage; // Pointer to the storage object.
    long storageOffset; // Also used to skip elements and provide new views.
    int refcount;

    char flag;

} THTensor;
```

As you can see, there is no actual float type data in the class except for the pointer to the storage.
The attributes like `stride` and `storageOffset` are just to skip elements on the same tensor storage to create new views of the same tensor.

## The Storage class

```C
typedef struct THStorage
{
    // We saw a lot of real types in the code.
    // Actually, they are just float.
    // You can find "#define real float" in torch/lib/TH/THGenerateFloatTypes.h. 
    real *data; // The actual float data.
    long size; // The total number of elements.
    int refcount;
    char flag;
    THAllocator *allocator; // Custom memory allocators for CPU/GPU.
    void *allocatorContext; // The extra context to store with the allocator.
    struct THStorage *view;
} THStorage;
```

As we can see, it contains the pointer to the actual data and a memory allocator to make memory for the data on CPU/GPU.

## CUDA Tensors

The above implementations are all for CPUs.
The CUDA implementation are in the `torch/lib/THC` directory.
However, the code looks very similar.
PyTorch will route through different paths as it chooses between CPU and GPU.

## The Tensor class today
The Tensor-Storage structure is preserved to the latest PyTorch today.
Tensor class is moved around by [the merge of Tensor and Variable classes](https://github.com/pytorch/pytorch/pull/5225) and [a follow-up PR removing the dead code](https://github.com/pytorch/pytorch/pull/5417).
Today the `Tensor` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/aten/src/ATen/templates/TensorBody.h#L92) as part of the ATen library,
and the `Storage` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/c10/core/Storage.h#L19) under `c10` merged from the Caffe2 library.


