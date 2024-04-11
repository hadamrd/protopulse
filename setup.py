from setuptools import find_packages, setup
import os
here = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(here, 'VERSION')
readme_path = os.path.join(here, 'README.md')
requirements_path = os.path.join(here, 'requirements.txt')
with open(readme_path, 'r') as readme_file:
    readme = readme_file.read()
with open(requirements_path, 'r') as requirements_file:
    requirements = requirements_file.read().splitlines()
with open(version_path, 'r') as version_file:
    version = version_file.read().strip()

setup(
    # Application name:
    name="protopulse",
    # Version number (initial):
    version=version,
    # Application author details:
    author="MAJDOUB Khalid",
    author_email="majdoub.khalid@gmail.com",
    # Packages
    packages=find_packages(),
    # Include additional files into the package
    include_package_data=True,
    # Details
    url="https://github.com/hadamrd/protopulse",
    #
    # license="LICENSE.txt",
    description="Library that helps build tcp custom protocols.",
    long_description=readme,
    long_description_content_type='text/markdown',
    # Dependent packages (distributions)
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Developers',
    ]
)