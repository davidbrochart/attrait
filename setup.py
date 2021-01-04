import setuptools

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
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
