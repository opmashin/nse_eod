import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nse_eod",
    version="0.0.1",
    author="opmashin",
    author_email="opmashin@protonmail.com",
    description="Package to download NSE EOD data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['pandas','bs4','requests'],
    url="https://github.com/opmashin/nse_eod",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
