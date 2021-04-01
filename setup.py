import setuptools

with open('README.md') as fh:
    long_description = fh.read()


def _requires_from_file(filename):
    return open(filename).read().splitlines()


setuptools.setup(
    name='ffptutils',
    version='0.1.1',
    author='Hideki Sekine',
    author_email='sekineh@me.com',
    description='a python library that reads and writes Spirent iTest ParameterTree (.ffpt) files',
    license='MIT',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sekineh/ffptutils-py",
    packages=setuptools.find_packages(),
    install_requires=_requires_from_file('requirements.txt'),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
    entry_points={  # Optional
        'console_scripts': [
            'ffpt2csv=ffptutils.scripts.ffpt2csv:main',
            'csv2ffpt=ffptutils.scripts.csv2ffpt:main',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/sekineh/ffptutils-py/issues',
        # 'Funding': 'https://donate.pypi.org',
        # 'Say Thanks!': 'http://saythanks.io/to/example',
        'Source': 'https://github.com/sekineh/ffptutils-py/',
    },
)
