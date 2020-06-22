
from setuptools import setup


def requirements():
    with open('./requirements.txt', 'r')as f:
        return f.read().splitlines()


setup(
    name='packager',
    version='1.0.0',
    py_modules=['packager'],
    include_package_data=True,
    install_requires=requirements(),
    entry_points='''
        [console_scripts]
        packager=packager.cli:cli
    '''
)
