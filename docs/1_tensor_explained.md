# Tensor Explained

Tensor is just a view of the storage.
The storage manages the actual memory allocation of the tensor.

Here are the core classes:
* The Python classes: [`torch/Tensor.py`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/Tensor.py), [`torch/Storage.py`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/Storage.py).
* The C++ wrappers: [`torch/csrc/generic/Tensor.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/csrc/generic/Tensor.h), [`torch/csrc/generic/Storage.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/csrc/generic/Storage.h)
* The actual C implementation: [`torch/lib/TH/generic/THTensor.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THTensor.h), [`torch/lib/TH/generic/THStorage.h`](https://github.com/haifeng-jin/pytorch-source/blob/master/torch/lib/TH/generic/THStorage.h).

What matters is the C implementations.

## About the `real` type
We saw a lot of `real` types in the code, but they are just `float`.
You can find `#define real float` in `torch/lib/TH/THGenerateFloatTypes.h`. 

## The Tensor class today
The Tensor-Storage structure is preserved to the latest PyTorch today.
Tensor class is moved around by [the merge of Tensor and Variable classes](https://github.com/pytorch/pytorch/pull/5225) and [a follow-up PR removing the dead code](https://github.com/pytorch/pytorch/pull/5417).
Today the `Tensor` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/aten/src/ATen/templates/TensorBody.h#L92) as part of the ATen library,
and the `Storage` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/c10/core/Storage.h#L19) under `c10` merged from the Caffe2 library.


