from setuptools import setup, find_packages
from os.path import join, dirname

setup(
    name='openskyapi',
    version='0.0.1',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    test_suite='test',
    install_requires=[
        'geographiclib==1.49',
        'requests==2.22.0',
    ]

)
