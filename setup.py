from setuptools import setup

setup(
    name='nug-server',
    version='0.1.0',
    packages=[
        'nug_server',
        'nug_server.services',
        'nug_server.network'
    ],
    url='https://github.com/Sibyx/nug-server',
    license='GPLv3',
    author='Jakub Dubec',
    author_email='xdubec@stuba.sk',
    description='Simple RFB server',
    entry_points={
        'console_scripts': [
            "nug-server = nug_server.__main__:main",
        ]
    },
    install_requires=[
        'zeroconf==0.38.*',
        'tomli >= 1.1.0 ; python_version < "3.11"',
        'opencv-python-headless'
    ],
)
