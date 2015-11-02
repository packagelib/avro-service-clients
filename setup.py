import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, "README.txt")) as f:
    README = f.read()
with open(os.path.join(here, "CHANGES.txt")) as f:
    CHANGES = f.read()
with open(os.path.join(here, "requirements.txt")) as _file:
    REQUIREMENTS = [line for line in _file.readlines()]


setup(
    name="schema-registry",
    version="1.0.0",
    description="schema-registry",
    long_description=README + "\n\n" + CHANGES,
    classifiers=[
      "Programming Language :: Python",
      "Framework :: Pyramid",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Alex Milstead",
    author_email="alex@amilstead.com",
    url="https://github.com/packagelib/schema-registry",
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIREMENTS,
    tests_require=REQUIREMENTS,
    test_suite="tests",
)
