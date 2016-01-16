from distutils.core import setup

setup(
    name='tspwiimote',
    version='0.1.0',
    url="http://github.com/boundary/pulse-wiimote/",
    author='David Gwartney',
    author_email='david_gwartney@bmc.com',
    packages=['tspwiimote', ],
    entry_points={
        'console_scripts': [
            'pulse-wiimote = tspwiimote.cli:main',
        ],
    },
    license='LICENSE',
    description='Example of integrating a Wiimote/Raspberry Pi to TrueSight Pulse',
    long_description=open('README.txt').read(),
    install_requires=[
        "tspapi >=0.1.1",
    ],
)
