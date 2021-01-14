import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="randfacts",
    version="0.2.5",
    author="Tabulate",
    author_email="tabulatejarl8@gmail.com",
    description="Package to generate random facts",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TabulateJarl8/randfacts",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
	include_package_data=True,
)
