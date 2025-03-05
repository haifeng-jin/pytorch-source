# Code structure

PyTorch contains both C++/CUDA and Python code.
The build system needs to compile the C++/CUDA code and bind it to `PyObject`s.
The C++ code implements the primitive classes like the `Tensor`, and primitive tensor ops.

## Libraries

PyTorch has migrated a lot of code from Lua Torch.
These migrated code live under `torch/lib`.

There are four of them:
* `TH`. The Torch ops on CPU.
* `THC`. The CUDA version of `TH`.
* `THNN`. The neural network ops on CPU.
* `THCUNN`. The CUDA version of `THNN`.

These are later turned into the `ATen` library.

## Core classes

The core classes like `Tensor`, `Storage` are implemented in C++ living under `torch/csrc`.

## Neural network classes

The Python `nn.Module` class lives under `torch/nn`.
It has the base classes and the built-in `nn.Module`s.

## Autograd

The entire autograd logic is implemented in Python for this version, but got moved into C++ implementation later.
The code lives under `torch/autograd`.

## Optimizers

It also implemented an SGD optimizer under `torch/optim`.

## Build system

The project relies on `setup.py` to build everything including both Python and C++ code.
In `setup.py`, it uses `setuptools.Extension` to define all the C++ extension modules.
For example:

```py
THNN = Extension("torch._thnn._THNN",
    libraries=['TH', 'THNN'],
    sources=['torch/csrc/nn/THNN.cpp'],
    language='c++',
    ...
)
```

All of the extension modules are written in C++/CUDA. No plain C code are found.

For the ops libraries (`TH`, `THC`, `THNN`, `THCUNN`), it uses custom build command to call `torch/lib/build_all.sh`.

## Generated code

There are also a lot of generated code files.


## Questions
* How does cwrap generate files?
* What is the C++ Module.cpp?
* Where are the CUDA ops? THC, THCUNN. How can those `.cu` files got compiled by a C++ compiler?
