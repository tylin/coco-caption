from setuptools import setup, find_namespace_packages

# Prepend pycocoevalcap to package names
package_names = ['pycocoevalcap.'+p for p in find_namespace_packages()]

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name='pycocoevalcap',
    version=1.2,
    maintainer='salaniz',
    description="MS-COCO Caption Evaluation for Python 3",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/salaniz/pycocoevalcap",
    packages=['pycocoevalcap']+package_names,
    package_dir={'pycocoevalcap': '.'},
    package_data={'': ['*.jar', '*.gz']},
    install_requires=['pycocotools>=2.0.2'],
    python_requires='>=3'
)
