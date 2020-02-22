# MyPy2Junit

[![Build Status](https://travis-ci.org/Dundee/mypy2junit.svg?branch=master)](https://travis-ci.org/Dundee/mypy2junit)

Script for converting output from MyPy to Junit XML format

## Usage

```
mypy somedir | mypy2junit > junit.xml
```

or:

```
mypy > output.txt
mypy2junit output.txt > junit.xml
```

## Installation

```
pip install mypy2junit
```
