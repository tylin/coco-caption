import sys
import os
import subprocess
from setuptools import setup, find_packages
import get_stanford_models

get_stanford_models.main()

packages = [p for p in find_packages() if "pycocoevalcap" in p]

setup(
    name="pycocoevalcap",
    packages=packages,
    package_dir={"pycocoevalcap": "pycocoevalcap"},
    install_requires=['pycocotools'],
    version="0.0",
    zip_safe=False,
    include_package_data=True,
)

