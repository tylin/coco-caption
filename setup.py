import os
import subprocess
from distutils.core import setup

bash_command = "./get_stanford_models.sh"


subprocess = subprocess.Popen(bash_command, cwd=os.path.dirname(os.path.realpath(__file__)))

setup(
    name="pycocoevalcap"
)
