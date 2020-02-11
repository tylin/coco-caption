from setuptools import setup, find_namespace_packages

# Prepend pycocoevalcap to package names
package_names = ['pycocoevalcap.'+p for p in find_namespace_packages()]

setup(
    name='pycocoevalcap',
    version=1.1,
    packages=['pycocoevalcap']+package_names,
    package_dir={'pycocoevalcap': '.'},
    package_data={'': ['*.jar', '*.gz']},
    install_requires=['pycocotools>=2.0.0']
)
