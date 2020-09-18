import re

from setuptools import setup


with open("mypy2junit.py", "rt", encoding="utf8") as f:
    version = re.search(r'__version__ = \'(.*?)\'', f.read()).group(1)

with open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name="mypy2junit",
    version=version,
    url="https://github.com/Dundee/mypy2junit",
    license="BSD-3-Clause",
    author="Daniel Milde",
    author_email="daniel@milde.cz",
    description="Script for converting output from MyPy to Junit XML format",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    #packages=find_packages("mypy2junit"),
    py_modules=["mypy2junit"],
    python_requires=">=3.5",
    entry_points={"console_scripts": ["mypy2junit = mypy2junit:main"]},
    extras_require={
        "dev": [
            "pytest",
        ],
    },
)
