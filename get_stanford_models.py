#!/usr/bin/env python
from __future__ import print_function

import os
import shutil
import zipfile

try:
    from urllib.request import urlretrieve
except ImportError:
    from urllib import urlretrieve


def main():
    core_nlp = "stanford-corenlp-full-2015-12-09"
    spice_lib = "pycocoevalcap/spice/lib"
    jar = "stanford-corenlp-3.6.0{}.jar"
    
    root_dir = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
    
    jar_file = os.path.join(root_dir, spice_lib, jar)
    if os.path.exists(jar_file.format("")):
        print("Found Stanford CoreNLP.")
    else:
        print("Downloading Stanford CoreNLP...")
        core_nlp_zip = core_nlp + ".zip"
        urlretrieve(
            "http://nlp.stanford.edu/software/{}".format(core_nlp_zip),
            core_nlp_zip)
        print("Unzipping {}...".format(core_nlp_zip))
        zip_ref = zipfile.ZipFile(core_nlp_zip, "r")
        zip_ref.extractall(spice_lib)
        zip_ref.close()
        shutil.move(
            os.path.join(spice_lib, core_nlp, jar.format("")),
            spice_lib)
        shutil.move(
            os.path.join(spice_lib, core_nlp, jar.format("-models")),
            spice_lib)
        os.remove(core_nlp_zip)
        shutil.rmtree(os.path.join(spice_lib, core_nlp))
        print("Done.")
    

if __name__ == "__main__":
    main()

