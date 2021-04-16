import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Qubit",
    version="0.0.1",
    author="Michiel Jacobs",
    author_email="michiel.jacobs@vub.be",
    description="Cheminformatics package for use with machine learning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Xergon-sci/Qubit",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
