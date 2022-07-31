import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cran-parser",
    version="0.1",
    author="James Blackburn",
    author_email="blackburnfjames@gmail.com",
    description=("A tool for creating install scripts from CRAN snapshots"),
    license="BSD",
    keywords="CRAN R",
    url="https://github.com/jimbob88/cran_parser",
    packages=['cran_parser', 'tests'],
    long_description=read('README.MD'),
    install_requires=read('requirements.txt'),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        'console_scripts': [
            'cran_parser = cran_parser:main',
        ],
    },
)
