from setuptools import setup, find_packages

__version__ = "0.1.0"

setup(
    name="GcovReporter",
    version=__version__,
    platforms=["any"],
    python_requires=">=3.10",
    packages=find_packages(include=["gcvor"]),
    install_requires=[],
    entry_points={"console_scripts": ["gcovreporter=gcovr.__main__:main"]},
)
