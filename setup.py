from setuptools import setup

setup(
    name='nug-server',
    version='0.1.0',
    packages=['nug_server'],
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
        'python-dotenv==0.19.*',
        'zeroconf==0.38.*',
        'opencv-python==4.*'
    ],
)
