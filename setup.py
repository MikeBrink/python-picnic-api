from setuptools import setup, find_packages
import sys

#if sys.version_info < (3, 6):
#    sys.exit('Sorry, Python < 3.6 is not supported')

#with open("README.md", "r") as fh:
#    long_description = fh.read()

setup(
    name='python-picnic-api',
    version='1.0.0',
    description='Unofficial picnic api for python',
    #long_description=long_description,
    #long_description_content_type="text/markdown",
    author='someone',
    author_email='someone@someone.someone',
    url='https://github.com/Sikerdebaard/python-picnic-api',
    python_requires=">=3.6",  # example
    packages=find_packages(),  # same as name
    install_requires=[
        'certifi>=2020.12.5',
        'chardet>=3.0.4',
        'idna>=2.10',
        'requests>=2.25.0',
        'urllib3>=1.26.2',
    ],
    entry_points={
        #'console_scripts': [
        #    'dcmrtstruct2nii=dcmrtstruct2nii.cli.dcmrtstruct2nii:run',
        #],
    },
)
