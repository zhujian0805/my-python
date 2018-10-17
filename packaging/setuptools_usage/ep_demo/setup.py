from setuptools import setup, find_packages

setup(
    name='mypackage',
    version="0.1",

    # Including all packages in src
    packages=find_packages('mypackage'),
    # Telling distutils packages are in src
    package_dir={'': 'mypackage'},
    entry_points={
        'mypackage.api.v1': [
            'main=mypackage:main',
        ],
    })
