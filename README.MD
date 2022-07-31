# `cran_parser`

A tool for creating install scripts from CRAN.

## Why is this tool needed?

If a package is no longer in the [R cran page](https://cran.r-project.org/) (this software uses sensR as the principle
example of this), then you can no longer install it on new versions of R because there are no binaries for it. The issue
stems even more, as you can't just install from a source file, but you have to go through and find all the sources that
also don't exist (or are no longer entirely compatible with your package). This can take a long time / be arduous, so I
created this short script to help download from CRAN and create an installer.

## Where can I find snapshots?

A good place to go is [MRAN](https://mran.microsoft.com/timemachine). The default for this software is [2019-05-24](https://cran.microsoft.com/snapshot/2019-05-24/) (a snapshot which has sensR).

## What do I need to compile R packages?
### macOS
Follow [this](https://ohdsi.github.io/Hades/rSetup.html#Installing_R_build_tools) guide to install Xcode

### Windows
Install [Rtools](https://cran.r-project.org/bin/windows/Rtools/)

### Ubuntu
`sudo apt install build-essential`

## The Command Line Interface
```commandline
$ python cran_parser.py  -h
usage: CRAN Downloader [-h] [--package PACKAGE] [--list-packages] [--search]
                       [--source SOURCE]

Create download script for R package

options:
  -h, --help         show this help message and exit
  --package PACKAGE  The package to create the installer for
  --list-packages    List all the available packages
  --search           Search for the package name parsed to [--package]
  --source SOURCE    The CRAN homepage to use
```

### How to search for a package
```commandline
python cran_parser.py  --search --package sensr
```

### How to make an installation script
```commandline
$ python cran_parser.py  --package sensR --source "https://cran.microsoft.com/snapshot/2019-05-24"
```
Creates:
```R
for (url in c("https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/mvtnorm_1.0-10.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/lattice_0.20-38.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/Matrix_1.2-17.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/survival_2.44-1.1.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/lattice_0.20-38.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/Matrix_1.2-17.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/survival_2.44-1.1.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/MASS_7.3-51.4.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/TH.data_1.0-10.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/lattice_0.20-38.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/zoo_1.8-5.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/sandwich_2.5-1.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/codetools_0.2-16.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/multcomp_1.4-10.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/MASS_7.3-51.4.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/numDeriv_2016.8-1.tar.gz", "https://cran.microsoft.com/snapshot/2019-05-24/src/contrib/sensR_1.5-1.tar.gz")) {install.packages(url, repos=NULL, method="libcurl")}
```

## Setting up with snap
```commandline
$ snapcraft --debug
$ sudo snap install jimbob88-cran-parser_0.1_multi.snap --devmode --dangerous
$ jimbob88-cran-parser.cran-parser -h
```
