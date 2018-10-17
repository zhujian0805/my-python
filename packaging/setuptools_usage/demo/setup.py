from setuptools import setup, find_packages
setup(
    name="demo",
    version="0.1",

    # Including all packages in src
    packages=find_packages('src'),
    # Telling distutils packages are in src
    package_dir={'': 'src'},
    package_data={
    # Including files with txt suffix
        '': ['*.txt'],
    # Including all data files in data
        'demo': ['data/*.dat'],
    },
    entry_points={
        'console_scripts': [
            'foo = demo:test',
            'bar = demo:test',
        ],
        'gui_scripts': [
            'baz = demo:test',
        ]
    })
