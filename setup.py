import sys
import os
import subprocess
from setuptools import setup, find_packages
import get_stanford_models

get_stanford_models.main()

setup(
    name="pycocoevalcap",
    packages=["pycocoevalcap"],
    package_dir={"pycocoevalcap": "pycocoevalcap"},
    install_requires=['pycocotools'],
    version="0.0",
    zip_safe=False,
    include_package_data=True,
)

