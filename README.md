# PyTorch Source

This repo is a fork of the PyTorch v0.1.1 release.
We try to read the code and understand the basics of PyTorch internal mechanisms.

Here are the this this repo added
* Build and install instructions.
* Explanation of the source code. (under `docs/`).
* Changed the `.travis.yml` CI into the GitHub Actions.

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
