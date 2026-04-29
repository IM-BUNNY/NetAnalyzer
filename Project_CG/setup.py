"""
Setup script for Ancient Indian Chess
Allows installation as a package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ancient-indian-chess",
    version="1.0.0",
    author="Chess Game Developer",
    description="A 3D chess game with ancient Indian theming using OpenGL",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ancient-indian-chess",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment :: Board Games",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyOpenGL>=3.1.7",
        "PyOpenGL-accelerate>=3.1.7",
        "glfw>=2.6.3",
        "numpy>=1.24.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "indian-chess=main:main",
        ],
    },
)
