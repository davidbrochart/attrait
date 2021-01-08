import setuptools
import os

def read(path):
    with open(path, 'r') as fhandle:
        return fhandle.read()

requirements = read(os.path.join(os.path.dirname(__file__), "requirements.txt"))
dev_reqs = read(os.path.join(os.path.dirname(__file__), 'requirements-dev.txt'))
extras_require = {"test": dev_reqs, "dev": dev_reqs}

with open("README.md") as f:
    long_description = f.read()

setuptools.setup(
    name="attrait",
    version="0.0.1",
    author="David Brochart",
    author_email="david.brochart@gmail.com",
    description="Asynchronous traitlets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davidbrochart/attrait",
    packages=['attrait'],
    python_requires=">=3.6.1",
    install_requires=requirements,
    extras_require=extras_require,
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
