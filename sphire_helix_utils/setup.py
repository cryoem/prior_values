import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "sphire_helix_utils",
    version = "0.0.2",
    author = "Markus Stabrin",
    author_email = "markus.stabrin@mpi-dortmund.mpg.de",
    description=("Fundamentals library for helical sphire"),
    license = "GPL",
    keywords = "sphire helix helical cryo-EM",
    url = "www.sphire.mpg.de",
    packages = ["sphire_helix_utils", "tests"],
    long_description=read("README.md"),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
        "License :: GPL License",
    ]
    )
