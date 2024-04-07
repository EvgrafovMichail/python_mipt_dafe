"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="solidipy_mipt",
    version="1.1.0",
    description="Make your ML solid!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kynemallv/python_mipt_dafe/tree/main/homeworks/sem2_hw1/solidipy_framework",
    author="Matvei Gorskii",
    author_email="matveygor41@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="ml",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10, <4",
    install_requires=["numpy", "matplotlib", "scikit-learn"],
    project_urls={
        "Bug Reports": "https://github.com/Kynemallv/python_mipt_dafe/issues/new?labels=bug&template=bug-report---.md",
        "Source": "https://github.com/Kynemallv/python_mipt_dafe/tree/main/homeworks/sem2_hw1/solidipy_framework",
    },
)
