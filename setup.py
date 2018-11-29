from setuptools import setup, find_packages
from Cython.Build import cythonize

setup(
    name='Python Examples',
    version='0.0.1',
    description='Python example code',
    url='https://github.com/w0251251/python_examples',
    author='Nicholas Tancredi',
    author_email='nicholastancredi@gmail.com',
    license='GPL3',
    packages=find_packages(),
    ext_modules=cythonize("examples/cython_array_sum/index.pyx"),
    install_requires=[
        'numpy',
        'pydantic',
        'pytypes',
        'Cython',
    ],
    extras_require={
        'dev': ['pylint']
    },
)
