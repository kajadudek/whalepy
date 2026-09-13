from pathlib import Path

from setuptools import find_packages, setup

long_description = (Path(__file__).parent / "README.md").read_text(encoding="utf-8")

setup(
    name="whalepy",
    version="1.0.0",
    description="WhalePy: A Python library of whale optimization algorithm variants for continuous optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Kaja Dudek, Natalia Luberda, Wojciech Ksiazek",
    author_email="wojciech.ksiazek@pk.edu.pl",
    url="https://github.com/kajadudek/whalepy",
    license="BSD-3-Clause",
    packages=find_packages(exclude=("benchmarks", "examples", "doc")),
    package_data={"whalepy": ["functions/functions_info/*.json"]},
    include_package_data=True,
    python_requires=">=3.10",
    install_requires=[],
    keywords=["whale optimization algorithm", "metaheuristics", "swarm intelligence", "optimization"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
