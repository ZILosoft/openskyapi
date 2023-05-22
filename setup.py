from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='openskyapi',
    version='0.0.2',
    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    test_suite='test',
    install_requires=[
        'geographiclib==1.49',
        'requests==2.31.0',
    ]

)
