import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="phantom-pureapi",
    version="0.0.2",
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
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.10",
)
