# export this for sure
export PBR_VERSION=4.0.2

# build the distribution
python setup.py sdist

# install the package
pip install .
