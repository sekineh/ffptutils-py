import setuptools

with open('README.md') as fh:
    long_description = fh.read()

setuptools.setup(
    name='ffptutils',
    version='0.0.1',
    author='Hideki Sekine',
    author_email='sekineh@me.com',
    description='a python library that reads and writes Spirent iTest ParameterTree (.ffpt) files',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sekineh/ffptutils-py",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
