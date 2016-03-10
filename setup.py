import os

from setuptools import find_packages
from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.md")) as f:
    README = f.read().rstrip("\n")
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read().rstrip("\n")
with open(os.path.join(here, "requirements", "core.txt")) as _file:
    REQUIREMENTS = [line.rstrip("\n") for line in _file.readlines()]
with open(os.path.join(here, "requirements", "test.txt")) as _file:
    TEST_REQUIREMENTS = REQUIREMENTS
    TEST_REQUIREMENTS += [line.rstrip("\n") for line in _file.readlines()]
with open(os.path.join(here, "VERSION")) as _file:
    VERSION = _file.read().rstrip("\n")


setup(
    name="avro-service-clients",
    version=VERSION,
    description="avro-service-clients",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha"
    ],
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    url="https://github.com/packagelib/avro-service-clients",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite="tests",
)
