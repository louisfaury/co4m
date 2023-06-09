from setuptools import setup, find_packages

setup(
    name="co4m",
    version="0.0",
    packages=find_packages(include=["co4m", "co4m/*"]),
    python_requires=">=3.6",
    license="Apache License 2.0",
    author="Louis Faury",
    author_email="l.faury@hotmail.fr",
    description="Connect Four Master",
)