# @file setup.py
from setuptools import setup
 
setup(
    # Other keywords
    name = "james test",
    url = "https://james-test.com",
    author_email = "jzhu@gmail.com",
    entry_points={
        'fooo': [
            'add = add:make',
            'remove = remove:make',
            'update = update:make',
        ],
    }
)
