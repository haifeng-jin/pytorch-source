# PyTorch Source

This repo is a fork of the PyTorch v0.1.1 release.
We try to read the code and understand the basics of PyTorch internal mechanisms.

Please refer to the [docs](https://github.com/haifeng-jin/pytorch-source/tree/master/docs) for how to navigate the codebase.

## Why use v0.1.1?

The latest PyTorch repo is too large to dive into, which contains different
distribution strategy, hardware abstraction, tracing, compiler, and so on.  One
could easily get lost when try to read those. However, our focus is the very
core features of PyTorch, which is CPU/GPU ops with autodiffs in eager mode.

The v0.1.1 version is rather small and managable. It only contains the CPU/GPU
ops, autodiff in eager mode.

In addition, the key ideas of these features did not change much in all the
following versions. These implementations can be traced through the commit
history into the large PyTorch codebase today. I will refer to the latest
implementation as we explore the source code.


## Build and install

Create the conda environment:

```shell
conda create --name pytorch
conda activate pytorch
```

Install the dependencies:

```shell
conda install python cmake make
conda install -c conda-forge cxx-compiler
pip install pip==25.0
pip install -r requirements.txt
```

Build and install torch in develop mode:

```shell
python setup.py build
pip install -e .
```

## This repo

Here are the things this repo added
* Build and install instructions.
* Explanation of the source code. (under `docs/`).
* Changed the `.travis.yml` CI into the GitHub Actions.
* Some code examples under `examples/`.
