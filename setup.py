import sys
import os
import subprocess
from setuptools import setup, find_packages

bash_command = "./get_stanford_models.sh"

curdir = os.path.dirname(os.path.realpath(__file__))
spicedir = os.path.join(curdir, "spice", "lib")
stanford_fmt = os.path.join(spicedir, "stanford-corenlp-3.6.0%s.jar")
base_jar = stanford_fmt % ""
model_jar = stanford_fmt % "-models"
# if os.path.exists(base_jar):
#     os.remove(base_jar)
# if os.path.exists(model_jar):
#     os.remove(model_jar)

if subprocess.call(bash_command, cwd=curdir) != 0:
    print("Stanford Jars could not be obtained and built. Do you have zip?")
    sys.exit(1)

setup(
    name="pycocoevalcap",
    version="0.0",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True
)

