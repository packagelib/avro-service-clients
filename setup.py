import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.txt")) as f:
    README = f.read().rstrip("\n")
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read().rstrip("\n")
with open(os.path.join(here, "requirements.txt")) as _file:
    REQUIREMENTS = [line.rstrip("\n") for line in _file.readlines()]
with open(os.path.join(here, "VERSION")) as _file:
    VERSION = _file.read().rstrip("\n")

setup(
    name="service-clients",
    version=VERSION,
    description="service-clients",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
      "Programming Language :: Python",
      "Framework :: Pyramid",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    url="https://github.com/packagelib/service-clients",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite="tests",
)
