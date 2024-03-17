import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyCHomP_utils",
    version="0.0.1",
    author="Marcio Gameiro",
    author_email="marciogameiro@gmail.com",
    description="pyCHomP utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/marciogameiro/pyCHomP_utils",
    package_dir={'':'src'},
    packages=['pyCHomP_utils'],
    install_requires=["pyCHomP2"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
