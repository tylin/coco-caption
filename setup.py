import sys
import os
import subprocess
from setuptools import setup, find_packages
import get_stanford_models

get_stanford_models.main()

setup(
    name="pycocoevalcap",
    version="0.0",
    packages=["pycocoevalcap"],
    zip_safe=False,
    include_package_data=True,
    install_requires=['pycocotools']
)

