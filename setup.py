import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phantom-pureapi-fedecar94",
    version="0.0.1",
    author="Federico Cardozo",
    author_email="fedecar94@outlook.com",
    description="Proof of concept of a web framework that i always wanted",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fedecar94/phantom-pureapi",
    project_urls={
        "Bug Tracker": "https://github.com/fedecar94/phantom-pureapi/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)