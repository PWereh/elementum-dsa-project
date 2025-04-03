"""Setup script for the Elementum DSA package.
"""

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requirements = fh.read().splitlines()

setup(
    name="elementum_dsa",
    version="1.0.0",
    author="Elementum Team",
    author_email="info@elementum-dsa.org",
    description="Elementum Domain-Specific Agent (DSA) Governance Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PWereh/elementum-dsa-project",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.3.1",
            "pytest-cov>=4.1.0",
            "black>=23.3.0",
            "mypy>=1.3.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
        ],
        "docs": [
            "mkdocs>=1.4.3",
            "mkdocstrings>=0.22.0",
        ],
    },
    include_package_data=True,
    package_data={
        "elementum_dsa": ["knowledge/schemas/*.json"],
    },
    entry_points={
        "console_scripts": [
            "elementum-dsa=app:main",
        ],
    },
)
