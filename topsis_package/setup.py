from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()

setup(
    name="Topsis-Ishita-102317254", 
    version="1.0.1",
    author="Ishita Goyal",
    author_email="igoyal1_be23@thapar.edu",
    description="A command-line Python package to implement the TOPSIS method.",
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/Ishita-01/Assi1_Topsis",
    

    packages=find_packages(), 
    
    install_requires=[
        'pandas',
        'numpy', 
    ],
    
    entry_points={
        'console_scripts': [
            'topsis=Topsis_Ishita_102317254.cli:main',
        ],
    },
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
    ],
    python_requires='>=3.6',
)