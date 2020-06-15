import setuptools

with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="trapy", # Replace with your own username
    version="0.4.0",
    author="Niklas Michel",
    author_email="niklas.michel@gmail.com",
    description="The Tape Response Assay Python Package for Somatosensory Research",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/niklasmichel/trapy",
    packages=setuptools.find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*",
                                               "demo", "*.demo", "*.demo.*", "demo.*", "demo*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license='MIT',
)
