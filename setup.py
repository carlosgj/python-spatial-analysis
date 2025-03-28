import re

from setuptools import setup

with open('spatialanalysis/__init__.py') as f:
    version = re.search("__version__ = '(.*?)'", f.read()).group(1)

setup(
    name='Spatial-Analysis',
    version=version,
    install_requires=[
        'numpy>=1.17,<2.0',
    ]
)
