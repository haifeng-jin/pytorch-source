pip uninstall torch -y
rm -rf build
python setup.py build
pip install -e .
