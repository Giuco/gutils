from setuptools import setup, find_packages

MODULE_NAME_IMPORT = 'gutils'  # this is how this module is imported in Python (name of the folder inside `src`)

setup(
    name='gutils',
    version='0.0.1',
    url='',
    license='MIT',
    author='giuliano',
    author_email='giucoferrari!gmail.com',
    description='',
    # package_dir={'': 'gutils'},
    packages=find_packages(),
    install_requires=[
        'pandas == 0.25.0',
        'sklearn',
        'unidecode == 1.1',
        'toolz == 0.10.0',
        'ipython == 7.16.3',
        'graphviz == 0.11.1',
    ]
)
