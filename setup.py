import sys
import os
import subprocess
from setuptools import setup, find_packages
import get_stanford_models

bash_command = "./get_stanford_models.sh"

get_stanford_models.main()

setup(
    name="pycocoevalcap",
    version="0.0",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)

