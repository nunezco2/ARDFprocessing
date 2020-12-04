# University of Illinois at Urbana-Champaign
# Illinois Informatics
# 
# ARDF file reader with concurrency
# To use in the analysis of fast force map AFM data
#
# @author: Santiago Nunez-Corrales <nunezco2@illinois.edu>

import setuptools


setuptools.setup(
    name='ARDFreader',
    version='0.1.0',
    author='Santiago Nunez-Corrales',
    author_email='nunezco2@illinois.edu',
    packages=['ardfreader'],
    license='LICENSE.txt',
    description='An ARDF reader package.',
    long_description=open('README.md').read(),
    python_requires='>3.6',
    install_requires=[
    ]
)