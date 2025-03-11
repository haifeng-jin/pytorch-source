# Tensor Explained

The Tensor-Storage structure is preserved to the latest PyTorch today.
Tensor class is moved around by [the merge of Tensor and Variable classes](https://github.com/pytorch/pytorch/pull/5225) and [a follow-up PR removing the dead code](https://github.com/pytorch/pytorch/pull/5417).
Today the `Tensor` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/aten/src/ATen/templates/TensorBody.h#L92) as part of the ATen library,
and the `Storage` class is [here](https://github.com/pytorch/pytorch/blob/v2.6.0/c10/core/Storage.h#L19) under `c10` merged from the Caffe2 library.
