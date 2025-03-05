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

You can see some `*.cu` and `*.cuh` files under `THC` and `THCUNN`.
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

## Python/C++ interfacing

The project relies on `setup.py` to build everything including both Python and C++ code.
It has a series of custom build classes to build the project, like `build_deps`, `build_ext`.
They will be executed during running `python setup.py build`,
the entry of which is `class build(...):`, which subsequently call the `build_deps`, and `build_ext` as its subcommands.

The `build_deps` builds the ops libraries (`TH`, `THC`, `THNN`, `THCUNN`) into
shared objects (`*.so`) to be linked by the python modules, so that these C++ libraries are callable from Python. It
uses custom build command to call `torch/lib/build_all.sh` to build the binary
files (`*.so`).

Then, it calls `tools.nnwrap.generate_wrappers()` to generate the python wrapper modules from custom format source files, `*.cwrap`.
In a `*.cwrap` file, `` for example, ...

```shell
more to be inserted in here.
```

Then, it uses `setuptools.Extension` to define all the C++ extension modules and pass them to the `setup()` function.
For example:

```py
THNN = Extension("torch._thnn._THNN",
    libraries=['TH', 'THNN'],
    sources=['torch/csrc/nn/THNN.cpp'],
    language='c++',
    ...
)
```

Similarly, it uses `build_ext` to the tensor methods implemented in C++ into a shared object (`*.so`) callable from Python.
The `tools.cwrap.cwrap()` to convert `'torch/csrc/generic/TensorMethods.cwrap'` into `'torch/csrc/generic/TensorMethods.cpp'`.

All of the extension modules are written in C++/CUDA. No plain C code are found.


## Questions
* How does cwrap generate files?
* What is the C++ Module.cpp?
* Where are the CUDA ops? THC, THCUNN. How can those `.cu` files got compiled by a C++ compiler?
