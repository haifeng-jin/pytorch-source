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

It follows the traditional built-in Python C++ interfacing using `setuptools.Extension`.
Each extension can be imported as a Python module.
However, the the module itself, including its functions, classes, methods are all defined in a `.cpp` file.
For the basics of such Python/C++ interfacing, please refer to the [Tiny Python C++](https://github.com/haifeng-jin/tiny-py-cpp) project.

For the specific case of PyTorch, as we mentioned before,
they implemented the basic `Tensor` related logics and the ops in C++.

The project relies on `setup.py` to build everything including both Python and C++ code.
Instead of a barebone C++ extension, it uses a series of custom classes to build the project.
They did these custom build mainly for two reasons.
The first is to build the underlying ops libraries of `TH`, `THC`, `THNN`, and `THCUNN`.
They are built as independent C++ projects.
The second reason is that the wrapper code, which wraps the C++ functionality into Python objects are not manually written,
but generated using Python scripts from template files marked as `.cwrap` files

There are only three `.cwrap` files.

```
torch/csrc/nn/THCUNN.cwrap
torch/csrc/nn/THNN.cwrap
torch/csrc/generic/TensorMethods.cwrap
```


## C++ building

The custom classes to build the project include `build_deps`, `build_ext`.
They will be executed during running `python setup.py build`.
The command first calls `class build(...):`, which subsequently call the `build_deps`, and `build_ext` as its subcommands.

The `build_deps` builds the ops libraries (`TH`, `THC`, `THNN`, `THCUNN`) into
shared objects (`*.so`) to be linked by the python modules, so that these C++ libraries are callable from Python.
It calls `torch/lib/build_all.sh` to build the binary files (`*.so`).

Then, it calls `tools.nnwrap.generate_wrappers()` to generate the python wrapper modules from template files, `*.cwrap`.
In a `*.cwrap` file, it only provides the minimal information needed for the Python module.
No information redundency at all.

Then, it uses `setuptools.Extension` to define all the C++ extension modules and pass them to the `setup()` function.
For example:

```py
THNN = Extension("torch._thnn._THNN",  # The python import path for the module
    libraries=['TH', 'THNN'], # required third-party (or C++ built-in) libraries
    sources=['torch/csrc/nn/THNN.cpp'], #The source files for the Python module. This is the generated file.
    language='c++',
    ...
)
```

The library can be imported from `torch._thnn._THNN`.

Similarly, it uses `build_ext` to build the tensor methods implemented in C++ into a shared object (`*.so`) callable from Python.
The `tools.cwrap.cwrap()` to convert `'torch/csrc/generic/TensorMethods.cwrap'` into `'torch/csrc/generic/TensorMethods.cpp'`.

All of the extension modules are written in C++/CUDA. No plain C code are found.
