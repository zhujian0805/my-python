from setuptools import setup, find_packages
setup(
    name = "funniest",
    version = "0.1",
    packages = find_packages(),
    scripts=['bin/funniest-joke'],
)
