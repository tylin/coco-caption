#!/usr/bin/python
# This script downloads the Stanford CoreNLP models.
import os
from urllib.request import urlretrieve
from zipfile import ZipFile

CORENLP = 'stanford-corenlp-full-2015-12-09'
SPICELIB = 'lib'
JAR = 'stanford-corenlp-3.6.0'
SPICEDIR = os.path.dirname(__file__)


def print_progress(transferred_blocks, block_size, total_size):
    current_mb = transferred_blocks * block_size / 1024 / 1024
    total_mb = total_size / 1024 / 1024
    percent = current_mb / total_mb
    progress_str = "Progress: {:5.1f}M / {:5.1f}M ({:6.1%})"
    print(progress_str.format(current_mb, total_mb, percent), end='\r')


def get_stanford_models():
    jar_name = os.path.join(SPICEDIR, SPICELIB, '{}.jar'.format(JAR))
    # Only download file if file does not yet exist. Else: do nothing
    if not os.path.exists(jar_name):
        print('Downloading {} for SPICE ...'.format(JAR))
        url = 'http://nlp.stanford.edu/software/{}.zip'.format(CORENLP)
        zip_file, headers = urlretrieve(url, reporthook=print_progress)
        print()
        print('Extracting {} ...'.format(JAR))
        file_name = os.path.join(CORENLP, JAR)
        # file names in zip use '/' separator regardless of OS
        zip_file_name = '/'.join([CORENLP, JAR])
        target_name = os.path.join(SPICEDIR, SPICELIB, JAR)
        for filef in ['{}.jar', '{}-models.jar']:
            ZipFile(zip_file).extract(filef.format(zip_file_name), SPICEDIR)
            os.rename(os.path.join(SPICEDIR, filef.format(file_name)),
                      filef.format(target_name))

        os.rmdir(os.path.join(SPICEDIR, CORENLP))
        os.remove(zip_file)
        print('Done.')


if __name__ == '__main__':
    # If run as a script, excute inside the spice/ folder.
    get_stanford_models()
