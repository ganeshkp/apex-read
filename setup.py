import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apex-read",
    version="0.1",
    author="Ganeshkumar Patil",
    author_email="ganeshkumar.patil@gmail.com",
    description="Reads Apex files and provides required information",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ganeshkp/apex-read",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)